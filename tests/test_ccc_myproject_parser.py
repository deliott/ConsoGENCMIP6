from unittest import TestCase
# import bin.ccc_myproject_parser
from bin.consomation.ccc_myproject_parser import Parser


class Test_CCC_MYPROJECT_Parser(TestCase):

    # def setUp(self):
    #     # self.path = '../tests/config_test.ini/'
    #     self.path = '/home/edupont/ccc_myproject_data/mock_ccc_myproject.log'

    """def test_parser_init(self):
        parser = Parser()
        self.assertEqual(parser.path_to_raw_data, "/default/path/")
        self.assertEqual(parser.list_of_possible_files_to_parse, [])

        This was deleted du to the addition of the use of the methods
        self.set_path_to_raw_data()
        self.get_list_of_possible_files_to_parse()

        in the __init__() of the Parser class
    """

        # self.assertEqual(parser.number_of_projects, 0)
    # def test_parse_config(self):
    #     self.assertEqual(True, True)

# @TODO : test if the fqdn does not give the answers expected
    def test_set_path_to_raw_data(self):
        parser = Parser()
        #parser.set_path_to_raw_data()
        # self.assertEqual(parser.path_to_raw_data[-20:], "/ccc_myproject_data/")
        self.assertEqual(parser.path_to_raw_data[-20:], "/default/path/")

# @TODO: test the opening is done properly using mock library in unittest.
    def test_set_open_raw_data_file(self):
        # set_path_to_raw_data(self)
        # self.assertEqual(parser.path_to_raw_data[-1], "/")
        pass

#    @mock.patch('os.listdir')
#     def test_get_list_of_possible_files_to_parse(self, mock_listdir):
#
#         # test if the end of the name properly taken into account
#         mock_listdir.return_value = ['ccc_myproject_20190515.log', 'ccc_myproject_20190514',
#                                      'ccc_myproject_20190515.dat', 'c.json', 'd.txt']
#         parser = Parser()
#         #parser.get_list_of_possible_files_to_parse()
#         files = parser.list_of_possible_files_to_parse
#         self.assertEqual(1, len(files))
#
#         # test if the begining of the name properly taken into account
#         mock_listdir.return_value = ['ccc_myproject.log', 'ccc_myproject_20190515.log', 'b.json']
#         parser = Parser()
#         #parser.get_list_of_possible_files_to_parse()
#         files = parser.list_of_possible_files_to_parse
#         self.assertEqual(1, len(files))
#
#
#
#
# @TODO Issue with this test. Try to repair the import in the patch.

#     def test_get_list_of_possible_files_to_parse(self):
#         # with mock.patch('bin.ccc_myproject_parser.Parser.os.listdir') as mock_listdir:
#         with mock.patch('bin.ccc_myproject_parser.Parser.os.listdir') as mock_listdir:
#             # test if the end of the name properly taken into account
#                 mock_listdir.return_value = ['ccc_myproject_20190515.log', 'ccc_myproject_20190514',
#                                              'ccc_myproject_20190515.dat', 'c.json', 'd.txt']
#                 parser = Parser()
#                 # parser.get_list_of_possible_files_to_parse()
#                 files = parser.list_of_possible_files_to_parse
#                 self.assertEqual(1, len(files))
#
#                 # test if the begining of the name properly taken into account
#                 mock_listdir.return_value = ['ccc_myproject.log', 'ccc_myproject_20190515.log', 'b.json']
#                 parser = Parser()
#                 # parser.get_list_of_possible_files_to_parse()
#                 files = parser.list_of_possible_files_to_parse
#                 self.assertEqual(1, len(files))



if __name__ == '__main__':
    unittest.main()