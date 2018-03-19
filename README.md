# news_donm_cc

Source code for my personal news aggregation site.
Coming soon to [https://news.donm.cc](https://news.donm.cc).

## Architecture

The _news.donm.cc_ is driven by three main components: 
an **extractor**, an HTTP **server** and an HTML **client** 
using JavaScript and CSS to provide 
[progressive enhancement](https://en.wikipedia.org/wiki/Progressive_enhancement).

The **extractor** process is run periodically by a cron job.
It polls news sources for new links, organizing them and saving them in a JSON file on the server.

The HTTP **server** generates the HTML **client** files and serves up the static assets.

The HTML **client** provides a core hypertext application to navigate the
list of aggregated news links.
Progressive enhancement using CSS and JavaScript provides 
improved usability for more capable browsers.  

## Technology

The **extractor** and HTTP **server** are written in [Rust](https://www.rust-lang.org/).
The HTML **client** is written in XHTML 4.01, CSS and JavaScript. 

## License

The code behind _news.donm.cc_ is made available under a BSD-style license; see the LICENSE file for details.