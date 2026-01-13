//! # dssp-io
//!
//! I/O library for DSSP secondary structure assignment.
//!
//! Provides parsers and writers for:
//! - PDB format (standard protein structure files)
//! - mmCIF format (modern structure format)
//! - DSSP output format (legacy and simple formats)
//! - JSON output format

pub mod pdb;
pub mod cif;
pub mod dssp;
pub mod json;
pub mod simple;
pub mod error;

pub use error::{IoError, Result};
pub use pdb::parse_pdb;
pub use cif::parse_cif;

/// Detect file format from extension
pub fn detect_format(path: &str) -> Option<FileFormat> {
    let lower = path.to_lowercase();
    if lower.ends_with(".pdb") || lower.ends_with(".ent") {
        Some(FileFormat::Pdb)
    } else if lower.ends_with(".cif") || lower.ends_with(".mmcif") {
        Some(FileFormat::Cif)
    } else if lower.ends_with(".dssp") {
        Some(FileFormat::Dssp)
    } else {
        None
    }
}

/// Supported file formats
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FileFormat {
    Pdb,
    Cif,
    Dssp,
    Json,
}
