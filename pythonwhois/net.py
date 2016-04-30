from codecs import encode, decode

from pythonwhois.exceptions import WhoisException

import socket, sys
import re


def get_whois_raw(domain, server="", previous=None, rfc3490=True, never_cut=False, with_server_list=False,
                  server_list=None, ignore_referral_servers=False):
    previous = previous or []
    server_list = server_list or []

    # The exceptions list has been integrated into the tld_zones.csv

    if rfc3490:  # This deals with encoding the WHOIS response/query
        if sys.version_info < (3, 0):
            domain = encode(domain if type(domain) is unicode else decode(domain, "utf8"), "idna")
        else:
            domain = encode(domain, "idna").decode("ascii")

    if not previous and not server:
        # They're looking up a root zone ('com')
        target_server = get_root_server(domain)
    else:
        # They're looking up a normal domain name
        target_server = server

        # Handle the EXAMPLE.COM case
        if domain.lower().strip() == 'example.com':
            target_server = 'whois.verisign-grs.com'

    # We apply options to specific servers here
    if target_server == "whois.jprs.jp":
        # Suppress Japanese output
        request_domain = "%s/e" % domain
    elif domain.endswith(".de") and (target_server == "whois.denic.de" or target_server == "de.whois-servers.net"):
        # Specific regional stuff
        request_domain = "-T dn,ace %s" % domain
    elif target_server == "whois.verisign-grs.com":
        request_domain = "=%s" % domain  # Avoid partial matches
    else:
        # It's a normal domain, no options
        request_domain = domain

    response = whois_request(request_domain, target_server)

    if never_cut:
        # If the caller has requested to 'never cut' responses, he will get the original response from the server (this is
        # useful for callers that are only interested in the raw data). Otherwise, if the target is verisign-grs, we will
        # select the data relevant to the requested domain, and discard the rest, so that in a multiple-option response the
        # parsing code will only touch the information relevant to the requested domain. The side-effect of this is that
        # when `never_cut` is set to False, any verisign-grs responses in the raw data will be missing header, footer, and
        # alternative domain options (this is handled a few lines below, after the verisign-grs processing).
        new_list = [response] + previous

    if target_server == "whois.verisign-grs.com":
        # VeriSign is a little... special. As it may return multiple full records and there's no way to do an exact query,
        # we need to actually find the correct record in the list.
        for record in response.split("\n\n"):
            if re.search("Domain Name: %s\n" % domain.upper(), record):
                response = record
                break

    if never_cut == False:
        new_list = [response] + previous

    server_list.append(target_server)

    # Ignore redirects from registries who publish the registrar data themselves, or if the user disables it
    # using the 'ignore_referral_servers' parameter.
    if not ignore_referral_servers and target_server not in ('whois.nic.xyz',):
        referral_match = re.compile(
            r"(refer|whois server|referral url|whois server|registrar whois):\s*([^\s]+\.[^\s]+)", re.IGNORECASE)

        for line in [x.strip() for x in response.splitlines()]:
            match = re.match(referral_match, line)

            if match is not None:
                referral_server = match.group(2)

                # We want to ignore anything non-WHOIS (eg. HTTP) for now.
                if referral_server != server and "://" not in referral_server:

                    # Referral to another WHOIS server...
                    # NOTE: Pass ignore_referral_servers=True to stop infinite loops
                    return get_whois_raw(domain, referral_server, new_list, server_list=server_list,
                                         with_server_list=with_server_list, ignore_referral_servers=True)

    if with_server_list:
        return (new_list, server_list)
    else:
        return new_list


def get_root_server(domain):
    data = whois_request(domain, "whois.iana.org")
    for line in [x.strip() for x in data.splitlines()]:
        match = re.match("refer:\s*([^\s]+)", line)
        if match is None:
            continue
        return match.group(1)
    raise WhoisException("No root WHOIS server found for domain.")


def whois_request(domain, server, port=43):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    sock.send(("%s\r\n" % domain).encode("utf-8"))
    buff = b""
    while True:
        data = sock.recv(1024)
        if len(data) == 0:
            break
        buff += data
    return buff.decode("utf-8", "replace")
