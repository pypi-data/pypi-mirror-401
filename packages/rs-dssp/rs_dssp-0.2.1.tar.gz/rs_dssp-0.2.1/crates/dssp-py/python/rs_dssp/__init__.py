"""
rs-dssp: High-performance DSSP secondary structure assignment.

A Rust-powered Python library for protein secondary structure assignment
using the DSSP algorithm (Kabsch & Sander, 1983).

Example:
    >>> import rs_dssp
    >>> result = rs_dssp.assign("protein.pdb")
    >>> print(result.sequence_c3)
    'HHHHHH----EEEE----'
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Literal, Sequence, overload

from .rs_dssp import (
    DsspResult as _DsspResult,
    ResidueInfo as _ResidueInfo,
    assign as _assign,
    assign_batch as _assign_batch,
    assign_from_coords as _assign_from_coords,
)

if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt
    import pandas as pd
    import polars as pl

__version__ = "0.2.1"
__all__ = [
    "assign",
    "assign_batch",
    "assign_from_coords",
    "assign_from_string",
    "to_dataframe",
    "DsspResult",
    "ResidueInfo",
    "SecondaryStructure",
    "cli",
]


# Secondary structure enum for type safety
class SecondaryStructure:
    """Secondary structure type constants."""

    # C8 classification
    ALPHA_HELIX = "H"
    HELIX_310 = "G"
    PI_HELIX = "I"
    BETA_STRAND = "E"
    BETA_BRIDGE = "B"
    TURN = "T"
    BEND = "S"
    PPII = "P"
    LOOP = " "

    # C3 classification
    HELIX = "H"
    SHEET = "E"
    COIL = "-"


# Re-export native classes
DsspResult = _DsspResult
ResidueInfo = _ResidueInfo


def assign(
    path: str | os.PathLike,
    *,
    calculate_sasa: bool = True,
    ppii_stretch: int = 3,
) -> DsspResult:
    """
    Assign secondary structure from a PDB/mmCIF file.

    Args:
        path: Path to PDB or mmCIF file (str or Path)
        calculate_sasa: Calculate solvent accessible surface area
        ppii_stretch: Minimum PPII helix stretch length

    Returns:
        DsspResult with secondary structure assignment

    Example:
        >>> result = rs_dssp.assign("protein.pdb")
        >>> print(result.sequence_c3)
    """
    return _assign(str(path), calculate_sasa, ppii_stretch)


def assign_from_coords(
    coords: npt.NDArray[np.floating],
    *,
    chain_id: str = "A",
    calculate_sasa: bool = True,
) -> DsspResult:
    """
    Assign secondary structure from coordinate array.

    Args:
        coords: NumPy array of shape (L, 4, 3) for N, CA, C, O atoms
        chain_id: Chain identifier
        calculate_sasa: Calculate solvent accessible surface area

    Returns:
        DsspResult with secondary structure assignment

    Example:
        >>> coords = np.random.randn(100, 4, 3).astype(np.float32)
        >>> result = rs_dssp.assign_from_coords(coords)
    """
    return _assign_from_coords(coords, chain_id, calculate_sasa)


def assign_batch(
    paths: Sequence[str | os.PathLike],
    *,
    n_threads: int = 0,
    calculate_sasa: bool = True,
) -> list[DsspResult | None]:
    """
    Assign secondary structure to multiple files in parallel.

    Args:
        paths: List of paths to PDB/mmCIF files
        n_threads: Number of threads (0 = auto)
        calculate_sasa: Calculate solvent accessible surface area

    Returns:
        List of DsspResult (None for failed files)

    Example:
        >>> results = rs_dssp.assign_batch(["a.pdb", "b.pdb"])
    """
    str_paths = [str(p) for p in paths]
    return _assign_batch(str_paths, n_threads, calculate_sasa)


def assign_from_string(
    pdb_string: str,
    *,
    calculate_sasa: bool = True,
) -> DsspResult:
    """
    Assign secondary structure from PDB string content.

    Args:
        pdb_string: PDB file content as string
        calculate_sasa: Calculate solvent accessible surface area

    Returns:
        DsspResult with secondary structure assignment

    Example:
        >>> with open("protein.pdb") as f:
        ...     result = rs_dssp.assign_from_string(f.read())
    """
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".pdb", delete=False) as f:
        f.write(pdb_string)
        tmp_path = f.name

    try:
        return _assign(tmp_path, calculate_sasa, 3)
    finally:
        os.unlink(tmp_path)


def to_dataframe(
    result: DsspResult,
    backend: Literal["pandas", "polars"] = "polars",
) -> pd.DataFrame | pl.DataFrame:
    """
    Convert DsspResult to a DataFrame.

    Args:
        result: DsspResult from assign()
        backend: "polars" (default) or "pandas"

    Returns:
        DataFrame with residue information
    """
    data = {
        "index": [],
        "chain_id": [],
        "seq_id": [],
        "amino_acid": [],
        "structure": [],
        "structure_c3": [],
        "phi": [],
        "psi": [],
        "accessibility": [],
    }

    for r in result.residues:
        data["index"].append(r.index)
        data["chain_id"].append(r.chain_id)
        data["seq_id"].append(r.seq_id)
        data["amino_acid"].append(r.amino_acid)
        data["structure"].append(r.structure)
        data["structure_c3"].append(r.structure_c3)
        data["phi"].append(r.phi)
        data["psi"].append(r.psi)
        data["accessibility"].append(r.accessibility)

    if backend == "polars":
        import polars as pl
        return pl.DataFrame(data)
    else:
        import pandas as pd
        return pd.DataFrame(data)
