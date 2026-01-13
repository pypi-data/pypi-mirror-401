//! I/O error types

use thiserror::Error;

/// Result type alias for I/O operations
pub type Result<T> = std::result::Result<T, IoError>;

/// Errors that can occur during I/O operations
#[derive(Error, Debug)]
pub enum IoError {
    /// Standard I/O error
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    /// Parse error at specific line
    #[error("Parse error at line {line}: {message}")]
    Parse { line: usize, message: String },

    /// Invalid record format
    #[error("Invalid record: {0}")]
    InvalidRecord(String),

    /// Missing required field
    #[error("Missing field: {0}")]
    MissingField(String),

    /// Unsupported format
    #[error("Unsupported format: {0}")]
    UnsupportedFormat(String),

    /// Float parse error
    #[error("Invalid number: {0}")]
    ParseFloat(#[from] std::num::ParseFloatError),

    /// Int parse error
    #[error("Invalid integer: {0}")]
    ParseInt(#[from] std::num::ParseIntError),

    /// JSON error
    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),

    /// Empty file
    #[error("Empty file or no valid records")]
    EmptyFile,
}

impl IoError {
    /// Create a parse error
    pub fn parse(line: usize, message: impl Into<String>) -> Self {
        Self::Parse {
            line,
            message: message.into(),
        }
    }

    /// Create an invalid record error
    pub fn invalid_record(message: impl Into<String>) -> Self {
        Self::InvalidRecord(message.into())
    }
}
