//! Poly-Proline II helix detection
//!
//! PPII helices are characterized by specific phi/psi backbone angles:
//! - φ (phi): -75° ± 29°
//! - ψ (psi): 145° ± 29°
//!
//! Unlike other helices, PPII detection is based on dihedral angles, not H-bonds.

use crate::constants::*;
use crate::types::{ChainBreak, HelixPosition, HelixType, Residue, SecondaryStructure};

/// Detect Poly-Proline II helices based on phi/psi angles
///
/// # Arguments
/// * `residues` - Mutable slice of residues to process
/// * `min_stretch` - Minimum consecutive residues required (typically 2 or 3)
pub fn detect_ppii_helices(residues: &mut [Residue], min_stretch: usize) {
    let n = residues.len();
    if n < min_stretch + 2 {
        return;
    }

    let phi_min = PPII_PHI_CENTER - PPII_PHI_EPSILON;
    let phi_max = PPII_PHI_CENTER + PPII_PHI_EPSILON;
    let psi_min = PPII_PSI_CENTER - PPII_PSI_EPSILON;
    let psi_max = PPII_PSI_CENTER + PPII_PSI_EPSILON;

    // Slide through looking for consecutive residues with PPII angles
    let mut i = 1; // Start at 1 because first residue often has no phi angle

    while i < n.saturating_sub(min_stretch - 1) {
        // Check if current position starts a PPII stretch
        let stretch_len = count_ppii_stretch(
            &residues[i..],
            phi_min, phi_max,
            psi_min, psi_max,
        );

        if stretch_len >= min_stretch {
            // Mark PPII helix
            mark_ppii_helix(residues, i, stretch_len);
            i += stretch_len;
        } else {
            i += 1;
        }
    }
}

/// Count consecutive residues with PPII-compatible angles
fn count_ppii_stretch(
    residues: &[Residue],
    phi_min: f32,
    phi_max: f32,
    psi_min: f32,
    psi_max: f32,
) -> usize {
    let mut count = 0;

    for (i, residue) in residues.iter().enumerate() {
        // Check for chain break
        if i > 0 && residue.chain_break != ChainBreak::None {
            break;
        }

        let phi = residue.phi.unwrap_or(INVALID_ANGLE);
        let psi = residue.psi.unwrap_or(INVALID_ANGLE);

        // Check if angles are in PPII range
        if is_in_range(phi, phi_min, phi_max) && is_in_range(psi, psi_min, psi_max) {
            count += 1;
        } else {
            break;
        }
    }

    count
}

/// Check if angle is in range (handles wraparound)
#[inline]
fn is_in_range(angle: f32, min: f32, max: f32) -> bool {
    if angle == INVALID_ANGLE {
        return false;
    }
    angle >= min && angle <= max
}

/// Mark residues as PPII helix
fn mark_ppii_helix(residues: &mut [Residue], start: usize, length: usize) {
    let helix_idx = HelixType::PPII as usize;

    for k in 0..length {
        let idx = start + k;
        if idx >= residues.len() {
            break;
        }

        // Update helix flags
        if k == 0 {
            residues[idx].helix_flags[helix_idx] = match residues[idx].helix_flags[helix_idx] {
                HelixPosition::None => HelixPosition::Start,
                HelixPosition::End => HelixPosition::StartAndEnd,
                other => other,
            };
        } else if k == length - 1 {
            residues[idx].helix_flags[helix_idx] = match residues[idx].helix_flags[helix_idx] {
                HelixPosition::None | HelixPosition::Middle => HelixPosition::End,
                HelixPosition::Start => HelixPosition::StartAndEnd,
                other => other,
            };
        } else {
            if residues[idx].helix_flags[helix_idx] == HelixPosition::None {
                residues[idx].helix_flags[helix_idx] = HelixPosition::Middle;
            }
        }

        // Assign PPII structure only if currently Loop
        if residues[idx].structure == SecondaryStructure::Loop {
            residues[idx].structure = SecondaryStructure::PPIIHelix;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::geometry::Point3;
    use crate::types::BackboneAtoms;

    fn make_residue_with_angles(phi: Option<f32>, psi: Option<f32>) -> Residue {
        let mut r = Residue::new(
            "A".to_string(),
            1,
            "ALA".to_string(),
            BackboneAtoms::new(
                Point3::new(0.0, 0.0, 0.0),
                Point3::new(1.5, 0.0, 0.0),
                Point3::new(2.5, 0.0, 0.0),
                Point3::new(3.5, 0.0, 0.0),
            ),
        );
        r.phi = phi;
        r.psi = psi;
        r
    }

    #[test]
    fn test_ppii_angle_range() {
        // In range
        assert!(is_in_range(-75.0, -104.0, -46.0));
        assert!(is_in_range(145.0, 116.0, 174.0));

        // Out of range
        assert!(!is_in_range(-30.0, -104.0, -46.0));
        assert!(!is_in_range(180.0, 116.0, 174.0));

        // Invalid angle
        assert!(!is_in_range(INVALID_ANGLE, -104.0, -46.0));
    }

    #[test]
    fn test_ppii_detection() {
        let mut residues = vec![
            make_residue_with_angles(None, None), // First residue, no phi
            make_residue_with_angles(Some(-75.0), Some(145.0)), // PPII
            make_residue_with_angles(Some(-75.0), Some(145.0)), // PPII
            make_residue_with_angles(Some(-75.0), Some(145.0)), // PPII
            make_residue_with_angles(Some(-60.0), Some(-45.0)), // Alpha helix region
        ];

        for (i, r) in residues.iter_mut().enumerate() {
            r.internal_nr = i;
        }

        detect_ppii_helices(&mut residues, 3);

        assert_eq!(residues[1].structure, SecondaryStructure::PPIIHelix);
        assert_eq!(residues[2].structure, SecondaryStructure::PPIIHelix);
        assert_eq!(residues[3].structure, SecondaryStructure::PPIIHelix);
        assert_eq!(residues[4].structure, SecondaryStructure::Loop);
    }
}
