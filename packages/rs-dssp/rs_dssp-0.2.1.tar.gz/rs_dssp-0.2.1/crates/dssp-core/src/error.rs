//! Error types for dssp-core

use thiserror::Error;

/// Result type alias for dssp-core operations
pub type Result<T> = std::result::Result<T, DsspError>;

/// Errors that can occur during DSSP calculation
#[derive(Error, Debug)]
pub enum DsspError {
    /// Missing backbone atom in a residue
    #[error("Missing backbone atom '{atom}' in residue {chain}:{seq_id}")]
    MissingAtom {
        atom: String,
        chain: String,
        seq_id: i32,
    },

    /// Invalid residue data
    #[error("Invalid residue: {0}")]
    InvalidResidue(String),

    /// Chain break detected without proper handling
    #[error("Unhandled chain break at residue {chain}:{seq_id}")]
    UnhandledChainBreak { chain: String, seq_id: i32 },

    /// Numerical error in geometry calculation
    #[error("Numerical error in geometry calculation: {0}")]
    NumericalError(String),

    /// Empty structure (no residues)
    #[error("Structure contains no residues")]
    EmptyStructure,

    /// Invalid structure data
    #[error("Invalid structure: {0}")]
    InvalidStructure(String),

    /// Index out of bounds
    #[error("Index {index} out of bounds for length {length}")]
    IndexOutOfBounds { index: usize, length: usize },
}

impl DsspError {
    /// Create a missing atom error
    pub fn missing_atom(atom: &str, chain: &str, seq_id: i32) -> Self {
        Self::MissingAtom {
            atom: atom.to_string(),
            chain: chain.to_string(),
            seq_id,
        }
    }

    /// Create a chain break error
    pub fn chain_break(chain: &str, seq_id: i32) -> Self {
        Self::UnhandledChainBreak {
            chain: chain.to_string(),
            seq_id,
        }
    }
}
