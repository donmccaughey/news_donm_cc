use serde_json;
use std;
use std::fmt;
use std::fmt::Display;
use std::io;
use std::path::Path;
use std::path::PathBuf;


#[derive(Debug)]
pub enum Error {
    InvalidPath(PathBuf, String),
    Io(io::Error),
    JsonConversion(serde_json::Error),
    JsonParsing(serde_json::Error),
}

impl Error {
    pub fn invalid_path(path: &Path) -> Error {
        Error::InvalidPath(path.to_path_buf(), path.to_string_lossy().to_string())
    }
}

impl Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            Error::InvalidPath(_, ref string) => write!(f, "Invalid path: {}", string),
            Error::Io(ref error) => write!(f, "IO error: {}", error),
            Error::JsonConversion(ref error) => write!(f, "JSON conversion error: {}", error),
            Error::JsonParsing(ref error) => write!(f, "JSON parsing error: {}", error),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match *self {
            Error::InvalidPath(_, _) => None,
            Error::Io(ref error) => Some(error),
            Error::JsonConversion(ref error) => Some(error),
            Error::JsonParsing(ref error) => Some(error),
        }
    }
}
