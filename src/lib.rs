#[macro_use]
extern crate serde_derive;

extern crate chrono;
extern crate serde;
extern crate serde_json;
extern crate url;
extern crate url_serde;


use chrono::DateTime;
use chrono::Utc;
use std::cmp::Ordering;
use std::collections::HashSet;
use std::error;
use std::fmt;
use std::fmt::Display;
use std::fs::create_dir_all;
use std::fs::File;
use std::fs::OpenOptions;
use std::io;
use std::io::ErrorKind::NotFound;
use std::io::Write;
use std::hash::Hash;
use std::hash::Hasher;
use std::path::Path;
use std::path::PathBuf;
use url::Url;


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
    pub fn read_from(path: &Path) -> Result<News, Error> {
        let stories = Story::read_all(path)?;
        Ok(News {
            stories: stories,
        })
    }

    pub fn add_stories(&mut self, stories: &[Story]) -> Vec<Story> {
        let mut stories_added: Vec<Story>;
        {
            let new_set: HashSet<&Story> = stories.iter().collect();
            let old_set: HashSet<&Story> = self.stories.iter().collect();
            let difference = new_set.difference(&old_set);
            stories_added = difference.cloned().cloned().collect();
        }
        self.stories.extend(stories_added.iter().cloned());
        self.stories.sort_by(Story::created_pub_title_order);
        stories_added.sort_by(Story::created_pub_title_order);
        stories_added
    }

    pub fn expire_stories(&mut self, expired_date: DateTime<Utc>) -> Vec<Story> {
        let i = match self.stories.binary_search_by(|ref story| story.created_date.cmp(&expired_date).reverse()) {
            Ok(i) => i,
            Err(i) => i,
        };
        self.stories.drain(i..).collect()
    }

    pub fn write_to(&self, path: &Path) -> Result<(), Error> {
        Story::write_all(&self.stories, path)
    }
}


impl Story {
    pub fn created_pub_title_order(a: &Story, b: &Story) -> Ordering {
        a.created_date.cmp(&b.created_date).reverse()
            .then(a.pub_date.cmp(&b.pub_date).reverse())
            .then(a.title.cmp(&b.title))
    }

    pub fn read_all(path: &Path) -> Result<Vec<Story>, Error> {
        let file = match File::open(path) {
            Ok(file) => file,
            Err(ref error) if NotFound == error.kind() => return Ok(Vec::new()),
            Err(error) => return Err(Error::Io(error)),
        };
        serde_json::from_reader(file)
            .map_err(Error::JsonParsing)
    }

    pub fn write_all(stories: &[Story], path: &Path) -> Result<(), Error> {
        match path.parent() {
            Some(parent) => create_dir_all(parent).map_err(Error::Io)?,
            None => return Err(Error::invalid_path(path)),
        };
        let json = serde_json::to_string_pretty(stories)
            .map_err(Error::JsonConversion)?;
        let mut file = OpenOptions::new()
            .create(true).truncate(true).write(true)
            .open(path).map_err(Error::Io)?;
        file.write_all(json.as_bytes())
            .map_err(Error::Io)
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

impl error::Error for Error {
    fn description(&self) -> &str {
        match *self {
            Error::InvalidPath(_, ref string) => &string,
            Error::Io(ref error) => error.description(),
            Error::JsonConversion(ref error) => error.description(),
            Error::JsonParsing(ref error) => error.description(),
        }
    }

    fn cause(&self) -> Option<&error::Error> {
        match *self {
            Error::InvalidPath(_, _) => None,
            Error::Io(ref error) => Some(error),
            Error::JsonConversion(ref error) => Some(error),
            Error::JsonParsing(ref error) => Some(error),
        }
    }
}


#[cfg(test)]
mod tests {
    use chrono::DateTime;
    use chrono::TimeZone;
    use chrono::Utc;
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    use super::*;
    use url::Url;

    impl News {
        fn new() -> News {
            News {
                stories: Vec::new(),
            }
        }
    }

    impl Story {
        fn new(id: &str, create_day: u32, pub_day: u32) -> Story {
            Story {
                comments: Url::parse(&format!("https://comments.example.com/{}", id)).unwrap(),
                created_date: Utc.yo(2018, create_day).and_hms(0, 0, 0),
                link: Url::parse(&format!("https://link.example.com/{}", id)).unwrap(),
                pub_date: Utc.yo(2018, pub_day).and_hms(0, 0, 0),
                title: format!("Story {}", id),
            }
        }

        fn hash_code(&self) -> u64 {
            let mut hasher = DefaultHasher::new();
            self.hash(&mut hasher);
            hasher.finish()
        }
    }

    #[test]
    fn test_news_add_stories() {
        let mut news = News::new();

        // add zero stories
        let stories_added = news.add_stories(&[]);

        assert_eq!(0, news.stories.len());
        assert_eq!(0, stories_added.len());

        // add one story
        let story101 = Story::new("101", 101, 101);
        let stories_added = news.add_stories(&[ story101 ]);

        assert_eq!(1, news.stories.len());
        assert_eq!("Story 101", news.stories[0].title);

        assert_eq!(1, stories_added.len());
        assert_eq!("Story 101", stories_added[0].title);

        // add one new and one duplicate story
        let story101dup = Story::new("101", 101, 101);
        let story102 = Story::new("102", 102, 102);
        let stories_added = news.add_stories(&[ story101dup, story102 ]);

        assert_eq!(2, news.stories.len());
        assert_eq!("Story 102", news.stories[0].title);
        assert_eq!("Story 101", news.stories[1].title);

        assert_eq!(1, stories_added.len());
        assert_eq!("Story 102", stories_added[0].title);

        // add three new stories and verify sort order
        let story103 = Story::new("103", 103, 103);
        let story100 = Story::new("100", 100, 100);
        let story104 = Story::new("104", 104, 104);
        let stories_added = news.add_stories(&[ story103, story100, story104 ]);

        assert_eq!(5, news.stories.len());
        assert_eq!("Story 104", news.stories[0].title);
        assert_eq!("Story 103", news.stories[1].title);
        assert_eq!("Story 102", news.stories[2].title);
        assert_eq!("Story 101", news.stories[3].title);
        assert_eq!("Story 100", news.stories[4].title);

        assert_eq!(3, stories_added.len());
        assert_eq!("Story 104", stories_added[0].title);
        assert_eq!("Story 103", stories_added[1].title);
        assert_eq!("Story 100", stories_added[2].title);
    }

    #[test]
    fn test_news_expire_stories() {
        let mut news = News::new();

        let story100 = Story::new("100", 100, 100);
        let story101 = Story::new("101", 101, 101);
        let story102 = Story::new("102", 102, 102);
        let story103 = Story::new("103", 103, 103);
        let story104 = Story::new("104", 104, 104);

        let story107 = Story::new("107", 107, 107);
        let story108 = Story::new("108", 108, 108);
        let stories_added = news.add_stories(&[
            story100, story101, story102, story103, story104,
            story107, story108,
            ]);

        assert_eq!(7, news.stories.len());
        assert_eq!("Story 108", stories_added[0].title);
        assert_eq!("Story 100", stories_added[6].title);

        // expired date exactly matches a created date

        let expired102 = Utc.yo(2018, 102).and_hms(0, 0, 0);
        let expired_stories = news.expire_stories(expired102);

        assert_eq!(3, expired_stories.len());
        assert_eq!("Story 102", expired_stories[0].title);
        assert_eq!("Story 101", expired_stories[1].title);
        assert_eq!("Story 100", expired_stories[2].title);

        assert_eq!(4, news.stories.len());
        assert_eq!("Story 108", news.stories[0].title);
        assert_eq!("Story 107", news.stories[1].title);
        assert_eq!("Story 104", news.stories[2].title);
        assert_eq!("Story 103", news.stories[3].title);

        // expired date does not match a created date

        let expired105 = Utc.yo(2018, 105).and_hms(0, 0, 0);
        let expired_stories = news.expire_stories(expired105);

        assert_eq!(2, expired_stories.len());
        assert_eq!("Story 104", expired_stories[0].title);
        assert_eq!("Story 103", expired_stories[1].title);

        assert_eq!(2, news.stories.len());
        assert_eq!("Story 108", news.stories[0].title);
        assert_eq!("Story 107", news.stories[1].title);
    }

    #[test]
    fn test_story_created_pub_title_order() {
        let story101 = Story::new("101", 101, 101);
        let story101dup = Story::new("101", 101, 101);
        assert_eq!(Ordering::Equal, Story::created_pub_title_order(&story101, &story101dup));

        let story102 = Story::new("102", 102, 102);
        assert_eq!(Ordering::Less, Story::created_pub_title_order(&story102, &story101));
        assert_eq!(Ordering::Greater, Story::created_pub_title_order(&story101, &story102));

        let story102pub99 = Story::new("102", 102, 99);
        assert_eq!(Ordering::Less, Story::created_pub_title_order(&story102, &story102pub99));
        assert_eq!(Ordering::Greater, Story::created_pub_title_order(&story102pub99, &story102));

        let story_a = Story::new("A", 103, 103);
        let story_b = Story::new("B", 103, 103);
        assert_eq!(Ordering::Less, Story::created_pub_title_order(&story_a, &story_b));
        assert_eq!(Ordering::Greater, Story::created_pub_title_order(&story_b, &story_a));
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
