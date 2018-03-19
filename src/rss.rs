use chrono::DateTime;
use chrono::Utc;
use news_error::NewsError;
use rfc_2822_format;
use serde_json;
use std::fs::create_dir_all;
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;
use url::Url;
use url_serde;


#[derive(Debug, Deserialize, Serialize)]
pub struct RSS {
    pub channel: Channel,
}

impl RSS {
    pub fn write(&self, path: &Path) -> Result<(), NewsError> {
        match path.parent() {
            Some(parent) => create_dir_all(parent).map_err(NewsError::IoError)?,
            None => return Err(NewsError::invalid_path(path)),
        };
        let json = serde_json::to_string_pretty(self)
            .map_err(NewsError::JSONConversionError)?;
        let mut file = OpenOptions::new()
            .create(true).truncate(true).write(true)
            .open(path).map_err(NewsError::IoError)?;
        file.write_all(json.as_bytes())
            .map_err(NewsError::IoError)
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
