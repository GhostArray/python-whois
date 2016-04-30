from .util import data_filename, read_dataset

import unicodecsv as csv


class LoadedData(object):
    __instance = None
    """ LoadedData: The singleton instance (if created already) """

    def __init__(self, filenames=None):
        self.filenames = {
            'first_names': 'common_first_names.dat',
            'airports': 'airports.dat',
            'countries': 'countries.dat',
            'countries3': 'countries3.dat',
            'states_au': 'states_au.dat',
            'states_ca': 'states_ca.dat',
            'states_us': 'states_us.dat',
        }

        filenames = filenames if isinstance(filenames, dict) else {}

        if len(filenames) > 0:
            self.filenames.update(filenames)

        for key, value in self.filenames.items():
            self.filenames[key] = data_filename(value)

        self.common_first_names = set()
        self.airports = {}
        self.countries = {}
        self.states_au = {}
        self.states_us = {}
        self.states_ca = {}

        try:
            with open(self.filenames['first_names'], 'rb') as csvfile:
                reader = csv.DictReader(csvfile, encoding='utf-8')

                for line in reader:
                    self.common_first_names.add(line["name"].lower())

        except IOError:
            pass

        if self.filenames['airports']:
            try:
                with open(self.filenames['airports'], 'rb') as csvfile:
                    reader = csv.reader(csvfile, encoding='utf-8')

                    for line in reader:
                        self.airports[line[4]] = line[2]
                        self.airports[line[5]] = line[2]
            except UnicodeEncodeError as e:
                raise e
            except IOError:
                # The distributor likely removed airports.dat for licensing reasons,
                # OR the file is not a valid CSV file. Please make sure the encoding
                # is UTF-8.
                pass

        import logging
        logging.info(read_dataset(self.filenames['countries'], "iso", "name", is_dict=True))


        self.countries = read_dataset(self.filenames['countries'], "iso", "name", is_dict=True)
        self.countries3 = read_dataset(self.filenames['countries3'], "iso3", "name", is_dict=True)
        self.states_au = read_dataset(self.filenames['states_au'], 0, 1)
        self.states_us = read_dataset(self.filenames['states_us'], "abbreviation", "name", is_dict=True)
        self.states_ca = read_dataset(self.filenames['states_ca'], "abbreviation", "name", is_dict=True)

        import logging
        logging.info(self.__dict__)

        # Because 'UK' is commonly used to refer to the United Kingdom, but formally not the ISO code...
        self.countries['UK'] = self.countries.get('GB')

        self.country_names = set([name.lower() for name in self.countries.values()])
