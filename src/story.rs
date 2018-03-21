use chrono::DateTime;
use chrono::Utc;
use news_error::NewsError;
use rss::Item;
use serde_json;
use std::collections::HashSet;
use std::fs::create_dir_all;
use std::fs::File;
use std::fs::OpenOptions;
use std::io::ErrorKind::NotFound;
use std::io::Write;
use std::hash::Hash;
use std::hash::Hasher;
use std::path::Path;
use url::Url;
use url_serde;


#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct Story {
    #[serde(with = "url_serde")]
    pub comments: Url,
    pub created_date: DateTime<Utc>,
    #[serde(with = "url_serde")]
    pub link: Url,
    pub pub_date: DateTime<Utc>,
    pub title: String,
}

impl Story {
    pub fn from_item(item: &Item, created_date: DateTime<Utc>) -> Story {
        Story {
            comments: item.comments.clone(),
            created_date: created_date.clone(),
            link: item.link.clone(),
            pub_date: item.pub_date.clone(),
            title: item.title.clone(),
        }
    }

    pub fn read_all(path: &Path) -> Result<HashSet<Story>, NewsError> {
        let file = match File::open(path) {
            Ok(file) => file,
            Err(ref error) if NotFound == error.kind() => return Ok(HashSet::new()),
            Err(error) => return Err(NewsError::IoError(error)),
        };
        serde_json::from_reader(file)
            .map_err(NewsError::JsonParsingError)
    }

    pub fn write_all(stories: &[&Story], path: &Path) -> Result<(), NewsError> {
        match path.parent() {
            Some(parent) => create_dir_all(parent).map_err(NewsError::IoError)?,
            None => return Err(NewsError::invalid_path(path)),
        };
        let json = serde_json::to_string_pretty(stories)
            .map_err(NewsError::JsonConversionError)?;
        let mut file = OpenOptions::new()
            .create(true).truncate(true).write(true)
            .open(path).map_err(NewsError::IoError)?;
        file.write_all(json.as_bytes())
            .map_err(NewsError::IoError)
    }
}

impl Eq for Story {}

impl Hash for Story {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.comments.hash(state);
    }
}

impl PartialEq for Story {
    fn eq(&self, other: &Story) -> bool {
        self.comments.as_str() == other.comments.as_str()
    }
}
