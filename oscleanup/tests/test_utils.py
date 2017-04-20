import unittest
from oscleanup.utils import *


class TestUtils(unittest.TestCase):

    def test_fff(self):
        # source the creds

        #
        x = fff()
        self.assertIsNotNone(x)

