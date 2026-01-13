//! PDB format parser
//!
//! Parses standard PDB files to extract backbone atom coordinates.

use crate::error::{IoError, Result};
use dssp_core::geometry::Point3;
use dssp_core::types::{AminoAcid, BackboneAtoms, Residue, Structure};
use std::collections::HashMap;
use std::io::{BufRead, BufReader, Read};

/// Parse a PDB file into a Structure
///
/// # Arguments
/// * `reader` - Input reader
///
/// # Returns
/// Parsed Structure or error
pub fn parse_pdb<R: Read>(reader: R) -> Result<Structure> {
    let reader = BufReader::new(reader);
    let mut builders: HashMap<ResidueKey, ResidueBuilder> = HashMap::new();
    let mut residue_order: Vec<ResidueKey> = Vec::new();
    let mut structure_id = String::new();

    for (line_num, line) in reader.lines().enumerate() {
        let line = line?;

        // Extract structure ID from HEADER
        if line.starts_with("HEADER") && structure_id.is_empty() {
            if line.len() >= 66 {
                structure_id = line[62..66].trim().to_string();
            }
        }

        // Parse ATOM and HETATM records
        if line.starts_with("ATOM  ") || line.starts_with("HETATM") {
            match parse_atom_line(&line) {
                Ok(atom) => {
                    let key = ResidueKey {
                        chain_id: atom.chain_id.clone(),
                        res_seq: atom.res_seq,
                        ins_code: atom.ins_code.clone(),
                    };

                    if !builders.contains_key(&key) {
                        residue_order.push(key.clone());
                        builders.insert(
                            key.clone(),
                            ResidueBuilder::new(
                                &atom.chain_id,
                                atom.res_seq,
                                &atom.ins_code,
                                &atom.res_name,
                            ),
                        );
                    }

                    if let Some(builder) = builders.get_mut(&key) {
                        builder.add_atom(&atom);
                    }
                }
                Err(e) => {
                    log::debug!("Skipping line {}: {}", line_num + 1, e);
                }
            }
        }

        // Stop at END or ENDMDL (only process first model)
        if line.starts_with("END") || line.starts_with("ENDMDL") {
            break;
        }
    }

    // Build residues in order
    let residues: Vec<Residue> = residue_order
        .iter()
        .filter_map(|key| {
            builders.remove(key).and_then(|b| b.build())
        })
        .collect();

    if residues.is_empty() {
        return Err(IoError::EmptyFile);
    }

    Ok(Structure::from_residues(residues))
}

/// Parse a PDB file from a file path
pub fn parse_pdb_file(path: &str) -> Result<Structure> {
    let file = std::fs::File::open(path)?;
    let mut structure = parse_pdb(file)?;
    if structure.id.is_empty() {
        // Use filename as ID
        structure.id = std::path::Path::new(path)
            .file_stem()
            .and_then(|s| s.to_str())
            .unwrap_or("unknown")
            .to_string();
    }
    Ok(structure)
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct ResidueKey {
    chain_id: String,
    res_seq: i32,
    ins_code: String,
}

#[derive(Debug)]
struct AtomRecord {
    chain_id: String,
    res_seq: i32,
    ins_code: String,
    res_name: String,
    atom_name: String,
    x: f32,
    y: f32,
    z: f32,
    alt_loc: char,
}

fn parse_atom_line(line: &str) -> Result<AtomRecord> {
    if line.len() < 54 {
        return Err(IoError::invalid_record("Line too short"));
    }

    // PDB format columns (1-indexed):
    // 1-6: Record name (ATOM/HETATM)
    // 13-16: Atom name
    // 17: Alternate location indicator
    // 18-20: Residue name
    // 22: Chain identifier
    // 23-26: Residue sequence number
    // 27: Insertion code
    // 31-38: X coordinate
    // 39-46: Y coordinate
    // 47-54: Z coordinate

    let alt_loc = line.chars().nth(16).unwrap_or(' ');

    Ok(AtomRecord {
        atom_name: line[12..16].trim().to_string(),
        res_name: line[17..20].trim().to_string(),
        chain_id: line[21..22].to_string(),
        res_seq: line[22..26].trim().parse()?,
        ins_code: line[26..27].trim().to_string(),
        x: line[30..38].trim().parse()?,
        y: line[38..46].trim().parse()?,
        z: line[46..54].trim().parse()?,
        alt_loc,
    })
}

struct ResidueBuilder {
    chain_id: String,
    seq_id: i32,
    ins_code: String,
    compound_id: String,
    n: Option<Point3>,
    ca: Option<Point3>,
    c: Option<Point3>,
    o: Option<Point3>,
    h: Option<Point3>,
    side_chain: Vec<(String, Point3)>,
    alt_loc_preferred: char,
}

impl ResidueBuilder {
    fn new(chain_id: &str, seq_id: i32, ins_code: &str, compound_id: &str) -> Self {
        Self {
            chain_id: chain_id.to_string(),
            seq_id,
            ins_code: ins_code.to_string(),
            compound_id: compound_id.to_string(),
            n: None,
            ca: None,
            c: None,
            o: None,
            h: None,
            side_chain: Vec::new(),
            alt_loc_preferred: ' ',
        }
    }

    fn add_atom(&mut self, atom: &AtomRecord) {
        // Handle alternate locations - prefer 'A' or first seen
        if atom.alt_loc != ' ' && self.alt_loc_preferred == ' ' {
            self.alt_loc_preferred = atom.alt_loc;
        }
        if atom.alt_loc != ' ' && atom.alt_loc != self.alt_loc_preferred {
            return;
        }

        let point = Point3::new(atom.x, atom.y, atom.z);

        match atom.atom_name.as_str() {
            "N" => self.n = Some(point),
            "CA" => self.ca = Some(point),
            "C" => self.c = Some(point),
            "O" | "OXT" => {
                if self.o.is_none() {
                    self.o = Some(point);
                }
            }
            "H" | "HN" | "H1" => {
                if self.h.is_none() {
                    self.h = Some(point);
                }
            }
            name if !name.starts_with('H') && name != "OXT" => {
                self.side_chain.push((name.to_string(), point));
            }
            _ => {}
        }
    }

    fn build(self) -> Option<Residue> {
        // Require all backbone atoms
        let n = self.n?;
        let ca = self.ca?;
        let c = self.c?;
        let o = self.o?;

        let backbone = if let Some(h) = self.h {
            BackboneAtoms::with_hydrogen(n, ca, c, o, h)
        } else {
            BackboneAtoms::new(n, ca, c, o)
        };

        let mut residue = Residue::new(
            self.chain_id,
            self.seq_id,
            self.compound_id.clone(),
            backbone,
        );
        residue.ins_code = self.ins_code;
        residue.amino_acid = AminoAcid::from_three_letter(&self.compound_id);
        residue.side_chain = self.side_chain;

        Some(residue)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_atom_line() {
        let line = "ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N  ";
        let atom = parse_atom_line(line).unwrap();

        assert_eq!(atom.atom_name, "N");
        assert_eq!(atom.res_name, "ALA");
        assert_eq!(atom.chain_id, "A");
        assert_eq!(atom.res_seq, 1);
        assert!((atom.x - 0.0).abs() < 0.001);
    }

    #[test]
    fn test_parse_pdb() {
        let pdb_text = r#"ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       1.500   0.000   0.000  1.00  0.00           C
ATOM      3  C   ALA A   1       2.500   0.000   0.000  1.00  0.00           C
ATOM      4  O   ALA A   1       3.500   0.000   0.000  1.00  0.00           O
END
"#;

        let structure = parse_pdb(pdb_text.as_bytes()).unwrap();

        assert_eq!(structure.residues.len(), 1);
        assert_eq!(structure.residues[0].amino_acid, AminoAcid::Ala);
    }
}
