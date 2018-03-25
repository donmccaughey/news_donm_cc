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
mod news_error;
mod options;
mod rfc_2822_format;
mod rss;


use chrono::{DateTime, Duration, Utc};
use news::News;
use news::Story;
use news_error::NewsError;
use options::Options;
use rss::RSS;
use std::error::Error;
use std::fs::{create_dir_all, OpenOptions};
use std::io::Write;
use std::path::Path;


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

fn write_chunk(chunk: &hyper::Chunk, path: &Path) -> Result<(), NewsError> {
    match path.parent() {
        Some(parent) => create_dir_all(parent).map_err(NewsError::IoError)?,
        None => return Err(NewsError::invalid_path(path)),
    };
    let mut file = OpenOptions::new()
        .create(true).truncate(true).write(true)
        .open(path).map_err(NewsError::IoError)?;
    file.write_all(chunk.as_ref()).map_err(NewsError::IoError)
}

fn main() {
    let options = Options::new();

    // read news JSON from file
    let mut news = match News::read_from(&options.news_path) {
        Ok(stories) => stories,
        Err(error) => {
            eprintln!("ERROR: {}: {}", options.news_path.display(), error.description());
            return;
        }
    };

    let chunk = match https_client::get_url("https://news.ycombinator.com/rss") {
        Ok(chunk) => chunk,
        Err(error) => {
            eprintln!("ERROR: {}", error.description());
            return;
        }
    };

    // write RSS XML to file
    match write_chunk(&chunk, &options.rss_xml_path) {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}: {}", options.rss_xml_path.display(), error.description());
            return;
        }
    };

    // parse RSS XML
    let rss: RSS = match serde_xml_rs::deserialize(chunk.as_ref()) {
        Ok(rss) => rss,
        Err(error) => {
            eprintln!("ERROR: {}", error.description());
            return;
        }
    };

    // write RSS JSON to file
    match rss.write(&options.rss_json_path) {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}: {}", options.rss_json_path.display(), error.description());
            return;
        }
    };

    // turn RSS items into stories
    let now = Utc::now();
    let rss_stories: Vec<Story> = rss.channel.items.iter()
        .map(|item| Story::from_item(&item, now))
        .collect();

    let new_stories = news.add_stories(&rss_stories);
    log_stories(Event::Added, &new_stories, now);

    let expired_date = now - Duration::days(30);

    let expired_stories = news.expire_stories(expired_date);
    log_stories(Event::Expired, &expired_stories, now);

    match news.write_to(&options.news_path) {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}: {}", options.news_path.display(), error.description());
            return;
        }
    };
}
