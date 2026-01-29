from __future__ import annotations

from pathlib import Path
import shutil
import zipfile
import typing


def package_worker(source_dir: Path, out_file: Path) -> Path:
    """Package a Python worker directory into a zip file suitable for embedding.

    Returns the path to the created zip file.
    """
    source_dir = Path(source_dir)
    out_file = Path(out_file)
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(source_dir.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(source_dir))
    return out_file


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("out", type=Path)
    args = p.parse_args()
    print(f"Packaging {args.source} -> {args.out}")
    package_worker(args.source, args.out)
