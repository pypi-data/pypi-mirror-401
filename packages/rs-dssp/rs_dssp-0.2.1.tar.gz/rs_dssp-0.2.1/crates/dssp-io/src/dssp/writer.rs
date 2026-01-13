//! Legacy DSSP format writer
//!
//! Writes output compatible with the original mkdssp program.

use dssp_core::constants::INVALID_ANGLE;
use dssp_core::types::{DsspResult, Residue, Statistics};
use std::io::Write;

/// Write DSSP output in legacy format
pub fn write_dssp<W: Write>(writer: &mut W, result: &DsspResult) -> std::io::Result<()> {
    write_header(writer, result)?;
    write_statistics(writer, &result.statistics)?;
    write_residue_header(writer)?;
    write_residues(writer, &result.structure.residues)?;
    Ok(())
}

fn write_header<W: Write>(writer: &mut W, result: &DsspResult) -> std::io::Result<()> {
    writeln!(
        writer,
        "==== Secondary Structure Definition by the program DSSP, rs-dssp version ===="
    )?;
    writeln!(
        writer,
        "REFERENCE W. KABSCH AND C.SANDER, BIOPOLYMERS 22 (1983) 2577-2637"
    )?;
    writeln!(
        writer,
        "                                                                          ."
    )?;
    writeln!(
        writer,
        "COMPND    {}",
        result.structure.id
    )?;
    Ok(())
}

fn write_statistics<W: Write>(writer: &mut W, stats: &Statistics) -> std::io::Result<()> {
    writeln!(
        writer,
        "{:5}{:3}{:3}{:3}{:3} TOTAL NUMBER OF RESIDUES, NUMBER OF CHAINS, NUMBER OF SS-BRIDGES(TOTAL,INTRACHAIN,INTERCHAIN) .",
        stats.residue_count,
        stats.chain_count,
        stats.ss_bridge_count,
        stats.intra_chain_ss_bridges,
        stats.ss_bridge_count.saturating_sub(stats.intra_chain_ss_bridges)
    )?;
    writeln!(
        writer,
        "{:8.1}   ACCESSIBLE SURFACE OF PROTEIN (ANGSTROM**2)                                                         .",
        stats.accessible_surface
    )?;

    // H-bond statistics
    let total_hbonds: u32 = stats.hbonds_per_distance.iter().sum();
    writeln!(
        writer,
        "{:5}{:5}{:5} TOTAL NUMBER OF HYDROGEN BONDS OF TYPE O(I)-->H-N(J)  , SAME NUMBER PER 100 RESIDUES              .",
        total_hbonds,
        stats.hbonds_parallel_bridges,
        stats.hbonds_antiparallel_bridges
    )?;

    Ok(())
}

fn write_residue_header<W: Write>(writer: &mut W) -> std::io::Result<()> {
    writeln!(
        writer,
        "  #  RESIDUE AA STRUCTURE BP1 BP2  ACC     N-H-->O    O-->H-N    N-H-->O    O-->H-N    TCO  KAPPA ALPHA  PHI   PSI    X-CA   Y-CA   Z-CA"
    )?;
    Ok(())
}

fn write_residues<W: Write>(writer: &mut W, residues: &[Residue]) -> std::io::Result<()> {
    for (i, residue) in residues.iter().enumerate() {
        write_residue_line(writer, i + 1, residue)?;
    }
    Ok(())
}

fn write_residue_line<W: Write>(writer: &mut W, nr: usize, residue: &Residue) -> std::io::Result<()> {
    // Format H-bond info
    let (nh_o_1, nh_o_e_1) = format_hbond(&residue.hbond_acceptor[0], nr);
    let (o_hn_1, o_hn_e_1) = format_hbond(&residue.hbond_donor[0], nr);
    let (nh_o_2, nh_o_e_2) = format_hbond(&residue.hbond_acceptor[1], nr);
    let (o_hn_2, o_hn_e_2) = format_hbond(&residue.hbond_donor[1], nr);

    // Format angles
    let tco = residue.tco.unwrap_or(0.0);
    let kappa = residue.kappa.unwrap_or(INVALID_ANGLE);
    let alpha = residue.alpha.unwrap_or(INVALID_ANGLE);
    let phi = residue.phi.unwrap_or(INVALID_ANGLE);
    let psi = residue.psi.unwrap_or(INVALID_ANGLE);

    // Format bridge partners
    let bp1 = residue.bridge_partners[0]
        .residue_idx
        .map(|i| i as i32 + 1)
        .unwrap_or(0);
    let bp2 = residue.bridge_partners[1]
        .residue_idx
        .map(|i| i as i32 + 1)
        .unwrap_or(0);

    writeln!(
        writer,
        "{:5} {:4}{}{} {} {}  {}{:4}{:4}{:5.0}{:6},{:4.1}{:6},{:4.1}{:6},{:4.1}{:6},{:4.1}  {:5.3}{:6.1}{:6.1}{:6.1}{:6.1}{:7.1}{:7.1}{:7.1}",
        nr,
        residue.seq_id,
        if residue.ins_code.is_empty() { " " } else { &residue.ins_code },
        &residue.chain_id[..1.min(residue.chain_id.len())],
        residue.amino_acid.as_char(),
        residue.compound_id.chars().next().unwrap_or(' '),
        residue.structure.as_char(),
        bp1,
        bp2,
        residue.accessibility,
        nh_o_1, nh_o_e_1,
        o_hn_1, o_hn_e_1,
        nh_o_2, nh_o_e_2,
        o_hn_2, o_hn_e_2,
        tco,
        kappa,
        alpha,
        phi,
        psi,
        residue.backbone.ca.x,
        residue.backbone.ca.y,
        residue.backbone.ca.z
    )
}

fn format_hbond(hbond: &dssp_core::types::HBond, current_nr: usize) -> (i32, f32) {
    match hbond.partner_idx {
        Some(partner) if hbond.is_bond() => {
            let offset = partner as i32 - current_nr as i32;
            (offset, hbond.energy as f32)
        }
        _ => (0, 0.0),
    }
}
