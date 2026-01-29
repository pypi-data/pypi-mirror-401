import json
import random
import re
from collections import defaultdict
from pathlib import Path

import datasets
import yaml
from datasets import ClassLabel, Features, Sequence, Value
from PIL import Image, ImageDraw
from rich.console import Console
from rich.progress import track

console = Console()


# ============================================================================
# Format Detection
# ============================================================================


def detect_format(data_dir: Path) -> str:
    """Auto-detect the dataset format (COCO or YOLO).

    Detection logic:
    - YOLO: Has data.yaml at root, or split dirs contain .txt label files
    - COCO: Has instances*.json files in split directories

    Returns:
        "yolo" or "coco"
    """
    # Check for YOLO data.yaml at root
    if (data_dir / "data.yaml").exists():
        return "yolo"

    # Check split directories
    for split_name in ["train", "test", "validation", "valid", "val"]:
        split_dir = data_dir / split_name
        if not split_dir.is_dir():
            continue

        # Check for YOLO-style labels directory or .txt files
        labels_dir = split_dir / "labels"
        if labels_dir.is_dir():
            txt_files = list(labels_dir.glob("*.txt"))
            if txt_files:
                return "yolo"

        # Check for .txt files directly in split (alternative YOLO structure)
        txt_files = list(split_dir.glob("*.txt"))
        # Filter out classes.txt
        txt_files = [f for f in txt_files if f.name != "classes.txt"]
        if txt_files:
            return "yolo"

        # Check for COCO instances*.json
        instances_pattern = re.compile(r"^instances.*\.json$")
        for f in split_dir.iterdir():
            if f.is_file() and instances_pattern.match(f.name):
                return "coco"

    # Default to COCO if no clear signal
    return "coco"


def load_coco_data(coco_path: Path):
    """Load COCO annotation file and return the data."""
    with coco_path.open() as f:
        return json.load(f)


def extract_categories(data: dict) -> dict:
    """Extract category mapping from COCO data (contiguous index -> name).

    COCO category IDs have gaps (e.g., no 66-72), so we map them to
    contiguous 0-indexed IDs matching the order they appear.
    """
    categories = sorted(data.get("categories", []), key=lambda c: c["id"])
    return {idx: cat["name"] for idx, cat in enumerate(categories)}


def find_instances_file(directory: Path) -> Path | None:
    """Find an instances*.json file in the given directory."""
    instances_pattern = re.compile(r"^instances.*\.json$")
    instances_files = [
        f
        for f in directory.iterdir()
        if f.is_file() and instances_pattern.match(f.name)
    ]
    return instances_files[0] if instances_files else None


def auto_detect_splits(data_dir: Path) -> dict[str, Path | None]:
    """Auto-detect train/test/validation directories and their annotations."""
    splits = {}

    for split_name in ["train", "test", "validation"]:
        split_dir = data_dir / split_name
        if split_dir.is_dir():
            instances_file = find_instances_file(split_dir)
            splits[split_name] = instances_file
        else:
            splits[split_name] = None

    return splits


def coco_to_metadata(coco_path: Path, out_path: Path):
    data = load_coco_data(coco_path)

    # Create mapping from COCO category IDs to contiguous 0-indexed IDs
    categories = sorted(data.get("categories", []), key=lambda c: c["id"])
    coco_id_to_index = {cat["id"]: idx for idx, cat in enumerate(categories)}

    objects = defaultdict(lambda: {"bbox": [], "category": []})
    console.print(f"  [dim]Loading annotations from {coco_path.name}...[/dim]")
    for ann in track(
        data.get("annotations", []), description="  [cyan]Processing annotations[/cyan]"
    ):
        img_id = ann["image_id"]
        objects[img_id]["bbox"].append([float(x) for x in ann["bbox"]])
        # Map COCO category ID to contiguous index
        contiguous_id = coco_id_to_index[ann["category_id"]]
        objects[img_id]["category"].append(contiguous_id)

    images = data.get("images", [])
    with out_path.open("w") as f:
        for img in track(images, description="  [cyan]Writing metadata[/cyan]"):
            img_id = img["id"]
            row = {
                "file_name": img["file_name"],
                "objects": objects.get(img_id, {"bbox": [], "category": []}),
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    console.print(f"  [dim]Processed {len(images):,} images[/dim]")

    return extract_categories(data)


# ============================================================================
# YOLO Format Functions
# ============================================================================


def load_yolo_classes(data_dir: Path) -> list[str]:
    """Load class names from YOLO dataset.

    Checks for:
    1. data.yaml at root (with 'names' key)
    2. classes.txt at root
    3. classes.txt in any split directory

    Returns:
        List of class names
    """
    # Check data.yaml first
    data_yaml = data_dir / "data.yaml"
    if data_yaml.exists():
        with data_yaml.open() as f:
            data = yaml.safe_load(f)
            if "names" in data:
                names = data["names"]
                # names can be a list or a dict {0: 'class0', 1: 'class1'}
                if isinstance(names, dict):
                    return [names[i] for i in sorted(names.keys())]
                return names

    # Check classes.txt at root
    classes_txt = data_dir / "classes.txt"
    if classes_txt.exists():
        return classes_txt.read_text().strip().split("\n")

    # Check classes.txt in split directories
    for split_name in ["train", "validation", "valid", "val", "test"]:
        split_dir = data_dir / split_name
        classes_txt = split_dir / "classes.txt"
        if classes_txt.exists():
            return classes_txt.read_text().strip().split("\n")

    return []


def find_yolo_labels_dir(split_dir: Path) -> Path | None:
    """Find the labels directory for a YOLO split.

    Checks:
    1. split_dir/labels/
    2. split_dir/ (if it contains .txt files)
    """
    labels_dir = split_dir / "labels"
    if labels_dir.is_dir():
        return labels_dir

    # Check if .txt files exist directly in split_dir
    txt_files = [f for f in split_dir.glob("*.txt") if f.name != "classes.txt"]
    if txt_files:
        return split_dir

    return None


def find_yolo_images_dir(split_dir: Path) -> Path | None:
    """Find the images directory for a YOLO split.

    Checks:
    1. split_dir/images/
    2. split_dir/ (if it contains image files)
    """
    images_dir = split_dir / "images"
    if images_dir.is_dir():
        return images_dir

    # Check if image files exist directly in split_dir
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    for f in split_dir.iterdir():
        if f.is_file() and f.suffix.lower() in image_extensions:
            return split_dir

    return None


def auto_detect_yolo_splits(data_dir: Path) -> dict[str, dict | None]:
    """Auto-detect YOLO splits and their labels/images directories.

    Returns:
        Dict mapping split names to {'labels': Path, 'images': Path} or None
    """
    splits = {}

    # YOLO uses 'valid' or 'val' commonly, map both to 'validation'
    split_mappings = {
        "train": ["train"],
        "validation": ["validation", "valid", "val"],
        "test": ["test"],
    }

    for canonical_name, aliases in split_mappings.items():
        for alias in aliases:
            split_dir = data_dir / alias
            if split_dir.is_dir():
                labels_dir = find_yolo_labels_dir(split_dir)
                images_dir = find_yolo_images_dir(split_dir)
                if labels_dir and images_dir:
                    splits[canonical_name] = {
                        "labels": labels_dir,
                        "images": images_dir,
                        "split_dir": split_dir,
                    }
                    break
        else:
            splits[canonical_name] = None

    return splits


def yolo_to_metadata(
    labels_dir: Path,
    images_dir: Path,
    out_path: Path,
    class_names: list[str],
) -> dict:
    """Convert YOLO annotations to metadata.jsonl format.

    YOLO format per .txt file (one line per object):
        class_id x_center y_center width height
    All values are normalized (0-1) relative to image dimensions.

    We convert to absolute COCO-style bbox: [x, y, width, height]
    where (x, y) is top-left corner.

    Args:
        labels_dir: Directory containing .txt label files
        images_dir: Directory containing image files
        out_path: Path to write metadata.jsonl
        class_names: List of class names

    Returns:
        Categories dict {idx: name}
    """
    categories = {idx: name for idx, name in enumerate(class_names)}

    # Find all image files
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    image_files = [
        f
        for f in images_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    console.print(f"  [dim]Found {len(image_files)} images in {images_dir}[/dim]")

    with out_path.open("w") as f:
        for img_path in track(
            image_files, description="  [cyan]Processing YOLO annotations[/cyan]"
        ):
            # Find corresponding label file
            label_file = labels_dir / (img_path.stem + ".txt")

            objects = {"bbox": [], "category": []}

            if label_file.exists():
                # Get image dimensions for denormalization
                with Image.open(img_path) as img:
                    img_width, img_height = img.size

                with label_file.open() as lf:
                    for line in lf:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split()
                        if len(parts) >= 5:
                            class_id = int(parts[0])
                            x_center = float(parts[1])
                            y_center = float(parts[2])
                            width = float(parts[3])
                            height = float(parts[4])

                            # Convert from YOLO normalized center format to
                            # absolute COCO format [x, y, width, height]
                            abs_width = width * img_width
                            abs_height = height * img_height
                            abs_x = (x_center * img_width) - (abs_width / 2)
                            abs_y = (y_center * img_height) - (abs_height / 2)

                            objects["bbox"].append(
                                [abs_x, abs_y, abs_width, abs_height]
                            )
                            objects["category"].append(class_id)

            row = {
                "file_name": img_path.name,
                "objects": objects,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    console.print(f"  [dim]Processed {len(image_files):,} images[/dim]")

    return categories


def yolo_obb_to_metadata(
    labels_dir: Path,
    images_dir: Path,
    out_path: Path,
    class_names: list[str],
) -> dict:
    """Convert YOLO OBB (Oriented Bounding Box) annotations to metadata.jsonl format.

    YOLO OBB format per .txt file (one line per object):
        class_id x1 y1 x2 y2 x3 y3 x4 y4
    All coordinates are normalized (0-1) relative to image dimensions.
    The 4 points represent the corners of the rotated bounding box.

    Args:
        labels_dir: Directory containing .txt label files
        images_dir: Directory containing image files
        out_path: Path to write metadata.jsonl
        class_names: List of class names

    Returns:
        Categories dict {idx: name}
    """
    categories = {idx: name for idx, name in enumerate(class_names)}

    # Find all image files
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    image_files = [
        f
        for f in images_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    console.print(f"  [dim]Found {len(image_files)} images in {images_dir}[/dim]")

    with out_path.open("w") as f:
        for img_path in track(
            image_files, description="  [cyan]Processing YOLO OBB annotations[/cyan]"
        ):
            # Find corresponding label file
            label_file = labels_dir / (img_path.stem + ".txt")

            objects = {"polygon": [], "category": []}

            if label_file.exists():
                # Get image dimensions for denormalization
                with Image.open(img_path) as img:
                    img_width, img_height = img.size

                with label_file.open() as lf:
                    for line in lf:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split()
                        if len(parts) >= 9:
                            class_id = int(parts[0])
                            # 4 corner points (x1,y1), (x2,y2), (x3,y3), (x4,y4)
                            points = []
                            for i in range(4):
                                x = float(parts[1 + i * 2]) * img_width
                                y = float(parts[2 + i * 2]) * img_height
                                points.extend([x, y])

                            objects["polygon"].append(points)
                            objects["category"].append(class_id)

            row = {
                "file_name": img_path.name,
                "objects": objects,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    console.print(f"  [dim]Processed {len(image_files):,} images[/dim]")

    return categories


def build_features_from_yolo(class_names: list[str]) -> tuple[Features, list[str]]:
    """Build HuggingFace Features from YOLO class names.

    Args:
        class_names: List of class names

    Returns:
        Tuple of (Features, class_names)
    """
    features = Features(
        {
            "image": datasets.Image(),
            "objects": {
                "bbox": Sequence(Sequence(Value("float32"), length=4)),
                "category": Sequence(ClassLabel(names=class_names)),
            },
        }
    )
    return features, class_names


def build_features_from_yolo_obb(class_names: list[str]) -> tuple[Features, list[str]]:
    """Build HuggingFace Features from YOLO OBB class names.

    Args:
        class_names: List of class names

    Returns:
        Tuple of (Features, class_names)
    """
    features = Features(
        {
            "image": datasets.Image(),
            "objects": {
                # 8 floats: x1,y1,x2,y2,x3,y3,x4,y4 (4 corner points)
                "polygon": Sequence(Sequence(Value("float32"), length=8)),
                "category": Sequence(ClassLabel(names=class_names)),
            },
        }
    )
    return features, class_names


def load_yolo_dataset_helper(
    data_dir: Path, class_names: list[str], splits_info: dict, is_obb: bool = False
):
    """Load a HuggingFace dataset from YOLO-format metadata.

    Args:
        data_dir: Directory containing the split subdirectories
        class_names: List of class names
        splits_info: Dict from auto_detect_yolo_splits with split details
        is_obb: Whether this is OBB format (oriented bounding boxes)

    Returns:
        A HuggingFace DatasetDict with properly typed features
    """
    if is_obb:
        features, names = build_features_from_yolo_obb(class_names)
    else:
        features, names = build_features_from_yolo(class_names)

    # Load each split individually from its images directory
    split_datasets = {}
    for split_name, split_info in splits_info.items():
        if split_info is None:
            continue
        images_dir = split_info["images"]
        split_ds = datasets.load_dataset(
            "imagefolder",
            data_dir=str(images_dir),
            features=features,
            split="train",  # imagefolder returns single split when loading from dir
        )
        split_datasets[split_name] = split_ds

    return datasets.DatasetDict(split_datasets)


def visualize_sample(
    metadata_path: Path, image_dir: Path, output_path: Path, categories: dict
):
    """Draw bounding boxes or polygons on a random sample image and save visualization."""
    # Read all metadata entries
    with metadata_path.open() as f:
        entries = [json.loads(line) for line in f if line.strip()]

    if not entries:
        console.print(f"  [yellow]⚠[/yellow] No entries found in {metadata_path}")
        return

    # Detect format: bbox (standard) or polygon (OBB)
    is_obb = "polygon" in entries[0].get("objects", {})

    # Pick a random entry with objects
    obj_key = "polygon" if is_obb else "bbox"
    entries_with_objects = [e for e in entries if e["objects"].get(obj_key)]
    if not entries_with_objects:
        console.print(
            f"  [yellow]⚠[/yellow] No images with annotations found in {metadata_path}"
        )
        return

    sample = random.choice(entries_with_objects)
    image_path = image_dir / sample["file_name"]

    if not image_path.exists():
        console.print(f"  [yellow]⚠[/yellow] Image not found at {image_path}")
        return

    # Load image and draw boxes
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    if is_obb:
        # Draw each oriented bounding box (polygon)
        for polygon, cat_id in zip(
            sample["objects"]["polygon"], sample["objects"]["category"]
        ):
            # polygon is [x1, y1, x2, y2, x3, y3, x4, y4]
            points = [
                (polygon[0], polygon[1]),
                (polygon[2], polygon[3]),
                (polygon[4], polygon[5]),
                (polygon[6], polygon[7]),
            ]
            draw.polygon(points, outline="red", width=3)

            # Draw category label at first point
            if categories and cat_id in categories:
                cat_name = categories[cat_id]
                draw.text((polygon[0], polygon[1] - 15), cat_name, fill="red")
    else:
        # Draw each bounding box
        for bbox, cat_id in zip(
            sample["objects"]["bbox"], sample["objects"]["category"]
        ):
            x, y, w, h = bbox
            # COCO format is [x, y, width, height], convert to corner coordinates
            draw.rectangle([x, y, x + w, y + h], outline="red", width=3)

            # Draw category label if available
            if categories and cat_id in categories:
                cat_name = categories[cat_id]
                draw.text((x, y - 15), cat_name, fill="red")

    # Save visualization
    img.save(output_path)
    console.print(
        f"  [green]✓[/green] Saved visualization to [cyan]{output_path}[/cyan]"
    )


def build_features_from_coco(coco_path: Path) -> tuple[Features, list[str]]:
    data = json.loads(coco_path.read_text())
    # COCO categories: list of {"id": int, "name": str, ...}
    cats = sorted(data["categories"], key=lambda c: c["id"])
    names = [c["name"] for c in cats]

    features = Features(
        {
            "image": datasets.Image(),
            "objects": {
                "bbox": Sequence(Sequence(Value("float32"), length=4)),
                # use "category" or "categories" to match your metadata.jsonl key
                "category": Sequence(ClassLabel(names=names)),
            },
        }
    )
    return features, names


def load_dataset_helper(data_dir: Path, annotation_file: Path):
    """Load a HuggingFace dataset from COCO-format metadata.

    Args:
        data_dir: Directory containing the split subdirectories (train/val/test)
        annotation_file: Path to the COCO annotations file (to extract features)

    Returns:
        A HuggingFace DatasetDict with properly typed features
    """
    features, names = build_features_from_coco(annotation_file)
    dataset = datasets.load_dataset(
        "imagefolder",
        data_dir=str(data_dir),
        features=features,
    )
    return dataset


def read_license_file(data_dir: Path) -> str | None:
    """Read license.txt from dataset directory if it exists.

    Args:
        data_dir: Root directory of the dataset

    Returns:
        License content as string, or None if not found
    """
    license_path = data_dir / "license.txt"
    if license_path.exists():
        return license_path.read_text().strip()
    # Also check for LICENSE (common convention)
    license_path = data_dir / "LICENSE"
    if license_path.exists():
        return license_path.read_text().strip()
    license_path = data_dir / "LICENSE.txt"
    if license_path.exists():
        return license_path.read_text().strip()
    return None


def read_citation_file(data_dir: Path) -> str | None:
    """Read citation.txt from dataset directory if it exists.

    Args:
        data_dir: Root directory of the dataset

    Returns:
        Citation content as string, or None if not found
    """
    citation_path = data_dir / "citation.txt"
    if citation_path.exists():
        return citation_path.read_text().strip()
    # Also check for CITATION.bib (common convention)
    citation_path = data_dir / "CITATION.bib"
    if citation_path.exists():
        return citation_path.read_text().strip()
    citation_path = data_dir / "CITATION"
    if citation_path.exists():
        return citation_path.read_text().strip()
    return None


def get_size_category(total_images: int) -> str:
    """Get HuggingFace size category string based on total image count.

    Args:
        total_images: Total number of images in the dataset

    Returns:
        Size category string (e.g., "1K<n<10K")
    """
    if total_images < 1000:
        return "n<1K"
    elif total_images < 10000:
        return "1K<n<10K"
    elif total_images < 100000:
        return "10K<n<100K"
    elif total_images < 1000000:
        return "100K<n<1M"
    else:
        return "n>1M"


def create_dataset_card(
    data_dir: Path,
    categories: dict,
    splits: list[str],
    repo_id: str | None = None,
    total_images: int | None = None,
) -> str:
    """Create a README.md dataset card for HuggingFace Hub.

    Args:
        data_dir: Root directory where README.md will be written
        categories: Dictionary mapping category IDs to names
        splits: List of split names (e.g., ['train', 'validation'])
        repo_id: Optional repo ID to replace REPO_ID placeholder in usage example
        total_images: Optional total number of images across all splits

    Returns:
        The README content as a string
    """
    repo_placeholder = repo_id if repo_id else "REPO_ID"

    # Read optional license and citation files
    license_content = read_license_file(data_dir)
    citation_content = read_citation_file(data_dir)

    # Determine license for YAML frontmatter
    # Use "other" if custom license found, otherwise "unknown"
    yaml_license = "other" if license_content else "unknown"

    # Build size category YAML if total_images provided
    size_category_yaml = ""
    if total_images is not None:
        size_category_yaml = f"\nsize_categories:\n- {get_size_category(total_images)}"

    # Build optional sections
    license_section = ""
    if license_content:
        license_section = f"""
## 📜 License

```
{license_content}
```
"""

    citation_section = ""
    if citation_content:
        citation_section = f"""
## 📝 Citation

If you use this dataset, please cite:

```bibtex
{citation_content}
```
"""

    # Add attribution note if either license or citation exists
    attribution_note = ""
    if license_content or citation_content:
        attribution_note = """
> ⚠️ **Note**: This dataset may have been derived from research work. Please review the license and citation information above before use.
"""

    readme_content = f"""---
license: {yaml_license}
task_categories:
- object-detection{size_category_yaml}
---

# Dataset Card

> **🚀 Uploaded using [hubify](https://github.com/benjamintli/hubify)** - Convert object detection datasets to HuggingFace format
{attribution_note}
This dataset contains object detection annotations converted to HuggingFace image dataset format.

## 📊 Dataset Details

- **🏷️ Number of classes**: {len(categories)}
- **📁 Splits**: {", ".join(splits)}
- **🖼️ Format**: Images with bounding box annotations

## 🎯 Classes

The dataset contains the following {len(categories)} classes:

{chr(10).join(f"- {name}" for name in categories.values())}
{license_section}{citation_section}
## 💻 Usage

```python
from datasets import load_dataset

dataset = load_dataset("{repo_placeholder}")
```

---

*Converted and uploaded with ❤️ using [hubify](https://github.com/benjamintli/hubify)*
"""

    readme_path = data_dir / "README.md"
    readme_path.write_text(readme_content)
    console.print(
        f"  [green]✓[/green] Created dataset card at [cyan]{readme_path}[/cyan]"
    )

    return readme_content


def get_hf_token(token_arg: str | None) -> str | None:
    """Get HuggingFace token from args, environment, or huggingface-cli.

    Args:
        token_arg: Token passed via CLI argument (takes priority)

    Returns:
        Token string or None if not found
    """
    import os

    # Priority 1: CLI argument
    if token_arg:
        return token_arg

    # Priority 2: Environment variable
    if "HF_TOKEN" in os.environ:
        return os.environ["HF_TOKEN"]

    # Priority 3: Try to get from huggingface_hub (if user ran `huggingface-cli login`)
    try:
        from huggingface_hub import HfFolder

        token = HfFolder.get_token()
        if token:
            return token
    except Exception:
        pass

    return None


def push_to_hub_helper(
    data_dir: Path, annotation_file: Path, repo_id: str, token: str | None
):
    """Push dataset to HuggingFace Hub.

    Args:
        data_dir: Directory containing the dataset
        annotation_file: Path to COCO annotations for features
        repo_id: HuggingFace Hub repo ID (username/dataset-name)
        token: HuggingFace API token (optional if logged in)
    """
    # Load the dataset
    console.print(f"[cyan]📦 Loading dataset from {data_dir}...[/cyan]")
    dataset = load_dataset_helper(data_dir, annotation_file)

    # Push to hub
    console.print(f"[cyan]⬆️  Pushing dataset to [bold]{repo_id}[/bold]...[/cyan]")
    dataset.push_to_hub(repo_id, token=token, private=False)
    console.print("[green]✓ Dataset successfully pushed![/green]")
    console.print(f"[cyan]🔗 View at: https://huggingface.co/datasets/{repo_id}[/cyan]")
