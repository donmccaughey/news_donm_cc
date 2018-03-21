use hyper;
use native_tls;
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
    JsonParsingError(serde_json::Error),
    JsonConversionError(serde_json::Error),
    HyperError(hyper::Error),
    TlsError(native_tls::Error),
    UriError(hyper::error::UriError),

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
            NewsError::JsonParsingError(ref error) => write!(f, "JSON parsing error: {}", error),
            NewsError::JsonConversionError(ref error) => write!(f, "JSON conversion error: {}", error),
            NewsError::HyperError(ref error) => write!(f, "Hyper error: {}", error),
            NewsError::TlsError(ref error) => write!(f, "TLS error: {}", error),
            NewsError::UriError(ref error) => write!(f, "URI error: {}", error),
        }
    }
}

impl Error for NewsError {
    fn description(&self) -> &str {
        match *self {
            NewsError::InvalidPath(_, ref string) => &string,
            NewsError::IoError(ref error) => error.description(),
            NewsError::JsonParsingError(ref error) => error.description(),
            NewsError::JsonConversionError(ref error) => error.description(),
            NewsError::HyperError(ref error) => error.description(),
            NewsError::TlsError(ref error) => error.description(),
            NewsError::UriError(ref error) => error.description(),
        }
    }
}
