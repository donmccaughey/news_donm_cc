use chrono::DateTime;
use chrono::Utc;
use news_error::NewsError;
use rfc_2822_format;
use serde_json;
use std::fs::create_dir_all;
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;
use url::Url;
use url_serde;


#[derive(Debug, Deserialize, Serialize)]
pub struct RSS {
    pub channel: Channel,
}

impl RSS {
    pub fn write(&self, path: &Path) -> Result<(), NewsError> {
        match path.parent() {
            Some(parent) => create_dir_all(parent).map_err(NewsError::IoError)?,
            None => return Err(NewsError::invalid_path(path)),
        };
        let json = serde_json::to_string_pretty(self)
            .map_err(NewsError::JsonConversionError)?;
        let mut file = OpenOptions::new()
            .create(true).truncate(true).write(true)
            .open(path).map_err(NewsError::IoError)?;
        file.write_all(json.as_bytes())
            .map_err(NewsError::IoError)
    }
}


#[derive(Debug, Deserialize, Serialize)]
pub struct Channel {
    pub description: String,
    #[serde(rename = "item")]
    pub items: Vec<Item>,
    #[serde(with = "url_serde")]
    pub link: Url,
    pub title: String,
}


#[derive(Debug, Deserialize, Serialize)]
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


#[cfg(test)]
mod tests {
    use serde_xml_rs;
    use super::*;

    #[test]
    fn test_item_from_xml() {
        let xml = r#"
            <item>\
                <title>Article One</title>\
                <link>https://news.example.com/article1</link>\
                <pubDate>Sun, 18 Mar 2018 23:43:03 +0000</pubDate>\
                <comments>https://news.example.com/article1/comments</comments>\
                <description><![CDATA[<a href="https://news.example.com/article1/comments">Comments</a>]]></description>\
            </item>
        "#;
        let item: Item = serde_xml_rs::deserialize(xml.as_bytes()).unwrap();
        assert_eq!("Article One", item.title);
        assert_eq!("https://news.example.com/article1", item.link.as_str());
        assert_eq!(1521416583, item.pub_date.timestamp());
        assert_eq!("https://news.example.com/article1/comments", item.comments.as_str());
        assert_eq!(r#"<a href="https://news.example.com/article1/comments">Comments</a>"#, item.description);
    }

    #[test]
    fn test_channel_from_xml() {
        let xml = r#"
            <channel>
                <title>News Channel</title>
                <link>https://news.example.com/news_channel</link>
                <description>Better than teevee.</description>
                <item>\
                    <title>Article One</title>\
                    <link>https://news.example.com/article1</link>\
                    <pubDate>Sun, 18 Mar 2018 23:43:03 +0000</pubDate>\
                    <comments>https://news.example.com/article1/comments</comments>\
                    <description><![CDATA[<a href="https://news.example.com/article1/comments">Comments</a>]]></description>\
                </item>
                <item>\
                    <title>Article Two</title>\
                    <link>https://news.example.com/article2</link>\
                    <pubDate>Sun, 18 Mar 2018 13:59:55 +0000</pubDate>\
                    <comments>https://news.example.com/article2/comments</comments>\
                    <description><![CDATA[<a href="https://news.example.com/article2/comments">Comments</a>]]></description>\
                </item>
            </channel>
        "#;
        let channel: Channel = serde_xml_rs::deserialize(xml.as_bytes()).unwrap();
        assert_eq!("News Channel", channel.title);
        assert_eq!("https://news.example.com/news_channel", channel.link.as_str());
        assert_eq!("Better than teevee.", channel.description);
        assert_eq!(2, channel.items.len());

        assert_eq!("Article One", channel.items[0].title);
        assert_eq!("https://news.example.com/article1", channel.items[0].link.as_str());
        assert_eq!(1521416583, channel.items[0].pub_date.timestamp());
        assert_eq!("https://news.example.com/article1/comments", channel.items[0].comments.as_str());
        assert_eq!(r#"<a href="https://news.example.com/article1/comments">Comments</a>"#, channel.items[0].description);

        assert_eq!("Article Two", channel.items[1].title);
        assert_eq!("https://news.example.com/article2", channel.items[1].link.as_str());
        assert_eq!(1521381595, channel.items[1].pub_date.timestamp());
        assert_eq!("https://news.example.com/article2/comments", channel.items[1].comments.as_str());
        assert_eq!(r#"<a href="https://news.example.com/article2/comments">Comments</a>"#, channel.items[1].description);
    }

    #[test]
    fn test_rss_from_xml() {
        let xml = r#"
            <rss version="2.0">
                <channel>
                    <title>News Channel</title>
                    <link>https://news.example.com/news_channel</link>
                    <description>Better than teevee.</description>
                    <item>\
                        <title>Article One</title>\
                        <link>https://news.example.com/article1</link>\
                        <pubDate>Sun, 18 Mar 2018 23:43:03 +0000</pubDate>\
                        <comments>https://news.example.com/article1/comments</comments>\
                        <description><![CDATA[<a href="https://news.example.com/article1/comments">Comments</a>]]></description>\
                    </item>
                </channel>
            </rss>
        "#;
        let rss: RSS = serde_xml_rs::deserialize(xml.as_bytes()).unwrap();
        assert_eq!("News Channel", rss.channel.title);
        assert_eq!("https://news.example.com/news_channel", rss.channel.link.as_str());
        assert_eq!("Better than teevee.", rss.channel.description);
        assert_eq!(1, rss.channel.items.len());

        assert_eq!("Article One", rss.channel.items[0].title);
        assert_eq!("https://news.example.com/article1", rss.channel.items[0].link.as_str());
        assert_eq!(1521416583, rss.channel.items[0].pub_date.timestamp());
        assert_eq!("https://news.example.com/article1/comments", rss.channel.items[0].comments.as_str());
        assert_eq!(r#"<a href="https://news.example.com/article1/comments">Comments</a>"#, rss.channel.items[0].description);
    }
}
