import pathlib
import yourdfpy

URDF_DIR = pathlib.Path(__file__).resolve().parents[2] / "urdf"


def load_custom_urdf(filename: str) -> yourdfpy.URDF:
    """Load a URDF file from the project's ``urdf`` directory.

    Parameters
    ----------
    filename : str
        Name of the URDF file relative to the ``urdf`` directory.

    Returns
    -------
    yourdfpy.URDF
        Parsed URDF object.
    """
    path = URDF_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"URDF file '{filename}' not found in {URDF_DIR}.")
    return yourdfpy.URDF.load(str(path))
