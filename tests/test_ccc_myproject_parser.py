from unittest import TestCase
import bin.ccc_myproject_parser

#from bin.ccc_myproject_parser import parse_config


class Test_CCC_MYPROJECT_Parser(TestCase):

    def setUp(self):
        #self.path = '../tests/config_test.ini/'
        self.path = '/home/edupont/ccc_myproject_data/mock_ccc_myproject.log'
    def test_parse_config(self):
        self.assertEqual(True, True)




if __name__ == '__main__':
    unittest.main()