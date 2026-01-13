//! mmCIF format parser
//!
//! Parses mmCIF files to extract atom coordinates.

use crate::error::{IoError, Result};
use dssp_core::geometry::Point3;
use dssp_core::types::{AminoAcid, BackboneAtoms, Residue, Structure};
use std::collections::HashMap;
use std::io::{BufRead, BufReader, Read};

/// Parse a mmCIF file into a Structure
pub fn parse_cif<R: Read>(reader: R) -> Result<Structure> {
    let reader = BufReader::new(reader);
    let lines: Vec<String> = reader.lines().collect::<std::io::Result<_>>()?;

    // Find _atom_site loop
    let (header, data) = find_atom_site_loop(&lines)?;

    // Parse atoms
    let atoms = parse_atom_site_data(&header, &data)?;

    // Build residues
    build_structure_from_atoms(atoms)
}

/// Parse mmCIF file from path
pub fn parse_cif_file(path: &str) -> Result<Structure> {
    let file = std::fs::File::open(path)?;
    let mut structure = parse_cif(file)?;
    if structure.id.is_empty() {
        structure.id = std::path::Path::new(path)
            .file_stem()
            .and_then(|s| s.to_str())
            .unwrap_or("unknown")
            .to_string();
    }
    Ok(structure)
}

#[derive(Debug, Default)]
struct AtomSiteHeader {
    type_symbol: Option<usize>,
    label_atom_id: Option<usize>,
    label_comp_id: Option<usize>,
    label_asym_id: Option<usize>,
    label_seq_id: Option<usize>,
    auth_asym_id: Option<usize>,
    auth_seq_id: Option<usize>,
    pdbx_pdb_ins_code: Option<usize>,
    cartn_x: Option<usize>,
    cartn_y: Option<usize>,
    cartn_z: Option<usize>,
    label_alt_id: Option<usize>,
    pdbx_pdb_model_num: Option<usize>,
}

#[derive(Debug)]
struct CifAtom {
    atom_name: String,
    res_name: String,
    chain_id: String,
    seq_id: i32,
    ins_code: String,
    x: f32,
    y: f32,
    z: f32,
    alt_loc: String,
    model_num: i32,
}

fn find_atom_site_loop(lines: &[String]) -> Result<(AtomSiteHeader, Vec<String>)> {
    let mut in_atom_site = false;
    let mut header = AtomSiteHeader::default();
    let mut col_idx = 0usize;
    let mut data_lines = Vec::new();

    for line in lines {
        let trimmed = line.trim();

        if trimmed.starts_with("loop_") {
            in_atom_site = false;
            col_idx = 0;
        } else if trimmed.starts_with("_atom_site.") {
            in_atom_site = true;
            let field = &trimmed[11..];

            match field {
                "type_symbol" => header.type_symbol = Some(col_idx),
                "label_atom_id" => header.label_atom_id = Some(col_idx),
                "label_comp_id" => header.label_comp_id = Some(col_idx),
                "label_asym_id" => header.label_asym_id = Some(col_idx),
                "label_seq_id" => header.label_seq_id = Some(col_idx),
                "auth_asym_id" => header.auth_asym_id = Some(col_idx),
                "auth_seq_id" => header.auth_seq_id = Some(col_idx),
                "pdbx_PDB_ins_code" => header.pdbx_pdb_ins_code = Some(col_idx),
                "Cartn_x" => header.cartn_x = Some(col_idx),
                "Cartn_y" => header.cartn_y = Some(col_idx),
                "Cartn_z" => header.cartn_z = Some(col_idx),
                "label_alt_id" => header.label_alt_id = Some(col_idx),
                "pdbx_PDB_model_num" => header.pdbx_pdb_model_num = Some(col_idx),
                _ => {}
            }
            col_idx += 1;
        } else if in_atom_site && !trimmed.is_empty() && !trimmed.starts_with('#') {
            if trimmed.starts_with('_') || trimmed.starts_with("loop_") {
                break;
            }
            data_lines.push(line.clone());
        }
    }

    if data_lines.is_empty() {
        return Err(IoError::EmptyFile);
    }

    Ok((header, data_lines))
}

fn parse_atom_site_data(header: &AtomSiteHeader, data: &[String]) -> Result<Vec<CifAtom>> {
    let mut atoms = Vec::new();

    for line in data {
        let fields = parse_cif_line(line);

        // Get required fields
        let atom_name = get_field(&fields, header.label_atom_id, "label_atom_id")?;
        let res_name = get_field(&fields, header.label_comp_id, "label_comp_id")?;
        let x: f32 = get_field(&fields, header.cartn_x, "Cartn_x")?.parse()?;
        let y: f32 = get_field(&fields, header.cartn_y, "Cartn_y")?.parse()?;
        let z: f32 = get_field(&fields, header.cartn_z, "Cartn_z")?.parse()?;

        // Prefer auth_* over label_* for chain and seq
        let chain_id = header.auth_asym_id
            .or(header.label_asym_id)
            .and_then(|i| fields.get(i))
            .map(|s| s.to_string())
            .unwrap_or_else(|| "A".to_string());

        let seq_id_str = header.auth_seq_id
            .or(header.label_seq_id)
            .and_then(|i| fields.get(i))
            .map(|s| s.as_str())
            .unwrap_or("1");
        let seq_id: i32 = seq_id_str.parse().unwrap_or(1);

        let ins_code = header.pdbx_pdb_ins_code
            .and_then(|i| fields.get(i))
            .map(|s| if s == "?" || s == "." { "" } else { s.as_str() })
            .unwrap_or("")
            .to_string();

        let alt_loc = header.label_alt_id
            .and_then(|i| fields.get(i))
            .map(|s| if s == "." { "" } else { s.as_str() })
            .unwrap_or("")
            .to_string();

        let model_num = header.pdbx_pdb_model_num
            .and_then(|i| fields.get(i))
            .and_then(|s| s.parse().ok())
            .unwrap_or(1);

        atoms.push(CifAtom {
            atom_name,
            res_name,
            chain_id,
            seq_id,
            ins_code,
            x,
            y,
            z,
            alt_loc,
            model_num,
        });
    }

    Ok(atoms)
}

fn parse_cif_line(line: &str) -> Vec<String> {
    let mut fields = Vec::new();
    let mut current = String::new();
    let mut in_quote = false;
    let mut quote_char = ' ';

    for c in line.chars() {
        if in_quote {
            if c == quote_char {
                in_quote = false;
                fields.push(current.clone());
                current.clear();
            } else {
                current.push(c);
            }
        } else if c == '\'' || c == '"' {
            in_quote = true;
            quote_char = c;
        } else if c.is_whitespace() {
            if !current.is_empty() {
                fields.push(current.clone());
                current.clear();
            }
        } else {
            current.push(c);
        }
    }

    if !current.is_empty() {
        fields.push(current);
    }

    fields
}

fn get_field<'a>(fields: &'a [String], idx: Option<usize>, name: &str) -> Result<String> {
    idx.and_then(|i| fields.get(i))
        .map(|s| s.to_string())
        .ok_or_else(|| IoError::MissingField(name.to_string()))
}

fn build_structure_from_atoms(atoms: Vec<CifAtom>) -> Result<Structure> {
    // Only use model 1
    let atoms: Vec<_> = atoms.into_iter().filter(|a| a.model_num == 1).collect();

    // Group by residue
    let mut residue_map: HashMap<(String, i32, String), ResidueData> = HashMap::new();
    let mut residue_order: Vec<(String, i32, String)> = Vec::new();

    for atom in atoms {
        // Skip non-standard residues or water
        if atom.res_name == "HOH" || atom.res_name == "WAT" {
            continue;
        }

        let key = (atom.chain_id.clone(), atom.seq_id, atom.ins_code.clone());

        if !residue_map.contains_key(&key) {
            residue_order.push(key.clone());
            residue_map.insert(key.clone(), ResidueData {
                chain_id: atom.chain_id.clone(),
                seq_id: atom.seq_id,
                ins_code: atom.ins_code.clone(),
                res_name: atom.res_name.clone(),
                n: None,
                ca: None,
                c: None,
                o: None,
                h: None,
                side_chain: Vec::new(),
                alt_loc_preferred: String::new(),
            });
        }

        if let Some(data) = residue_map.get_mut(&key) {
            // Handle alternate locations
            if !atom.alt_loc.is_empty() {
                if data.alt_loc_preferred.is_empty() {
                    data.alt_loc_preferred = atom.alt_loc.clone();
                }
                if atom.alt_loc != data.alt_loc_preferred {
                    continue;
                }
            }

            let point = Point3::new(atom.x, atom.y, atom.z);

            match atom.atom_name.as_str() {
                "N" => data.n = Some(point),
                "CA" => data.ca = Some(point),
                "C" => data.c = Some(point),
                "O" | "OXT" => {
                    if data.o.is_none() {
                        data.o = Some(point);
                    }
                }
                "H" | "HN" => data.h = Some(point),
                name if !name.starts_with('H') => {
                    data.side_chain.push((name.to_string(), point));
                }
                _ => {}
            }
        }
    }

    // Build residues
    let residues: Vec<Residue> = residue_order
        .iter()
        .filter_map(|key| {
            residue_map.remove(key).and_then(|data| data.build())
        })
        .collect();

    if residues.is_empty() {
        return Err(IoError::EmptyFile);
    }

    Ok(Structure::from_residues(residues))
}

struct ResidueData {
    chain_id: String,
    seq_id: i32,
    ins_code: String,
    res_name: String,
    n: Option<Point3>,
    ca: Option<Point3>,
    c: Option<Point3>,
    o: Option<Point3>,
    h: Option<Point3>,
    side_chain: Vec<(String, Point3)>,
    alt_loc_preferred: String,
}

impl ResidueData {
    fn build(self) -> Option<Residue> {
        let n = self.n?;
        let ca = self.ca?;
        let c = self.c?;
        let o = self.o?;

        let backbone = if let Some(h) = self.h {
            BackboneAtoms::with_hydrogen(n, ca, c, o, h)
        } else {
            BackboneAtoms::new(n, ca, c, o)
        };

        let mut residue = Residue::new(self.chain_id, self.seq_id, self.res_name.clone(), backbone);
        residue.ins_code = self.ins_code;
        residue.amino_acid = AminoAcid::from_three_letter(&self.res_name);
        residue.side_chain = self.side_chain;

        Some(residue)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_cif_line() {
        let line = "ATOM 1 N N . ALA A 1 1 ? 0.000 0.000 0.000 1.00 0.00 ? ? ? ? ? ? A N 1";
        let fields = parse_cif_line(line);
        assert!(!fields.is_empty());
    }
}
