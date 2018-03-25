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


mod https_client;
mod news;
mod options;
mod rfc_2822_format;
mod rss;


use chrono::{DateTime, Utc};
use news::News;
use news::Story;
use news::error::NewsError;
use options::Options;
use rss::RSS;
use std::error::Error;


enum Event {
    Added,
    Expired,
}


fn log_stories(event: Event, stories: &[Story], date_time: DateTime<Utc>) {
    let count = stories.len();
    let story_noun = if count == 1 { "story" } else { "stories" };
    match event {
        Event::Added => println!("news:{}: Found {} new {}", date_time, count, story_noun),
        Event::Expired => println!("news:{}: Removed {} expired {}", date_time, count, story_noun),
    };
    for story in stories.iter() {
        println!("    - {}", story.title);
    }
}

fn main() {
    match run() {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}", error.description());
        }
    }
}

fn run() -> Result<(), NewsError> {
    let options = Options::new();

    let mut news = News::read_from(&options.news_path)?;

    let chunk = https_client::get_url("https://news.ycombinator.com/rss")?;
    https_client::write_chunk(&chunk, &options.rss_xml_path)?;

    let rss: RSS = serde_xml_rs::deserialize(chunk.as_ref())
        .map_err(NewsError::XmlParsingError)?;
    rss.write(&options.rss_json_path)?;

    let rss_stories: Vec<Story> = rss.channel.items.iter()
        .map(|item| Story::from_item(&item, options.now_date))
        .collect();

    let new_stories = news.add_stories(&rss_stories);
    log_stories(Event::Added, &new_stories, options.now_date);

    let expired_stories = news.expire_stories(options.expired_date);
    log_stories(Event::Expired, &expired_stories, options.now_date);

    news.write_to(&options.news_path)?;

    Ok(())
}
