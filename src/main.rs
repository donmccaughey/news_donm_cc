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


use chrono::{DateTime, Duration, Utc};
use futures::Stream;
use hyper::Client;
use hyper_tls::HttpsConnector;
use std::collections::HashSet;
use std::error::Error;
use std::fs::{create_dir_all, File, OpenOptions};
use std::hash::{Hash, Hasher};
use std::io::Write;
use std::path::PathBuf;
use tokio_core::reactor::Core;


mod rfc_2822_format {
    use chrono::{DateTime, Utc};
    use serde::{self, Deserialize, Serializer, Deserializer};

    pub fn serialize<S>(date: &DateTime<Utc>, serializer: S) -> Result<S::Ok, S::Error>
        where S: Serializer
    {
        serializer.serialize_str(&date.to_rfc2822())
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<DateTime<Utc>, D::Error>
        where D: Deserializer<'de>
    {
        let string = String::deserialize(deserializer)?;
        match DateTime::parse_from_rfc2822(&string) {
            Ok(datetime) => Ok(datetime.with_timezone(&Utc)),
            Err(error) => Err(serde::de::Error::custom(error)),
        }
    }
}


#[derive(Serialize, Deserialize, Debug)]
struct Options {
    stories_dir: PathBuf,
}

impl Options {
    fn new() -> Options {
        Options {
            stories_dir: PathBuf::from("./tmp"),
        }
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
    #[serde(rename = "pubDate", with = "rfc_2822_format")]
    pub_date: DateTime<Utc>,
    title: String,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Story {
    #[serde(with = "url_serde")]
    comments: url::Url,
    created_date: DateTime<Utc>,
    #[serde(with = "url_serde")]
    link: url::Url,
    pub_date: DateTime<Utc>,
    title: String,
}

impl Story {
    fn from_item(item: &Item, created_date: DateTime<Utc>) -> Story {
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


fn main() {
    let options = Options::new();

    match create_dir_all(&options.stories_dir) {
        Ok(_) => (),
        Err(error) => {
            println!("ERROR: {}", error.description());
            return;
        }
    }

    // read stories JSON to file
    let stories_path = options.stories_dir.join("stories.json");
    let saved_stories: HashSet<Story> = match File::open(&stories_path) {
        Ok(mut stories_file) => {
            match serde_json::from_reader(stories_file) {
                Ok(saved_stories) => saved_stories,
                Err(error) => {
                    println!("ERROR: {}: {}", stories_path.display(), error.description());
                    return;
                }
            }
        },
        Err(error) => {
            println!("ERROR: {}: {}", stories_path.display(), error.description());
            HashSet::new()
        }
    };

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
        Ok(body_chunk) => body_chunk,
        Err(error) => {
            println!("ERROR: {}", error.description());
            return;
        }
    };

    let body_bytes = body_chunk.as_ref();

    // write RSS XML to file
    let rss_xml_path = options.stories_dir.join("rss.xml");
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
    let rss_json_path = options.stories_dir.join("rss.json");
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
    let created_date = Utc::now();
    let rss_stories: HashSet<Story> = rss.channel.items
        .iter()
        .map(|item| Story::from_item(&item, created_date))
        .collect();

    let difference = rss_stories.difference(&saved_stories);
    let mut new_stories: Vec<&Story> = difference.collect();
    let new_count = new_stories.len();
    let new_word = if new_count == 1 { "story" } else { "stories" };
    println!("news:{}: Found {} new {}", Utc::now(), new_count, new_word);
    for story in new_stories.iter() {
        println!("    - {}", story.title);
    }

    let expired_date = created_date + Duration::days(30);
    let expired_stories: Vec<&Story> = saved_stories.iter()
        .filter(|story| story.created_date >= expired_date)
        .collect();
    let expired_count = expired_stories.len();
    let expired_word = if expired_count == 1 { "story" } else { "stories" };
    println!("news:{}: Removed {} expired {}", Utc::now(), expired_count, expired_word);
    for story in expired_stories.iter() {
        println!("    - {}", story.title);
    }

    let mut updated_stories: Vec<&Story> = saved_stories.iter()
        .filter(|story| story.created_date < expired_date)
        .collect();
    updated_stories.append(&mut new_stories);

    updated_stories.sort_by(|a, b| {
        a.created_date.cmp(&b.created_date).reverse()
            .then(a.pub_date.cmp(&b.pub_date).reverse())
            .then(a.title.cmp(&b.title))
    });

    // convert stories to JSON
    let updated_stories_json = match serde_json::to_string_pretty(&updated_stories) {
        Ok(updated_stories_json) => updated_stories_json,
        Err(error) => {
            println!("ERROR: {}", error.description());
            return;
        }
    };

    // write stories JSON to file
    let stories_path = options.stories_dir.join("stories.json");
    let mut stories_file = match OpenOptions::new().create(true).truncate(true).write(true).open(&stories_path) {
        Ok(file) => file,
        Err(error) => {
            println!("ERROR: {}: {}", stories_path.display(), error.description());
            return;
        }
    };
    match stories_file.write_all(updated_stories_json.as_bytes()) {
        Ok(_) => (),
        Err(error) => {
            println!("ERROR: {}: {}", stories_path.display(), error.description());
            return;
        }
    };
}
