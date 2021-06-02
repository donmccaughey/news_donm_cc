use hyper;
use native_tls;
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
    Hyper(hyper::Error),
    News(news::Error),
    Tls(native_tls::Error),
    Uri(hyper::error::UriError),
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
            Error::Hyper(ref error) => write!(f, "Hyper error: {}", error),
            Error::News(ref error) => write!(f, "News error: {}", error),
            Error::Tls(ref error) => write!(f, "TLS error: {}", error),
            Error::Uri(ref error) => write!(f, "URI error: {}", error),
            Error::XmlParsing(ref error) => write!(f, "XML parsing error: {}", error),
        }
    }
}

impl error::Error for Error {
    fn cause(&self) -> Option<&dyn error::Error> {
        match *self {
            Error::InvalidPath(_, _) => None,
            Error::Io(ref error) => Some(error),
            Error::JsonConversion(ref error) => Some(error),
            Error::Hyper(ref error) => Some(error),
            Error::News(ref error) => Some(error),
            Error::Tls(ref error) => Some(error),
            Error::Uri(ref error) => Some(error),
            Error::XmlParsing(ref error) => Some(error),
        }
    }
}
