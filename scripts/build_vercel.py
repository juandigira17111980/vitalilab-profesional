"""Prepare public assets without importing the app or accessing its database."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def prepare_static_assets(root: Path = ROOT) -> int:
    source = root / "app" / "static"
    destination = root / "public" / "static"
    if not source.is_dir():
        raise FileNotFoundError("Expected app/static in the project root")
    shutil.copytree(source, destination, dirs_exist_ok=True)
    return sum(path.is_file() for path in destination.rglob("*"))


if __name__ == "__main__":
    print(f"Vercel public assets prepared: {prepare_static_assets()} files")
