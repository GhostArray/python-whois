from tests import TestCase

from pythonwhois import util


class TestUtil(TestCase):
    def test_precompile_regexes_list(self):
        compiled = util.precompile_regexes([r'.*', r'^$'])

        self.assertIsNotNone(compiled[0])
        self.assertIsNotNone(compiled[1])
        self.assertFalse(isinstance(compiled[0], str))

    def test_precompile_regexes_falsy(self):
        self.assertEqual(util.precompile_regexes(None), [])
        self.assertEqual(util.precompile_regexes([]), [])
        self.assertEqual(util.precompile_regexes({}), [])

    def test_data_filename(self):
        import os

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

        self.assertEqual(util.data_filename('google.exe'),
                         path + '/google.exe')
