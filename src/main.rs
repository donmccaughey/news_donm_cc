#[macro_use]
extern crate serde_derive;

extern crate chrono;
extern crate futures;
extern crate hyper;
extern crate hyper_tls;
extern crate native_tls;
extern crate serde;
extern crate serde_json;
extern crate serde_xml_rs;
extern crate tokio_core;
extern crate url;
extern crate url_serde;


use chrono::{DateTime, Utc};
use std::error::Error;
use futures::Stream;
use hyper::Client;
use hyper_tls::HttpsConnector;
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;
use tokio_core::reactor::Core;


mod rfc_822_format {
    use chrono::{DateTime, Utc, TimeZone};
    use serde::{self, Deserialize, Serializer, Deserializer};

    // Sun, 11 Mar 2018 00:55:15 +0000
    // day, dd mmm yyyy hh:mm:ss +zzzz
    const FORMAT: &'static str = "%a, %e %b %Y %H:%M:%S %z";

    pub fn serialize<S>(date: &DateTime<Utc>, serializer: S) -> Result<S::Ok, S::Error>
        where S: Serializer
    {
        let s = format!("{}", date.format(FORMAT));
        serializer.serialize_str(&s)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<DateTime<Utc>, D::Error>
        where D: Deserializer<'de>
    {
        let s = String::deserialize(deserializer)?;
        Utc.datetime_from_str(&s, FORMAT).map_err(serde::de::Error::custom)
    }
}


#[derive(Serialize, Deserialize, Debug)]
struct RSS {
    channel: Channel,
}

#[derive(Serialize, Deserialize, Debug)]
struct Channel {
    description: String,
    #[serde(rename = "item")]
    items: Vec<Item>,
    #[serde(with = "url_serde")]
    link: url::Url,
    title: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct Item {
    #[serde(with = "url_serde")]
    comments: url::Url,
    description: String,
    #[serde(with = "url_serde")]
    link: url::Url,
    #[serde(rename = "pubDate", with = "rfc_822_format")]
    pub_date: DateTime<Utc>,
    title: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct Story {
    #[serde(with = "url_serde")]
    comments: url::Url,
    date: DateTime<Utc>,
    #[serde(with = "url_serde")]
    link: url::Url,
    title: String,
}

impl Story {
    fn from_item(item: &Item) -> Story {
        Story {
            comments: item.comments.clone(),
            date: item.pub_date.clone(),
            link: item.link.clone(),
            title: item.title.clone(),
        }
    }
}


fn main() {
    let mut core = Core::new().unwrap();

    let handle = core.handle();
    let connector = HttpsConnector::new(4, &handle).unwrap();
    let client = Client::configure()
        .connector(connector)
        .build(&handle);

    let uri = "https://news.ycombinator.com/rss".parse().unwrap();

    let response = match core.run(client.get(uri)) {
        Ok(response) => response,
        Err(error) => {
            println!("ERROR: {}", error.description());
            return;
        }
    };

    let body_chunk = match core.run(response.body().concat2()) {
        Ok(response) => response,
        Err(error) => {
            println!("ERROR: {}", error.description());
            return;
        }
    };

    let body_bytes = body_chunk.as_ref();

    // write RSS XML to file
    let rss_xml_path = Path::new("rss.xml");
    let mut rss_xml_file = match OpenOptions::new().create(true).write(true).open(&rss_xml_path) {
        Ok(rss_xml_file) => rss_xml_file,
        Err(error) => {
            println!("ERROR: {}: {}", rss_xml_path.display(), error.description());
            return;
        }
    };
    match rss_xml_file.write_all(body_bytes) {
        Ok(_) => (),
        Err(error) => {
            println!("ERROR: {}: {}", rss_xml_path.display(), error.description());
            return;
        }
    };

    // parse RSS XML
    let rss: RSS = match serde_xml_rs::deserialize(body_bytes) {
        Ok(rss) => rss,
        Err(error) => {
            println!("ERROR: {}", error.description());
            return;
        }
    };

    // convert RSS to JSON
    let rss_json = match serde_json::to_string_pretty(&rss) {
        Ok(rss_json) => rss_json,
        Err(error) => {
            println!("ERROR: {}", error.description());
            return;
        }
    };

    // write RSS JSON to file
    let rss_json_path = Path::new("rss.json");
    let mut rss_json_file = match OpenOptions::new().create(true).write(true).open(&rss_json_path) {
        Ok(rss_json_file) => rss_json_file,
        Err(error) => {
            println!("ERROR: {}: {}", rss_json_path.display(), error.description());
            return;
        }
    };

    match rss_json_file.write_all(rss_json.as_bytes()) {
        Ok(_) => (),
        Err(error) => {
            println!("ERROR: {}: {}", rss_json_path.display(), error.description());
            return;
        }
    };

    // turn RSS items into stories
    let mut new_stories: Vec<Story> = Vec::new();
    for item in rss.channel.items.iter() {
        let story = Story::from_item(&item);
        new_stories.push(story);
    }

    // convert stories to JSON
    let new_stories_json = match serde_json::to_string_pretty(&new_stories) {
        Ok(new_stories_json) => new_stories_json,
        Err(error) => {
            println!("ERROR: {}", error.description());
            return;
        }
    };

    // write stories JSON to file
    let stories_path = Path::new("stories.json");
    let mut stories_file = match OpenOptions::new().create(true).write(true).open(&stories_path) {
        Ok(file) => file,
        Err(error) => {
            println!("ERROR: {}: {}", stories_path.display(), error.description());
            return;
        }
    };
    match stories_file.write_all(new_stories_json.as_bytes()) {
        Ok(_) => (),
        Err(error) => {
            println!("ERROR: {}: {}", stories_path.display(), error.description());
            return;
        }
    };
}
