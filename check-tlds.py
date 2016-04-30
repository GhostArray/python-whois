#!/usr/bin/env python

# This script will do an IANA lookup for a list of TLDs, and compare the
# response of IANA to the WHOIS server in the list. IANA does not appear to be
# aware of all the new TLDs yet, so this is a quick way to check what TLDs need
# an exception in the WHOIS lookup code.

import sys
import pythonwhois
import csv


def main():
    first_line = True

    # Obtained from https://domainpunch.com/tlds/ (1,293 zones)
    with open('./data/tld_zones.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            # We use the following values:
            #   [0] = Running Total
            #   [5] = The punycode version of the IDN (what we want)
            #   [6] = The WHOIS server

            # Skip the first line (which contains headings)
            if first_line:
                first_line = False

                continue

            if len(row) < 6:  # Nope
                continue

            tld = row[5]
            server = row[6]

            domain = 'domain.{}'.format(tld)

            try:
                root_server = pythonwhois.net.get_root_server(domain)

                if root_server.strip() != server.strip():
                    print("[ERR] WHOIS server doesn't match for '.{}'! List indicates '{}', IANA said '{}'."
                          .format(tld, server, root_server))

                    sys.exit(1)
            except Exception:
                print "[ERR] Unknown WHOIS server for '.{}'! List indicates '{}'.".format(tld, server)

                sys.exit(1)

            print u'[OK ] IANA and list agree that the WHOIS server for \'.{}\' is \'{}\'.'.format(tld, root_server)


if __name__ == '__main__':
    main()
