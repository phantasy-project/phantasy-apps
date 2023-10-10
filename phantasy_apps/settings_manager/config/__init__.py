import pathlib
import json


_CWDIR = pathlib.Path(__file__).parent

with open(_CWDIR.joinpath("sym_z_map.json"), "r") as fp:
    SYM_Z_MAP = json.load(fp)
    Z_SYM_MAP = {v: k for k, v in SYM_Z_MAP.items()}
    ALL_SYM = SYM_Z_MAP.keys()


def z2sym(z: int) -> str:
    """Return the chemical element symbol from the atomic number."""
    return Z_SYM_MAP.get(z, None)


def sym2z(sym: str) -> int:
    """Return the atomic number of the given chemical element symbol."""
    return SYM_Z_MAP.get(sym, None)
