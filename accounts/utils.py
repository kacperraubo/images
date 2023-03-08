"""
Filename: tests.py
Author: Kacper Raubo
Creation date: 03/08/2023

Provides utilities for the rest of the code.
"""

from urllib.parse import urlencode, urlparse, urlunparse
from datetime import datetime, timedelta

def generate_expiring_link(url, seconds):
    parsed_url = urlparse(url)
    query_params = parsed_url.query
    query_dict = dict(urlencode(query_params, doseq=True))
    expires = datetime.now() + timedelta(seconds=seconds)
    query_dict['expires'] = expires.timestamp()
    query_params = urlencode(query_dict)
    new_url_parts = (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, query_params, parsed_url.fragment)
    return urlunparse(new_url_parts)
