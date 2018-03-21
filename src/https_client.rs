use futures::Stream;
use hyper::Body;
use hyper::Chunk;
use hyper::Client;
use hyper::client::HttpConnector;
use hyper_tls::HttpsConnector;
use news_error::NewsError;
use tokio_core::reactor::Core;


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
