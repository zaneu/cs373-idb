import bs4


def check_if_str(x):
    """
    returns if the element is a BeautifulSoup string
    this is useful for filtering the entries given
    """

    return type(x) is bs4.element.NavigableString or \
            type(x) is str or \
            type(x) is unicode


def remove_whitespace_from_listing(listing):
    """
    removes all whitespace from a listing (tag)
    """
    
    if check_if_str(listing):
        value = listing.strip()
        return value if value else None

    values = map(lambda x: x.strip() if check_if_str(x) else x, listing)
    values = filter(lambda x: x, values)

    return values


def values_from_listing(listing):
    """
    returns a list of strings representing values in a table
    listing must be a bs4 Tag element
    """

    values = filter(check_if_str, listing.contents)
    values = map(str, values)
    values = map(lambda x: x.strip(), values)
    values = filter(lambda x: x, values)

    return values


def string_from_listing(listing):
    """
    condenses the listing into a string
    """

    if check_if_str(listing):
        return listing

    if listing.string:
        return listing.string

    return "".join(string_from_listing(value) for value in listing.contents)


