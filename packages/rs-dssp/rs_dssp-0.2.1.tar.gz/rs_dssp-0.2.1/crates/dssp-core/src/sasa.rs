//! Solvent Accessible Surface Area (SASA) calculation
//!
//! Uses the Shrake-Rupley algorithm with Fibonacci sphere sampling
//! to estimate the accessible surface area of each residue.
//!
//! Optimized with k-d tree spatial indexing for O(n log n) neighbor queries.

use crate::constants::*;
use crate::geometry::Point3;
use crate::types::Residue;
use kiddo::{ImmutableKdTree, SquaredEuclidean};
use std::f32::consts::PI as PI_F32_CONST;

/// Atom representation for SASA calculation
#[derive(Debug, Clone, Copy)]
struct Atom {
    pos: Point3,
    radius: f32,
}

/// Generate Fibonacci sphere points for sampling
///
/// Uses the golden angle to distribute points approximately uniformly on a sphere.
fn generate_sphere_points(n: usize) -> Vec<Point3> {
    let golden_angle = PI_F32_CONST * (3.0 - 5.0_f32.sqrt());
    let mut points = Vec::with_capacity(n);

    for i in 0..n {
        let y = 1.0 - (i as f32 / (n - 1) as f32) * 2.0;
        let radius_at_y = (1.0 - y * y).sqrt();
        let theta = golden_angle * i as f32;

        points.push(Point3::new(
            radius_at_y * theta.cos(),
            y,
            radius_at_y * theta.sin(),
        ));
    }

    points
}

/// Calculate SASA for all residues in a structure
///
/// # Arguments
/// * `residues` - Mutable slice of residues
/// * `n_points` - Number of sampling points per atom (default: 100)
pub fn calculate_sasa(residues: &mut [Residue], n_points: usize) {
    // Generate sphere sampling points
    let sphere_points = generate_sphere_points(n_points);

    // Collect all atoms with their radii
    let atoms = collect_atoms(residues);
    let n_atoms = atoms.len();

    if n_atoms == 0 {
        return;
    }

    // Build k-d tree for spatial indexing
    let kdtree = build_kdtree(&atoms);

    // Calculate surface area for each atom
    let atom_sasa: Vec<f32> = atoms
        .iter()
        .enumerate()
        .map(|(i, atom)| {
            calculate_atom_sasa_kdtree(atom, i, &atoms, &sphere_points, &kdtree)
        })
        .collect();

    // Assign SASA to residues
    assign_sasa_to_residues(residues, &atom_sasa);
}

/// Collect all atoms from residues for SASA calculation
fn collect_atoms(residues: &[Residue]) -> Vec<Atom> {
    let mut atoms = Vec::new();

    for residue in residues {
        // Backbone atoms
        atoms.push(Atom {
            pos: residue.backbone.n,
            radius: RADIUS_N + RADIUS_WATER,
        });
        atoms.push(Atom {
            pos: residue.backbone.ca,
            radius: RADIUS_CA + RADIUS_WATER,
        });
        atoms.push(Atom {
            pos: residue.backbone.c,
            radius: RADIUS_C + RADIUS_WATER,
        });
        atoms.push(Atom {
            pos: residue.backbone.o,
            radius: RADIUS_O + RADIUS_WATER,
        });

        // Side chain atoms
        for (_, pos) in &residue.side_chain {
            atoms.push(Atom {
                pos: *pos,
                radius: RADIUS_SIDE_ATOM + RADIUS_WATER,
            });
        }
    }

    atoms
}

/// Build k-d tree from atoms for efficient spatial queries
fn build_kdtree(atoms: &[Atom]) -> ImmutableKdTree<f32, 3> {
    let entries: Vec<[f32; 3]> = atoms
        .iter()
        .map(|a| [a.pos.x, a.pos.y, a.pos.z])
        .collect();
    ImmutableKdTree::new_from_slice(&entries)
}

/// Maximum atom radius (CA + water probe) for k-d tree range queries
const MAX_ATOM_RADIUS: f32 = RADIUS_CA + RADIUS_WATER;

/// Calculate SASA for a single atom using k-d tree for neighbor lookup
fn calculate_atom_sasa_kdtree(
    atom: &Atom,
    atom_idx: usize,
    all_atoms: &[Atom],
    sphere_points: &[Point3],
    kdtree: &ImmutableKdTree<f32, 3>,
) -> f32 {
    let radius_sq = atom.radius * atom.radius;
    let surface_area = FOUR_PI as f32 * radius_sq;

    // Query radius: atom radius + max possible neighbor radius
    let query_radius = atom.radius + MAX_ATOM_RADIUS;
    let query_radius_sq = query_radius * query_radius;

    // Find nearby atoms using k-d tree (O(log n) instead of O(n))
    let query_point = [atom.pos.x, atom.pos.y, atom.pos.z];
    let neighbors = kdtree.within::<SquaredEuclidean>(&query_point, query_radius_sq);

    // Filter to actual nearby atoms
    let nearby: Vec<(usize, f32)> = neighbors
        .iter()
        .filter_map(|n| {
            let idx = n.item as usize;
            if idx == atom_idx {
                return None;
            }
            let other = &all_atoms[idx];
            let max_dist = atom.radius + other.radius;
            if atom.pos.distance_sq(&other.pos) < max_dist * max_dist {
                Some((idx, other.radius))
            } else {
                None
            }
        })
        .collect();

    if nearby.is_empty() {
        return surface_area;
    }

    // Count exposed points
    let mut exposed = 0;

    for point in sphere_points {
        let surface_point = Point3::new(
            atom.pos.x + point.x * atom.radius,
            atom.pos.y + point.y * atom.radius,
            atom.pos.z + point.z * atom.radius,
        );

        let occluded = nearby.iter().any(|(i, neighbor_radius)| {
            let neighbor = &all_atoms[*i];
            surface_point.distance_sq(&neighbor.pos) < neighbor_radius * neighbor_radius
        });

        if !occluded {
            exposed += 1;
        }
    }

    let fraction_exposed = exposed as f32 / sphere_points.len() as f32;
    surface_area * fraction_exposed
}

/// Assign calculated SASA values to residues
fn assign_sasa_to_residues(residues: &mut [Residue], atom_sasa: &[f32]) {
    let mut atom_idx = 0;

    for residue in residues {
        let mut total_sasa = 0.0;

        // Backbone atoms (4 per residue)
        for _ in 0..4 {
            if atom_idx < atom_sasa.len() {
                total_sasa += atom_sasa[atom_idx];
                atom_idx += 1;
            }
        }

        // Side chain atoms
        for _ in 0..residue.side_chain.len() {
            if atom_idx < atom_sasa.len() {
                total_sasa += atom_sasa[atom_idx];
                atom_idx += 1;
            }
        }

        residue.accessibility = total_sasa;
    }
}

/// Calculate total SASA for a structure
pub fn calculate_total_sasa(residues: &[Residue]) -> f64 {
    residues.iter().map(|r| r.accessibility as f64).sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::types::BackboneAtoms;

    #[test]
    fn test_sphere_points() {
        let points = generate_sphere_points(100);
        assert_eq!(points.len(), 100);

        // Check that points are approximately on unit sphere
        for point in &points {
            let len = point.length();
            assert!((len - 1.0).abs() < 0.01);
        }
    }

    #[test]
    fn test_single_atom_sasa() {
        // For an isolated atom, SASA should be approximately 4*pi*r^2
        let atom = Atom {
            pos: Point3::new(0.0, 0.0, 0.0),
            radius: 1.87 + 1.4, // CA + water
        };

        let atoms = vec![atom];
        let sphere_points = generate_sphere_points(100);
        let kdtree = build_kdtree(&atoms);
        let sasa = calculate_atom_sasa_kdtree(&atom, 0, &atoms, &sphere_points, &kdtree);

        let expected = FOUR_PI as f32 * atom.radius * atom.radius;
        assert!((sasa - expected).abs() / expected < 0.1); // Within 10%
    }

    #[test]
    fn test_sasa_calculation() {
        let mut residues = vec![
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
            ),
        ];

        calculate_sasa(&mut residues, 50);

        // Should have non-zero accessibility
        assert!(residues[0].accessibility > 0.0);
    }
}
