//! mmCIF format parser and writer

mod parser;
mod writer;

pub use parser::parse_cif;
pub use writer::write_cif;
