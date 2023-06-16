# To Do

- `News` object is now frequently `modified` due to item updating and 
    news page "new item" bar doesn't work as intended
- support filtering out items that only appear briefly 
  - `Source` supports a count of times it's been seen and a `visible` flag
  - subclass `Source` to calculate `visible` based on source site criteria
    (e.g. count > 3 for hn & r, any count for blogs)
  - add `visible` property to `Item` that aggregates `visible` flags from `Source`s
  - add `visible_items` property to `News` to iterate over visible items
- remove support for single source from `Item.decode()`
- remove "tn" -> "~n" conversion code from `News.decode()`
- update item title when item changes
  - keep a history of item titles
- about page
- in `Sites.decode()`, implement `Site.decode()` and add a way to update
    each sites in the `Site.sites` list
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
  - cnn to https://lite.cnn.com/en
  - https://youtubetranscript.com
  - https://threadreaderapp.com
  - pay walls to https://archive.ph
    - https://archive.vn/rsxDl --> archive.today --> source site
    - wsj
    - economist
  - Twitter, tweet and sub-tweet media links
    - https://twitter.com/TurnerNovak/status/1654577231937544192
    - https://twitter.com/TurnerNovak/status/1654577231937544192/photo/1
- filter / search news
  - by domain name
  - by keywords
