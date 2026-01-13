//! Helix detection
//!
//! Detects three types of helices based on hydrogen bonding patterns:
//! - 3₁₀ helix (G): i+3 -> i H-bond pattern
//! - α helix (H): i+4 -> i H-bond pattern (highest priority)
//! - π helix (I): i+5 -> i H-bond pattern

use crate::constants::BEND_THRESHOLD;
use crate::hbond::test_bond;
use crate::types::{ChainBreak, HelixPosition, HelixType, Residue, SecondaryStructure};

/// Detect all helix types (3-10, alpha, pi)
///
/// This function:
/// 1. Identifies helix patterns for each type based on H-bond patterns
/// 2. Marks bend positions (kappa > 70°)
/// 3. Assigns secondary structure based on helix patterns with priority rules
///
/// # Arguments
/// * `residues` - Mutable slice of residues to process
pub fn detect_helices(residues: &mut [Residue]) {
    // Process each helix type: 3-10 (stride=3), alpha (stride=4), pi (stride=5)
    for helix_type in HelixType::hbond_types() {
        detect_helix_type(residues, helix_type);
    }

    // Mark bends (kappa > 70 degrees)
    for residue in residues.iter_mut() {
        if let Some(kappa) = residue.kappa {
            residue.is_bend = kappa > BEND_THRESHOLD;
        }
    }

    // Assign secondary structure based on helix patterns
    assign_helix_structures(residues);
}

/// Detect helices of a specific type
///
/// A helix is formed when there are consecutive residues with the appropriate
/// H-bond pattern. For each H-bond from residue[i+stride] to residue[i],
/// we mark positions as Start, Middle, or End.
fn detect_helix_type(residues: &mut [Residue], helix_type: HelixType) {
    let stride = helix_type.stride();
    let n = residues.len();

    if n <= stride {
        return;
    }

    let helix_idx = helix_type as usize;

    for i in 0..(n - stride) {
        // Check for chain break
        if !no_chain_break(&residues[i..=i + stride]) {
            continue;
        }

        // Test for H-bond from residue[i+stride] (donor) to residue[i] (acceptor)
        let acceptor_idx = residues[i].internal_nr;
        if test_bond(&residues[i + stride], acceptor_idx) {
            // Mark the end position (residue i+stride has the H-bond)
            let end_idx = i + stride;
            match residues[end_idx].helix_flags[helix_idx] {
                HelixPosition::Start => {
                    residues[end_idx].helix_flags[helix_idx] = HelixPosition::StartAndEnd;
                }
                HelixPosition::None | HelixPosition::Middle => {
                    residues[end_idx].helix_flags[helix_idx] = HelixPosition::End;
                }
                _ => {}
            }

            // Mark middle residues
            for j in (i + 1)..(i + stride) {
                if residues[j].helix_flags[helix_idx] == HelixPosition::None {
                    residues[j].helix_flags[helix_idx] = HelixPosition::Middle;
                }
            }

            // Mark the start position (residue i accepts the H-bond)
            match residues[i].helix_flags[helix_idx] {
                HelixPosition::End => {
                    residues[i].helix_flags[helix_idx] = HelixPosition::StartAndEnd;
                }
                HelixPosition::None | HelixPosition::Middle => {
                    residues[i].helix_flags[helix_idx] = HelixPosition::Start;
                }
                _ => {}
            }
        }
    }
}

/// Assign helix secondary structure types based on detected patterns
///
/// Priority: α-helix > 3₁₀-helix/π-helix
///
/// A helix is assigned when two consecutive helix starts are found,
/// meaning there's a continuous stretch of the H-bond pattern.
fn assign_helix_structures(residues: &mut [Residue]) {
    let n = residues.len();

    // Alpha helices first (highest priority)
    // Requires two consecutive starts to form a helix
    for i in 1..n.saturating_sub(4) {
        let idx = HelixType::Alpha as usize;
        if residues[i].helix_flags[idx].is_start()
            && residues[i - 1].helix_flags[idx].is_start()
        {
            // Assign helix to residues i through i+3
            for j in i..=(i + 3).min(n - 1) {
                if !residues[j].structure.is_strand() {
                    residues[j].structure = SecondaryStructure::AlphaHelix;
                }
            }
        }
    }

    // 3-10 helices (only if not already alpha helix)
    for i in 1..n.saturating_sub(3) {
        let idx = HelixType::H310 as usize;
        if residues[i].helix_flags[idx].is_start()
            && residues[i - 1].helix_flags[idx].is_start()
        {
            // Check if region is available (not already alpha helix)
            let available = (i..=(i + 2).min(n - 1)).all(|j| {
                matches!(
                    residues[j].structure,
                    SecondaryStructure::Loop | SecondaryStructure::Helix310
                )
            });

            if available {
                for j in i..=(i + 2).min(n - 1) {
                    residues[j].structure = SecondaryStructure::Helix310;
                }
            }
        }
    }

    // Pi helices (can override alpha helix in some implementations)
    for i in 1..n.saturating_sub(5) {
        let idx = HelixType::Pi as usize;
        if residues[i].helix_flags[idx].is_start()
            && residues[i - 1].helix_flags[idx].is_start()
        {
            // Check if region is available (not strand)
            let available = (i..=(i + 4).min(n - 1)).all(|j| {
                !residues[j].structure.is_strand()
            });

            if available {
                for j in i..=(i + 4).min(n - 1) {
                    // Only assign if currently loop or already pi helix
                    if matches!(
                        residues[j].structure,
                        SecondaryStructure::Loop | SecondaryStructure::PiHelix
                    ) {
                        residues[j].structure = SecondaryStructure::PiHelix;
                    }
                }
            }
        }
    }
}

/// Check for no chain break in a slice of residues
#[inline]
fn no_chain_break(residues: &[Residue]) -> bool {
    if residues.len() < 2 {
        return true;
    }

    let first_chain = &residues[0].chain_id;
    residues[1..].iter().all(|r| {
        r.chain_id == *first_chain && r.chain_break == ChainBreak::None
    })
}

/// Check for no chain break in a range of residues by indices
pub fn no_chain_break_range(residues: &[Residue], start: usize, end: usize) -> bool {
    if end >= residues.len() || start > end {
        return false;
    }
    no_chain_break(&residues[start..=end])
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_helix_type_stride() {
        assert_eq!(HelixType::H310.stride(), 3);
        assert_eq!(HelixType::Alpha.stride(), 4);
        assert_eq!(HelixType::Pi.stride(), 5);
    }

    #[test]
    fn test_helix_position() {
        assert!(HelixPosition::Start.is_start());
        assert!(HelixPosition::StartAndEnd.is_start());
        assert!(!HelixPosition::End.is_start());
        assert!(!HelixPosition::None.is_start());

        assert!(HelixPosition::End.is_end());
        assert!(HelixPosition::StartAndEnd.is_end());
        assert!(!HelixPosition::Start.is_end());
    }
}
