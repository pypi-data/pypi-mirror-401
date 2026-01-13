//! Main DSSP assignment logic
//!
//! Coordinates the full DSSP algorithm:
//! 1. Preprocess structure (chain breaks, dihedral angles, H positions)
//! 2. Calculate hydrogen bonds
//! 3. Detect beta sheets
//! 4. Detect helices
//! 5. Detect PPII helices
//! 6. Detect turns and bends
//! 7. Calculate SASA
//! 8. Collect statistics

use crate::constants::*;
use crate::geometry::{calculate_alpha, calculate_kappa, calculate_tco, dihedral_angle};
use crate::hbond::{calculate_all_hbonds, calculate_hydrogen_position, find_nearby_pairs};
use crate::helix::{detect_helices, no_chain_break_range};
use crate::ppii::detect_ppii_helices;
use crate::sasa::{calculate_sasa, calculate_total_sasa};
use crate::strand::calculate_beta_sheets;
use crate::turn::detect_turns_and_bends;
use crate::types::{ChainBreak, DsspResult, HBond, Statistics, Structure};

/// Configuration options for DSSP calculation
#[derive(Debug, Clone)]
pub struct DsspConfig {
    /// Minimum stretch length for PPII helix detection (2 or 3)
    pub min_ppii_stretch: usize,
    /// Whether to calculate surface accessibility
    pub calculate_accessibility: bool,
    /// Number of points for SASA calculation
    pub sasa_points: usize,
    /// Prefer pi helices over alpha helices
    pub prefer_pi_helices: bool,
}

impl Default for DsspConfig {
    fn default() -> Self {
        Self {
            min_ppii_stretch: MIN_PPII_STRETCH,
            calculate_accessibility: true,
            sasa_points: SASA_NUM_POINTS,
            prefer_pi_helices: true,
        }
    }
}

/// Main DSSP calculation entry point
///
/// # Arguments
/// * `structure` - Mutable structure to process
/// * `config` - Configuration options
///
/// # Returns
/// Statistics from the calculation
pub fn calculate_dssp(structure: &mut Structure, config: &DsspConfig) -> Statistics {
    let mut stats = Statistics::default();

    if structure.is_empty() {
        return stats;
    }

    // Step 1: Preprocess structure
    preprocess_structure(structure);

    // Step 2: Find nearby CA pairs for H-bond calculation
    let pairs = find_nearby_pairs(&structure.residues);

    // Step 3: Calculate hydrogen bond energies
    calculate_all_hbonds(&mut structure.residues, &pairs);

    // Step 4: Calculate beta sheets (before helices for priority)
    calculate_beta_sheets(&mut structure.residues, &pairs, &mut stats);

    // Step 5: Detect helices
    detect_helices(&mut structure.residues);

    // Step 6: Detect PPII helices
    detect_ppii_helices(&mut structure.residues, config.min_ppii_stretch);

    // Step 7: Detect turns and bends
    detect_turns_and_bends(&mut structure.residues);

    // Step 8: Calculate SASA
    if config.calculate_accessibility {
        calculate_sasa(&mut structure.residues, config.sasa_points);
        stats.accessible_surface = calculate_total_sasa(&structure.residues);
    }

    // Step 9: Collect statistics
    calculate_statistics(structure, &mut stats);

    stats
}

/// Calculate DSSP and return full result
pub fn calculate_dssp_full(mut structure: Structure, config: &DsspConfig) -> DsspResult {
    let statistics = calculate_dssp(&mut structure, config);
    DsspResult {
        structure,
        statistics,
    }
}

/// Preprocess structure: calculate dihedral angles and hydrogen positions
fn preprocess_structure(structure: &mut Structure) {
    let n = structure.residues.len();

    // Update internal indices
    structure.update_internal_indices();

    // First pass: detect chain breaks
    for i in 1..n {
        let prev_c = &structure.residues[i - 1].backbone.c;
        let curr_n = &structure.residues[i].backbone.n;

        if prev_c.distance(curr_n) > MAX_PEPTIDE_BOND_LENGTH {
            structure.residues[i].chain_break = if structure.residues[i - 1].chain_id
                == structure.residues[i].chain_id
            {
                ChainBreak::Gap
            } else {
                ChainBreak::NewChain
            };
        }
    }

    // Second pass: calculate geometry for each residue
    for i in 0..n {
        // Assign hydrogen position
        if i > 0 && structure.residues[i].chain_break == ChainBreak::None {
            let h = calculate_hydrogen_position(
                &structure.residues[i].backbone.n,
                &structure.residues[i].backbone.ca,
                &structure.residues[i - 1].backbone.c,
            );
            structure.residues[i].backbone.h = Some(h);
        }

        // Calculate phi angle (C(i-1)-N(i)-CA(i)-C(i))
        if i > 0 && structure.residues[i].chain_break == ChainBreak::None {
            let phi = dihedral_angle(
                &structure.residues[i - 1].backbone.c,
                &structure.residues[i].backbone.n,
                &structure.residues[i].backbone.ca,
                &structure.residues[i].backbone.c,
            );
            if phi != INVALID_ANGLE {
                structure.residues[i].phi = Some(phi);
            }
        }

        // Calculate psi angle (N(i)-CA(i)-C(i)-N(i+1))
        if i + 1 < n && structure.residues[i + 1].chain_break == ChainBreak::None {
            let psi = dihedral_angle(
                &structure.residues[i].backbone.n,
                &structure.residues[i].backbone.ca,
                &structure.residues[i].backbone.c,
                &structure.residues[i + 1].backbone.n,
            );
            if psi != INVALID_ANGLE {
                structure.residues[i].psi = Some(psi);
            }
        }

        // Calculate omega angle (CA(i)-C(i)-N(i+1)-CA(i+1))
        if i + 1 < n && structure.residues[i + 1].chain_break == ChainBreak::None {
            let omega = dihedral_angle(
                &structure.residues[i].backbone.ca,
                &structure.residues[i].backbone.c,
                &structure.residues[i + 1].backbone.n,
                &structure.residues[i + 1].backbone.ca,
            );
            if omega != INVALID_ANGLE {
                structure.residues[i].omega = Some(omega);
            }
        }

        // Calculate kappa (virtual bond angle at CA)
        if i >= 2 && i + 2 < n && no_chain_break_range(&structure.residues, i - 2, i + 2) {
            let kappa = calculate_kappa(
                &structure.residues[i - 2].backbone.ca,
                &structure.residues[i].backbone.ca,
                &structure.residues[i + 2].backbone.ca,
            );
            if kappa != INVALID_ANGLE {
                structure.residues[i].kappa = Some(kappa);
            }
        }

        // Calculate alpha (CA virtual torsion)
        if i >= 1 && i + 2 < n && no_chain_break_range(&structure.residues, i - 1, i + 2) {
            let alpha = calculate_alpha(
                &structure.residues[i - 1].backbone.ca,
                &structure.residues[i].backbone.ca,
                &structure.residues[i + 1].backbone.ca,
                &structure.residues[i + 2].backbone.ca,
            );
            if alpha != INVALID_ANGLE {
                structure.residues[i].alpha = Some(alpha);
            }
        }

        // Calculate TCO (CO bond angle)
        if i > 0 && structure.residues[i].chain_break == ChainBreak::None {
            structure.residues[i].tco = Some(calculate_tco(
                &structure.residues[i].backbone.c,
                &structure.residues[i].backbone.o,
                &structure.residues[i - 1].backbone.c,
                &structure.residues[i - 1].backbone.o,
            ));
        }
    }

    // Initialize H-bond arrays
    for residue in &mut structure.residues {
        residue.hbond_acceptor = [HBond::none(), HBond::none()];
        residue.hbond_donor = [HBond::none(), HBond::none()];
    }

    // Identify chains
    structure.identify_chains();
}

/// Calculate statistics from processed structure
fn calculate_statistics(structure: &Structure, stats: &mut Statistics) {
    stats.residue_count = structure.residues.len() as u32;
    stats.chain_count = structure.chains.len() as u32;

    // Count H-bonds and track distances
    for residue in &structure.residues {
        for hbond in &residue.hbond_acceptor {
            if hbond.is_bond() {
                stats.hbond_count += 1;

                if let Some(partner_idx) = hbond.partner_idx {
                    let k = partner_idx as i32 - residue.internal_nr as i32;
                    if k >= -5 && k <= 5 {
                        stats.hbonds_per_distance[(k + 5) as usize] += 1;
                    }
                }
            }
        }
    }

    // Count SS bridges
    stats.ss_bridge_count = structure.ss_bonds.len() as u32;
    for &(i, j) in &structure.ss_bonds {
        if structure.residues[i].chain_id == structure.residues[j].chain_id {
            stats.intra_chain_ss_bridges += 1;
        }
    }

    // Count alpha helix lengths
    count_helix_lengths(structure, stats);
}

/// Count alpha helix lengths for histogram
fn count_helix_lengths(structure: &Structure, stats: &mut Statistics) {
    use crate::types::SecondaryStructure;

    let mut helix_len = 0u32;
    let mut prev_chain = String::new();

    for residue in &structure.residues {
        if residue.chain_id != prev_chain {
            if helix_len > 0 {
                let idx = (helix_len as usize).min(30) - 1;
                stats.residues_per_alpha_helix[idx] += 1;
            }
            helix_len = 0;
            prev_chain = residue.chain_id.clone();
        }

        if residue.structure == SecondaryStructure::AlphaHelix {
            helix_len += 1;
        } else if helix_len > 0 {
            let idx = (helix_len as usize).min(30) - 1;
            stats.residues_per_alpha_helix[idx] += 1;
            helix_len = 0;
        }
    }

    // Handle last helix
    if helix_len > 0 {
        let idx = (helix_len as usize).min(30) - 1;
        stats.residues_per_alpha_helix[idx] += 1;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::geometry::Point3;
    use crate::types::{BackboneAtoms, Residue};

    fn make_test_structure(n_residues: usize) -> Structure {
        let residues: Vec<Residue> = (0..n_residues)
            .map(|i| {
                let x = i as f32 * 3.8; // Approximate CA-CA distance
                Residue::new(
                    "A".to_string(),
                    (i + 1) as i32,
                    "ALA".to_string(),
                    BackboneAtoms::new(
                        Point3::new(x, 0.0, 0.0),
                        Point3::new(x + 1.5, 0.5, 0.0),
                        Point3::new(x + 2.5, 0.0, 0.0),
                        Point3::new(x + 3.3, 0.5, 0.0),
                    ),
                )
            })
            .collect();

        Structure::from_residues(residues)
    }

    #[test]
    fn test_preprocess() {
        let mut structure = make_test_structure(5);
        preprocess_structure(&mut structure);

        // Should have internal indices assigned
        for (i, residue) in structure.residues.iter().enumerate() {
            assert_eq!(residue.internal_nr, i);
        }

        // Should have hydrogen positions calculated (except first)
        assert!(structure.residues[0].backbone.h.is_none());
        for i in 1..5 {
            assert!(structure.residues[i].backbone.h.is_some());
        }
    }

    #[test]
    fn test_calculate_dssp() {
        let mut structure = make_test_structure(10);
        let config = DsspConfig::default();

        let stats = calculate_dssp(&mut structure, &config);

        assert_eq!(stats.residue_count, 10);
        assert!(stats.chain_count >= 1);
    }

    #[test]
    fn test_empty_structure() {
        let mut structure = Structure::new("test".to_string());
        let config = DsspConfig::default();

        let stats = calculate_dssp(&mut structure, &config);

        assert_eq!(stats.residue_count, 0);
    }
}
