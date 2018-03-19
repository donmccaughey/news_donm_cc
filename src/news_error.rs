use serde_json;
use std::error::Error;
use std::fmt;
use std::io;
use std::path::Path;
use std::path::PathBuf;


#[derive(Debug)]
pub enum NewsError {
    InvalidPath(PathBuf, String),
    IoError(io::Error),
    JSONParsingError(serde_json::Error),
    JSONConversionError(serde_json::Error),
}

impl NewsError {
    pub fn invalid_path(path: &Path) -> NewsError {
        NewsError::InvalidPath(path.to_path_buf(), path.to_string_lossy().to_string())
    }
}

impl fmt::Display for NewsError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            NewsError::InvalidPath(_, ref string) => write!(f, "Invalid path: {}", string),
            NewsError::IoError(ref error) => write!(f, "IO error: {}", error),
            NewsError::JSONParsingError(ref error) => write!(f, "JSON parsing error: {}", error),
            NewsError::JSONConversionError(ref error) => write!(f, "JSON conversion error: {}", error),
        }
    }
}

impl Error for NewsError {
    fn description(&self) -> &str {
        match *self {
            NewsError::InvalidPath(_, ref string) => &string,
            NewsError::IoError(ref error) => error.description(),
            NewsError::JSONParsingError(ref error) => error.description(),
            NewsError::JSONConversionError(ref error) => error.description(),
        }
    }
}
