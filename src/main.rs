#[macro_use]
extern crate serde_derive;

extern crate futures;
extern crate hyper;
extern crate hyper_tls;
extern crate native_tls;
extern crate serde;
extern crate serde_xml_rs;
extern crate tokio_core;


use std::io::{self, Write};
use futures::Stream;
use hyper::Client;
use hyper_tls::HttpsConnector;
use tokio_core::reactor::Core;


#[derive(Deserialize, Debug)]
struct RSSFeed {
    channel: Channel,
}

#[derive(Deserialize, Debug)]
struct Channel {
    title: String,
    link: String,
    description: String,
    #[serde(rename = "item")]
    items: Vec<Item>,
}

#[derive(Deserialize, Debug)]
struct Item {
    title: String,
    link: String,
    #[serde(rename = "pubDate")]
    pub_date: String,
    comments: String,
    description: String,
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
}
