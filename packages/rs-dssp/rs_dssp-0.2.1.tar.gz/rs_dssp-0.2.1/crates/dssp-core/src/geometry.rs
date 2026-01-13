//! 3D geometry operations for DSSP calculations
//!
//! Provides Point3 type and geometric functions including:
//! - Vector operations (dot, cross, normalize)
//! - Distance calculations
//! - Dihedral angle calculations (phi, psi, omega)
//! - Virtual bond angle (kappa)

use crate::constants::{INVALID_ANGLE, PI_F32, RAD_TO_DEG};
use serde::{Deserialize, Serialize};
use std::ops::{Add, Mul, Sub};

/// 3D point/vector with SIMD-friendly memory layout
#[derive(Debug, Clone, Copy, Default, PartialEq, Serialize, Deserialize)]
#[repr(C, align(16))]
pub struct Point3 {
    pub x: f32,
    pub y: f32,
    pub z: f32,
    #[serde(skip)]
    _pad: f32,
}

impl Point3 {
    /// Create a new Point3
    #[inline]
    pub const fn new(x: f32, y: f32, z: f32) -> Self {
        Self { x, y, z, _pad: 0.0 }
    }

    /// Create a zero vector
    #[inline]
    pub const fn zero() -> Self {
        Self::new(0.0, 0.0, 0.0)
    }

    /// Create from array
    #[inline]
    pub const fn from_array(arr: [f32; 3]) -> Self {
        Self::new(arr[0], arr[1], arr[2])
    }

    /// Convert to array
    #[inline]
    pub const fn to_array(self) -> [f32; 3] {
        [self.x, self.y, self.z]
    }

    /// Calculate squared distance to another point
    #[inline]
    pub fn distance_sq(&self, other: &Point3) -> f32 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        let dz = self.z - other.z;
        dx * dx + dy * dy + dz * dz
    }

    /// Calculate distance to another point
    #[inline]
    pub fn distance(&self, other: &Point3) -> f32 {
        self.distance_sq(other).sqrt()
    }

    /// Calculate squared length of vector
    #[inline]
    pub fn length_sq(&self) -> f32 {
        self.x * self.x + self.y * self.y + self.z * self.z
    }

    /// Calculate length of vector
    #[inline]
    pub fn length(&self) -> f32 {
        self.length_sq().sqrt()
    }

    /// Dot product with another vector
    #[inline]
    pub fn dot(&self, other: &Point3) -> f32 {
        self.x * other.x + self.y * other.y + self.z * other.z
    }

    /// Cross product with another vector
    #[inline]
    pub fn cross(&self, other: &Point3) -> Point3 {
        Point3::new(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )
    }

    /// Normalize the vector
    #[inline]
    pub fn normalize(&self) -> Point3 {
        let len = self.length();
        if len > 1e-10 {
            Point3::new(self.x / len, self.y / len, self.z / len)
        } else {
            *self
        }
    }

    /// Scale the vector by a factor
    #[inline]
    pub fn scale(&self, factor: f32) -> Point3 {
        Point3::new(self.x * factor, self.y * factor, self.z * factor)
    }

    /// Negate the vector
    #[inline]
    pub fn neg(&self) -> Point3 {
        Point3::new(-self.x, -self.y, -self.z)
    }

    /// Check if the point is valid (no NaN or Inf values)
    #[inline]
    pub fn is_valid(&self) -> bool {
        self.x.is_finite() && self.y.is_finite() && self.z.is_finite()
    }
}

impl Add for Point3 {
    type Output = Point3;

    #[inline]
    fn add(self, other: Point3) -> Point3 {
        Point3::new(self.x + other.x, self.y + other.y, self.z + other.z)
    }
}

impl Sub for Point3 {
    type Output = Point3;

    #[inline]
    fn sub(self, other: Point3) -> Point3 {
        Point3::new(self.x - other.x, self.y - other.y, self.z - other.z)
    }
}

impl Mul<f32> for Point3 {
    type Output = Point3;

    #[inline]
    fn mul(self, scalar: f32) -> Point3 {
        Point3::new(self.x * scalar, self.y * scalar, self.z * scalar)
    }
}

impl Mul<Point3> for f32 {
    type Output = Point3;

    #[inline]
    fn mul(self, point: Point3) -> Point3 {
        point * self
    }
}

/// Calculate dihedral angle (phi, psi, omega) between four points
/// Returns angle in degrees, or INVALID_ANGLE (360.0) if calculation fails
///
/// The dihedral angle is the angle between two planes:
/// - Plane 1: defined by points p1, p2, p3
/// - Plane 2: defined by points p2, p3, p4
///
/// # Arguments
/// * `p1` - First point
/// * `p2` - Second point (axis start)
/// * `p3` - Third point (axis end)
/// * `p4` - Fourth point
pub fn dihedral_angle(p1: &Point3, p2: &Point3, p3: &Point3, p4: &Point3) -> f32 {
    // Following DSSP C++ convention:
    // Vectors are in reverse direction for proper sign
    let v12 = *p1 - *p2;
    let v23 = *p2 - *p3;
    let v34 = *p3 - *p4;

    // Cross products for planes
    let x = v12.cross(&v23);
    let y = v23.cross(&v34);

    // Compute the dihedral angle
    let z = x.cross(&y);
    let v23_len = v23.length();

    if v23_len < 1e-10 {
        return INVALID_ANGLE;
    }

    let v23_norm = v23.scale(1.0 / v23_len);
    let d = z.dot(&v23_norm);

    let cross_dot = x.dot(&y);

    if cross_dot.abs() < 1e-10 && d.abs() < 1e-10 {
        return INVALID_ANGLE;
    }

    let angle = d.atan2(cross_dot) * RAD_TO_DEG;

    // Normalize to [-180, 180]
    if angle > 180.0 {
        angle - 360.0
    } else if angle < -180.0 {
        angle + 360.0
    } else {
        angle
    }
}

/// Calculate cosine of angle between two vectors defined by four points
/// Returns cos(angle between v12 and v34) where v12 = p1-p2, v34 = p3-p4
///
/// # Arguments
/// * `p1` - Start of first vector
/// * `p2` - End of first vector
/// * `p3` - Start of second vector
/// * `p4` - End of second vector
pub fn cosine_angle(p1: &Point3, p2: &Point3, p3: &Point3, p4: &Point3) -> f32 {
    let v12 = *p1 - *p2;
    let v34 = *p3 - *p4;

    let len_sq = v12.length_sq() * v34.length_sq();
    if len_sq < 1e-20 {
        return 0.0;
    }

    let cos = v12.dot(&v34) / len_sq.sqrt();
    cos.clamp(-1.0, 1.0)
}

/// Calculate virtual bond angle (kappa) at a CA position
/// This is the angle at CA[i] formed by CA[i-2] -> CA[i] -> CA[i+2]
///
/// # Arguments
/// * `ca_prev2` - CA position of residue i-2
/// * `ca` - CA position of residue i
/// * `ca_next2` - CA position of residue i+2
///
/// # Returns
/// Kappa angle in degrees, or INVALID_ANGLE if calculation fails
pub fn calculate_kappa(ca_prev2: &Point3, ca: &Point3, ca_next2: &Point3) -> f32 {
    let v1 = *ca_prev2 - *ca; // ca_prev2 -> ca
    let v2 = *ca_next2 - *ca; // ca_next2 -> ca

    let len_sq = v1.length_sq() * v2.length_sq();
    if len_sq < 1e-20 {
        return INVALID_ANGLE;
    }

    let cos_kappa = v1.dot(&v2) / len_sq.sqrt();
    let cos_kappa = cos_kappa.clamp(-1.0, 1.0);

    // kappa = pi - angle, convert to degrees
    (PI_F32 - cos_kappa.acos()) * RAD_TO_DEG
}

/// Calculate alpha (CA virtual torsion angle)
/// This is the dihedral angle CA[i-1] - CA[i] - CA[i+1] - CA[i+2]
///
/// # Arguments
/// * `ca_prev` - CA position of residue i-1
/// * `ca` - CA position of residue i
/// * `ca_next` - CA position of residue i+1
/// * `ca_next2` - CA position of residue i+2
///
/// # Returns
/// Alpha angle in degrees
pub fn calculate_alpha(
    ca_prev: &Point3,
    ca: &Point3,
    ca_next: &Point3,
    ca_next2: &Point3,
) -> f32 {
    dihedral_angle(ca_prev, ca, ca_next, ca_next2)
}

/// Calculate TCO (cosine of C=O angle with previous C=O)
///
/// # Arguments
/// * `c` - Current carbonyl carbon
/// * `o` - Current carbonyl oxygen
/// * `prev_c` - Previous carbonyl carbon
/// * `prev_o` - Previous carbonyl oxygen
///
/// # Returns
/// Cosine of angle between current and previous C=O vectors
pub fn calculate_tco(c: &Point3, o: &Point3, prev_c: &Point3, prev_o: &Point3) -> f32 {
    cosine_angle(c, o, prev_c, prev_o)
}

/// Calculate angle in degrees from three points
/// Returns the angle at p2 formed by p1-p2-p3
pub fn angle_degrees(p1: &Point3, p2: &Point3, p3: &Point3) -> f32 {
    let v1 = *p1 - *p2;
    let v2 = *p3 - *p2;

    let len_sq = v1.length_sq() * v2.length_sq();
    if len_sq < 1e-20 {
        return INVALID_ANGLE;
    }

    let cos_angle = v1.dot(&v2) / len_sq.sqrt();
    let cos_angle = cos_angle.clamp(-1.0, 1.0);

    cos_angle.acos() * RAD_TO_DEG
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_point3_operations() {
        let a = Point3::new(1.0, 2.0, 3.0);
        let b = Point3::new(4.0, 5.0, 6.0);

        // Addition
        let sum = a + b;
        assert!((sum.x - 5.0).abs() < 1e-6);
        assert!((sum.y - 7.0).abs() < 1e-6);
        assert!((sum.z - 9.0).abs() < 1e-6);

        // Subtraction
        let diff = b - a;
        assert!((diff.x - 3.0).abs() < 1e-6);
        assert!((diff.y - 3.0).abs() < 1e-6);
        assert!((diff.z - 3.0).abs() < 1e-6);

        // Dot product
        let dot = a.dot(&b);
        assert!((dot - 32.0).abs() < 1e-6); // 1*4 + 2*5 + 3*6

        // Cross product
        let cross = a.cross(&b);
        assert!((cross.x - (-3.0)).abs() < 1e-6); // 2*6 - 3*5
        assert!((cross.y - 6.0).abs() < 1e-6); // 3*4 - 1*6
        assert!((cross.z - (-3.0)).abs() < 1e-6); // 1*5 - 2*4
    }

    #[test]
    fn test_distance() {
        let a = Point3::new(0.0, 0.0, 0.0);
        let b = Point3::new(3.0, 4.0, 0.0);
        assert!((a.distance(&b) - 5.0).abs() < 1e-6);
    }

    #[test]
    fn test_normalize() {
        let v = Point3::new(3.0, 4.0, 0.0);
        let n = v.normalize();
        assert!((n.x - 0.6).abs() < 1e-6);
        assert!((n.y - 0.8).abs() < 1e-6);
        assert!((n.z - 0.0).abs() < 1e-6);
        assert!((n.length() - 1.0).abs() < 1e-6);
    }

    #[test]
    fn test_dihedral_angle() {
        // Test with known geometry
        let p1 = Point3::new(1.0, 0.0, 0.0);
        let p2 = Point3::new(0.0, 0.0, 0.0);
        let p3 = Point3::new(0.0, 1.0, 0.0);
        let p4 = Point3::new(0.0, 1.0, 1.0);

        let angle = dihedral_angle(&p1, &p2, &p3, &p4);
        // Expected: 90 degrees (or close to it)
        assert!((angle - 90.0).abs() < 1.0 || (angle + 90.0).abs() < 1.0);
    }

    #[test]
    fn test_kappa() {
        // Linear chain: kappa should be ~0 degrees (no bend)
        let ca_prev2 = Point3::new(0.0, 0.0, 0.0);
        let ca = Point3::new(1.0, 0.0, 0.0);
        let ca_next2 = Point3::new(2.0, 0.0, 0.0);

        let kappa = calculate_kappa(&ca_prev2, &ca, &ca_next2);
        // For a linear chain, kappa (bend angle) should be close to 0 degrees
        assert!(kappa.abs() < 1.0 || kappa == INVALID_ANGLE, "Linear chain kappa: {}", kappa);

        // Right angle bend: kappa should be ~90 degrees
        let ca_prev2 = Point3::new(0.0, 0.0, 0.0);
        let ca = Point3::new(1.0, 0.0, 0.0);
        let ca_next2 = Point3::new(1.0, 1.0, 0.0);

        let kappa = calculate_kappa(&ca_prev2, &ca, &ca_next2);
        assert!((kappa - 90.0).abs() < 1.0, "Right angle kappa: {}", kappa);
    }
}
