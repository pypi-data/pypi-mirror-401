# rs-dssp

A high-performance Rust implementation of the DSSP (Dictionary of Secondary Structure of Proteins) algorithm.

## Features

- **Full C8 Classification**: Supports all 8 secondary structure types (H, G, I, E, B, T, S, P)
- **High Accuracy**: >97% agreement with reference DSSP on TS50 benchmark
- **Multiple Input Formats**: PDB and mmCIF file support
- **Multiple Output Formats**: Legacy DSSP, JSON, simple sequence, mmCIF annotations
- **Parallel Processing**: Multi-threaded batch processing with Rayon
- **Python Bindings**: Full Python API via PyO3
- **SASA Calculation**: Solvent accessible surface area using Shrake-Rupley algorithm

## Installation

### Rust CLI

Build from source:

```bash
git clone https://github.com/your-org/rs-dssp
cd rs-dssp
cargo build --release

# The binary will be at target/release/rs-dssp
./target/release/rs-dssp --help
```

### Python Package (Local Installation with uv)

The Python bindings are built using PyO3 and maturin. Use `uv` for easy local installation:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to the Python bindings crate
cd crates/dssp-py

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Build and install in development mode
uv pip install maturin
maturin develop --release

# Or build a wheel for distribution
maturin build --release
uv pip install ../target/wheels/rs_dssp-*.whl
```

### Using uvx (One-shot execution)

For quick one-shot usage without permanent installation:

```bash
# Run maturin directly via uvx
cd crates/dssp-py
uvx maturin develop --release
```

### Alternative: pip installation (from local build)

```bash
cd crates/dssp-py
pip install maturin
maturin develop --release
```

> **Note**: PyPI publication is not yet available. Please use local installation methods above.

## Usage

### Command Line

```bash
# Basic usage
rs-dssp protein.pdb -o result.dssp

# JSON output
rs-dssp protein.pdb --format json -o result.json

# Simple sequence output
rs-dssp protein.pdb --format simple

# Batch processing with 8 threads
rs-dssp *.pdb -j 8 -o results/

# C3 simplified classification
rs-dssp protein.pdb --c3

# mmCIF input
rs-dssp protein.cif -o result.dssp
```

### Python API

```python
import rs_dssp

# From PDB file
result = rs_dssp.assign("protein.pdb")
print(result.sequence)      # 'HHHHHH    EEEE    '
print(result.sequence_c3)   # 'HHHHHH----EEEE----'
print(result.aa_sequence)   # 'MKTAYIAKQR...'

# Access individual residues
for res in result.residues:
    print(f"{res.chain_id}:{res.seq_id} {res.amino_acid} -> {res.structure}")

# From NumPy coordinates
import numpy as np
coords = np.array([...])  # shape: (L, 4, 3) - N, CA, C, O
result = rs_dssp.assign_from_coords(coords)

# Batch processing
results = rs_dssp.assign_batch(["a.pdb", "b.pdb"], n_threads=4)
```

### Rust Library

```rust
use dssp_core::{calculate_dssp, DsspConfig, Structure};
use dssp_io::pdb::parse_pdb;
use std::fs::File;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Parse PDB file
    let file = File::open("protein.pdb")?;
    let mut structure = parse_pdb(file)?;

    // Calculate DSSP
    let config = DsspConfig::default();
    let stats = calculate_dssp(&mut structure, &config);

    // Get results
    println!("SS sequence: {}", structure.ss_sequence());
    println!("Residue count: {}", stats.residue_count);

    Ok(())
}
```

## Secondary Structure Classification

### C8 (Full)

| Code | Structure | Description |
|------|-----------|-------------|
| H | α-helix | 4-residue H-bond pattern |
| G | 3₁₀-helix | 3-residue H-bond pattern |
| I | π-helix | 5-residue H-bond pattern |
| E | β-strand | Extended in β-sheet |
| B | β-bridge | Isolated β-bridge |
| T | Turn | H-bonded turn |
| S | Bend | High curvature (κ > 70°) |
| P | PPII | Poly-Proline II helix |
| (space) | Loop | No regular structure |

### C3 (Simplified)

| Code | C8 Mapping |
|------|------------|
| H | H, G, I |
| E | E, B |
| - | T, S, P, (space) |

## Algorithm

The implementation follows the original Kabsch & Sander (1983) algorithm:

1. **Hydrogen Bond Detection**: Calculates H-bond energy using the electrostatic formula:
   ```
   E = -27.888 × (1/r_ON + 1/r_CH - 1/r_OH - 1/r_CN) kcal/mol
   ```
   Bonds with E < -0.5 kcal/mol are considered hydrogen bonds.

2. **Helix Detection**: Identifies 3₁₀, α, and π helices based on consecutive H-bond patterns.

3. **Beta Sheet Detection**: Detects parallel and antiparallel bridges, assembles ladders and sheets.

4. **Turn/Bend Detection**: Marks turns near helix starts and bends at high curvature regions.

5. **PPII Detection**: Identifies Poly-Proline II helices based on φ/ψ angles.

## Benchmarks

Performance comparison on TS50 dataset (50 proteins, 6860 residues):

| Implementation | Throughput (res/ms) | Speedup vs mkdssp |
|----------------|---------------------|-------------------|
| **rs-dssp (batch)** | **190.6** | **2593x** |
| dssp-py (Python bindings) | 82.5 | 1122x |
| rs-dssp (per-file) | 23.8 | 324x |
| PyDSSP (NumPy) | 20.2 | 275x |
| mkdssp (C++ reference) | 0.1 | 1x |

- **rs-dssp batch mode** processes all files in a single invocation with parallel execution
- **dssp-py** calls Rust directly via PyO3 FFI (no process spawn overhead)
- **mkdssp** is slow due to ~500MB dictionary loading per invocation

Accuracy: >97% C3 agreement with reference DSSP.

## References

- Kabsch, W. & Sander, C. (1983). Dictionary of protein secondary structure: Pattern recognition of hydrogen-bonded and geometrical features. *Biopolymers*, 22(12), 2577-2637.

## License

MIT OR Apache-2.0
