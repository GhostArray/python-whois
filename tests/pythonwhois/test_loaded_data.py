from tests import TestCase

from pythonwhois import LoadedData


class TestLoadedData(TestCase):
    def test_construct(self):
        data = LoadedData()

        self.assertIsNotNone(data.common_first_names, 'common_first_name is None!')
        self.assertIsNotNone(data.airports, 'airports is None!')
        self.assertIsNotNone(data.countries, 'countries is None!')
        self.assertIsNotNone(data.states_au, 'states_au is None!')
        self.assertIsNotNone(data.states_ca, 'states_ca is None!')
        self.assertIsNotNone(data.states_us, 'states_us is None!')

    def test_construct_filenames(self):
        data = LoadedData({'test': 'test.dat'})

        self.assertEqual(data.filenames['test'].split('/')[-1], 'test.dat')

    def test_pass_ioerror(self):
        # This assumes the user removed the airports.dat for licensing
        # reasons.
        data = LoadedData({'airports': 'noexist.dat'})

        self.assertEqual(data.airports, {})
