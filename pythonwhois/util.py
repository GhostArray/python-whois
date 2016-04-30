import re
import os
import unicodecsv as csv


def precompile_regexes(source, flags=0):
    return [re.compile(regex, flags) for regex in source]


def precompile_regexes_dict(source, flags=0):
    return dict((key, re.compile(regex, flags)) for (key, regex) in source.items())


def data_filename(filename):
    path = os.path.abspath(os.path.dirname(__file__) + '/../data/' + filename)

    return path


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

        with open(filename, 'rb') as csvfile:
            if is_dict:
                reader = csv.DictReader(csvfile, encoding='utf-8')
            else:
                reader = csv.reader(csvfile, encoding='utf-8')

            for line in reader:
                result[line[abbrev_key]] = line[name_key]

        return result
    except UnicodeEncodeError as e:
        print('Unicode encoding error for data file \'{}\''.format(filename))

        raise e
    except IOError as e:
        # File not found probably because the user removed the airports.dat
        # file for licensing reasons, so we will ignore it.
        pass


# Regex modification utilities
def preprocess_regex(regex):
    # Fix for #2; prevents a ridiculous amount of varying size permutations.
    regex = re.sub(r"\\s\*\(\?P<([^>]+)>\.\+\)", r"\s*(?P<\1>\S.*)", regex)
    # Experimental fix for #18; removes unnecessary variable-size whitespace
    # matching, since we're stripping results anyway.
    regex = re.sub(r"\[ \]\*\(\?P<([^>]+)>\.\*\)", r"(?P<\1>.*)", regex)
    return regex


def dotify(string):
    return "".join([char + r"\.?" for char in string])


def commaify_dict(source):
    return dict((key + ",", regex.replace("$", ",$")) for (key, regex) in source.items())


def allow_trailing_comma_dict(regexes):
    combined_dict = dict()
    combined_dict.update(regexes)
    combined_dict.update(commaify_dict(regexes))
    return combined_dict
