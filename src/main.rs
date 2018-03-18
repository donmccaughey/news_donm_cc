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


mod options;
mod rfc_2822_format;
mod rss;
mod story;


use chrono::{Duration, Utc};
use futures::Stream;
use hyper::Client;
use hyper_tls::HttpsConnector;
use options::Options;
use rss::RSS;
use std::collections::HashSet;
use std::error::Error;
use std::fs::{create_dir_all, OpenOptions};
use std::io;
use std::io::Write;
use std::path::Path;
use story::Story;
use tokio_core::reactor::Core;


fn get_url(url_string: &str) -> Result<hyper::Chunk, hyper::Error> {
    let uri = url_string.parse()?;

    let mut core = Core::new().unwrap();

    let handle = core.handle();
    let connector = HttpsConnector::new(4, &handle).unwrap();
    let client = Client::configure()
        .connector(connector)
        .build(&handle);

    let response = core.run(client.get(uri))?;
    core.run(response.body().concat2())
}

fn write_chunk(chunk: &hyper::Chunk, path: &Path) -> Result<(), io::Error> {
    let mut file = OpenOptions::new()
        .create(true).truncate(true).write(true)
        .open(path)?;
    file.write_all(chunk.as_ref())
}

fn main() {
    let options = Options::new();

    match create_dir_all(&options.stories_dir) {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}", error.description());
            return;
        }
    }

    // read stories JSON from file
    let stories_path = options.stories_dir.join("stories.json");
    let saved_stories = match Story::read_all(&stories_path) {
        Ok(saved_stories) => saved_stories,
        Err(error) => {
            eprintln!("ERROR: {}: {}", stories_path.display(), error.description());
            return;
        }
    };

    let chunk = match get_url("https://news.ycombinator.com/rss") {
        Ok(chunk) => chunk,
        Err(error) => {
            eprintln!("ERROR: {}", error.description());
            return;
        }
    };

    // write RSS XML to file
    let rss_xml_path = options.stories_dir.join("rss.xml");
    match write_chunk(&chunk, &rss_xml_path) {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}: {}", rss_xml_path.display(), error.description());
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
    let rss_json_path = options.stories_dir.join("rss.json");
    match rss.write(&rss_json_path) {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}: {}", rss_json_path.display(), error.description());
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

    let stories_path = options.stories_dir.join("stories.json");
    match Story::write_all(&updated_stories, &stories_path) {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}: {}", stories_path.display(), error.description());
            return;
        }
    };
}
