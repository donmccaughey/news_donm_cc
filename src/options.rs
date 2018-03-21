use std::path::PathBuf;


#[derive(Serialize, Deserialize, Debug)]
pub struct Options {
    pub out_dir: PathBuf,

    pub news_path: PathBuf,
    pub rss_xml_path: PathBuf,
    pub rss_json_path: PathBuf,
}

impl Options {
    pub fn new() -> Options {
        let out_dir = PathBuf::from("./tmp");
        Options {
            news_path: out_dir.join("news.json"),
            rss_xml_path: out_dir.join("rss.xml"),
            rss_json_path: out_dir.join("rss.json"),
            out_dir: out_dir,
        }
    }
}
