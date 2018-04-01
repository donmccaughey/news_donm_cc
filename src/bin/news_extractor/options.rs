use chrono::{DateTime, Duration, Utc};
use std::path::PathBuf;


#[derive(Serialize, Deserialize, Debug)]
pub struct Options {
    pub out_dir: PathBuf,

    pub news_path: PathBuf,
    pub rss_json_path: PathBuf,
    pub rss_xml_path: PathBuf,

    pub now_date: DateTime<Utc>,
    pub expired_date: DateTime<Utc>,
}

impl Options {
    pub fn new() -> Options {
        let out_dir = PathBuf::from("./tmp");
        let now = Utc::now();

        Options {
            out_dir: out_dir.clone(),

            news_path: out_dir.join("news.json"),
            rss_json_path: out_dir.join("rss.json"),
            rss_xml_path: out_dir.join("rss.xml"),

            now_date: now,
            expired_date: now - Duration::days(30),
        }
    }
}
