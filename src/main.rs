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
use futures::Stream;
use hyper::Client;
use hyper_tls::HttpsConnector;
use std::io::{self, Write};
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
struct RSSFeed {
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
            println!("ERROR: {:?}", error);
            return;
        }
    };

    let body_chunk = match core.run(response.body().concat2()) {
        Ok(response) => response,
        Err(error) => {
            println!("ERROR: {:?}", error);
            return;
        }
    };

    let body_bytes = body_chunk.as_ref();

    io::stdout().write(body_bytes).unwrap();
    println!("");
    println!("");

    let rss_feed: RSSFeed = serde_xml_rs::deserialize(body_bytes).unwrap();
    println!("channel:");
    println!("    title: {}", rss_feed.channel.title);
    println!("    link: {}", rss_feed.channel.link);
    println!("    description: {}", rss_feed.channel.description);
    println!("    {} items:", rss_feed.channel.items.len());
    println!("");
    for i in 0..rss_feed.channel.items.len() {
        let item = &rss_feed.channel.items[i];
        println!("    {:2}) title: {}", i, item.title);
        println!("        link: {}", item.link);
        println!("        pub_date: {}", item.pub_date);
        println!("        comments: {}", item.comments);
        println!("        description: {}", item.description);
        println!("");
    }

    let mut stories: Vec<Story> = Vec::new();
    for item in rss_feed.channel.items.iter() {
        let story = Story::from_item(&item);
        stories.push(story);
    }

    let stories_json = match serde_json::to_string_pretty(&stories) {
        Ok(stories_json) => stories_json,
        Err(error) => {
            println!("ERROR: {:?}", error);
            return;
        }
    };
    println!("{}", stories_json);
}
