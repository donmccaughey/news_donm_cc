from textwrap import dedent


def not_found(_e):
    html = dedent(
        '''
        <!doctype html>
        <html lang=en>
        <link rel=icon href=data:,>
        <meta charset=utf-8>
        <title>News</title>
        <p>404 Not found.
        '''
    ).strip()
    return html, 404
