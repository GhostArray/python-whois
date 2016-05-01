import re
import os
import unicodecsv as csv


def precompile_regexes(source, flags=0):
    """
    Pre-compiles either a list or a dict of string regexes into
    compiled ``re`` objects.

    :param source: The list or dict of regexes
    :param flags: The flags to apply on these regexes (e.g., re.IGNORECASE)

    :return: A list or dictionary of pre-compiled regexes
    """

    if not source:
        return []

    if isinstance(source, dict):  # Iterate differently if it's a dict
        return dict((key, re.compile(regex, flags)) for (key, regex) in source.items())

    # Otherwise, use the list.
    return [re.compile(regex, flags) for regex in source]


def data_filename(filename):
    """
    This will return the full path to the file in the data/ directory.

    :param filename: The filename to suffix

    :return: The absolute path to the file
    """

    return os.path.abspath(os.path.dirname(__file__) + '/../data/' + filename)


def read_dataset(filename, abbrev_key, name_key, is_dict=False):
    """
    Loads a file with abbrevation data and returns a filled
    dictionary. We should handle encoding correctly across
    Python 2 and 3 right now.

    :param filename: The (full path) to the file
    :param abbrev_key: The key used to identify the abbreviation column
    :param name_key: The key used to identify the full name column
    :param is_dict: Should we use the dictionary loader instead

    :return: The loaded data
    """

    try:
        result = {}

        # Load the dataset with the encoding agnostic 'unicodecsv'
        with open(filename, 'rb') as csvfile:
            if is_dict:  # Use the dict reader
                reader = csv.DictReader(csvfile, encoding='utf-8')
            else:  # Use the normal reader
                reader = csv.reader(csvfile, encoding='utf-8')

            for line in reader:
                # Iterate through and use the given keys to find the positions of the values
                result[line[abbrev_key]] = line[name_key]

        return result
    except UnicodeEncodeError as e:
        print('Unicode encoding error for data file \'{}\''.format(filename))

        raise e
    except IOError:
        # File not found probably because the user removed the airports.dat
        # file for licensing reasons, so we will ignore it.
        pass


def preprocess_regex(regex):
    """
    Process the regexes to remove any that might be of an issue.

    :param regex: The regex to process

    :return: The modified regex
    """

    # Prevents a ridiculous amount of varying size permutations (making it hang)
    #   https://github.com/joepie91/python-whois/issues/2
    regex = re.sub(r"\\s\*\(\?P<([^>]+)>\.\+\)", r"\s*(?P<\1>\S.*)", regex)

    # An experimental fix for #18, removes unnecessary variable-size whitespace
    # matching, since we're stripping the results anyways.
    #   https://github.com/joepie91/python-whois/issues/18
    regex = re.sub(r"\[ \]\*\(\?P<([^>]+)>\.\*\)", r"(?P<\1>.*)", regex)

    return regex


def dotify(regex):
    """
    Suffixes the regex with a regex that matches a period after
    the domain name.

    :param regex: The regex to suffix to

    :return: The dotified regex
    """

    return "".join([char + r"\.?" for char in regex])


def commaify_dict(source):
    """
    Modifies the keys and values in the dict to have commas
    suffixed to the ends.

    :param source: The dict of regexes

    :return: The modified dictionary
    """

    return dict((key + ",", regex.replace("$", ",$")) for (key, regex) in source.items())


def trailing_comma_dict(regexes):
    """
    Applies the commaify_dict() function on the parameter,
    allowing it to match things with commas at the end.

    :param regexes: The dict of regexes

    :return: The modified dictionary
    """

    # Create and merge them all together
    combined_dict = dict()
    combined_dict.update(regexes)
    combined_dict.update(commaify_dict(regexes))

    return combined_dict
