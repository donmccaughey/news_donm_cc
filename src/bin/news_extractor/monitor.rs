use crate::options::Options;
use news::Story;


pub struct Monitor<'a> {
    options: &'a Options,
}

impl<'a> Monitor<'a> {
    pub fn new(options: &Options) -> Monitor {
        Monitor {
            options: options,
        }
    }

    pub fn added_stories(&self, stories: &[Story]) {
        let count = stories.len();
        println!("news:{}: Found {} new {}", self.options.now_date, count, story_noun(count));
        print_stories(stories);
    }

    pub fn expired_stories(&self, stories: &[Story]) {
        let count = stories.len();
        println!("news:{}: Removed {} expired {}", self.options.now_date, count, story_noun(count));
        print_stories(stories);
    }
}


fn print_stories(stories: &[Story]) {
    for story in stories.iter() {
        println!("    - {}", story.title);
    }
}

fn story_noun(count: usize) -> &'static str {
    if count == 1 { "story" } else { "stories" }
}
