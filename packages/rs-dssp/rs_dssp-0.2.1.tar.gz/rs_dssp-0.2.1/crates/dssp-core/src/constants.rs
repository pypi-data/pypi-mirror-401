//! DSSP algorithm constants
//!
//! Constants derived from Kabsch & Sander (1983) Biopolymers 22:2577-2637

use std::f64::consts::PI;

// ============================================================================
// Hydrogen Bond Constants
// ============================================================================

/// Kabsch-Sander coupling constant: 332 * 0.42 * 0.2 = 27.888 kcal/mol*Å
/// This comes from electrostatic interaction: q1*q2/ε where
/// q1 = 0.42e (partial charge on N-H)
/// q2 = 0.20e (partial charge on C=O)
/// 332 = conversion factor to kcal/mol*Å
///
/// Note: This is POSITIVE because the formula subtracts the 1/rOH term,
/// which is the largest for favorable H-bonds, making the sum negative.
/// So E = COUPLING_CONSTANT * (negative sum) gives negative energy for good bonds.
pub const COUPLING_CONSTANT: f64 = 27.888;

/// Maximum hydrogen bond energy threshold for considering a bond (kcal/mol)
/// Bonds with E < -0.5 kcal/mol are considered hydrogen bonds
pub const MAX_HBOND_ENERGY: f64 = -0.5;

/// Minimum hydrogen bond energy (floor value) to avoid numerical issues (kcal/mol)
pub const MIN_HBOND_ENERGY: f64 = -9.9;

/// Default energy for no bond or invalid calculation
pub const NO_BOND_ENERGY: f64 = 0.0;

// ============================================================================
// Distance Constants
// ============================================================================

/// Minimum distance to avoid division by zero in energy calculation (Å)
pub const MIN_DISTANCE: f32 = 0.5;

/// Minimum C-alpha distance squared for considering H-bond pairs (Å²)
/// Only residue pairs with CA-CA distance < 9.0Å are considered
pub const MIN_CA_DISTANCE: f32 = 9.0;
pub const MIN_CA_DISTANCE_SQ: f32 = MIN_CA_DISTANCE * MIN_CA_DISTANCE;

/// Maximum peptide bond length for chain continuity (Å)
/// If C-N distance > 2.5Å, there's a chain break
pub const MAX_PEPTIDE_BOND_LENGTH: f32 = 2.5;

/// Standard N-H bond length (Å)
pub const NH_BOND_LENGTH: f32 = 1.0;

// ============================================================================
// Angle Constants
// ============================================================================

/// Bend threshold angle (degrees)
/// κ > 70° indicates a bend in the backbone
pub const BEND_THRESHOLD: f32 = 70.0;

/// Pi constant for angle calculations
pub const PI_F32: f32 = std::f32::consts::PI;
pub const PI_F64: f64 = PI;

/// Degrees to radians conversion
pub const DEG_TO_RAD: f32 = PI_F32 / 180.0;
pub const RAD_TO_DEG: f32 = 180.0 / PI_F32;

// ============================================================================
// PPII Helix Constants
// ============================================================================

/// Poly-Proline II helix phi angle center (degrees)
pub const PPII_PHI_CENTER: f32 = -75.0;

/// Poly-Proline II helix phi angle tolerance (degrees)
pub const PPII_PHI_EPSILON: f32 = 29.0;

/// Poly-Proline II helix psi angle center (degrees)
pub const PPII_PSI_CENTER: f32 = 145.0;

/// Poly-Proline II helix psi angle tolerance (degrees)
pub const PPII_PSI_EPSILON: f32 = 29.0;

/// Minimum PPII helix stretch length
pub const MIN_PPII_STRETCH: usize = 3;

// ============================================================================
// Van der Waals Radii for SASA Calculation (Å)
// ============================================================================

/// Radius of nitrogen atom
pub const RADIUS_N: f32 = 1.65;

/// Radius of C-alpha atom
pub const RADIUS_CA: f32 = 1.87;

/// Radius of carbonyl carbon atom
pub const RADIUS_C: f32 = 1.76;

/// Radius of carbonyl oxygen atom
pub const RADIUS_O: f32 = 1.4;

/// Default radius for side chain atoms
pub const RADIUS_SIDE_ATOM: f32 = 1.8;

/// Radius of water molecule (probe radius)
pub const RADIUS_WATER: f32 = 1.4;

// ============================================================================
// Helix Strides
// ============================================================================

/// Stride for 3-10 helix (i+3 -> i hydrogen bond)
pub const HELIX_310_STRIDE: usize = 3;

/// Stride for alpha helix (i+4 -> i hydrogen bond)
pub const HELIX_ALPHA_STRIDE: usize = 4;

/// Stride for pi helix (i+5 -> i hydrogen bond)
pub const HELIX_PI_STRIDE: usize = 5;

// ============================================================================
// Beta Sheet Constants
// ============================================================================

/// Maximum gap in bulge extension for parallel bridges
pub const MAX_BULGE_GAP_PARALLEL: usize = 6;

/// Maximum gap in bulge extension (smaller side)
pub const MAX_BULGE_GAP_SMALL: usize = 3;

// ============================================================================
// SASA Calculation Constants
// ============================================================================

/// Number of points for Fibonacci sphere sampling
pub const SASA_NUM_POINTS: usize = 100;

/// 4π for surface area calculation
pub const FOUR_PI: f64 = 4.0 * PI;

// ============================================================================
// Output Format Constants
// ============================================================================

/// Invalid angle marker (360.0 indicates angle could not be calculated)
pub const INVALID_ANGLE: f32 = 360.0;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_coupling_constant() {
        // Verify the coupling constant calculation
        let expected = 332.0 * 0.42 * 0.20;
        assert!((COUPLING_CONSTANT - expected).abs() < 0.001);
    }

    #[test]
    fn test_ca_distance_sq() {
        assert!((MIN_CA_DISTANCE_SQ - 81.0).abs() < 0.001);
    }
}
