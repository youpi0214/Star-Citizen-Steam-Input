from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

VERSION_TAG = re.compile(r"v?(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*))?")


def next_version(tags: list[str], bump: str) -> tuple[int, int, int]:
    versions = []
    for tag in tags:
        match = VERSION_TAG.fullmatch(tag)
        if match:
            versions.append(tuple(int(part or 0) for part in match.groups()))
    major, minor, _ = max(versions, default=(0, 0, 0))
    if bump == "major":
        return major + 1, 0, 0
    if bump == "minor":
        return major, minor + 1, 0
    raise ValueError(f"Unknown bump: {bump}")


def update_vdf(text: str, major: int, minor: int) -> str:
    for field, value in (("major_revision", major), ("minor_revision", minor)):
        pattern = re.compile(rf'(?m)^(\s*"{field}"\s+")\d+("[^\S\r\n]*\r?$)')
        text, count = pattern.subn(lambda match: f"{match[1]}{value}{match[2]}", text)
        if count != 1:
            raise ValueError(f"Expected exactly one numeric {field}, found {count}")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bump", choices=("minor", "major"))
    parser.add_argument("--vdf", type=Path, default=Path("mapping/controller_configuration.vdf"))
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    tags = subprocess.check_output(["git", "tag", "--list"], text=True).splitlines()
    major, minor, patch = next_version(tags, args.bump)
    tag = f"v{major}.{minor}.{patch}"

    # Preserve whitespace and line endings, and validate both fields before writing.
    text = args.vdf.read_bytes().decode("utf-8")
    args.vdf.write_bytes(update_vdf(text, major, minor).encode("utf-8"))
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as output:
            output.write(f"tag={tag}\n")
    print(tag)


if __name__ == "__main__":
    main()
