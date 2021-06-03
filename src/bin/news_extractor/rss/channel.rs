use super::Item;
use url::Url;
use url_serde;


#[derive(Debug, Deserialize, Serialize)]
pub struct Channel {
    pub description: String,
    #[serde(rename = "item")]
    pub items: Vec<Item>,
    #[serde(with = "url_serde")]
    pub link: Url,
    pub title: String,
}


#[cfg(test)]
mod tests {
    use serde_xml_rs;
    use super::*;

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
        let channel: Channel = serde_xml_rs::from_reader(xml.as_bytes()).unwrap();
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
}
