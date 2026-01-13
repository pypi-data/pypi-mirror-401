//! Python bindings for rs-dssp
//!
//! Provides Python access to the DSSP algorithm through PyO3.

use dssp_core::{calculate_dssp_full, DsspConfig, Structure};
use dssp_io::pdb::parse_pdb;
use numpy::PyReadonlyArray3;
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use rayon::prelude::*;
use std::fs::File;

/// Python module for rs-dssp
#[pymodule]
fn rs_dssp(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(assign, m)?)?;
    m.add_function(wrap_pyfunction!(assign_from_coords, m)?)?;
    m.add_function(wrap_pyfunction!(assign_batch, m)?)?;
    m.add_class::<DsspResult>()?;
    m.add_class::<ResidueInfo>()?;
    Ok(())
}

/// DSSP calculation result
#[pyclass]
#[derive(Clone)]
pub struct DsspResult {
    /// Secondary structure sequence (C8)
    #[pyo3(get)]
    pub sequence: String,
    /// Secondary structure sequence (C3: H, E, -)
    #[pyo3(get)]
    pub sequence_c3: String,
    /// Amino acid sequence
    #[pyo3(get)]
    pub aa_sequence: String,
    /// Structure identifier
    #[pyo3(get)]
    pub structure_id: String,
    /// Number of residues
    #[pyo3(get)]
    pub residue_count: usize,
    /// List of residue information
    residues: Vec<ResidueInfo>,
}

#[pymethods]
impl DsspResult {
    /// Get residue information
    #[getter]
    fn residues(&self) -> Vec<ResidueInfo> {
        self.residues.clone()
    }

    fn __repr__(&self) -> String {
        format!(
            "DsspResult(id='{}', residues={}, sequence='{}')",
            self.structure_id,
            self.residue_count,
            if self.sequence.len() > 50 {
                format!("{}...", &self.sequence[..50])
            } else {
                self.sequence.clone()
            }
        )
    }

    fn __len__(&self) -> usize {
        self.residue_count
    }
}

/// Information about a single residue
#[pyclass]
#[derive(Clone)]
pub struct ResidueInfo {
    #[pyo3(get)]
    pub index: usize,
    #[pyo3(get)]
    pub chain_id: String,
    #[pyo3(get)]
    pub seq_id: i32,
    #[pyo3(get)]
    pub amino_acid: char,
    #[pyo3(get)]
    pub structure: char,
    #[pyo3(get)]
    pub structure_c3: char,
    #[pyo3(get)]
    pub phi: Option<f32>,
    #[pyo3(get)]
    pub psi: Option<f32>,
    #[pyo3(get)]
    pub accessibility: f32,
}

#[pymethods]
impl ResidueInfo {
    fn __repr__(&self) -> String {
        format!(
            "ResidueInfo({}:{}, {}, {})",
            self.chain_id, self.seq_id, self.amino_acid, self.structure
        )
    }
}

/// Assign secondary structure from a PDB file
///
/// Args:
///     path: Path to PDB or mmCIF file
///     calculate_sasa: Whether to calculate surface accessibility (default: True)
///     ppii_stretch: Minimum PPII helix stretch length (default: 3)
///
/// Returns:
///     DsspResult containing secondary structure assignment
#[pyfunction]
#[pyo3(signature = (path, calculate_sasa=true, ppii_stretch=3))]
fn assign(path: &str, calculate_sasa: bool, ppii_stretch: usize) -> PyResult<DsspResult> {
    let file = File::open(path).map_err(|e| PyValueError::new_err(e.to_string()))?;

    let structure = if path.to_lowercase().ends_with(".cif") || path.to_lowercase().ends_with(".mmcif") {
        dssp_io::cif::parse_cif(file).map_err(|e| PyValueError::new_err(e.to_string()))?
    } else {
        parse_pdb(file).map_err(|e| PyValueError::new_err(e.to_string()))?
    };

    let config = DsspConfig {
        calculate_accessibility: calculate_sasa,
        min_ppii_stretch: ppii_stretch,
        ..Default::default()
    };

    let result = calculate_dssp_full(structure, &config);
    Ok(convert_result(&result))
}

/// Assign secondary structure from coordinate array
///
/// Args:
///     coords: Numpy array of shape (L, 4, 3) containing N, CA, C, O coordinates
///     chain_id: Chain identifier (default: "A")
///     calculate_sasa: Whether to calculate surface accessibility (default: True)
///
/// Returns:
///     DsspResult containing secondary structure assignment
#[pyfunction]
#[pyo3(signature = (coords, chain_id="A", calculate_sasa=true))]
fn assign_from_coords<'py>(
    coords: PyReadonlyArray3<'py, f32>,
    chain_id: &str,
    calculate_sasa: bool,
) -> PyResult<DsspResult> {
    let coords = coords.as_array();
    let shape = coords.shape();

    if shape.len() != 3 || shape[1] != 4 || shape[2] != 3 {
        return Err(PyValueError::new_err(
            "coords must have shape (L, 4, 3) where 4 is N, CA, C, O",
        ));
    }

    let n_residues = shape[0];
    let mut residues = Vec::with_capacity(n_residues);

    for i in 0..n_residues {
        let n = dssp_core::geometry::Point3::new(
            coords[[i, 0, 0]],
            coords[[i, 0, 1]],
            coords[[i, 0, 2]],
        );
        let ca = dssp_core::geometry::Point3::new(
            coords[[i, 1, 0]],
            coords[[i, 1, 1]],
            coords[[i, 1, 2]],
        );
        let c = dssp_core::geometry::Point3::new(
            coords[[i, 2, 0]],
            coords[[i, 2, 1]],
            coords[[i, 2, 2]],
        );
        let o = dssp_core::geometry::Point3::new(
            coords[[i, 3, 0]],
            coords[[i, 3, 1]],
            coords[[i, 3, 2]],
        );

        let backbone = dssp_core::types::BackboneAtoms::new(n, ca, c, o);
        residues.push(dssp_core::types::Residue::new(
            chain_id.to_string(),
            (i + 1) as i32,
            "ALA".to_string(),
            backbone,
        ));
    }

    let structure = Structure::from_residues(residues);

    let config = DsspConfig {
        calculate_accessibility: calculate_sasa,
        ..Default::default()
    };

    let result = calculate_dssp_full(structure, &config);
    Ok(convert_result(&result))
}

/// Assign secondary structure to multiple PDB files in parallel
///
/// Args:
///     paths: List of paths to PDB/mmCIF files
///     n_threads: Number of threads (0 = auto)
///     calculate_sasa: Whether to calculate surface accessibility
///
/// Returns:
///     List of DsspResult or None for failed files
#[pyfunction]
#[pyo3(signature = (paths, n_threads=0, calculate_sasa=true))]
fn assign_batch(
    paths: Vec<String>,
    n_threads: usize,
    calculate_sasa: bool,
) -> PyResult<Vec<Option<DsspResult>>> {
    if n_threads > 0 {
        rayon::ThreadPoolBuilder::new()
            .num_threads(n_threads)
            .build_global()
            .ok();
    }

    let config = DsspConfig {
        calculate_accessibility: calculate_sasa,
        ..Default::default()
    };

    let results: Vec<Option<DsspResult>> = paths
        .par_iter()
        .map(|path| {
            let file = match File::open(path) {
                Ok(f) => f,
                Err(_) => return None,
            };

            let structure = if path.to_lowercase().ends_with(".cif") {
                dssp_io::cif::parse_cif(file).ok()?
            } else {
                parse_pdb(file).ok()?
            };

            let result = calculate_dssp_full(structure, &config);
            Some(convert_result(&result))
        })
        .collect();

    Ok(results)
}

fn convert_result(result: &dssp_core::types::DsspResult) -> DsspResult {
    let residues: Vec<ResidueInfo> = result
        .structure
        .residues
        .iter()
        .enumerate()
        .map(|(i, r)| ResidueInfo {
            index: i,
            chain_id: r.chain_id.clone(),
            seq_id: r.seq_id,
            amino_acid: r.amino_acid.as_char(),
            structure: r.structure.as_char(),
            structure_c3: r.structure.to_c3_char(),
            phi: r.phi,
            psi: r.psi,
            accessibility: r.accessibility,
        })
        .collect();

    DsspResult {
        sequence: result.structure.ss_sequence(),
        sequence_c3: result.structure.ss_sequence_c3(),
        aa_sequence: result.structure.aa_sequence(),
        structure_id: result.structure.id.clone(),
        residue_count: result.structure.residues.len(),
        residues,
    }
}
