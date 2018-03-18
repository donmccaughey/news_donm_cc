use chrono::{DateTime, Utc};
use rss::Item;
use std::hash::{Hash, Hasher};
use url::Url;
use url_serde;


#[derive(Serialize, Deserialize, Debug, Clone)]
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
