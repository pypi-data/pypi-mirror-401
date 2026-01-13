"""Type stubs for rs_dssp."""

from __future__ import annotations

import os
from typing import Literal, Sequence

import numpy as np
import numpy.typing as npt
import pandas as pd
import polars as pl

__version__: str

class SecondaryStructure:
    ALPHA_HELIX: str
    HELIX_310: str
    PI_HELIX: str
    BETA_STRAND: str
    BETA_BRIDGE: str
    TURN: str
    BEND: str
    PPII: str
    LOOP: str
    HELIX: str
    SHEET: str
    COIL: str

class ResidueInfo:
    index: int
    chain_id: str
    seq_id: int
    amino_acid: str
    structure: str
    structure_c3: str
    phi: float | None
    psi: float | None
    accessibility: float

class DsspResult:
    sequence: str
    sequence_c3: str
    aa_sequence: str
    structure_id: str
    residue_count: int
    residues: list[ResidueInfo]
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...

def assign(
    path: str | os.PathLike,
    *,
    calculate_sasa: bool = True,
    ppii_stretch: int = 3,
) -> DsspResult: ...

def assign_from_coords(
    coords: npt.NDArray[np.floating],
    *,
    chain_id: str = "A",
    calculate_sasa: bool = True,
) -> DsspResult: ...

def assign_batch(
    paths: Sequence[str | os.PathLike],
    *,
    n_threads: int = 0,
    calculate_sasa: bool = True,
) -> list[DsspResult | None]: ...

def assign_from_string(
    pdb_string: str,
    *,
    calculate_sasa: bool = True,
) -> DsspResult: ...

def to_dataframe(
    result: DsspResult,
    backend: Literal["pandas", "polars"] = "polars",
) -> pd.DataFrame | pl.DataFrame: ...
