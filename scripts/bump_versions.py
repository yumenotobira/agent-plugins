#!/usr/bin/env python3
"""Bump the version of plugins changed between two git refs.

Finds plugins/<name>/ directories with changes in BASE...HEAD and bumps the
"version" in plugins/<name>/.claude-plugin/plugin.json.

Usage:
  scripts/bump_versions.py                       # changes vs origin/main, patch
  scripts/bump_versions.py --base main~3 --head HEAD --level minor
  scripts/bump_versions.py --plugin foo          # bump specific plugin(s), no diff
  scripts/bump_versions.py --dry-run

Prints "name old -> new" per bumped plugin. If $GITHUB_OUTPUT is set, also
writes `bumped=<space-separated names>` there for use in GitHub Actions.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = "plugins"
MANIFEST = Path(".claude-plugin") / "plugin.json"
INITIAL_VERSION = "0.1.0"
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def changed_plugins(base: str, head: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{head}", "--", f"{PLUGINS_DIR}/"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    names = {Path(p).parts[1] for p in out.splitlines() if len(Path(p).parts) > 2}
    # Only plugins that still exist (deleted plugins are skipped).
    return sorted(n for n in names if (ROOT / PLUGINS_DIR / n / MANIFEST).is_file())


def bump(version: str | None, level: str) -> str:
    if not version:
        return INITIAL_VERSION
    m = SEMVER.match(version)
    if not m:
        sys.exit(f"error: unsupported version format: {version!r} (expected X.Y.Z)")
    major, minor, patch = map(int, m.groups())
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def bump_plugin(name: str, level: str, dry_run: bool) -> tuple[str | None, str]:
    path = ROOT / PLUGINS_DIR / name / MANIFEST
    if not path.is_file():
        sys.exit(f"error: {path.relative_to(ROOT)} not found")
    data = json.loads(path.read_text())
    old = data.get("version")
    new = bump(old, level)
    if not dry_run:
        data["version"] = new
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return old, new


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", default="origin/main", help="base ref (default: origin/main)")
    p.add_argument("--head", default="HEAD", help="head ref (default: HEAD)")
    p.add_argument("--level", choices=["patch", "minor", "major"], default="patch")
    p.add_argument("--plugin", action="append", help="bump this plugin explicitly (repeatable)")
    p.add_argument("--dry-run", action="store_true", help="show what would change")
    args = p.parse_args()

    names = args.plugin or changed_plugins(args.base, args.head)
    if not names:
        print("no plugin changes")

    for name in names:
        old, new = bump_plugin(name, args.level, args.dry_run)
        print(f"{name} {old or '(none)'} -> {new}")

    if out := os.environ.get("GITHUB_OUTPUT"):
        with open(out, "a") as f:
            f.write(f"bumped={' '.join(names)}\n")


if __name__ == "__main__":
    main()
