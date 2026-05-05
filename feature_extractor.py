import re
from urllib.parse import urlparse


def extract_features(url):
    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname else ''

    features = {}

    features['length_url'] = len(url)
    features['length_hostname'] = len(hostname)

    features['ip'] = 1 if re.match(
        r'^\d{1,3}(\.\d{1,3}){3}$',
        hostname
    ) else 0

    features['nb_dots'] = url.count('.')
    features['nb_hyphens'] = url.count('-')
    features['nb_at'] = url.count('@')
    features['nb_qm'] = url.count('?')
    features['nb_and'] = url.count('&')
    features['nb_eq'] = url.count('=')
    features['nb_underscore'] = url.count('_')
    features['nb_percent'] = url.count('%')
    features['nb_slash'] = url.count('/')
    features['nb_colon'] = url.count(':')

    features['nb_www'] = url.lower().count('www')
    features['nb_com'] = url.lower().count('.com')

    features['https_token'] = 1 if url.startswith('https') else 0

    digits = sum(c.isdigit() for c in url)
    features['ratio_digits_url'] = digits / len(url) if len(url) else 0

    if hostname:
        subdomains = hostname.count('.') - 1
        if hostname.startswith('www.'):
            subdomains -= 1
        features['nb_subdomains'] = max(0, subdomains)
    else:
        features['nb_subdomains'] = 0

    return features