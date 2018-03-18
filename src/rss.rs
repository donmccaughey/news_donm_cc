use chrono::{DateTime, Utc};
use rfc_2822_format;
use url::Url;
use url_serde;


#[derive(Serialize, Deserialize, Debug)]
pub struct RSS {
    pub channel: Channel,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Channel {
    pub description: String,
    #[serde(rename = "item")]
    pub items: Vec<Item>,
    #[serde(with = "url_serde")]
    pub link: Url,
    pub title: String,
}

#[derive(Serialize, Deserialize, Debug)]
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
