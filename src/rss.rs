use chrono::DateTime;
use chrono::Utc;
use rfc_2822_format;
use serde_json;
use std::error::Error;
use std::fmt;
use std::fs::create_dir_all;
use std::fs::OpenOptions;
use std::io;
use std::io::Write;
use std::path::Path;
use std::path::PathBuf;
use url::Url;
use url_serde;


#[derive(Debug)]
pub enum RSSError {
    InvalidPath(PathBuf, String),
    IoError(io::Error),
    JSONConversionError(serde_json::Error),
}

impl RSSError {
    fn invalid_path(path: &Path) -> RSSError {
        RSSError::InvalidPath(path.to_path_buf(), path.to_string_lossy().to_string())
    }
}

impl fmt::Display for RSSError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            RSSError::InvalidPath(_, ref string) => write!(f, "Invalid path: {}", string),
            RSSError::IoError(ref error) => write!(f, "IO error: {}", error),
            RSSError::JSONConversionError(ref error) => write!(f, "JSON conversion error: {}", error),
        }
    }
}

impl Error for RSSError {
    fn description(&self) -> &str {
        match *self {
            RSSError::InvalidPath(_, ref string) => &string,
            RSSError::IoError(ref error) => error.description(),
            RSSError::JSONConversionError(ref error) => error.description(),
        }
    }
}


#[derive(Debug, Deserialize, Serialize)]
pub struct RSS {
    pub channel: Channel,
}

impl RSS {
    pub fn write(&self, path: &Path) -> Result<(), RSSError> {
        match path.parent() {
            Some(parent) => create_dir_all(parent).map_err(RSSError::IoError)?,
            None => return Err(RSSError::invalid_path(path)),
        };
        let json = serde_json::to_string_pretty(self)
            .map_err(RSSError::JSONConversionError)?;
        let mut file = OpenOptions::new()
            .create(true).truncate(true).write(true)
            .open(path).map_err(RSSError::IoError)?;
        file.write_all(json.as_bytes())
            .map_err(RSSError::IoError)
    }
}


#[derive(Debug, Deserialize, Serialize)]
pub struct Channel {
    pub description: String,
    #[serde(rename = "item")]
    pub items: Vec<Item>,
    #[serde(with = "url_serde")]
    pub link: Url,
    pub title: String,
}


#[derive(Debug, Deserialize, Serialize)]
pub struct Item {
    #[serde(with = "url_serde")]
    pub comments: Url,
    pub description: String,
    #[serde(with = "url_serde")]
    pub link: Url,
    #[serde(rename = "pubDate", with = "rfc_2822_format")]
    pub pub_date: DateTime<Utc>,
    pub title: String,
}
