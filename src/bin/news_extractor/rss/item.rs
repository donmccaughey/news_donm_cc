use chrono::DateTime;
use chrono::Utc;
use news::Story;
use rfc_2822_format;
use url::Url;
use url_serde;


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

impl Item {
    pub fn to_story(&self, created_date: DateTime<Utc>) -> Story {
        Story {
            comments: self.comments.clone(),
            created_date: created_date.clone(),
            link: self.link.clone(),
            pub_date: self.pub_date.clone(),
            title: self.title.clone(),
        }
    }
}


#[cfg(test)]
mod tests {
    use serde_xml_rs;
    use super::*;

    #[test]
    fn test_item_to_story() {
        let pub_date = DateTime::parse_from_rfc2822("Wed, 21 Mar 2018 22:33:19 +0000")
            .unwrap().with_timezone(&Utc);
        let item = Item {
            comments: Url::parse("https://example.com/comments").unwrap(),
            description: "Some stuff happened.".to_string(),
            link: Url::parse("https://example.com/link").unwrap(),
            pub_date: pub_date,
            title: "A News Story".to_string(),
        };
        let created_date = DateTime::parse_from_rfc2822("Thu, 22 Mar 2018 13:08:18 +0000")
            .unwrap().with_timezone(&Utc);
        let story = item.to_story(created_date);
        assert_eq!(item.comments, story.comments);
        assert_eq!(created_date, story.created_date);
        assert_eq!(item.link, story.link);
        assert_eq!(item.pub_date, story.pub_date);
        assert_eq!(item.title, story.title);
    }

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
}
