aws s3 sync wwwroot s3://news.donm.cc \
    --acl public-read \
    --exclude '.DS_Store' \
    --exclude 'data/*'

