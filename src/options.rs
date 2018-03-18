use std::path::PathBuf;


#[derive(Serialize, Deserialize, Debug)]
pub struct Options {
    pub stories_dir: PathBuf,
}

impl Options {
    pub fn new() -> Options {
        Options {
            stories_dir: PathBuf::from("./tmp"),
        }
    }
}
