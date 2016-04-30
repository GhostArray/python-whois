import re
import os
import csv


def precompile_regexes(source, flags=0):
    return [re.compile(regex, flags) for regex in source]


def precompile_regexes_dict(source, flags=0):
    return dict((key, re.compile(regex, flags)) for (key, regex) in source.items())


def data_filename(filename):
    path = os.path.abspath(os.path.dirname(__file__) + '/../data/' + filename)

    return path


def read_dataset(filename, destination, abbrev_key, name_key, is_dict=False):
    # type: (str, dict, str, str, bool) -> None
    try:
        filename = data_filename(filename)

        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile) if is_dict else csv.reader(csvfile)

            for line in reader:
                destination[line[abbrev_key]] = line[name_key]
    except IOError as e:
        # We SHOULDN'T ignore this unless it's the airport database.
        if filename != 'airports.dat':
            raise e


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
