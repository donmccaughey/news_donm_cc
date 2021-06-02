#[macro_use]
extern crate serde_derive;

extern crate chrono;
extern crate serde;
extern crate serde_json;
extern crate url;
extern crate url_serde;


mod error;
mod news;
mod story;


pub use crate::error::Error;
pub use crate::news::News;
pub use crate::story::Story;
