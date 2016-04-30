from .net import get_whois_raw
from .parse import parse_raw_whois
from .exceptions import WhoisException


def get_whois(domain, normalized=None):
    """
    Gets WHOIS information for a domain name.

    :param domain: The domain name
    :param normalized: A list of data to be normalized
    """

    normalized = normalized or []

    raw_data, server_list = get_whois_raw(domain, with_server_list=True)

    # Unlisted handles will be looked up on the last WHOIS server that was queried. This may be changed to also query
    # other servers in the future, if it turns out that there are cases where the last WHOIS server in the chain doesn't
    # actually hold the handle contact details, but another WHOIS server in the chain does.
    return parse_raw_whois(raw_data, normalized=normalized, never_query_handles=False, handle_server=server_list[-1])
