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
        self.assertEqual(liste1 ,[57, 93] )

        fileparser2 = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190514.log')
        liste2 = fileparser2.get_project_last_line()
        self.assertEqual(liste2 ,[2984, 3050] )

        # fileparser2 = FileParser('path')
        # liste2 = fileparser2.get_project_last_line()
        # self.assertEqual(liste2, [])

    def test_set_path_to_individual_projects_directory(self):
        fileparser1 = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
        self.assertEqual(fileparser1.set_path_to_individual_projects_directory(),\
                         '/home/edupont/ccc_myproject_data/mock_ccc_myproject')

        fileparser2 = FileParser('/home/eldupont/ccc_myproject_data/ccc_myproject_20190514.log')
        self.assertEqual(fileparser2.set_path_to_individual_projects_directory(), \
                         '/home/eldupont/ccc_myproject_data/ccc_myproject_20190514')


if __name__ == '__main__':
    unittest.main()