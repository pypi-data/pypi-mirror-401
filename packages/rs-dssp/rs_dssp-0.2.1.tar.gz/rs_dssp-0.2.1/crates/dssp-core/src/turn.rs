//! Turn and bend detection
//!
//! - Turn (T): Residues adjacent to helix starts but not in the helix
//! - Bend (S): High curvature region (kappa > 70°)

use crate::types::{HelixPosition, HelixType, Residue, SecondaryStructure};

/// Detect turns and bends, assign final structure
///
/// This should be called after helix and strand detection.
///
/// # Arguments
/// * `residues` - Mutable slice of residues to process
pub fn detect_turns_and_bends(residues: &mut [Residue]) {
    let n = residues.len();

    for i in 1..n.saturating_sub(1) {
        // Only process Loop residues
        if residues[i].structure != SecondaryStructure::Loop {
            continue;
        }

        // Check if this residue is in a turn
        let is_turn = is_in_turn(&residues, i);

        if is_turn {
            residues[i].structure = SecondaryStructure::Turn;
        } else if residues[i].is_bend {
            residues[i].structure = SecondaryStructure::Bend;
        }
    }
}

/// Check if residue at index i is in a turn
///
/// A turn is defined as residues that are within stride distance of a helix start,
/// but not assigned as part of the helix itself.
fn is_in_turn(residues: &[Residue], i: usize) -> bool {
    for helix_type in HelixType::hbond_types() {
        let stride = helix_type.stride();
        let helix_idx = helix_type as usize;

        // Check if any residue within stride distance before i is a helix start
        for k in 1..stride {
            if i >= k {
                let flag = residues[i - k].helix_flags[helix_idx];
                if matches!(flag, HelixPosition::Start | HelixPosition::StartAndEnd) {
                    // Check if residue i-k+stride would put us at or beyond i
                    // This means residue i is in the "turn" region
                    if i - k + stride > i {
                        return true;
                    }
                }
            }
        }
    }

    false
}

/// Alternative turn detection: check for hydrogen-bonded turns
///
/// A hydrogen-bonded turn of type n exists if there's an H-bond
/// from residue i to residue i+n where n = 3, 4, or 5.
///
/// This is used to mark 'T' for residues i+1 through i+n-1.
pub fn detect_hbonded_turns(residues: &mut [Residue]) {
    let n = residues.len();

    // For each helix type, mark turns
    for helix_type in HelixType::hbond_types() {
        let stride = helix_type.stride();
        let helix_idx = helix_type as usize;

        for i in 0..n.saturating_sub(stride) {
            // Check if residue i is a helix start for this type
            let flag = residues[i].helix_flags[helix_idx];
            if !flag.is_start() {
                continue;
            }

            // Mark intermediate residues as turns (if they're still Loop)
            for j in (i + 1)..(i + stride) {
                if j < n && residues[j].structure == SecondaryStructure::Loop {
                    // Only mark as turn if not already part of a helix
                    let is_helix = residues[j].helix_flags.iter().any(|f| {
                        matches!(f, HelixPosition::Middle | HelixPosition::Start | HelixPosition::End | HelixPosition::StartAndEnd)
                    });

                    if !is_helix {
                        residues[j].structure = SecondaryStructure::Turn;
                    }
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::geometry::Point3;
    use crate::types::BackboneAtoms;

    fn make_residue() -> Residue {
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
        )
    }

    #[test]
    fn test_bend_detection() {
        let mut residues = vec![make_residue(), make_residue(), make_residue()];
        residues[1].is_bend = true;

        for (i, r) in residues.iter_mut().enumerate() {
            r.internal_nr = i;
        }

        detect_turns_and_bends(&mut residues);

        assert_eq!(residues[1].structure, SecondaryStructure::Bend);
    }

    #[test]
    fn test_turn_not_overwrite_helix() {
        let mut residues = vec![make_residue(); 5];

        for (i, r) in residues.iter_mut().enumerate() {
            r.internal_nr = i;
        }

        // Mark residue 2 as alpha helix
        residues[2].structure = SecondaryStructure::AlphaHelix;

        detect_turns_and_bends(&mut residues);

        // Should not overwrite helix assignment
        assert_eq!(residues[2].structure, SecondaryStructure::AlphaHelix);
    }
}
