use news;
use serde_json;
use serde_xml_rs;
use std::error;
use std::fmt;
use std::io;
use std::path::Path;
use std::path::PathBuf;


#[derive(Debug)]
pub enum Error {
    InvalidPath(PathBuf, String),
    Io(io::Error),
    JsonConversion(serde_json::Error),
    News(news::Error),
    Reqwest(reqwest::Error),
    XmlParsing(serde_xml_rs::Error),
}

impl Error {
    pub fn invalid_path(path: &Path) -> Error {
        Error::InvalidPath(path.to_path_buf(), path.to_string_lossy().to_string())
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            Error::InvalidPath(_, ref string) => write!(f, "Invalid path: {}", string),
            Error::Io(ref error) => write!(f, "IO error: {}", error),
            Error::JsonConversion(ref error) => write!(f, "JSON conversion error: {}", error),
            Error::News(ref error) => write!(f, "News error: {}", error),
            Error::Reqwest(ref error) => write!(f, "Reqwest error: {}", error),
            Error::XmlParsing(ref error) => write!(f, "XML parsing error: {}", error),
        }
    }
}

impl error::Error for Error {
    fn source(&self) -> Option<&(dyn error::Error + 'static)> {
        match *self {
            Error::InvalidPath(_, _) => None,
            Error::Io(ref error) => Some(error),
            Error::JsonConversion(ref error) => Some(error),
            Error::News(ref error) => Some(error),
            Error::Reqwest(ref error) => Some(error),
            Error::XmlParsing(ref error) => Some(error),
        }
    }
}
