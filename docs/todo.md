# To Do

- extractor error after adding reddit

    /Users/donmcc/.pyenv/versions/news-venv/bin/python /Users/donmcc/Developer/Don/donm_cc/news/src/extractor.py --cache-dir=tmp 
    INFO:botocore.credentials:Found credentials in shared credentials file: ~/.aws/credentials
    WARNING:news.url:Value Error parsing "TupleSpace": bad query field: 'TupleSpace'
    INFO:extractor.py:Added 24 and removed 1 items.

    {
        "url": "http://wiki.c2.com/?TupleSpace",
        "title": "Tuple Space",
        "source": {
            "url": "https://news.ycombinator.com/item?id=35741416",
            "site_id": "hn"
        },
        "created": "2023-04-28T14:25:03.968685+00:00",
        "modified": "2023-04-28T14:25:03.968685+00:00"
    },
 
    
    Process finished with exit code 0

- sf.streetsblog, no title

        {
			"url": "https://sf.streetsblog.org/2023/04/24/423264/",
			"title": "",
			"source": {
				"url": "https://sf.streetsblog.org/2023/04/24/423264/",
				"site_id": "sb"
			},
			"created": "2023-04-24T16:10:04.637352+00:00",
			"modified": "2023-04-24T16:10:04.637352+00:00"
		},

- shared block list between hacker news and reddit
- about page
- medium blog post
  - https://blog.medium.com/now-you-can-embed-mastodon-posts-in-medium-stories-99b11d0baa7f
- AWS site
  - http://reasoning-machines.s3-website.ca-central-1.amazonaws.com/
- handle wayback machine URLs
  - https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm
  - http://web.archive.org/web/20180516153837/http://www.adreca.net/NAND-Flash-Data-Recovery-Cookbook.pdf
  - https://web.archive.org/web/20081225064415/http://pcmcia.org/
  - https://web.archive.org/web/20150516094013/http://www.the-tls.co.uk/tls/public/article1555487.ece
  - https://web.archive.org/web/20160304085903/http://thestartuptoolkit.com/blog/2011/10/the_coffeeshop_fallacy/
  - https://web.archive.org/web/20180101160950/https://squid314.livejournal.com/324957.html
  - https://web.archive.org/web/20230314015249/https://twitter.com/vxunderground/status/1635427567271329792
- get YouTube user from YouTube URL
  - youtube.com/@kevinsyoza from https://www.youtube.com/watch?v=LGUR3YmYA8s
        <span itemprop="author" itemscope itemtype="http://schema.org/Person">
            <link itemprop="url" href="http://www.youtube.com/@allones3078">
            <link itemprop="name" content="All Ones">
        </span>
  - https://www.youtube.com/@cgtimemachine1257/videos
  - https://www.youtube.com/playlist?list=PL3GWPKM6L17H0RyU2o7p9gCnepjSTaHia
- public suffix list https://publicsuffix.org
- `docked` - Python alternative to `Dockerfile` https://github.com/orsinium-labs/docked
- should fragments be allowed in URLs?
  - https://sr.ht/~icefox/oorandom/#a-brief-history-of-random-numbers
- special handling for archive.org
  - https://ia601707.us.archive.org/28/items/gov.uscourts.cand.364454/gov.uscourts.cand.364454.385.0.pdf
- transform `keep_entry()` method into a score and bubble the score up
- change `News.add_new() to take (items, now) instead of news`
- split `modified` into `items_added` and `items_removed`
- json responses
- add container smoke test
- statsd and datadog 
- where should `query.py` live?
- improve AWS permissions to read/write S3 bucket
- make page footer sticky to the window
- Cache wraps Store and Cache write on first `get()`
- ecr container versioning
- unify command line options and ENV
- ENV variable to control logging level
- link rewriting
  - reddit links to old reddit
  - cnn to https://lite.cnn.com/en
  - npr to https://text.npr.org
    - https://text.npr.org/1165680024
    - https://www.npr.org/2023/03/23/1165680024/perennial-rice-plant-once-harvest-again-and-again
    - https://text.npr.org/1162588784
    - https://www.npr.org/sections/health-shots/2023/03/15/1162588784/the-peoples-hospital-ricardo-nuila-treats-mostly-uninsured-undocumented
    - https://text.npr.org/542238978
    - https://www.npr.org/sections/thetwo-way/2017/08/08/542238978/-financial-times-issues-103-year-old-correction
  - https://www.nytimes.com/timeswire
  - https://youtubetranscript.com
  - https://threadreaderapp.com
  - pay walls to https://archive.ph
    - https://archive.vn/rsxDl --> archive.today --> source site
    - wsj
    - economist
- filter / search news
  - by domain name
  - by keywords
