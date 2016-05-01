pythonwhois
===========

[![Build Status](https://travis-ci.org/GhostArray/python-whois.svg?branch=develop)](https://travis-ci.org/GhostArray/python-whois) 
[![Coverage Status](https://coveralls.io/repos/github/GhostArray/python-whois/badge.svg?branch=develop)](https://coveralls.io/github/GhostArray/python-whois?branch=develop)


A Python library for retrieving and parsing WHOIS information.

## Installation

This package is available on **pip**, all you need to do to install it is:

```pip install pythonwhois```

## Instructions

The manual has moved into the GitHub wiki pages, there are also many examples and lots of information and documentation about the APIs.

The old manual (from *doc/*) is available online [here](http://cryto.net/pythonwhois).

## Goals

* Complete output testing, coverage, and documentation
* 100% coverage of all WHOIS server formats.
* Generating accurate and complete data.
* Consistent and performant parsing system

## Features

* WHOIS data retrieval
    * Return raw results
	* Follows WHOIS server redirects
	* Won't get stuck on multiple-result responses from Verisign's servers (try google.com)
	
* WHOIS data parsing
	* Base information (registrar information, contacts, etc.)
	* Dates/times (registration, expiry, ...)
	* EPP status codes
	* **Full registrant information**
	* Nameserver information
* WHOIS data normalization *(optional)*
	* Attempts to intelligently reformat WHOIS data for better accuracy and (human) readability
	* Converts various abbreviation types to full locality names
		* Airport codes
		* Country names (2- and 3-letter ISO codes)
		* US states and territories
		* Canadian states and territories
		* Australian states
	* Identifies both organization and person names, and moves or reformats them where necessary
	* Identifies names where the first and last name are swapped around, and fixes them
	* Deduplicates names, even *across fields*, and even when they're not 100% identical
	* Recognizes common (legal) abbreviations, and ensures that they are in the correct case
* `pwhois`, a CLI WHOIS tool that uses **pythonwhois**
	* Easily readable output format
	* Can also output raw WHOIS data
	* Output as JSON
* Automated testing suite
	* Will detect and warn about any changes in parsed data compared to previous runs
	* Backwards compatibility for old searches and parsers

## Non-Features

### IP Range Lookups

`pythonwhois` does not yet support WHOIS lookups on IP ranges (including single IPs), although this will be added at some point in the future. In the meantime, consider using [`ipwhois`](https://github.com/secynic/ipwhois) - it offers functionality and an API similar to `pythonwhois`, but for IPs. It also supports delegated RWhois.

Do note that `ipwhois` does not offer a normalization feature, and does not (yet) come with a command-line tool. Additionally, `ipwhois` is maintained by Philip Hane and not by me; please make sure to file bugs relating to it in the `ipwhois` repository, not in that of `pythonwhois`.

## Changelog

### 3.0.0 (in development)

Intends to improve the overall code quality, documentation, coverage, and Python 3 compatibility.

This release **will deprecate old methods**, and thus may not be backwards compatible with your code. In version 3.0.0, we have **removed the whois()** function from the `pythonwhois` module. Otherwise, all API methods will remain the same, although they may function differently internally.

### 2.4.0

A lot of changes were made to the normalization, and the performance under Python 2.x was significantly improved. The average parsing time under Python 2.7 has dropped by 94% (!), and on my system averages out at 18ms. Performance under Python 3.x is [unchanged](https://github.com/joepie91/python-whois/issues/27). `pythonwhois` will now expand a lot of abbreviations in normalized mode, such as airport codes, ISO country codes, and US/CA/AU state abbreviations. The consequence of this is that the library is now bigger (as it ships a list of these abbreviations). Also note that there *may* be licensing consequences, in particular regarding the airport code database. More information about that can be found below.

### 2.3.0

Python 3 support was fixed. Creation date parsing for contacts was fixed; correct timestamps will now be returned, rather than unformatted ones - if your application relies on the broken variant, you'll need to change your code. Some additional parameters were added to the `net` and `parse` methods to facilitate NIC handle lookups; the defaults are backwards-compatible, and these changes should not have any consequences for your code. Thai WHOIS parsing was implemented, but is a little spotty - data may occasionally be incorrectly split up. Please submit a bug report if you run across any issues.

### 2.2.0

The internal workings of `get_whois_raw` have been changed, to better facilitate parsing of WHOIS data from registries that may return multiple partial matches for a query, such as `whois.verisign-grs.com`. This change means that, by default, `get_whois_raw` will now strip out the part of such a response that does not pertain directly to the requested domain. If your application requires an unmodified raw WHOIS response and is calling `get_whois_raw` directly, you should use the new `never_cut` parameter to keep pythonwhois from doing this post-processing. As this is a potentially breaking behaviour change, the minor version has been bumped.

## Issues?

* It doesn't work *at all*?
* It doesn't parse the data for a particular domain?
* There's an inaccuracy in parsing the data for a domain, even just a small one?

If any of those apply, don't hesitate to file an issue! Our goal is 100% coverage, and we need your feedback to reach that goal.

## Data sources

This library uses a number of third-party datasets for normalization:

* `airports.dat`: [OpenFlights Airports Database](http://openflights.org/data.html) ([Open Database License 1.0](http://opendatacommons.org/licenses/odbl/1.0/), [Database Contents License 1.0](http://opendatacommons.org/licenses/dbcl/1.0/))
* `countries.dat`: [Country List](https://github.com/umpirsky/country-list) (MIT license)
* `countries3.dat`: [ISO countries list](https://gist.github.com/eparreno/205900) (license unspecified)
* `states_au.dat`: Part of `pythonwhois` (WTFPL/CC0)
* `states_us.dat`: [State Table](http://statetable.com/) (license unspecified, free reuse encouraged)
* `states_ca.dat`: [State Table](http://statetable.com/) (license unspecified, free reuse encouraged)
* `common_first_names.dat`: [Social Security Administration](http://www.ssa.gov/OACT/babynames/), via [hadley/data-baby-names](https://github.com/hadley/data-baby-names) (license unspecified, provided by US government)

Be aware that the OpenFlights database in particular **has potential licensing consequences**; if you do not wish to be bound by these potential consequences, you may simply delete the `airports.dat` file from your distribution. `pythonwhois` will assume there is no database available, and will not perform airport code conversion (but still function correctly otherwise). This also applies to other included datasets.

## Contributing

To clone the repository, do the following:
```sh
git clone git@github.com:GhostArray/python-whois.git # Clone the repository
cd python-whois # Change directories
virtualenv -p`which python` .venv  # Create a new virtual environment
source .venv/bin/activate   # Enter the Python environment
pip install -e . --upgrade  # Install the core dependencies
pip install -r dev-dependencies.txt  # Install the developer dependencies
```

### Testing

For testing we use Nose, which means running tests is as easy as:
```bash
nosetests
```

For which you should get:

```
...
-------------------------
Ran 3 tests in 11.037s

OK
```

### Pull Requests
Feel free to fork and submit pull requests (to the `develop` branch)! Please make sure to run the test suite before commiting and submitting a PR, information for how to test are at the top of this document.

All commands are relative to the root directory of the repository.

## License

This library may be used under the WTFPL - or, if you take issue with that, consider it to be under the CC0.