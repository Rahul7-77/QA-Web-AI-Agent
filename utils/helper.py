import validators
from urllib.parse import urljoin

def is_valid_url(url):
    """ Checks if url passed is a valid url or not """
    return bool(validators.url(url))

def normalize_url(base_url, relative_url):
    """ Converts a relative URL to an absolute URL using a base URL """
    return urljoin(base_url,relative_url.strip())
