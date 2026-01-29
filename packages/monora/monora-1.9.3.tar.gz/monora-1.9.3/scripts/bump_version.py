#!/usr/bin/env python3
"""Bump Python + Node SDK versions together."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def update_text(path: Path, pattern: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"Pattern not found in {path}")
    path.write_text(updated, encoding="utf-8")


def update_json(path: Path, updater) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    updater(data)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validate_version(value: str) -> str:
    if not re.match(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$", value):
        raise argparse.ArgumentTypeError("Version must look like 1.2.3 or 1.2.3-rc.1")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump Monora Python + Node versions together.")
    parser.add_argument("version", type=validate_version, help="New version (e.g. 1.9.3)")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    version = args.version

    update_text(
        root / "pyproject.toml",
        r"^version = \"[^\"]+\"$",
        f"version = \"{version}\"",
    )
    update_text(
        root / "setup.py",
        r"version=\"[^\"]+\"",
        f"version=\"{version}\"",
    )
    update_text(
        root / "monora" / "__version__.py",
        r"__version__ = \"[^\"]+\"",
        f"__version__ = \"{version}\"",
    )

    update_json(
        root / "monora-node" / "package.json",
        lambda data: data.__setitem__("version", version),
    )

    def update_lock(data: dict) -> None:
        data["version"] = version
        packages = data.get("packages")
        if isinstance(packages, dict) and "" in packages:
            packages[""]["version"] = version

    update_json(root / "monora-node" / "package-lock.json", update_lock)

    print(f"Updated versions to {version}")


if __name__ == "__main__":
    main()
