//! # dssp-core
//!
//! Core DSSP (Dictionary of Secondary Structure of Proteins) algorithm implementation.
//!
//! This crate provides the complete DSSP algorithm for assigning secondary structure
//! to protein residues based on hydrogen bonding patterns.
//!
//! ## Features
//!
//! - Full C8 classification (H, G, I, E, B, T, S, P)
//! - Kabsch-Sander hydrogen bond energy calculation
//! - Helix detection (α, 3₁₀, π, PPII)
//! - Beta sheet detection (strands, bridges, ladders, sheets)
//! - Turn and bend detection
//! - Solvent accessible surface area (SASA) calculation
//!
//! ## Example
//!
//! ```ignore
//! use dssp_core::{Structure, calculate_dssp, DsspConfig};
//!
//! let mut structure = Structure::from_residues(residues);
//! let config = DsspConfig::default();
//! let stats = calculate_dssp(&mut structure, &config);
//! ```

pub mod constants;
pub mod error;
pub mod geometry;
pub mod types;
pub mod hbond;
pub mod helix;
pub mod ppii;
pub mod strand;
pub mod turn;
pub mod sasa;
pub mod assign;

// Re-export commonly used types
pub use constants::*;
pub use error::{DsspError, Result};
pub use types::*;
pub use geometry::Point3;
pub use assign::{calculate_dssp, calculate_dssp_full, DsspConfig};
