use chrono::{DateTime, Utc};
use rss::Item;
use serde_json;
use std::collections::HashSet;
use std::error::Error;
use std::fmt;
use std::fs::File;
use std::io;
use std::io::ErrorKind::NotFound;
use std::hash::{Hash, Hasher};
use std::path::Path;
use url::Url;
use url_serde;


#[derive(Debug)]
pub enum StoryError {
    IoError(io::Error),
    ParsingError(serde_json::Error),
}

impl fmt::Display for StoryError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.description())
    }
}

impl Error for StoryError {
    fn description(&self) -> &str {
        match *self {
            StoryError::IoError(ref error) => error.description(),
            StoryError::ParsingError(ref error) => error.description(),
        }
    }
}


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

    pub fn read_all(path: &Path) -> Result<HashSet<Story>, StoryError> {
        let file = match File::open(path) {
            Ok(file) => file,
            Err(ref error) if NotFound == error.kind() => return Ok(HashSet::new()),
            Err(error) => return Err(StoryError::IoError(error)),
        };
        serde_json::from_reader(file).map_err(StoryError::ParsingError)
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
