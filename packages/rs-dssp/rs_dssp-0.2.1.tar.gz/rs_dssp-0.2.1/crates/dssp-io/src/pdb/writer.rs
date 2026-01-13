//! PDB format writer (placeholder)

use dssp_core::types::Structure;
use std::io::Write;

/// Write structure to PDB format
pub fn write_pdb<W: Write>(_writer: &mut W, _structure: &Structure) -> std::io::Result<()> {
    // PDB writing is not typically needed for DSSP output
    // This is a placeholder for potential future use
    Ok(())
}
