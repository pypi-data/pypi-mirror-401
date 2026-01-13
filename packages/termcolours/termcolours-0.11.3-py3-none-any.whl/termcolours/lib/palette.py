# ./src/termcolours/lib/palette.py

"""
Module for generatig a named palette
"""

from typing import Generator
from pathlib import Path
from importlib import resources

from .softdev.debug import cprintd
from .. import APPNAME, PALETTE_FOLDER, ROOTPATH
from .. import APPNAME

# PALETTE_FOLDER = "assets"
FTITLE = __file__.split("/", maxsplit=-1)[-1].split(".", maxsplit=-1)[0]
# APPNAME = "termcolours"


def get_ssv_files(palettes_path: str | Path) -> Generator:
    if isinstance(palettes_path, Path):
        for file in palettes_path.glob("*.ssv"):
            if file.is_file():
                yield file
    else:  # Traversable
        for file in palettes_path:
            if file.is_file() and file.name.endswith(".ssv"):
                yield file


def list_palettes(palettes_path: str | Path) -> dict:
    loc = f"{APPNAME}::{FTITLE}.list_palettes"
    # palettes_path = ROOTPATH / "src" / f"{APPNAME}" / PALETTE_FOLDER
    cprintd(f"{palettes_path = }", location=loc)
    if not palettes_path.exists():
        cprintd(f"{palettes_path.exists() = }", location=loc)
        palettes_path = resources.files(f"{APPNAME}").joinpath(PALETTE_FOLDER)
    result = {}

    for palette_path in get_ssv_files(palettes_path):
        if palette_path.is_file():
            # apalette = {'name': "", 'path': palette_path}
            name = None
            with palette_path.open("r", encoding="utf-8") as fin:
                first_line = fin.readline().rstrip("\n")
                if "palette" in first_line:
                    name = first_line.lstrip("# ").split(";")[0].\
                            split(":")[1].strip()
                name = name or palette_path.stem
                result.update({name:  palette_path})

    return {k: result[k] for k in sorted(result.keys())}

