use error::Error;
use futures::Stream;
use hyper::Body;
use hyper::Chunk;
use hyper::Client;
use hyper::client::HttpConnector;
use hyper_tls::HttpsConnector;
use std::fs::create_dir_all;
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;
use tokio_core::reactor::Core;


pub fn get_url(url_string: &str) -> Result<Chunk, Error> {
    let mut https_client = HttpsClient::new()?;
    https_client.get(url_string)
}

pub fn write_chunk(chunk: &Chunk, path: &Path) -> Result<(), Error> {
    match path.parent() {
        Some(parent) => create_dir_all(parent).map_err(Error::Io)?,
        None => return Err(Error::invalid_path(path)),
    };
    let mut file = OpenOptions::new()
        .create(true).truncate(true).write(true)
        .open(path).map_err(Error::Io)?;
    file.write_all(chunk.as_ref()).map_err(Error::Io)
}


#[derive(Debug)]
pub struct HttpsClient {
    core: Core,
    client: Client<HttpsConnector<HttpConnector>, Body>,
}

impl HttpsClient {
    pub fn new() -> Result<HttpsClient, Error> {
        let core = Core::new().map_err(Error::Io)?;
        let handle = core.handle();
        let connector = HttpsConnector::new(4, &handle).map_err(Error::Tls)?;
        let client = Client::configure().connector(connector).build(&handle);
        Ok(
            HttpsClient {
                core: core,
                client: client,
            }
        )
    }

    pub fn get(&mut self, url_string: &str) -> Result<Chunk, Error> {
        let uri = url_string.parse().map_err(Error::Uri)?;
        let response = self.core.run(self.client.get(uri)).map_err(Error::Hyper)?;
        self.core.run(response.body().concat2()).map_err(Error::Hyper)
    }
}
