from unittest import TestCase
import unittest.mock as mock
import bin.ccc_myproject_fileparser  as FileParser

class TestFileParser(TestCase):
    pass

    @mock.patch('os.listdir')
    def test_parser_init(self, mock_listdir):
        mock_listdir.return_value = ['ccc_myproject_20190515.log']

        fileparser = FileParser()
        file = fileparser.path_to_file
        self.assertEqual('ccc_myproject_20190515.log', file)

        # # test if the begining of the name properly taken into account
        # mock_listdir.return_value = ['ccc_myproject.log', 'ccc_myproject_20190515.log', 'b.json']
        # parser = Parser()
        # parser.get_list_of_possible_files_to_parse()
        # files = parser.list_of_possible_files_to_parse
        # self.assertEqual(1, len(files))


if __name__ == '__main__':
    unittest.main()