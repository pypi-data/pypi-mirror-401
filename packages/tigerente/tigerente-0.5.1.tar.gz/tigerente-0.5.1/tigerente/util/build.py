import json
import logging
import os
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path

import mpy_cross
import yaml


class UnexpectedResponseError(BaseException): ...


mpy_cross.set_version("1.20", 6)
mpy_cross.fix_perms()


def build_py(src: Path, dest: Path, src_dir: Path):
    result = subprocess.run(
        [mpy_cross.mpy_cross, src, "-o", dest],
        check=False,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to build {src} (to {dest}) using mpy-cross", result.stderr.decode("utf-8"))


def copy(src: Path, dest: Path, src_dir: Path):
    shutil.copy(src, dest)


def build_yaml(src: Path, dest: Path, src_dir: Path):
    with src.open() as f:
        data = yaml.safe_load(f)
    dest.write_text(json.dumps(data))


file_builders = {".py": (build_py, ".mpy"), ".yaml": (build_yaml, ".json")}


def build(src_dir: Path, build_dir: Path, only: list[Path] | None = None):
    src_dir = src_dir.absolute()
    built_paths = []
    for file in only if only is not None else src_dir.glob("**"):
        if file.is_dir():
            if file == src_dir:
                continue
            folder = build_dir / file.relative_to(src_dir)
            built_paths.append(folder)
            if file.exists():
                os.makedirs(folder, exist_ok=True)
            else:
                os.rmdir(folder)
            continue
        # Skip stub files
        if file.suffix == ".pyi":
            continue
        builder, new_suffix = file_builders.get(file.suffix, (copy, file.suffix))
        if not builder:
            logging.warning(f"Unable to build {file.suffix} file.")
            continue
        wanted_dest = build_dir / file.with_suffix(new_suffix).relative_to(src_dir)
        os.makedirs(wanted_dest.parent, exist_ok=True)
        built_paths.append(wanted_dest)

        if not file.exists():
            os.remove(wanted_dest)
            continue

        builder(file, wanted_dest, src_dir)
    return built_paths


@contextmanager
def built(src_dir: Path, paths: list[Path] | None = None):
    with tempfile.TemporaryDirectory() as build_dir_str:
        build_dir = Path(build_dir_str)
        built_paths = build(src_dir, build_dir, only=paths)
        yield build_dir, built_paths
