//! JSON output format

use dssp_core::types::{DsspResult, Residue, Statistics};
use serde::{Deserialize, Serialize};
use std::io::Write;

/// JSON-serializable residue information
#[derive(Debug, Serialize, Deserialize)]
pub struct ResidueJson {
    pub index: usize,
    pub chain_id: String,
    pub seq_id: i32,
    pub ins_code: String,
    pub amino_acid: char,
    pub structure_c8: char,
    pub structure_c3: char,
    pub phi: Option<f32>,
    pub psi: Option<f32>,
    pub accessibility: f32,
}

/// JSON-serializable DSSP result
#[derive(Debug, Serialize, Deserialize)]
pub struct DsspResultJson {
    pub structure_id: String,
    pub residue_count: usize,
    pub chain_count: usize,
    pub ss_sequence_c8: String,
    pub ss_sequence_c3: String,
    pub aa_sequence: String,
    pub residues: Vec<ResidueJson>,
    pub statistics: StatisticsJson,
}

/// JSON-serializable statistics
#[derive(Debug, Serialize, Deserialize)]
pub struct StatisticsJson {
    pub residue_count: u32,
    pub chain_count: u32,
    pub hbond_count: u32,
    pub accessible_surface: f64,
}

impl From<&DsspResult> for DsspResultJson {
    fn from(result: &DsspResult) -> Self {
        let residues: Vec<ResidueJson> = result
            .structure
            .residues
            .iter()
            .enumerate()
            .map(|(i, r)| ResidueJson::from_residue(i, r))
            .collect();

        Self {
            structure_id: result.structure.id.clone(),
            residue_count: result.structure.residues.len(),
            chain_count: result.structure.chains.len(),
            ss_sequence_c8: result.structure.ss_sequence(),
            ss_sequence_c3: result.structure.ss_sequence_c3(),
            aa_sequence: result.structure.aa_sequence(),
            residues,
            statistics: StatisticsJson::from(&result.statistics),
        }
    }
}

impl ResidueJson {
    fn from_residue(index: usize, residue: &Residue) -> Self {
        Self {
            index,
            chain_id: residue.chain_id.clone(),
            seq_id: residue.seq_id,
            ins_code: residue.ins_code.clone(),
            amino_acid: residue.amino_acid.as_char(),
            structure_c8: residue.structure.as_char(),
            structure_c3: residue.structure.to_c3_char(),
            phi: residue.phi,
            psi: residue.psi,
            accessibility: residue.accessibility,
        }
    }
}

impl From<&Statistics> for StatisticsJson {
    fn from(stats: &Statistics) -> Self {
        Self {
            residue_count: stats.residue_count,
            chain_count: stats.chain_count,
            hbond_count: stats.hbond_count,
            accessible_surface: stats.accessible_surface,
        }
    }
}

/// Write DSSP result as JSON
pub fn write_json<W: Write>(writer: &mut W, result: &DsspResult) -> std::io::Result<()> {
    let json_result = DsspResultJson::from(result);
    let json_str = serde_json::to_string_pretty(&json_result)
        .map_err(|e| std::io::Error::new(std::io::ErrorKind::Other, e))?;
    writeln!(writer, "{}", json_str)
}

/// Write DSSP result as compact JSON (single line)
pub fn write_json_compact<W: Write>(writer: &mut W, result: &DsspResult) -> std::io::Result<()> {
    let json_result = DsspResultJson::from(result);
    let json_str = serde_json::to_string(&json_result)
        .map_err(|e| std::io::Error::new(std::io::ErrorKind::Other, e))?;
    writeln!(writer, "{}", json_str)
}
