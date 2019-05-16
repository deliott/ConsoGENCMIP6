from unittest import TestCase
import unittest.mock as mock
from bin.ccc_myproject_fileparser import FileParser
import bin.ccc_myproject_fileparser as ccc_myproject_fileparser


class TestFileParser(TestCase):

    # def setUp(self):
    #     self.fileparser1 = FileParser()

    def test_parser_init(self):
        fileparser = FileParser()
        file = fileparser.path_to_file
        self.assertEqual('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log', file)

    # @mock.patch('os.listdir')
    # def test_parser_init_with_mock(self, mock_listdir):
    #     mock_listdir.return_value = ['ccc_myproject_20190514.log']
    #
    #     fileparser = FileParser()
    #     file = fileparser.path_to_file
    #     self.assertEqual('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log', file)


# @TODO : Problem with the mock to solve.
    def test_parser_init_with_mock(self):
        with mock.patch('bin.ccc_myproject_fileparser.Parser', autospec=True) as mock_Parser:
        # with mock.patch('bin.ccc_myproject_fileparser.ccc_myproject_parser.Parser') as mock_Parser:

            mock_Parser.path_to_raw_data = "/default/path/"
            mock_Parser.list_of_possible_files_to_parse = ['fichier1.txt']

            print("....... \n....... ")
            print(dir(mock_Parser))
            print("....... \n....... ")
            print(mock_Parser.path_to_raw_data)

            fileparser1 = FileParser()
            print("....... \n....... ")
            print(fileparser1) # returns <bin.ccc_myproject_fileparser.FileParser object at 0x7f41a535d240> not correct ?
            print("....... \n..... ")
            print(fileparser1.path_to_file)  #should return the mock results istead returns <MagicMock name='Parser().path_to_raw_data.__add__()' id='139919921453656'>
            print("....... \n....... ")

            self.assertEqual(fileparser1.path_to_file, "/default/path/fichier1.txt")
            # self.assertTrue(True)












        # mock_listdir.return_value = '/current/working/directory'
        #
        # fileparser = FileParser()
        # file = fileparser.path_to_file
        # self.assertEqual('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log', file)


        # # test if the begining of the name properly taken into account
        # mock_listdir.return_value = ['ccc_myproject.log', 'ccc_myproject_20190515.log', 'b.json']
        # parser = Parser()
        # parser.get_list_of_possible_files_to_parse()
        # files = parser.list_of_possible_files_to_parse
        # self.assertEqual(1, len(files))


    def test_parser_init(self):
        fileparser = FileParser()
        file = fileparser.path_to_file
        self.assertEqual('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log', file)


if __name__ == '__main__':
    unittest.main()