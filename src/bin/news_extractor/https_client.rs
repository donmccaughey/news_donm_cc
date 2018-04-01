use futures::Stream;
use hyper::Body;
use hyper::Chunk;
use hyper::Client;
use hyper::client::HttpConnector;
use hyper_tls::HttpsConnector;
use news::error::NewsError;
use std::fs::create_dir_all;
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;
use tokio_core::reactor::Core;


pub fn get_url(url_string: &str) -> Result<Chunk, NewsError> {
    let mut https_client = HttpsClient::new()?;
    https_client.get(url_string)
}

pub fn write_chunk(chunk: &Chunk, path: &Path) -> Result<(), NewsError> {
    match path.parent() {
        Some(parent) => create_dir_all(parent).map_err(NewsError::IoError)?,
        None => return Err(NewsError::invalid_path(path)),
    };
    let mut file = OpenOptions::new()
        .create(true).truncate(true).write(true)
        .open(path).map_err(NewsError::IoError)?;
    file.write_all(chunk.as_ref()).map_err(NewsError::IoError)
}


#[derive(Debug)]
pub struct HttpsClient {
    core: Core,
    client: Client<HttpsConnector<HttpConnector>, Body>,
}

impl HttpsClient {
    pub fn new() -> Result<HttpsClient, NewsError> {
        let core = Core::new().map_err(NewsError::IoError)?;
        let handle = core.handle();
        let connector = HttpsConnector::new(4, &handle).map_err(NewsError::TlsError)?;
        let client = Client::configure().connector(connector).build(&handle);
        Ok(
            HttpsClient {
                core: core,
                client: client,
            }
        )
    }

    pub fn get(&mut self, url_string: &str) -> Result<Chunk, NewsError> {
        let uri = url_string.parse().map_err(NewsError::UriError)?;
        let response = self.core.run(self.client.get(uri)).map_err(NewsError::HyperError)?;
        self.core.run(response.body().concat2()).map_err(NewsError::HyperError)
    }
}
