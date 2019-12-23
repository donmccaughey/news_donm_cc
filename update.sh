cp tmp/news.json wwwroot/data/news.json
aws s3 cp \
    wwwroot/data/news.json \
    s3://news.donm.cc/data/news.json \
    --acl public-read \

