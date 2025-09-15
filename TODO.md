# To Do

- debug duplicate items
		{
			"url": "https://modelcontextprotocol.io/specification/2025-06-18",
			"url_identity": "modelcontextprotocol.io",
			"title": "MCP Specification - 2025-06-18",
			"sources": [
				{
					"url": "https://lobste.rs/s/agsbxp/mcp_specification_2025_06_18",
					"site_id": "lob",
					"count": 1
				}
			],
			"created": "2025-06-19T01:10:03.060164+00:00",
			"modified": "2025-06-19T01:10:03.060164+00:00",
			"seq_id": 71505
		},
		{
			"url": "https://modelcontextprotocol.io/specification/2025-06-18",
			"url_identity": "modelcontextprotocol.io",
			"title": "MCP Specification \u2013 2025-06-18",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44314289",
					"site_id": "hn",
					"count": 8
				},
				{
					"url": "https://lobste.rs/s/agsbxp/mcp_specification_2025_06_18",
					"site_id": "lob",
					"count": 26
				}
			],
			"created": "2025-06-19T01:10:03.060164+00:00",
			"modified": "2025-06-19T01:10:03.060164+00:00",
			"seq_id": 71506
		},
		{
			"url": "https://modelcontextprotocol.io/specification/2025-06-18/changelog",
			"url_identity": "modelcontextprotocol.io",
			"title": "MCP Specification \u2013 version 2025-06-18 changes",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44314289",
					"site_id": "hn",
					"count": 157
				}
			],
			"created": "2025-06-19T01:50:03.260011+00:00",
			"modified": "2025-06-19T01:50:03.260011+00:00",
			"seq_id": 71509
		},

- why do some old daringfireball items reappear?
		{
			"url": "https://daringfireball.net/linked/2025/06/07/bill-atkinson-rip",
			"url_identity": "daringfireball.net",
			"title": "Bill Atkinson Dies From Cancer at 74",
			"sources": [
				{
					"url": "https://daringfireball.net/linked/2025/06/07/bill-atkinson-rip",
					"site_id": "df",
					"count": 10
				}
			],
			"created": "2025-06-22T18:55:03.455357+00:00",
			"modified": "2025-06-22T18:55:03.455357+00:00",
			"seq_id": 72182
		},

- check of neuters.de has fixed captcha issue with Reuters API
  - https://github.com/HookedBehemoth/neuters/issues/42
- figure out how to check package versions in `pyproject.toml` against apk versions
  - https://pkgs.alpinelinux.org/packages
- paginate the `/sites` page
- understand how requests handles redirects
  - Update `Feed.get_items()` to detect redirects correctly
- support patterns in `SKIP_SITES`
- support filtering out items that only appear briefly 
  - `Source` supports a count of times it's been seen and a `visible` flag
  - subclass `Source` to calculate `visible` based on source site criteria
    (e.g. count > 3 for hn & r, any count for blogs)
  - add `visible` property to `Item` that aggregates `visible` flags from `Source`s
  - add `visible_items` property to `News` to iterate over visible items
- inconsistent `FLASK_CACHE_DIR="$(TMP)"` vs `--cache-dir="$(TMP)"`
- update item title when item changes
  - keep a history of item titles
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
- public suffix list https://publicsuffix.org
- should fragments be allowed in URLs? yes!
  - https://sr.ht/~icefox/oorandom/#a-brief-history-of-random-numbers
- special handling for archive.org
  - https://ia601707.us.archive.org/28/items/gov.uscourts.cand.364454/gov.uscourts.cand.364454.385.0.pdf
- transform `keep_entry()` method into a score and bubble the score up
- change `News.add_new() to take (items, now) instead of news`
- split `modified` into `items_added` and `items_removed`
- add container smoke test
- where should `query.py` live?
- improve AWS permissions to read/write S3 bucket
- make `S3Store` and other `Store` classes general purpose 
- Cache wraps Store and Cache write on first `read()`
- ecr container versioning
- unify command line options and ENV
- ENV variable to control logging level
- search
  - include search box on search page, prefilled with query
  - include "found n of m items" on search page as `.page-info`
  - paginate search results
  - include domain name
    - full domains (`daringfireball.net`)
    - partial domains('daringfireball')
- sites page
  - include links back to main page
  - don't open individual site pages in new tab
- how to deal with Hacker News changing URLs for items?
        {
			"url": "https://www.wsj.com/opinion/rfk-jr-hhs-moves-to-restore-public-trust-in-vaccines-45495112",
			"url_identity": "wsj.com",
			"title": "RFK Jr.: HHS Moves to Restore Public Trust in Vaccines",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44229533",
					"site_id": "hn",
					"count": 48
				}
			],
			"created": "2025-06-10T02:40:02.933802+00:00",
			"modified": "2025-06-10T02:40:02.933802+00:00",
			"seq_id": 69832
		},
		{
			"url": "https://www.nbcnews.com/health/health-news/kennedy-guts-acip-cdc-vaccine-panel-rcna211935",
			"url_identity": "nbcnews.com",
			"title": "Kennedy guts CDC's vaccine panel of independent experts",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44229533",
					"site_id": "hn",
					"count": 6
				}
			],
			"created": "2025-06-09T21:35:03.349180+00:00",
			"modified": "2025-06-09T21:35:03.349180+00:00",
			"seq_id": 69796
		},

		{
			"url": "https://www.theguardian.com/world/live/2025/jun/12/air-india-flight-ai171-plane-crash-ahmedabad-india-latest-updates",
			"url_identity": "theguardian.com",
			"title": "Air India flight to London crashes in Ahmedabad with more than 240 onboard",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44255602",
					"site_id": "hn",
					"count": 88
				}
			],
			"created": "2025-06-12T11:55:03.536138+00:00",
			"modified": "2025-06-12T11:55:03.536138+00:00",
			"seq_id": 70277
		},
		{
			"url": "https://economictimes.indiatimes.com/news/india/plane-crashes-near-ahmedabad-airport-smoke-seen-emanating-from-adani-airport-premises/articleshow/121798578.cms?from=mdr",
			"url_identity": "economictimes.indiatimes.com",
			"title": "Air India passenger plane with over 200 onboard crashes near Meghaninagar",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44255602",
					"site_id": "hn",
					"count": 7
				}
			],
			"created": "2025-06-12T11:20:03.443754+00:00",
			"modified": "2025-06-12T11:20:03.443754+00:00",
			"seq_id": 70271
		},

		{
			"url": "https://github.com/oils-for-unix/oils.vim/blob/main/doc/algorithms.md",
			"url_identity": "github.com/oils-for-unix",
			"title": "Three Algorithms for YSH Syntax Highlighting",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44265216",
					"site_id": "hn",
					"count": 152
				}
			],
			"created": "2025-06-13T04:00:03.651157+00:00",
			"modified": "2025-06-13T04:00:03.651157+00:00",
			"seq_id": 70420
		},
		{
			"url": "https://codeberg.org/oils/oils.vim/src/branch/main/doc/algorithms.md",
			"url_identity": "codeberg.org/oils",
			"title": "Three Algorithms for YSH Syntax Highlighting",
			"sources": [
				{
					"url": "https://lobste.rs/s/n8gpfg/three_algorithms_for_ysh_syntax",
					"site_id": "lob",
					"count": 158
				},
				{
					"url": "https://news.ycombinator.com/item?id=44265216",
					"site_id": "hn",
					"count": 8
				}
			],
			"created": "2025-06-13T02:25:02.842840+00:00",
			"modified": "2025-06-13T02:25:02.842840+00:00",
			"seq_id": 70411
		},

		{
			"url": "https://modelcontextprotocol.io/specification/2025-06-18/changelog",
			"url_identity": "modelcontextprotocol.io",
			"title": "MCP Specification \u2013 version 2025-06-18 changes",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44314289",
					"site_id": "hn",
					"count": 157
				}
			],
			"created": "2025-06-19T01:50:03.260011+00:00",
			"modified": "2025-06-19T01:50:03.260011+00:00",
			"seq_id": 71509
		},
		{
			"url": "https://modelcontextprotocol.io/specification/2025-06-18",
			"url_identity": "modelcontextprotocol.io",
			"title": "MCP Specification \u2013 2025-06-18",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44314289",
					"site_id": "hn",
					"count": 8
				},
				{
					"url": "https://lobste.rs/s/agsbxp/mcp_specification_2025_06_18",
					"site_id": "lob",
					"count": 26
				}
			],
			"created": "2025-06-19T01:10:03.060164+00:00",
			"modified": "2025-06-19T01:10:03.060164+00:00",
			"seq_id": 71506
		},

		{
			"url": "https://www.lemonde.fr/en/science/article/2025/06/21/gwada-negative-french-scientists-find-new-blood-type-in-woman_6742577_10.html",
			"url_identity": "lemonde.fr",
			"title": "A new blood type discovered in France: \"Gwada negative\", a global exception",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44335517",
					"site_id": "hn",
					"count": 239
				}
			],
			"created": "2025-06-21T15:25:02.769856+00:00",
			"modified": "2025-06-21T15:25:02.769856+00:00",
			"seq_id": 71986
		},
		{
			"url": "https://entrevue.fr/en/un-groupe-sanguin-inedit-decouvert-en-france-gwada-negatif-une-exception-mondiale/",
			"url_identity": "entrevue.fr",
			"title": "A new blood type discovered in France: \"Gwada negative\", a global exception",
			"sources": [
				{
					"url": "https://news.ycombinator.com/item?id=44335517",
					"site_id": "hn",
					"count": 52
				}
			],
			"created": "2025-06-21T10:45:02.761390+00:00",
			"modified": "2025-06-21T10:45:02.761390+00:00",
			"seq_id": 71940
		},
