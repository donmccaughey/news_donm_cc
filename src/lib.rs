#[macro_use]
extern crate serde_derive;


mod error;
mod news;
mod story;


pub use crate::error::Error;
pub use crate::news::News;
pub use crate::story::Story;
