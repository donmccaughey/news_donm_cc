use chrono::DateTime;
use chrono::Utc;
use serde_json;
use std::collections::HashSet;
use std::fs::create_dir_all;
use std::fs::File;
use std::fs::OpenOptions;
use std::io::ErrorKind::NotFound;
use std::io::Write;
use std::path::Path;
use super::Error;
use super::Story;


#[derive(Debug, Deserialize, Serialize)]
pub struct News {
    pub stories: Vec<Story>,
}


impl News {
    pub fn new() -> News {
        News {
            stories: Vec::new(),
        }
    }

    pub fn read_from(path: &Path) -> Result<News, Error> {
        let file = match File::open(path) {
            Ok(file) => file,
            Err(ref error) if NotFound == error.kind() => return Ok(News::new()),
            Err(error) => return Err(Error::Io(error)),
        };
        serde_json::from_reader(file)
            .map_err(Error::JsonParsing)
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
        match path.parent() {
            Some(parent) => create_dir_all(parent).map_err(Error::Io)?,
            None => return Err(Error::invalid_path(path)),
        };
        let json = serde_json::to_string_pretty(self)
            .map_err(Error::JsonConversion)?;
        let mut file = OpenOptions::new()
            .create(true).truncate(true).write(true)
            .open(path).map_err(Error::Io)?;
        file.write_all(json.as_bytes())
            .map_err(Error::Io)
    }
}


#[cfg(test)]
mod tests {
    use chrono::TimeZone;
    use chrono::Utc;
    use super::*;

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
}
