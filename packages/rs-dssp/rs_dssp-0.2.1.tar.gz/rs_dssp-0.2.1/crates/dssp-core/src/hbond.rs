//! Hydrogen bond calculation
//!
//! Implements the Kabsch-Sander hydrogen bond energy formula:
//! E = k * (1/r_ON + 1/r_CH - 1/r_OH - 1/r_CN)
//!
//! where k = -27.888 kcal/mol*Å

use crate::constants::*;
use crate::geometry::Point3;
use crate::types::{AminoAcid, HBond, Residue};

/// Calculate hydrogen atom position from backbone geometry
///
/// The amide hydrogen is placed along the bisector of the N-C(prev) and N-CA vectors,
/// at a distance of ~1.01 Å from the nitrogen.
///
/// # Arguments
/// * `n` - Nitrogen position of current residue
/// * `ca` - CA position of current residue
/// * `prev_c` - Carbonyl carbon of previous residue
///
/// # Returns
/// Calculated hydrogen position
pub fn calculate_hydrogen_position(n: &Point3, ca: &Point3, prev_c: &Point3) -> Point3 {
    // Vector from C(i-1) to N(i)
    let vec_cn = *n - *prev_c;
    let cn_len = vec_cn.length();

    // Vector from CA(i) to N(i)
    let vec_can = *n - *ca;
    let can_len = vec_can.length();

    if cn_len > 1e-6 && can_len > 1e-6 {
        // Normalize both vectors
        let cn_norm = vec_cn * (1.0 / cn_len);
        let can_norm = vec_can * (1.0 / can_len);

        // Sum of unit vectors gives bisector direction
        let vec_nh = cn_norm + can_norm;
        let nh_len = vec_nh.length();

        if nh_len > 1e-6 {
            // Place H at ~1.01 Å from N along the bisector
            let nh_norm = vec_nh * (NH_BOND_LENGTH / nh_len);
            return *n + nh_norm;
        }
    }

    // Fallback: place H at N if geometry is degenerate
    *n
}

/// Calculate hydrogen bond energy using Kabsch-Sander formula
///
/// E = k * (1/r_ON + 1/r_CH - 1/r_OH - 1/r_CN)
///
/// where:
/// - k = -27.888 kcal/mol*Å (COUPLING_CONSTANT)
/// - r_ON = O...N distance
/// - r_CH = C...H distance
/// - r_OH = O...H distance
/// - r_CN = C...N distance
///
/// # Arguments
/// * `donor` - Donor residue (N-H group)
/// * `acceptor` - Acceptor residue (C=O group)
///
/// # Returns
/// Energy in kcal/mol. Negative values indicate favorable bonds.
/// Returns 0.0 if calculation is invalid (e.g., Proline donor).
pub fn calculate_hbond_energy(donor: &Residue, acceptor: &Residue) -> f64 {
    // Proline cannot be a donor (no amide hydrogen)
    if donor.amino_acid == AminoAcid::Pro {
        return NO_BOND_ENERGY;
    }

    // Get hydrogen position (calculated or explicit)
    let h = donor.backbone.h.unwrap_or(donor.backbone.n);
    let n = &donor.backbone.n;
    let c = &acceptor.backbone.c;
    let o = &acceptor.backbone.o;

    // Calculate all four distances
    let d_ho = h.distance(o) as f64;
    let d_hc = h.distance(c) as f64;
    let d_nc = n.distance(c) as f64;
    let d_no = n.distance(o) as f64;

    // Check for minimum distances to avoid numerical issues
    let min_dist = MIN_DISTANCE as f64;
    if d_ho < min_dist || d_hc < min_dist || d_nc < min_dist || d_no < min_dist {
        return MIN_HBOND_ENERGY;
    }

    // Kabsch-Sander formula
    // Note: The formula in the original paper uses 1/r_ON - 1/r_CH + 1/r_CN - 1/r_OH
    // But we follow the dssp implementation which computes it as:
    // E = k * (1/r_ON + 1/r_CH - 1/r_OH - 1/r_CN)
    let energy = COUPLING_CONSTANT * (1.0 / d_no + 1.0 / d_hc - 1.0 / d_ho - 1.0 / d_nc);

    // Round to 3 decimal places for DSSP compatibility
    let energy = (energy * 1000.0).round() / 1000.0;

    // Clamp to minimum energy
    energy.max(MIN_HBOND_ENERGY)
}

/// Test if there is a hydrogen bond from residue a (donor) to residue b (acceptor)
///
/// # Arguments
/// * `donor` - Donor residue
/// * `acceptor_idx` - Index of acceptor residue
///
/// # Returns
/// true if a valid H-bond exists
#[inline]
pub fn test_bond(donor: &Residue, acceptor_idx: usize) -> bool {
    (donor.hbond_acceptor[0].partner_idx == Some(acceptor_idx)
        && donor.hbond_acceptor[0].energy < MAX_HBOND_ENERGY)
        || (donor.hbond_acceptor[1].partner_idx == Some(acceptor_idx)
            && donor.hbond_acceptor[1].energy < MAX_HBOND_ENERGY)
}

/// Test if acceptor receives an H-bond from donor at given index
#[inline]
pub fn test_accept(acceptor: &Residue, donor_idx: usize) -> bool {
    (acceptor.hbond_donor[0].partner_idx == Some(donor_idx)
        && acceptor.hbond_donor[0].energy < MAX_HBOND_ENERGY)
        || (acceptor.hbond_donor[1].partner_idx == Some(donor_idx)
            && acceptor.hbond_donor[1].energy < MAX_HBOND_ENERGY)
}

/// Update hydrogen bond arrays for a donor-acceptor pair
///
/// Maintains the two best (lowest energy) H-bonds for each role.
fn update_hbond(
    donor: &mut Residue,
    acceptor: &mut Residue,
    donor_idx: usize,
    acceptor_idx: usize,
    energy: f64,
) {
    // Update donor's acceptor list (bonds where this residue donates N-H)
    if energy < donor.hbond_acceptor[0].energy {
        donor.hbond_acceptor[1] = donor.hbond_acceptor[0];
        donor.hbond_acceptor[0] = HBond::new(acceptor_idx, energy);
    } else if energy < donor.hbond_acceptor[1].energy {
        donor.hbond_acceptor[1] = HBond::new(acceptor_idx, energy);
    }

    // Update acceptor's donor list (bonds where this residue accepts via C=O)
    if energy < acceptor.hbond_donor[0].energy {
        acceptor.hbond_donor[1] = acceptor.hbond_donor[0];
        acceptor.hbond_donor[0] = HBond::new(donor_idx, energy);
    } else if energy < acceptor.hbond_donor[1].energy {
        acceptor.hbond_donor[1] = HBond::new(donor_idx, energy);
    }
}

/// Calculate all hydrogen bond energies for a list of residue pairs
///
/// # Arguments
/// * `residues` - Mutable slice of residues
/// * `pairs` - List of (i, j) index pairs to check
pub fn calculate_all_hbonds(residues: &mut [Residue], pairs: &[(usize, usize)]) {
    // We need to calculate energies first, then update
    // because we can't have mutable borrows of multiple residues at once
    let mut bonds: Vec<(usize, usize, f64)> = Vec::with_capacity(pairs.len() * 2);

    // Calculate all energies
    for &(i, j) in pairs {
        // Skip if same residue or adjacent (no i,i or i,i+1 bonds)
        if j <= i + 1 {
            continue;
        }

        // i as donor, j as acceptor
        let energy_ij = calculate_hbond_energy(&residues[i], &residues[j]);
        if energy_ij < NO_BOND_ENERGY - 0.01 {
            bonds.push((i, j, energy_ij));
        }

        // j as donor, i as acceptor (skip if j = i + 2 for the reverse)
        if j > i + 2 {
            let energy_ji = calculate_hbond_energy(&residues[j], &residues[i]);
            if energy_ji < NO_BOND_ENERGY - 0.01 {
                bonds.push((j, i, energy_ji));
            }
        }
    }

    // Sort by energy to process strongest bonds first
    bonds.sort_by(|a, b| a.2.partial_cmp(&b.2).unwrap_or(std::cmp::Ordering::Equal));

    // Update residues with calculated bonds
    for (donor_idx, acceptor_idx, energy) in bonds {
        // Split the slice to get mutable references to both residues
        if donor_idx < acceptor_idx {
            let (left, right) = residues.split_at_mut(acceptor_idx);
            update_hbond(
                &mut left[donor_idx],
                &mut right[0],
                donor_idx,
                acceptor_idx,
                energy,
            );
        } else {
            let (left, right) = residues.split_at_mut(donor_idx);
            update_hbond(
                &mut right[0],
                &mut left[acceptor_idx],
                donor_idx,
                acceptor_idx,
                energy,
            );
        }
    }
}

/// Find all residue pairs within CA distance threshold for H-bond calculation
///
/// # Arguments
/// * `residues` - Slice of residues
///
/// # Returns
/// Vector of (i, j) index pairs where i < j and CA distance < threshold
pub fn find_nearby_pairs(residues: &[Residue]) -> Vec<(usize, usize)> {
    let n = residues.len();
    let mut pairs = Vec::new();

    for i in 0..n.saturating_sub(1) {
        let ca_i = &residues[i].backbone.ca;

        for j in (i + 1)..n {
            let ca_j = &residues[j].backbone.ca;

            if ca_i.distance_sq(ca_j) <= MIN_CA_DISTANCE_SQ {
                pairs.push((i, j));
            }
        }
    }

    pairs
}

/// Find nearby pairs using parallel computation (for large structures)
#[cfg(feature = "parallel")]
pub fn find_nearby_pairs_parallel(residues: &[Residue]) -> Vec<(usize, usize)> {
    use rayon::prelude::*;

    let n = residues.len();

    (0..n)
        .into_par_iter()
        .flat_map(|i| {
            let ca_i = &residues[i].backbone.ca;
            ((i + 1)..n)
                .filter_map(|j| {
                    let ca_j = &residues[j].backbone.ca;
                    if ca_i.distance_sq(ca_j) <= MIN_CA_DISTANCE_SQ {
                        Some((i, j))
                    } else {
                        None
                    }
                })
                .collect::<Vec<_>>()
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::types::BackboneAtoms;

    fn make_test_residue(n: Point3, ca: Point3, c: Point3, o: Point3, aa: AminoAcid) -> Residue {
        let mut r = Residue::new(
            "A".to_string(),
            1,
            aa.to_three_letter().to_string(),
            BackboneAtoms::new(n, ca, c, o),
        );
        r.amino_acid = aa;
        r
    }

    #[test]
    fn test_hydrogen_position() {
        // Simple geometry: N at origin, CA at (1, 1, 0), prev_C at (1, -1, 0)
        // This should place H in the negative x direction (bisecting the two vectors from N)
        let n = Point3::new(0.0, 0.0, 0.0);
        let ca = Point3::new(1.0, 1.0, 0.0);
        let prev_c = Point3::new(1.0, -1.0, 0.0);

        let h = calculate_hydrogen_position(&n, &ca, &prev_c);

        // H should be approximately in the negative x direction from N
        // (bisector of N-CA and N-prev_C vectors points away from the CA-C side)
        assert!(h.x < 0.0, "H should be in negative x direction: h.x = {}", h.x);
        assert!(h.y.abs() < 0.1, "H should be near y=0: h.y = {}", h.y);
        assert!(h.z.abs() < 0.1, "H should be near z=0: h.z = {}", h.z);

        // Check distance is approximately 1.0 Å
        let dist = n.distance(&h);
        assert!((dist - 1.0).abs() < 0.1, "H-N distance should be ~1.0 Å: dist = {}", dist);
    }

    #[test]
    fn test_proline_no_donor() {
        let donor = make_test_residue(
            Point3::new(0.0, 0.0, 0.0),
            Point3::new(1.5, 0.0, 0.0),
            Point3::new(2.5, 0.0, 0.0),
            Point3::new(3.5, 0.0, 0.0),
            AminoAcid::Pro,
        );

        let acceptor = make_test_residue(
            Point3::new(10.0, 0.0, 0.0),
            Point3::new(11.5, 0.0, 0.0),
            Point3::new(12.5, 0.0, 0.0),
            Point3::new(13.5, 0.0, 0.0),
            AminoAcid::Ala,
        );

        let energy = calculate_hbond_energy(&donor, &acceptor);
        assert_eq!(energy, NO_BOND_ENERGY);
    }

    #[test]
    fn test_hbond_energy_sign() {
        // Create a favorable H-bond geometry where H is close to O
        // For a good H-bond, d_ho should be small (~1.8-2.0 Å)
        let mut donor = make_test_residue(
            Point3::new(0.0, 0.0, 0.0),   // N at origin
            Point3::new(1.5, 0.5, 0.0),   // CA
            Point3::new(2.5, 0.0, 0.0),   // C
            Point3::new(3.5, 0.5, 0.0),   // O
            AminoAcid::Ala,
        );
        // Set explicit H position pointing toward acceptor O
        donor.backbone.h = Some(Point3::new(-1.0, 0.0, 0.0));

        // Acceptor with O close to donor H
        let acceptor = make_test_residue(
            Point3::new(-6.0, 0.0, 0.0),  // N (far away)
            Point3::new(-5.0, 0.0, 0.0),  // CA
            Point3::new(-4.0, 0.0, 0.0),  // C
            Point3::new(-2.9, 0.0, 0.0),  // O at -2.9 (close to H at -1), d_ho = 1.9 Å
            AminoAcid::Ala,
        );

        let energy = calculate_hbond_energy(&donor, &acceptor);
        // Energy should be negative for a favorable bond
        // For this geometry:
        // d_ho = 1.9 Å, d_no = 2.9 Å, d_hc = 3.0 Å, d_nc = 4.0 Å
        // E = 27.888 * (1/2.9 + 1/3.0 - 1/1.9 - 1/4.0)
        //   = 27.888 * (0.345 + 0.333 - 0.526 - 0.25)
        //   = 27.888 * (-0.098)
        //   = -2.73 kcal/mol
        assert!(energy < 0.0, "Energy should be negative: {}", energy);
        assert!(energy < MAX_HBOND_ENERGY, "Energy should be below -0.5: {}", energy);
    }
}
