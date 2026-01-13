//! Criterion benchmarks for DSSP core algorithm.
//!
//! These benchmarks measure pure algorithm performance, excluding CLI and I/O overhead.

use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion, Throughput};
use dssp_core::{calculate_dssp, DsspConfig, Structure};
use dssp_io::pdb::parse_pdb;
use std::fs::File;
use std::path::Path;

/// Load test structures from TS50 dataset
fn load_test_structures() -> Vec<(String, Structure)> {
    let pdb_dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .join("benches/data/pdb");

    let mut structures = Vec::new();

    if pdb_dir.exists() {
        for entry in std::fs::read_dir(&pdb_dir).unwrap() {
            let entry = entry.unwrap();
            let path = entry.path();
            if path.extension().map(|e| e == "pdb").unwrap_or(false) {
                let name = path.file_stem().unwrap().to_string_lossy().to_string();
                if let Ok(file) = File::open(&path) {
                    if let Ok(structure) = parse_pdb(file) {
                        structures.push((name, structure));
                    }
                }
            }
        }
    }

    // Sort by residue count for consistent ordering
    structures.sort_by_key(|(_, s)| s.residues.len());
    structures
}

/// Get a medium-sized structure for consistent benchmarking
fn get_medium_structure() -> Option<Structure> {
    let structures = load_test_structures();
    if structures.is_empty() {
        return None;
    }
    // Pick a structure around the median size
    let idx = structures.len() / 2;
    Some(structures[idx].1.clone())
}

/// Get a small, medium, and large structure for scaling benchmarks
fn get_size_samples() -> Vec<(String, Structure)> {
    let structures = load_test_structures();
    if structures.len() < 3 {
        return structures;
    }

    let small_idx = structures.len() / 4;
    let medium_idx = structures.len() / 2;
    let large_idx = structures.len() * 3 / 4;

    vec![
        ("small".to_string(), structures[small_idx].1.clone()),
        ("medium".to_string(), structures[medium_idx].1.clone()),
        ("large".to_string(), structures[large_idx].1.clone()),
    ]
}

/// Benchmark DSSP with SASA calculation (full mode)
fn bench_dssp_with_sasa(c: &mut Criterion) {
    let structure = match get_medium_structure() {
        Some(s) => s,
        None => {
            eprintln!("Warning: No test structures found. Skipping benchmark.");
            return;
        }
    };

    let residue_count = structure.residues.len() as u64;
    let mut group = c.benchmark_group("dssp_with_sasa");
    group.throughput(Throughput::Elements(residue_count));

    group.bench_function("medium_protein", |b| {
        b.iter(|| {
            let mut s = structure.clone();
            let config = DsspConfig {
                calculate_accessibility: true,
                ..Default::default()
            };
            calculate_dssp(black_box(&mut s), black_box(&config))
        })
    });

    group.finish();
}

/// Benchmark DSSP without SASA calculation (core secondary structure only)
fn bench_dssp_without_sasa(c: &mut Criterion) {
    let structure = match get_medium_structure() {
        Some(s) => s,
        None => {
            eprintln!("Warning: No test structures found. Skipping benchmark.");
            return;
        }
    };

    let residue_count = structure.residues.len() as u64;
    let mut group = c.benchmark_group("dssp_without_sasa");
    group.throughput(Throughput::Elements(residue_count));

    group.bench_function("medium_protein", |b| {
        b.iter(|| {
            let mut s = structure.clone();
            let config = DsspConfig {
                calculate_accessibility: false,
                ..Default::default()
            };
            calculate_dssp(black_box(&mut s), black_box(&config))
        })
    });

    group.finish();
}

/// Benchmark how DSSP scales with protein size
fn bench_dssp_scaling(c: &mut Criterion) {
    let samples = get_size_samples();
    if samples.is_empty() {
        eprintln!("Warning: No test structures found. Skipping benchmark.");
        return;
    }

    let mut group = c.benchmark_group("dssp_scaling");

    for (name, structure) in &samples {
        let residue_count = structure.residues.len() as u64;
        group.throughput(Throughput::Elements(residue_count));

        // Without SASA (to compare core algorithm scaling)
        group.bench_with_input(
            BenchmarkId::new("no_sasa", format!("{}_{}_res", name, residue_count)),
            structure,
            |b, structure| {
                b.iter(|| {
                    let mut s = structure.clone();
                    let config = DsspConfig {
                        calculate_accessibility: false,
                        ..Default::default()
                    };
                    calculate_dssp(black_box(&mut s), black_box(&config))
                })
            },
        );

        // With SASA
        group.bench_with_input(
            BenchmarkId::new("with_sasa", format!("{}_{}_res", name, residue_count)),
            structure,
            |b, structure| {
                b.iter(|| {
                    let mut s = structure.clone();
                    let config = DsspConfig {
                        calculate_accessibility: true,
                        ..Default::default()
                    };
                    calculate_dssp(black_box(&mut s), black_box(&config))
                })
            },
        );
    }

    group.finish();
}

/// Benchmark all TS50 structures to compute total throughput
fn bench_ts50_total(c: &mut Criterion) {
    let structures = load_test_structures();
    if structures.is_empty() {
        eprintln!("Warning: No test structures found. Skipping benchmark.");
        return;
    }

    let total_residues: u64 = structures.iter().map(|(_, s)| s.residues.len() as u64).sum();
    let mut group = c.benchmark_group("ts50_total");
    group.throughput(Throughput::Elements(total_residues));

    group.bench_function("all_without_sasa", |b| {
        b.iter(|| {
            for (_, structure) in &structures {
                let mut s = structure.clone();
                let config = DsspConfig {
                    calculate_accessibility: false,
                    ..Default::default()
                };
                calculate_dssp(black_box(&mut s), black_box(&config));
            }
        })
    });

    group.bench_function("all_with_sasa", |b| {
        b.iter(|| {
            for (_, structure) in &structures {
                let mut s = structure.clone();
                let config = DsspConfig {
                    calculate_accessibility: true,
                    ..Default::default()
                };
                calculate_dssp(black_box(&mut s), black_box(&config));
            }
        })
    });

    group.finish();
}

criterion_group!(
    benches,
    bench_dssp_with_sasa,
    bench_dssp_without_sasa,
    bench_dssp_scaling,
    bench_ts50_total
);
criterion_main!(benches);
