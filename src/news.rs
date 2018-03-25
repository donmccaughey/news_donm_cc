use chrono::DateTime;
use chrono::Utc;
use news_error::NewsError;
use rss::Item;
use serde_json;
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


#[derive(Debug, Deserialize, Serialize)]
pub struct News {
    pub stories: Vec<Story>,
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

impl News {
    pub fn read_from(path: &Path) -> Result<News, NewsError> {
        let stories = Story::read_all(path)?;
        Ok(News {
            stories: stories,
        })
    }

    pub fn write_to(&self, path: &Path) -> Result<(), NewsError> {
        Story::write_all(&self.stories, path)
    }
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

    pub fn read_all(path: &Path) -> Result<Vec<Story>, NewsError> {
        let file = match File::open(path) {
            Ok(file) => file,
            Err(ref error) if NotFound == error.kind() => return Ok(Vec::new()),
            Err(error) => return Err(NewsError::IoError(error)),
        };
        serde_json::from_reader(file)
            .map_err(NewsError::JsonParsingError)
    }

    pub fn write_all(stories: &[Story], path: &Path) -> Result<(), NewsError> {
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
        self.comments == other.comments
    }
}


#[cfg(test)]
mod tests {
    use chrono::DateTime;
    use chrono::Utc;
    use rss::Item;
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    use super::*;
    use url::Url;

    impl Story {
        fn hash_code(&self) -> u64 {
            let mut hasher = DefaultHasher::new();
            self.hash(&mut hasher);
            hasher.finish()
        }
    }

    #[test]
    fn test_story_from_item() {
        let pub_date = DateTime::parse_from_rfc2822("Wed, 21 Mar 2018 22:33:19 +0000")
            .unwrap().with_timezone(&Utc);
        let item = Item {
            comments: Url::parse("https://example.com/comments").unwrap(),
            description: "Some stuff happened.".to_string(),
            link: Url::parse("https://example.com/link").unwrap(),
            pub_date: pub_date,
            title: "A News Story".to_string(),
        };
        let created_date = DateTime::parse_from_rfc2822("Thu, 22 Mar 2018 13:08:18 +0000")
            .unwrap().with_timezone(&Utc);
        let story = Story::from_item(&item, created_date);
        assert_eq!(item.comments, story.comments);
        assert_eq!(created_date, story.created_date);
        assert_eq!(item.link, story.link);
        assert_eq!(item.pub_date, story.pub_date);
        assert_eq!(item.title, story.title);
    }

    #[test]
    fn test_story_eq() {
        let url1 = Url::parse("https://example.com/one").unwrap();
        let url2 = Url::parse("https://example.com/two").unwrap();

        let date1 = DateTime::parse_from_rfc2822("Wed, 21 Mar 2018 22:33:19 +0000")
            .unwrap().with_timezone(&Utc);
        let date2 = DateTime::parse_from_rfc2822("Thu, 22 Mar 2018 01:59:58 +0000")
            .unwrap().with_timezone(&Utc);

        let story1 = Story {
            comments: url1.clone(),
            created_date: date1.clone(),
            link: url1.clone(),
            pub_date: date1.clone(),
            title: "Some Title".to_string(),
        };
        let mut story2 = story1.clone();

        assert_eq!(story1, story2);
        assert_eq!(story2, story1);
        assert_eq!(story1.hash_code(), story2.hash_code());

        story2.title = "Another Title".to_string();

        assert_eq!(story1, story2);
        assert_eq!(story2, story1);
        assert_eq!(story1.hash_code(), story2.hash_code());

        story2.pub_date = date2.clone();

        assert_eq!(story1, story2);
        assert_eq!(story2, story1);
        assert_eq!(story1.hash_code(), story2.hash_code());

        story2.link = url2.clone();

        assert_eq!(story1, story2);
        assert_eq!(story2, story1);
        assert_eq!(story1.hash_code(), story2.hash_code());

        story2.created_date = date2.clone();

        assert_eq!(story1, story2);
        assert_eq!(story2, story1);
        assert_eq!(story1.hash_code(), story2.hash_code());

        story2 = story1.clone();
        story2.comments = url2;

        assert_ne!(story1, story2);
        assert_ne!(story2, story1);
        assert_ne!(story1.hash_code(), story2.hash_code());
    }
}
