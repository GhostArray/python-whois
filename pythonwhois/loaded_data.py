from .util import data_filename, read_dataset

import csv


class LoadedData(object):
    __instance = None
    """ LoadedData: The singleton instance (if created already) """

    def __init__(self):
        self.common_first_names = set()
        self.airports = {}
        self.countries = {}
        self.states_au = {}
        self.states_us = {}
        self.states_ca = {}

        try:
            with open(data_filename('common_first_names.dat'), 'r') as csvfile:
                reader = csv.DictReader(csvfile)

                for line in reader:
                    self.common_first_names.add(line["name"].lower())

        except IOError as e:
            pass

        try:
            with open(data_filename('airports.dat'), 'r') as csvfile:
                reader = csv.reader(csvfile)

                for line in reader:
                    self.airports[line[4]] = line[2]
                    self.airports[line[5]] = line[2]
        except IOError as e:
            # The distributor likely removed airports.dat for licensing reasons. We'll just leave an empty dict.
            pass

        read_dataset("countries.dat", self.countries, "iso", "name", is_dict=True)
        read_dataset("countries3.dat", self.countries, "iso3", "name", is_dict=True)
        read_dataset("states_au.dat", self.states_au, 0, 1)
        read_dataset("states_us.dat", self.states_us, "abbreviation", "name", is_dict=True)
        read_dataset("states_ca.dat", self.states_ca, "abbreviation", "name", is_dict=True)

        # Because 'UK' is commonly used to refer to the United Kingdom, but formally not the ISO code...
        self.countries['UK'] = self.countries['GB']

        self.country_names = set([name.lower() for name in self.countries.values()])
