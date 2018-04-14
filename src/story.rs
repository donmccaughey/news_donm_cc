use chrono::DateTime;
use chrono::Utc;
use std::cmp::Ordering;
use std::hash::Hash;
use std::hash::Hasher;
use url::Url;
use url_serde;


#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct Story {
    #[serde(with = "url_serde")]
    pub comments: Url,
    pub created_date: DateTime<Utc>,
    pub id: u32,
    #[serde(with = "url_serde")]
    pub link: Url,
    pub pub_date: DateTime<Utc>,
    pub title: String,
}

impl Story {
    pub fn standard_order(a: &Story, b: &Story) -> Ordering {
        a.created_date.cmp(&b.created_date).reverse()
            .then(a.pub_date.cmp(&b.pub_date).reverse())
            .then(a.title.cmp(&b.title))
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
    use chrono::TimeZone;
    use chrono::Utc;
    use std::collections::hash_map::DefaultHasher;
    use std::hash::Hash;
    use std::hash::Hasher;
    use super::*;
    use url::Url;

    impl Story {
        pub fn new(id: &str, create_day: u32, pub_day: u32) -> Story {
            Story {
                comments: Url::parse(&format!("https://comments.example.com/{}", id)).unwrap(),
                created_date: Utc.yo(2018, create_day).and_hms(0, 0, 0),
                id: 42,
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
    fn test_story_created_pub_title_order() {
        let story101 = Story::new("101", 101, 101);
        let story101dup = Story::new("101", 101, 101);
        assert_eq!(Ordering::Equal, Story::standard_order(&story101, &story101dup));

        let story102 = Story::new("102", 102, 102);
        assert_eq!(Ordering::Less, Story::standard_order(&story102, &story101));
        assert_eq!(Ordering::Greater, Story::standard_order(&story101, &story102));

        let story102pub99 = Story::new("102", 102, 99);
        assert_eq!(Ordering::Less, Story::standard_order(&story102, &story102pub99));
        assert_eq!(Ordering::Greater, Story::standard_order(&story102pub99, &story102));

        let story_a = Story::new("A", 103, 103);
        let story_b = Story::new("B", 103, 103);
        assert_eq!(Ordering::Less, Story::standard_order(&story_a, &story_b));
        assert_eq!(Ordering::Greater, Story::standard_order(&story_b, &story_a));
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
            id: 42,
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
