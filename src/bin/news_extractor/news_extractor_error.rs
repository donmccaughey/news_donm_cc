use hyper;
use native_tls;
use serde_json;
use serde_xml_rs;
use std::error::Error;
use std::fmt;
use std::io;
use std::path::Path;
use std::path::PathBuf;


#[derive(Debug)]
pub enum NewsExtractorError {
    InvalidPath(PathBuf, String),
    IoError(io::Error),
    JsonParsingError(serde_json::Error),
    JsonConversionError(serde_json::Error),
    HyperError(hyper::Error),
    TlsError(native_tls::Error),
    UriError(hyper::error::UriError),
    XmlParsingError(serde_xml_rs::Error),

}

impl NewsExtractorError {
    pub fn invalid_path(path: &Path) -> NewsExtractorError {
        NewsExtractorError::InvalidPath(path.to_path_buf(), path.to_string_lossy().to_string())
    }
}

impl fmt::Display for NewsExtractorError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            NewsExtractorError::InvalidPath(_, ref string) => write!(f, "Invalid path: {}", string),
            NewsExtractorError::IoError(ref error) => write!(f, "IO error: {}", error),
            NewsExtractorError::JsonParsingError(ref error) => write!(f, "JSON parsing error: {}", error),
            NewsExtractorError::JsonConversionError(ref error) => write!(f, "JSON conversion error: {}", error),
            NewsExtractorError::HyperError(ref error) => write!(f, "Hyper error: {}", error),
            NewsExtractorError::TlsError(ref error) => write!(f, "TLS error: {}", error),
            NewsExtractorError::UriError(ref error) => write!(f, "URI error: {}", error),
            NewsExtractorError::XmlParsingError(ref error) => write!(f, "XML parsing error: {}", error),
        }
    }
}

impl Error for NewsExtractorError {
    fn description(&self) -> &str {
        match *self {
            NewsExtractorError::InvalidPath(_, ref string) => &string,
            NewsExtractorError::IoError(ref error) => error.description(),
            NewsExtractorError::JsonParsingError(ref error) => error.description(),
            NewsExtractorError::JsonConversionError(ref error) => error.description(),
            NewsExtractorError::HyperError(ref error) => error.description(),
            NewsExtractorError::TlsError(ref error) => error.description(),
            NewsExtractorError::UriError(ref error) => error.description(),
            NewsExtractorError::XmlParsingError(ref error) => error.description(),
        }
    }
}
