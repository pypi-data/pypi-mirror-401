//! Core data structures for DSSP
//!
//! This module defines the primary types used throughout the DSSP algorithm:
//! - `SecondaryStructure`: C8 classification enum
//! - `AminoAcid`: Standard amino acid types
//! - `Residue`: Complete residue information
//! - `Structure`: Protein structure container
//! - Helper types for hydrogen bonds, bridges, and helices

use crate::constants::{MAX_HBOND_ENERGY, NO_BOND_ENERGY};
use crate::geometry::Point3;
use serde::{Deserialize, Serialize};
use std::fmt;

// ============================================================================
// Secondary Structure Types
// ============================================================================

/// Secondary structure type using C8 classification
/// Based on DSSP (Kabsch & Sander 1983)
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default, Serialize, Deserialize)]
#[repr(u8)]
pub enum SecondaryStructure {
    /// Loop/Coil (default)
    #[default]
    Loop = b' ',
    /// Alpha helix (H) - i+4 -> i hydrogen bond pattern
    AlphaHelix = b'H',
    /// Beta bridge (B) - isolated beta-bridge
    BetaBridge = b'B',
    /// Extended strand (E) - in beta-sheet
    Strand = b'E',
    /// 3-10 helix (G) - i+3 -> i hydrogen bond pattern
    Helix310 = b'G',
    /// Pi helix (I) - i+5 -> i hydrogen bond pattern
    PiHelix = b'I',
    /// Turn (T) - hydrogen bonded turn
    Turn = b'T',
    /// Bend (S) - high curvature region
    Bend = b'S',
    /// Poly-Proline II helix (P)
    PPIIHelix = b'P',
}

impl SecondaryStructure {
    /// Convert to single character representation
    pub fn as_char(&self) -> char {
        match self {
            SecondaryStructure::Loop => ' ',
            SecondaryStructure::AlphaHelix => 'H',
            SecondaryStructure::BetaBridge => 'B',
            SecondaryStructure::Strand => 'E',
            SecondaryStructure::Helix310 => 'G',
            SecondaryStructure::PiHelix => 'I',
            SecondaryStructure::Turn => 'T',
            SecondaryStructure::Bend => 'S',
            SecondaryStructure::PPIIHelix => 'P',
        }
    }

    /// Convert to C3 classification
    /// - 0: Loop (space, S, T, P)
    /// - 1: Helix (H, G, I)
    /// - 2: Strand (E, B)
    pub fn to_c3(&self) -> u8 {
        match self {
            SecondaryStructure::Loop
            | SecondaryStructure::Turn
            | SecondaryStructure::Bend
            | SecondaryStructure::PPIIHelix => 0,
            SecondaryStructure::AlphaHelix
            | SecondaryStructure::Helix310
            | SecondaryStructure::PiHelix => 1,
            SecondaryStructure::Strand | SecondaryStructure::BetaBridge => 2,
        }
    }

    /// Convert to C3 character
    /// - '-': Loop
    /// - 'H': Helix
    /// - 'E': Strand
    pub fn to_c3_char(&self) -> char {
        match self.to_c3() {
            0 => '-',
            1 => 'H',
            2 => 'E',
            _ => unreachable!(),
        }
    }

    /// Create from character
    pub fn from_char(c: char) -> Option<Self> {
        match c {
            ' ' | '-' => Some(SecondaryStructure::Loop),
            'H' => Some(SecondaryStructure::AlphaHelix),
            'B' => Some(SecondaryStructure::BetaBridge),
            'E' => Some(SecondaryStructure::Strand),
            'G' => Some(SecondaryStructure::Helix310),
            'I' => Some(SecondaryStructure::PiHelix),
            'T' => Some(SecondaryStructure::Turn),
            'S' => Some(SecondaryStructure::Bend),
            'P' => Some(SecondaryStructure::PPIIHelix),
            _ => None,
        }
    }

    /// Check if this is a helix type
    pub fn is_helix(&self) -> bool {
        matches!(
            self,
            SecondaryStructure::AlphaHelix
                | SecondaryStructure::Helix310
                | SecondaryStructure::PiHelix
                | SecondaryStructure::PPIIHelix
        )
    }

    /// Check if this is a strand type
    pub fn is_strand(&self) -> bool {
        matches!(
            self,
            SecondaryStructure::Strand | SecondaryStructure::BetaBridge
        )
    }
}

impl fmt::Display for SecondaryStructure {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.as_char())
    }
}

// ============================================================================
// Helix Types
// ============================================================================

/// Helix type for internal tracking
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
#[repr(u8)]
pub enum HelixType {
    /// 3-10 helix (stride = 3)
    #[default]
    H310 = 0,
    /// Alpha helix (stride = 4)
    Alpha = 1,
    /// Pi helix (stride = 5)
    Pi = 2,
    /// Poly-Proline II helix
    PPII = 3,
}

impl HelixType {
    /// Get the stride (number of residues) for this helix type
    pub fn stride(&self) -> usize {
        match self {
            HelixType::H310 => 3,
            HelixType::Alpha => 4,
            HelixType::Pi => 5,
            HelixType::PPII => 0, // PPII doesn't use stride-based detection
        }
    }

    /// Get all H-bond based helix types
    pub fn hbond_types() -> [HelixType; 3] {
        [HelixType::H310, HelixType::Alpha, HelixType::Pi]
    }
}

/// Position within a helix
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum HelixPosition {
    /// Not part of a helix
    #[default]
    None,
    /// Start of helix (has outgoing H-bond)
    Start,
    /// Middle of helix
    Middle,
    /// End of helix (has incoming H-bond)
    End,
    /// Both start and end (in overlapping helices)
    StartAndEnd,
}

impl HelixPosition {
    /// Check if this position marks a helix start
    pub fn is_start(&self) -> bool {
        matches!(self, HelixPosition::Start | HelixPosition::StartAndEnd)
    }

    /// Check if this position marks a helix end
    pub fn is_end(&self) -> bool {
        matches!(self, HelixPosition::End | HelixPosition::StartAndEnd)
    }
}

// ============================================================================
// Bridge Types
// ============================================================================

/// Bridge type between beta strands
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum BridgeType {
    #[default]
    None,
    Parallel,
    AntiParallel,
}

// ============================================================================
// Hydrogen Bond Types
// ============================================================================

/// Hydrogen bond information
#[derive(Debug, Clone, Copy, Default)]
pub struct HBond {
    /// Index of bonded residue (None if no bond)
    pub partner_idx: Option<usize>,
    /// Bond energy in kcal/mol (negative = favorable)
    pub energy: f64,
}

impl HBond {
    /// Create a new hydrogen bond
    pub fn new(partner_idx: usize, energy: f64) -> Self {
        Self {
            partner_idx: Some(partner_idx),
            energy,
        }
    }

    /// Create an empty (no bond) entry
    pub fn none() -> Self {
        Self {
            partner_idx: None,
            energy: NO_BOND_ENERGY,
        }
    }

    /// Check if this is a valid hydrogen bond
    pub fn is_bond(&self) -> bool {
        self.partner_idx.is_some() && self.energy < MAX_HBOND_ENERGY
    }
}

/// Bridge partner information
#[derive(Debug, Clone, Default)]
pub struct BridgePartner {
    /// Index of partner residue
    pub residue_idx: Option<usize>,
    /// Ladder number (for sheet identification)
    pub ladder: u32,
    /// Whether this is a parallel bridge
    pub parallel: bool,
}

// ============================================================================
// Chain Break Types
// ============================================================================

/// Chain break type
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum ChainBreak {
    /// No chain break
    #[default]
    None,
    /// New chain starts here
    NewChain,
    /// Gap in sequence numbering
    Gap,
}

// ============================================================================
// Amino Acid Types
// ============================================================================

/// Standard amino acid types
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default, Serialize, Deserialize)]
#[repr(u8)]
pub enum AminoAcid {
    Ala = b'A',
    Arg = b'R',
    Asn = b'N',
    Asp = b'D',
    Cys = b'C',
    Gln = b'Q',
    Glu = b'E',
    Gly = b'G',
    His = b'H',
    Ile = b'I',
    Leu = b'L',
    Lys = b'K',
    Met = b'M',
    Phe = b'F',
    Pro = b'P',
    Ser = b'S',
    Thr = b'T',
    Trp = b'W',
    Tyr = b'Y',
    Val = b'V',
    #[default]
    Unknown = b'X',
}

impl AminoAcid {
    /// Create from one-letter code
    pub fn from_char(c: char) -> Self {
        match c.to_ascii_uppercase() {
            'A' => AminoAcid::Ala,
            'R' => AminoAcid::Arg,
            'N' => AminoAcid::Asn,
            'D' => AminoAcid::Asp,
            'C' => AminoAcid::Cys,
            'Q' => AminoAcid::Gln,
            'E' => AminoAcid::Glu,
            'G' => AminoAcid::Gly,
            'H' => AminoAcid::His,
            'I' => AminoAcid::Ile,
            'L' => AminoAcid::Leu,
            'K' => AminoAcid::Lys,
            'M' => AminoAcid::Met,
            'F' => AminoAcid::Phe,
            'P' => AminoAcid::Pro,
            'S' => AminoAcid::Ser,
            'T' => AminoAcid::Thr,
            'W' => AminoAcid::Trp,
            'Y' => AminoAcid::Tyr,
            'V' => AminoAcid::Val,
            _ => AminoAcid::Unknown,
        }
    }

    /// Create from three-letter code
    pub fn from_three_letter(code: &str) -> Self {
        match code.to_uppercase().as_str() {
            "ALA" => AminoAcid::Ala,
            "ARG" => AminoAcid::Arg,
            "ASN" => AminoAcid::Asn,
            "ASP" => AminoAcid::Asp,
            "CYS" => AminoAcid::Cys,
            "GLN" => AminoAcid::Gln,
            "GLU" => AminoAcid::Glu,
            "GLY" => AminoAcid::Gly,
            "HIS" | "HID" | "HIE" | "HIP" => AminoAcid::His,
            "ILE" => AminoAcid::Ile,
            "LEU" => AminoAcid::Leu,
            "LYS" => AminoAcid::Lys,
            "MET" | "MSE" => AminoAcid::Met, // MSE = selenomethionine
            "PHE" => AminoAcid::Phe,
            "PRO" => AminoAcid::Pro,
            "SER" => AminoAcid::Ser,
            "THR" => AminoAcid::Thr,
            "TRP" => AminoAcid::Trp,
            "TYR" => AminoAcid::Tyr,
            "VAL" => AminoAcid::Val,
            _ => AminoAcid::Unknown,
        }
    }

    /// Convert to one-letter code
    pub fn as_char(&self) -> char {
        *self as u8 as char
    }

    /// Convert to three-letter code
    pub fn to_three_letter(&self) -> &'static str {
        match self {
            AminoAcid::Ala => "ALA",
            AminoAcid::Arg => "ARG",
            AminoAcid::Asn => "ASN",
            AminoAcid::Asp => "ASP",
            AminoAcid::Cys => "CYS",
            AminoAcid::Gln => "GLN",
            AminoAcid::Glu => "GLU",
            AminoAcid::Gly => "GLY",
            AminoAcid::His => "HIS",
            AminoAcid::Ile => "ILE",
            AminoAcid::Leu => "LEU",
            AminoAcid::Lys => "LYS",
            AminoAcid::Met => "MET",
            AminoAcid::Phe => "PHE",
            AminoAcid::Pro => "PRO",
            AminoAcid::Ser => "SER",
            AminoAcid::Thr => "THR",
            AminoAcid::Trp => "TRP",
            AminoAcid::Tyr => "TYR",
            AminoAcid::Val => "VAL",
            AminoAcid::Unknown => "UNK",
        }
    }

    /// Check if this is Proline (no amide hydrogen)
    pub fn is_proline(&self) -> bool {
        *self == AminoAcid::Pro
    }
}

impl fmt::Display for AminoAcid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.as_char())
    }
}

// ============================================================================
// Backbone Atoms
// ============================================================================

/// Backbone atoms for a single residue
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct BackboneAtoms {
    /// Nitrogen
    pub n: Point3,
    /// C-alpha
    pub ca: Point3,
    /// Carbonyl carbon
    pub c: Point3,
    /// Carbonyl oxygen
    pub o: Point3,
    /// Amide hydrogen (computed if not provided)
    pub h: Option<Point3>,
}

impl BackboneAtoms {
    /// Create new backbone atoms
    pub fn new(n: Point3, ca: Point3, c: Point3, o: Point3) -> Self {
        Self {
            n,
            ca,
            c,
            o,
            h: None,
        }
    }

    /// Create with explicit hydrogen
    pub fn with_hydrogen(n: Point3, ca: Point3, c: Point3, o: Point3, h: Point3) -> Self {
        Self {
            n,
            ca,
            c,
            o,
            h: Some(h),
        }
    }

    /// Check if all backbone atoms are valid
    pub fn is_valid(&self) -> bool {
        self.n.is_valid() && self.ca.is_valid() && self.c.is_valid() && self.o.is_valid()
    }
}

// ============================================================================
// Residue
// ============================================================================

/// Complete residue information
#[derive(Debug, Clone)]
pub struct Residue {
    // Identity
    /// Chain identifier
    pub chain_id: String,
    /// Sequence number (from PDB)
    pub seq_id: i32,
    /// Insertion code
    pub ins_code: String,
    /// Compound ID (three-letter code)
    pub compound_id: String,
    /// Amino acid type
    pub amino_acid: AminoAcid,

    // Coordinates
    /// Backbone atoms
    pub backbone: BackboneAtoms,
    /// Side chain atoms (name, position)
    pub side_chain: Vec<(String, Point3)>,

    // Computed geometry
    /// Phi dihedral angle (degrees)
    pub phi: Option<f32>,
    /// Psi dihedral angle (degrees)
    pub psi: Option<f32>,
    /// Omega dihedral angle (degrees)
    pub omega: Option<f32>,
    /// Kappa virtual bond angle (degrees)
    pub kappa: Option<f32>,
    /// Alpha CA virtual torsion (degrees)
    pub alpha: Option<f32>,
    /// TCO (cosine of C=O angle)
    pub tco: Option<f32>,

    // Secondary structure
    /// Assigned secondary structure
    pub structure: SecondaryStructure,
    /// Helix position flags for each helix type
    pub helix_flags: [HelixPosition; 4],
    /// Whether this residue is at a bend
    pub is_bend: bool,

    // Hydrogen bonding
    /// H-bonds where this residue is donor (N-H...O=C)
    pub hbond_acceptor: [HBond; 2],
    /// H-bonds where this residue is acceptor (C=O...H-N)
    pub hbond_donor: [HBond; 2],

    // Beta structure
    /// Bridge partners
    pub bridge_partners: [BridgePartner; 2],
    /// Sheet identifier
    pub sheet_id: u32,
    /// Strand identifier
    pub strand_id: u32,

    // Disulfide bridge
    /// SS-bridge number (if in disulfide bridge)
    pub ss_bridge_nr: Option<u8>,

    // Chain break tracking
    /// Type of chain break before this residue
    pub chain_break: ChainBreak,

    // Internal numbering
    /// Internal sequential number (0-based)
    pub internal_nr: usize,

    // SASA
    /// Accessible surface area (Å²)
    pub accessibility: f32,
}

impl Residue {
    /// Create a new residue with minimal information
    pub fn new(
        chain_id: String,
        seq_id: i32,
        compound_id: String,
        backbone: BackboneAtoms,
    ) -> Self {
        let amino_acid = AminoAcid::from_three_letter(&compound_id);
        Self {
            chain_id,
            seq_id,
            ins_code: String::new(),
            compound_id,
            amino_acid,
            backbone,
            side_chain: Vec::new(),
            phi: None,
            psi: None,
            omega: None,
            kappa: None,
            alpha: None,
            tco: None,
            structure: SecondaryStructure::Loop,
            helix_flags: [HelixPosition::None; 4],
            is_bend: false,
            hbond_acceptor: [HBond::none(), HBond::none()],
            hbond_donor: [HBond::none(), HBond::none()],
            bridge_partners: [BridgePartner::default(), BridgePartner::default()],
            sheet_id: 0,
            strand_id: 0,
            ss_bridge_nr: None,
            chain_break: ChainBreak::None,
            internal_nr: 0,
            accessibility: 0.0,
        }
    }

    /// Check if this residue can be a hydrogen bond donor (has N-H)
    pub fn can_donate(&self) -> bool {
        !self.amino_acid.is_proline()
    }

    /// Get residue identifier string (e.g., "A:42")
    pub fn id(&self) -> String {
        if self.ins_code.is_empty() {
            format!("{}:{}", self.chain_id, self.seq_id)
        } else {
            format!("{}:{}{}", self.chain_id, self.seq_id, self.ins_code)
        }
    }
}

impl Default for Residue {
    fn default() -> Self {
        Self::new(
            String::new(),
            0,
            "UNK".to_string(),
            BackboneAtoms::default(),
        )
    }
}

// ============================================================================
// Chain Information
// ============================================================================

/// Chain information
#[derive(Debug, Clone, Default)]
pub struct ChainInfo {
    /// Chain identifier
    pub id: String,
    /// Start index in residues array
    pub start_idx: usize,
    /// End index in residues array (exclusive)
    pub end_idx: usize,
}

// ============================================================================
// Structure
// ============================================================================

/// Complete protein structure
#[derive(Debug, Clone, Default)]
pub struct Structure {
    /// Structure identifier (e.g., PDB ID)
    pub id: String,
    /// All residues
    pub residues: Vec<Residue>,
    /// Chain information
    pub chains: Vec<ChainInfo>,
    /// Disulfide bonds (residue index pairs)
    pub ss_bonds: Vec<(usize, usize)>,
}

impl Structure {
    /// Create a new structure with the given ID
    pub fn new(id: String) -> Self {
        Self {
            id,
            residues: Vec::new(),
            chains: Vec::new(),
            ss_bonds: Vec::new(),
        }
    }

    /// Create from a vector of residues
    pub fn from_residues(residues: Vec<Residue>) -> Self {
        let mut structure = Self {
            id: String::new(),
            residues,
            chains: Vec::new(),
            ss_bonds: Vec::new(),
        };
        structure.update_internal_indices();
        structure.identify_chains();
        structure
    }

    /// Update internal indices for all residues
    pub fn update_internal_indices(&mut self) {
        for (i, residue) in self.residues.iter_mut().enumerate() {
            residue.internal_nr = i;
        }
    }

    /// Identify chains from residues
    pub fn identify_chains(&mut self) {
        self.chains.clear();
        if self.residues.is_empty() {
            return;
        }

        let mut current_chain = self.residues[0].chain_id.clone();
        let mut start_idx = 0;

        for (i, residue) in self.residues.iter().enumerate() {
            if residue.chain_id != current_chain {
                self.chains.push(ChainInfo {
                    id: current_chain.clone(),
                    start_idx,
                    end_idx: i,
                });
                current_chain = residue.chain_id.clone();
                start_idx = i;
            }
        }

        // Add last chain
        self.chains.push(ChainInfo {
            id: current_chain,
            start_idx,
            end_idx: self.residues.len(),
        });
    }

    /// Get the secondary structure sequence as a string (C8)
    pub fn ss_sequence(&self) -> String {
        self.residues.iter().map(|r| r.structure.as_char()).collect()
    }

    /// Get the secondary structure sequence as a string (C3)
    pub fn ss_sequence_c3(&self) -> String {
        self.residues
            .iter()
            .map(|r| r.structure.to_c3_char())
            .collect()
    }

    /// Get the amino acid sequence as a string
    pub fn aa_sequence(&self) -> String {
        self.residues.iter().map(|r| r.amino_acid.as_char()).collect()
    }

    /// Get the number of residues
    pub fn len(&self) -> usize {
        self.residues.len()
    }

    /// Check if structure is empty
    pub fn is_empty(&self) -> bool {
        self.residues.is_empty()
    }
}

// ============================================================================
// Statistics
// ============================================================================

/// Statistics from DSSP calculation
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct Statistics {
    /// Total number of residues
    pub residue_count: u32,
    /// Number of chains
    pub chain_count: u32,
    /// Number of SS bridges (total)
    pub ss_bridge_count: u32,
    /// Number of intra-chain SS bridges
    pub intra_chain_ss_bridges: u32,
    /// Total hydrogen bond count
    pub hbond_count: u32,
    /// Hydrogen bonds in parallel bridges
    pub hbonds_parallel_bridges: u32,
    /// Hydrogen bonds in antiparallel bridges
    pub hbonds_antiparallel_bridges: u32,
    /// Histogram of H-bonds by distance (i to i+k for k=-5 to +5)
    pub hbonds_per_distance: [u32; 11],
    /// Histogram of residues per alpha helix
    pub residues_per_alpha_helix: [u32; 30],
    /// Histogram of parallel bridges per ladder
    pub parallel_bridges_per_ladder: [u32; 30],
    /// Histogram of antiparallel bridges per ladder
    pub antiparallel_bridges_per_ladder: [u32; 30],
    /// Histogram of ladders per sheet
    pub ladders_per_sheet: [u32; 30],
    /// Total accessible surface area (Å²)
    pub accessible_surface: f64,
}

// ============================================================================
// DSSP Result
// ============================================================================

/// Complete DSSP calculation result
#[derive(Debug, Clone)]
pub struct DsspResult {
    /// Processed structure
    pub structure: Structure,
    /// Calculation statistics
    pub statistics: Statistics,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_secondary_structure() {
        assert_eq!(SecondaryStructure::AlphaHelix.as_char(), 'H');
        assert_eq!(SecondaryStructure::Strand.to_c3(), 2);
        assert_eq!(SecondaryStructure::Loop.to_c3_char(), '-');
    }

    #[test]
    fn test_amino_acid() {
        assert_eq!(AminoAcid::from_char('A'), AminoAcid::Ala);
        assert_eq!(AminoAcid::from_three_letter("ALA"), AminoAcid::Ala);
        assert!(AminoAcid::Pro.is_proline());
        assert!(!AminoAcid::Ala.is_proline());
    }

    #[test]
    fn test_hbond() {
        let bond = HBond::new(10, -1.5);
        assert!(bond.is_bond());
        assert_eq!(bond.partner_idx, Some(10));

        let no_bond = HBond::none();
        assert!(!no_bond.is_bond());
    }
}
