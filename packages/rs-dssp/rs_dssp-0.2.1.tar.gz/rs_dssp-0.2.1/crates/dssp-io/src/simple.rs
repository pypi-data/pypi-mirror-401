//! Simple output format
//!
//! Outputs secondary structure as a simple sequence of characters.

use dssp_core::types::{DsspResult, Structure};
use std::io::Write;

/// Output mode for simple format
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SimpleMode {
    /// C8 classification (H, G, I, E, B, T, S, P, space)
    C8,
    /// C3 classification (H, E, -)
    C3,
}

/// Write simple output format
///
/// Outputs format: `<ss_sequence> <structure_id>`
pub fn write_simple<W: Write>(
    writer: &mut W,
    result: &DsspResult,
    mode: SimpleMode,
) -> std::io::Result<()> {
    let seq = match mode {
        SimpleMode::C8 => result.structure.ss_sequence().replace(' ', "-"),
        SimpleMode::C3 => result.structure.ss_sequence_c3(),
    };

    writeln!(writer, "{}\t{}", seq, result.structure.id)
}

/// Write simple output with amino acid sequence
pub fn write_simple_with_aa<W: Write>(
    writer: &mut W,
    result: &DsspResult,
    mode: SimpleMode,
) -> std::io::Result<()> {
    let ss_seq = match mode {
        SimpleMode::C8 => result.structure.ss_sequence().replace(' ', "-"),
        SimpleMode::C3 => result.structure.ss_sequence_c3(),
    };
    let aa_seq = result.structure.aa_sequence();

    writeln!(writer, ">{}", result.structure.id)?;
    writeln!(writer, "AA: {}", aa_seq)?;
    writeln!(writer, "SS: {}", ss_seq)
}

/// Write only the secondary structure sequence (no ID)
pub fn write_sequence_only<W: Write>(
    writer: &mut W,
    structure: &Structure,
    mode: SimpleMode,
) -> std::io::Result<()> {
    let seq = match mode {
        SimpleMode::C8 => structure.ss_sequence().replace(' ', "-"),
        SimpleMode::C3 => structure.ss_sequence_c3(),
    };

    writeln!(writer, "{}", seq)
}

/// Write in FASTA-like format
pub fn write_fasta<W: Write>(
    writer: &mut W,
    result: &DsspResult,
    mode: SimpleMode,
) -> std::io::Result<()> {
    let seq = match mode {
        SimpleMode::C8 => result.structure.ss_sequence().replace(' ', "-"),
        SimpleMode::C3 => result.structure.ss_sequence_c3(),
    };

    writeln!(writer, ">{}", result.structure.id)?;

    // Write sequence in 80-character lines
    for chunk in seq.as_bytes().chunks(80) {
        writeln!(writer, "{}", std::str::from_utf8(chunk).unwrap_or(""))?;
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use dssp_core::types::{BackboneAtoms, Residue, SecondaryStructure, Statistics};
    use dssp_core::geometry::Point3;

    fn make_test_result() -> DsspResult {
        let mut residues = vec![
            Residue::new(
                "A".to_string(),
                1,
                "ALA".to_string(),
                BackboneAtoms::new(
                    Point3::new(0.0, 0.0, 0.0),
                    Point3::new(1.5, 0.0, 0.0),
                    Point3::new(2.5, 0.0, 0.0),
                    Point3::new(3.5, 0.0, 0.0),
                ),
            ),
        ];
        residues[0].structure = SecondaryStructure::AlphaHelix;

        let mut structure = Structure::from_residues(residues);
        structure.id = "test".to_string();

        DsspResult {
            structure,
            statistics: Statistics::default(),
        }
    }

    #[test]
    fn test_simple_output() {
        let result = make_test_result();
        let mut output = Vec::new();

        write_simple(&mut output, &result, SimpleMode::C8).unwrap();

        let output_str = String::from_utf8(output).unwrap();
        assert!(output_str.contains("H"));
        assert!(output_str.contains("test"));
    }
}
