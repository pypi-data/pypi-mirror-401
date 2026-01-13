//! mmCIF secondary structure annotation writer

use dssp_core::types::{DsspResult, SecondaryStructure};
use std::io::Write;

/// Write secondary structure annotations in mmCIF format
pub fn write_cif<W: Write>(writer: &mut W, result: &DsspResult) -> std::io::Result<()> {
    writeln!(writer, "# Secondary structure annotation from rs-dssp")?;
    writeln!(writer)?;
    writeln!(writer, "loop_")?;
    writeln!(writer, "_struct_conf.id")?;
    writeln!(writer, "_struct_conf.conf_type_id")?;
    writeln!(writer, "_struct_conf.beg_label_asym_id")?;
    writeln!(writer, "_struct_conf.beg_label_seq_id")?;
    writeln!(writer, "_struct_conf.end_label_asym_id")?;
    writeln!(writer, "_struct_conf.end_label_seq_id")?;

    let residues = &result.structure.residues;
    let mut conf_id = 1;
    let mut i = 0;

    while i < residues.len() {
        let ss = residues[i].structure;
        if ss == SecondaryStructure::Loop {
            i += 1;
            continue;
        }

        let start_chain = &residues[i].chain_id;
        let start_seq = residues[i].seq_id;
        let mut end_seq = start_seq;
        let mut j = i + 1;

        // Find contiguous region with same structure
        while j < residues.len()
            && residues[j].structure == ss
            && residues[j].chain_id == *start_chain
        {
            end_seq = residues[j].seq_id;
            j += 1;
        }

        let conf_type = match ss {
            SecondaryStructure::AlphaHelix => "HELX_RH_AL_P",
            SecondaryStructure::Helix310 => "HELX_RH_3T_P",
            SecondaryStructure::PiHelix => "HELX_RH_PI_P",
            SecondaryStructure::PPIIHelix => "HELX_LH_PP_P",
            SecondaryStructure::Strand | SecondaryStructure::BetaBridge => "STRN",
            SecondaryStructure::Turn => "TURN_TY1_P",
            SecondaryStructure::Bend => "BEND",
            SecondaryStructure::Loop => continue,
        };

        writeln!(
            writer,
            "{} {} {} {} {} {}",
            conf_id, conf_type, start_chain, start_seq, start_chain, end_seq
        )?;

        conf_id += 1;
        i = j;
    }

    Ok(())
}
