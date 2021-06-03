#[macro_use]
extern crate serde_derive;


mod error;
mod monitor;
mod options;
mod rfc_2822_format;
mod rss;


use crate::error::Error;
use monitor::Monitor;
use news::News;
use options::Options;
use rss::Rss;
use std::fs::create_dir_all;
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;


pub fn write_file(bytes: &[u8], path: &Path) -> Result<(), Error> {
    match path.parent() {
        Some(parent) => create_dir_all(parent).map_err(Error::Io)?,
        None => return Err(Error::invalid_path(path)),
    };
    let mut file = OpenOptions::new()
        .create(true).truncate(true).write(true)
        .open(path).map_err(Error::Io)?;
    file.write_all(bytes).map_err(Error::Io)
}


fn main() -> Result<(), error::Error> {
    let options = Options::new();
    let monitor = Monitor::new(&options);

    let mut response = reqwest::blocking::get("https://news.ycombinator.com/rss")
        .map_err(Error::Reqwest)?;
    let mut buffer: Vec<u8> = vec![];
    response.copy_to(&mut buffer).map_err(Error::Reqwest)?;
    write_file(&buffer, &options.rss_xml_path)?;

    let rss: Rss = serde_xml_rs::from_reader(&*buffer)
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
