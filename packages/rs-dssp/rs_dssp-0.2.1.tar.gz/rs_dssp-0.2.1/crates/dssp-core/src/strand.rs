//! Beta strand and bridge detection
//!
//! Implements detection of:
//! - Beta bridges (parallel and antiparallel)
//! - Beta strands (connected bridges forming ladders)
//! - Beta sheets (connected ladders)

use crate::hbond::{test_accept, test_bond};
use crate::helix::no_chain_break_range;
use crate::types::{BridgePartner, BridgeType, Residue, SecondaryStructure, Statistics};
use std::collections::{HashSet, VecDeque};

/// A beta bridge between two strands
#[derive(Debug, Clone)]
pub struct Bridge {
    pub bridge_type: BridgeType,
    pub i_residues: Vec<usize>,
    pub j_residues: Vec<usize>,
    pub chain_i: String,
    pub chain_j: String,
    pub ladder: u32,
    pub sheet: u32,
}

impl Bridge {
    fn new(bridge_type: BridgeType, i: usize, j: usize, residues: &[Residue]) -> Self {
        Self {
            bridge_type,
            i_residues: vec![i],
            j_residues: vec![j],
            chain_i: residues[i].chain_id.clone(),
            chain_j: residues[j].chain_id.clone(),
            ladder: 0,
            sheet: 0,
        }
    }
}

/// Test for parallel or antiparallel bridge between two residues
///
/// Parallel bridge patterns:
/// ```text
/// Pattern I:          Pattern II:
///   i-1  O...H  j        i-1        j
///    |         |          |        /
///    i  H...O  j+1        i  H...O j+1
///    |         |          |        \
///   i+1        j+2       i+1 O...H  j+2
/// ```
///
/// Antiparallel bridge patterns:
/// ```text
/// Pattern III:        Pattern IV:
///   i-1        j+1      i-1        j+1
///    |         |         |         |
///    i  O...H  j         i <---->  j
///    |         |         |         |
///   i+1 H...O  j-1      i+1        j-1
/// ```
pub fn test_bridge(residues: &[Residue], i: usize, j: usize) -> BridgeType {
    // Need neighbors for all patterns
    if i < 1 || j < 1 || i + 1 >= residues.len() || j + 1 >= residues.len() {
        return BridgeType::None;
    }

    // Check chain continuity around both residues
    if !no_chain_break_range(residues, i - 1, i + 1)
        || !no_chain_break_range(residues, j - 1, j + 1)
    {
        return BridgeType::None;
    }

    // Get internal indices
    let idx_i_prev = residues[i - 1].internal_nr;
    let idx_i = residues[i].internal_nr;
    let _idx_i_next = residues[i + 1].internal_nr;
    let idx_j_prev = residues[j - 1].internal_nr;
    let idx_j = residues[j].internal_nr;
    let _idx_j_next = residues[j + 1].internal_nr;

    // Parallel bridge:
    // (i+1 donates to j) AND (j donates to i-1)
    // OR (j+1 donates to i) AND (i donates to j-1)
    let parallel = (test_bond(&residues[i + 1], idx_j) && test_bond(&residues[j], idx_i_prev))
        || (test_bond(&residues[j + 1], idx_i) && test_bond(&residues[i], idx_j_prev));

    // Antiparallel bridge:
    // (i+1 donates to j-1) AND (j+1 donates to i-1)
    // OR (j donates to i) AND (i donates to j)
    let antiparallel =
        (test_bond(&residues[i + 1], idx_j_prev) && test_bond(&residues[j + 1], idx_i_prev))
            || (test_bond(&residues[j], idx_i) && test_bond(&residues[i], idx_j));

    // Could also check:
    // OR (i accepts from j) AND (j accepts from i)
    let antiparallel = antiparallel
        || (test_accept(&residues[i], idx_j) && test_accept(&residues[j], idx_i));

    if parallel {
        BridgeType::Parallel
    } else if antiparallel {
        BridgeType::AntiParallel
    } else {
        BridgeType::None
    }
}

/// Calculate beta sheets from bridges
pub fn calculate_beta_sheets(
    residues: &mut [Residue],
    pairs: &[(usize, usize)],
    stats: &mut Statistics,
) {
    let mut bridges: Vec<Bridge> = Vec::new();

    // Find all bridges
    for &(i, j) in pairs {
        // Skip if residues are too close
        if j <= i + 3 {
            continue;
        }

        let bridge_type = test_bridge(residues, i, j);
        if bridge_type == BridgeType::None {
            continue;
        }

        // Try to extend existing bridge
        let extended = extend_existing_bridge(&mut bridges, i, j, bridge_type);

        if !extended {
            bridges.push(Bridge::new(bridge_type, i, j, residues));
        }
    }

    // Sort bridges by first residue index
    bridges.sort_by(|a, b| {
        a.i_residues
            .first()
            .cmp(&b.i_residues.first())
            .then(a.j_residues.first().cmp(&b.j_residues.first()))
    });

    // Extend ladders with bulges
    extend_ladders_with_bulges(&mut bridges, residues);

    // Assign sheets and ladders
    assign_sheets_and_ladders(&mut bridges, residues, stats);

    // Assign secondary structure
    assign_strand_structures(&bridges, residues, stats);
}

/// Try to extend an existing bridge with a new residue pair
fn extend_existing_bridge(
    bridges: &mut [Bridge],
    i: usize,
    j: usize,
    bridge_type: BridgeType,
) -> bool {
    for bridge in bridges.iter_mut() {
        if bridge.bridge_type != bridge_type {
            continue;
        }

        // Check if this extends the bridge
        let last_i = *bridge.i_residues.last().unwrap();
        let extends = match bridge_type {
            BridgeType::Parallel => {
                let last_j = *bridge.j_residues.last().unwrap();
                i == last_i + 1 && j == last_j + 1
            }
            BridgeType::AntiParallel => {
                let first_j = *bridge.j_residues.first().unwrap();
                i == last_i + 1 && j + 1 == first_j
            }
            BridgeType::None => false,
        };

        if extends {
            bridge.i_residues.push(i);
            match bridge_type {
                BridgeType::Parallel => bridge.j_residues.push(j),
                BridgeType::AntiParallel => bridge.j_residues.insert(0, j),
                BridgeType::None => {}
            }
            return true;
        }
    }
    false
}

/// Extend ladders with bulges (allow small gaps in ladder)
fn extend_ladders_with_bulges(bridges: &mut Vec<Bridge>, residues: &[Residue]) {
    let mut i = 0;
    while i < bridges.len() {
        let mut j = i + 1;
        while j < bridges.len() {
            if can_merge_with_bulge(&bridges[i], &bridges[j], residues) {
                let bridge_j = bridges.remove(j);
                merge_bridges(&mut bridges[i], bridge_j);
            } else {
                j += 1;
            }
        }
        i += 1;
    }
}

/// Check if two bridges can be merged with a bulge
fn can_merge_with_bulge(a: &Bridge, b: &Bridge, residues: &[Residue]) -> bool {
    if a.bridge_type != b.bridge_type {
        return false;
    }

    let ibi = *a.i_residues.first().unwrap();
    let iei = *a.i_residues.last().unwrap();
    let jbi = *a.j_residues.first().unwrap();
    let jei = *a.j_residues.last().unwrap();
    let ibj = *b.i_residues.first().unwrap();
    let iej = *b.i_residues.last().unwrap();
    let jbj = *b.j_residues.first().unwrap();
    let jej = *b.j_residues.last().unwrap();

    // Check chain continuity
    let i_min = ibi.min(ibj);
    let i_max = iei.max(iej);
    let j_min = jbi.min(jbj);
    let j_max = jei.max(jej);

    if !no_chain_break_range(residues, i_min, i_max)
        || !no_chain_break_range(residues, j_min, j_max)
    {
        return false;
    }

    // Check gap sizes
    let gap_i = ibj.saturating_sub(iei);
    let gap_j = match a.bridge_type {
        BridgeType::Parallel => jbj.saturating_sub(jei),
        BridgeType::AntiParallel => jbi.saturating_sub(jej),
        BridgeType::None => return false,
    };

    // Overlap check
    if iei >= ibj && ibi <= iej {
        return false;
    }

    // Bulge rules:
    // - One gap can be 0-5 residues, other must be 0-2
    // - Or both gaps must be 0-2
    (gap_i < 6 && gap_j < 3) || (gap_i < 3 && gap_j < 6) || (gap_i < 3 && gap_j < 3)
}

/// Merge two bridges
fn merge_bridges(a: &mut Bridge, b: Bridge) {
    a.i_residues.extend(b.i_residues);
    a.i_residues.sort();
    a.i_residues.dedup();

    match a.bridge_type {
        BridgeType::Parallel => {
            a.j_residues.extend(b.j_residues);
            a.j_residues.sort();
            a.j_residues.dedup();
        }
        BridgeType::AntiParallel => {
            let mut new_j = b.j_residues;
            new_j.extend(a.j_residues.drain(..));
            new_j.sort();
            new_j.reverse();
            new_j.dedup();
            a.j_residues = new_j;
        }
        BridgeType::None => {}
    }
}

/// Assign sheet and ladder IDs to bridges
fn assign_sheets_and_ladders(
    bridges: &mut [Bridge],
    _residues: &mut [Residue],
    stats: &mut Statistics,
) {
    let mut sheet_id = 1u32;
    let mut ladder_id = 1u32;
    let mut assigned: HashSet<usize> = HashSet::new();

    for start_idx in 0..bridges.len() {
        if assigned.contains(&start_idx) {
            continue;
        }

        // BFS to find all connected bridges
        let mut sheet_bridges: Vec<usize> = Vec::new();
        let mut queue: VecDeque<usize> = VecDeque::new();
        queue.push_back(start_idx);

        while let Some(idx) = queue.pop_front() {
            if assigned.contains(&idx) {
                continue;
            }
            assigned.insert(idx);
            sheet_bridges.push(idx);

            for other_idx in 0..bridges.len() {
                if !assigned.contains(&other_idx)
                    && bridges_linked(&bridges[idx], &bridges[other_idx])
                {
                    queue.push_back(other_idx);
                }
            }
        }

        // Assign sheet and ladder IDs
        for &idx in &sheet_bridges {
            bridges[idx].sheet = sheet_id;
            bridges[idx].ladder = ladder_id;
            ladder_id += 1;

            // Update statistics
            let len = bridges[idx].i_residues.len().min(30);
            if len > 0 {
                if bridges[idx].bridge_type == BridgeType::Parallel {
                    stats.parallel_bridges_per_ladder[len - 1] += 1;
                } else {
                    stats.antiparallel_bridges_per_ladder[len - 1] += 1;
                }
            }
        }

        // Update ladders per sheet histogram
        let ladder_count = sheet_bridges.len().min(30);
        if ladder_count > 0 {
            stats.ladders_per_sheet[ladder_count - 1] += 1;
        }

        sheet_id += 1;
    }
}

/// Check if two bridges share any residues (are linked)
fn bridges_linked(a: &Bridge, b: &Bridge) -> bool {
    a.i_residues.iter().any(|r| b.i_residues.contains(r) || b.j_residues.contains(r))
        || a.j_residues.iter().any(|r| b.i_residues.contains(r) || b.j_residues.contains(r))
}

/// Assign strand/bridge secondary structure
fn assign_strand_structures(bridges: &[Bridge], residues: &mut [Residue], stats: &mut Statistics) {
    for bridge in bridges {
        // Determine structure type
        let ss = if bridge.i_residues.len() > 1 || bridge.j_residues.len() > 1 {
            SecondaryStructure::Strand
        } else {
            SecondaryStructure::BetaBridge
        };

        // Update H-bond statistics
        let hbond_count = bridge.i_residues.len() + 1;
        match bridge.bridge_type {
            BridgeType::Parallel => {
                stats.hbonds_parallel_bridges += hbond_count as u32;
            }
            BridgeType::AntiParallel => {
                stats.hbonds_antiparallel_bridges += hbond_count as u32;
            }
            BridgeType::None => {}
        }

        // Assign structure to i-strand residues
        for (k, &i) in bridge.i_residues.iter().enumerate() {
            if residues[i].structure != SecondaryStructure::Strand {
                residues[i].structure = ss;
            }
            residues[i].sheet_id = bridge.sheet;

            // Set beta partner
            let partner_idx = match bridge.bridge_type {
                BridgeType::Parallel => bridge.j_residues.get(k).copied(),
                BridgeType::AntiParallel => bridge
                    .j_residues
                    .len()
                    .checked_sub(1)
                    .and_then(|last| last.checked_sub(k))
                    .and_then(|idx| bridge.j_residues.get(idx).copied()),
                BridgeType::None => None,
            };

            if let Some(partner) = partner_idx {
                let slot = if residues[i].bridge_partners[0].residue_idx.is_none() {
                    0
                } else {
                    1
                };
                residues[i].bridge_partners[slot] = BridgePartner {
                    residue_idx: Some(partner),
                    ladder: bridge.ladder,
                    parallel: bridge.bridge_type == BridgeType::Parallel,
                };
            }
        }

        // Assign structure to j-strand residues
        for (k, &j) in bridge.j_residues.iter().enumerate() {
            if residues[j].structure != SecondaryStructure::Strand {
                residues[j].structure = ss;
            }
            residues[j].sheet_id = bridge.sheet;

            // Set beta partner
            let partner_idx = match bridge.bridge_type {
                BridgeType::Parallel => bridge.i_residues.get(k).copied(),
                BridgeType::AntiParallel => bridge
                    .i_residues
                    .len()
                    .checked_sub(1)
                    .and_then(|last| last.checked_sub(k))
                    .and_then(|idx| bridge.i_residues.get(idx).copied()),
                BridgeType::None => None,
            };

            if let Some(partner) = partner_idx {
                let slot = if residues[j].bridge_partners[0].residue_idx.is_none() {
                    0
                } else {
                    1
                };
                residues[j].bridge_partners[slot] = BridgePartner {
                    residue_idx: Some(partner),
                    ladder: bridge.ladder,
                    parallel: bridge.bridge_type == BridgeType::Parallel,
                };
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bridge_type() {
        assert_ne!(BridgeType::Parallel, BridgeType::AntiParallel);
        assert_eq!(BridgeType::default(), BridgeType::None);
    }
}
