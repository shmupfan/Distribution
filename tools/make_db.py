#!/usr/bin/env python3
"""Build db.json, the MiSTer Downloader / Update All database for every
core in cores.json.

    python3 tools/make_db.py

Each core repo keeps the MiSTer-devel layout: releases/Arcade-<Core>_<date>.rbf,
parent MRAs in releases/, alternatives in releases/_alternatives/_<game>/.
Files install where MiSTer-devel's distribution puts them: the RBF to
_Arcade/cores/ with the "Arcade-" prefix stripped, MRAs to _Arcade/.
URLs point at raw.githubusercontent.com pinned to the commit in cores.json,
so they never change under existing installs.
"""
import hashlib
import json
import subprocess
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_ID = "shmupfan"


def git(local, *args):
    return subprocess.run(["git", "-C", str(local), *args], check=True,
                          capture_output=True).stdout


def install_path(rel):
    """releases/<rel> -> install path on the SD card."""
    name = rel.rsplit("/", 1)[-1]
    if rel.endswith(".rbf"):
        if "/" in rel:
            raise SystemExit(f"RBF outside releases/ root: {rel}")
        return "_Arcade/cores/" + (name[len("Arcade-"):] if name.startswith("Arcade-") else name)
    if rel.endswith(".mra"):
        return "_Arcade/" + rel
    return None  # README and anything else stays in the repo


def main():
    cfg = json.loads((ROOT / "cores.json").read_text())
    files, folders = {}, {"_Arcade": {}, "_Arcade/cores": {}}
    for core in cfg["cores"]:
        local = (ROOT / core["local"]).resolve()
        commit = git(local, "rev-parse", core["commit"]).decode().strip()
        names = git(local, "ls-tree", "-r", "--name-only", commit, "releases/").decode().splitlines()
        rbfs = [n for n in names if n.endswith(".rbf")]
        if len(rbfs) != 1:
            raise SystemExit(f"{core['name']}: expected one RBF in releases/, found {rbfs}")
        for n in names:
            rel = n[len("releases/"):]
            dest = install_path(rel)
            if dest is None:
                continue
            if dest in files:
                raise SystemExit(f"duplicate install path {dest}")
            data = git(local, "show", f"{commit}:{n}")
            files[dest] = {
                "hash": hashlib.md5(data).hexdigest(),
                "size": len(data),
                "url": f"https://raw.githubusercontent.com/{core['repo']}/{commit}/"
                       + urllib.parse.quote(n),
            }
            parts = dest.split("/")[:-1]
            for i in range(1, len(parts) + 1):
                folders.setdefault("/".join(parts[:i]), {})
        print(f"{core['name']}: {commit[:12]}, {sum(1 for n in names if install_path(n[9:]))} files")
    db = {"db_id": DB_ID, "timestamp": int(time.time()),
          "files": dict(sorted(files.items())), "folders": dict(sorted(folders.items()))}
    (ROOT / "db.json").write_text(json.dumps(db, indent=2) + "\n")
    print(f"wrote db.json: {len(files)} files, {len(folders)} folders")


if __name__ == "__main__":
    main()
