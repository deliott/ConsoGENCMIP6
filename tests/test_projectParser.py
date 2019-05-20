import unittest
from unittest import TestCase
from bin.ccc_myproject_projectparser import ProjectParser
from bin.ccc_myproject_fileparser import FileParser
from datetime import date


class TestProjectParser(TestCase):

    def setUp(self) -> None:
        # @TODO : check if we need to import Parent and Child classes or if just Child is enough.
        self.file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
        self.project_to_parse1 = ProjectParser(self.file_to_parse.set_path_to_individual_projects_directory() +
                                               "/project_1.log")
        self.project_to_parse2 = ProjectParser(self.file_to_parse.set_path_to_individual_projects_directory() +
                                               "/project_2.log")

        # @TODO: We should mock the creation of these files.
        self.complete_file_to_parse = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log')
        self.complete_file_to_parse.create_individual_projects_directory()
        self.complete_file_to_parse.copy_project_from_raw_input()
        self.complete_project_to_parse = ProjectParser(
            self.complete_file_to_parse.set_path_to_individual_projects_directory() + "/project_1.log")

    def test_project_parser_init(self):
        pass

    def test_get_project_name(self):
        self.project_to_parse1.get_project_name()
        self.assertEqual(self.project_to_parse1.project_name, 'gencmip6')

        self.project_to_parse2.get_project_name()
        self.assertEqual(self.project_to_parse2.project_name, 'gen0826')

    def test_get_project_machine(self):
        self.project_to_parse1.get_project_machine()
        self.assertEqual(self.project_to_parse1.project_machine, 'Irene')

        self.project_to_parse2.get_project_machine()
        self.assertEqual(self.project_to_parse2.project_machine, 'Irene')

    def test_get_processor_type_list(self):
        self.project_to_parse1.get_processor_type_list()
        self.assertEqual(self.project_to_parse1.project_processor_list, ['Skylake'])

        self.project_to_parse2.get_processor_type_list()
        self.assertEqual(self.project_to_parse2.project_processor_list, ['KNL', 'Skylake'])

    def test_get_file_date(self):
        self.project_to_parse1.get_file_date()
        self.assertEqual(self.project_to_parse1.file_date, date(2019, 5, 13))

        self.complete_project_to_parse.get_file_date()
        self.assertEqual(self.complete_project_to_parse.file_date, date(2019, 5, 14))

    def test_get_project_deadline(self):
        self.project_to_parse2.get_project_deadline()
        self.assertEqual(self.project_to_parse2.project_deadline, date(2019, 11, 4))

        self.complete_project_to_parse.get_project_deadline()
        self.assertEqual(self.complete_project_to_parse.project_deadline, date(2020, 5, 2))


if __name__ == '__main__':
    unittest.main()
