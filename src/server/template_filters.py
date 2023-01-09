from news import Age, Item, URL


def age(item: Item) -> str:
    return ' class=new' if item.age == Age.NEW else ''


# TODO: unify with gen/markup/attributes.py
def href(url: URL) -> str:
    href = str(url)
    if href == '':
        return "''"

    chars = set(href)

    if "'" in chars:
        if '"' in chars:
            href = href.replace('"', '&quot;')
        return f'"{href}"'

    if chars & SPECIAL_CHARS:
        return f"'{href}'"

    return href


# See "ASCII whitespace" in https://infra.spec.whatwg.org/#ascii-whitespace
ASCII_WHITESPACE = {
    '\t',  # tab
    '\n',  # new line
    '\f',  # form feed
    '\r',  # carriage return
    ' ',
}

# See "Unquoted attribute value syntax" in section 13.1.2.3 "Attributes" of
# https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
SPECIAL_CHARS = ASCII_WHITESPACE | {
    '"',
    "'",
    '=',
    '<',
    '>',
    '`',
}
