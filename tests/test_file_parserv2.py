from unittest import TestCase
import unittest.mock as mock
from bin.ccc_myproject_fileparser import FileParser
import bin.ccc_myproject_fileparser as ccc_myproject_fileparser


class TestFileParser(TestCase):

    # def setUp(self):
    #     self.fileparser1 = FileParser()

    # def test_parser_init(self):
    #     fileparser = FileParser()
    #     file = fileparser.path_to_file
    #     self.assertEqual('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log', file)



    def test_parser_init2(self):
        fileparser = FileParser('path')
        file = fileparser.path_to_file
        self.assertEqual('path', file)

    def test_get_project_last_line(self):
        fileparser1 = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
        liste1 = fileparser1.get_project_last_line()
        self.assertEqual(liste1 ,[57, 123] )

        # fileparser2 = FileParser('path')
        # liste2 = fileparser2.get_project_last_line()
        # self.assertEqual(liste2, [])






if __name__ == '__main__':
    unittest.main()