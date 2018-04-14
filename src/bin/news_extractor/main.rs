#[macro_use]
extern crate serde_derive;

extern crate chrono;
extern crate futures;
extern crate hyper;
extern crate hyper_tls;
extern crate native_tls;
extern crate news;
extern crate serde;
extern crate serde_json;
extern crate serde_xml_rs;
extern crate tokio_core;
extern crate url;
extern crate url_serde;


mod error;
mod https_client;
mod monitor;
mod options;
mod rfc_2822_format;
mod rss;


use monitor::Monitor;
use news::News;
use options::Options;
use rss::Rss;
use std::error::Error;


fn main() {
    match run() {
        Ok(_) => (),
        Err(error) => {
            eprintln!("ERROR: {}", error.description());
        }
    }
}

fn run() -> Result<(), error::Error> {
    let options = Options::new();
    let monitor = Monitor::new(&options);

    let chunk = https_client::get_url("https://news.ycombinator.com/rss")?;
    https_client::write_chunk(&chunk, &options.rss_xml_path)?;

    let rss: Rss = serde_xml_rs::deserialize(chunk.as_ref())
        .map_err(error::Error::XmlParsing)?;
    rss.write(&options.rss_json_path)?;

    let mut news = News::read_from(&options.news_path)
        .map_err(error::Error::News)?;

    let new_stories = news.add_stories(&rss.create_stories(options.now_date));
    monitor.added_stories(&new_stories);

    let expired_stories = news.expire_stories(options.expired_date);
    monitor.expired_stories(&expired_stories);

    if new_stories.len() > 0 || expired_stories.len() > 0 {
        news.modified_date = options.now_date.clone();
        news.write_to(&options.news_path)
            .map_err(error::Error::News)
    } else {
        Ok(())
    }
}
