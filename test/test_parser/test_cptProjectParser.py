import unittest
from unittest import TestCase
from bin.parser.cpt_projectparser import AdaProjectParser
from bin.parser.ccc_myproject_fileparser import FileParser


class TestProjectParser(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        path_log = '/home/edupont/cpt_data/mocks/mock_cpt_20190528.log'
        # self.empty_file_to_parse = FileParser(path_log)
        self.project_to_parse = AdaProjectParser(path_log)

        self.mock_dict = {
            "date": "2019-05-27",
            "project": "100592",
            "processor_type": {
                "ADA": {
                    "total": 222538.38,
                    "allocated": 4700000,
                    "sous_projet": {
                        "100592": {
                            "login_conso": {
                                "abcd027": 103403.16,
                                "abcd017": 62730.88,
                                "abcd019": 43445.44,
                                "abcd006": 11689.89,
                                "abcd002": 1255.20,
                                "abcd004": 13.77,
                                "abcd005": 0.04,
                                "abcd001": 0.0,
                                "abcd025": 0.0,
                                "abcd013": 0.0,
                                "abcd030": 0.0,
                                "abcd024": 0.0,
                                "abcd003": 0.0,
                                "abcd018": 0.0,
                                "abcd011": 0.0,
                                "abcd032": 0.0,
                                "abcd012": 0.0,
                                "abcd014": 0.0,
                                "abcd015": 0.0,
                                "abcd023": 0.0,
                                "abcd028": 0.0,
                                "abcd007": 0.0,
                                "abcd020": 0.0,
                                "abcd029": 0.0,
                                "abcd026": 0.0,
                                "abcd016": 0.0,
                                "abcd010": 0.0,
                                "abcd022": 0.0,
                                "abcd031": 0.0
                            },
                            "subtotal": 222538.38
                        },
                    }
                }
            },
            "machine": "ADA",
            "project_deadline": "2020-04-30",
            "project_startdate": "2019-05-01"
        }



        # # @TODO : check if we need to import Parent and Child classes or if just Child is enough.
        # self.file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mocks/mock_ccc_myproject.log')
        # self.project_to_parse = AdaProjectParser(self.file_to_parse.set_path_to_individual_projects_directory() +
        #                                        "/project_1.log")
        # self.project_to_parse2 = AdaProjectParser(self.file_to_parse.set_path_to_individual_projects_directory() +
        #                                        "/project_2.log")
        #
        # # @TODO: We should mock the creation of these files.
        # self.complete_file_to_parse = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log')
        # self.complete_file_to_parse.create_individual_projects_directory()
        # self.complete_file_to_parse.copy_project_from_raw_input()
        # self.complete_project_to_parse = AdaProjectParser(
        #     self.complete_file_to_parse.set_path_to_individual_projects_directory() + "/project_1.log")

    # def test_project_parser_init(self):
    #     pass

    def test_set_project_name(self):

        self.assertEqual(self.project_to_parse.project_name, '')
        self.project_to_parse.set_project_name()
        self.assertEqual(self.project_to_parse.project_name, '100592')

    def test_set_project_machine(self):
        self.project_to_parse.set_project_machine()
        self.assertEqual(self.project_to_parse.project_machine, 'ADA')

    def test_set_processor_type_list(self):
        self.project_to_parse.get_processor_type_list()
        self.assertEqual(self.project_to_parse.project_processor_list, ['ADA'])

    def test_convert_jjmmyyyy_to_yyyymmjj(self):
        self.assertEqual( self.project_to_parse.convert_jjmmyyyy_to_yyyymmjj('01-34-6789'), '6789-34-01')
        self.assertEqual( self.project_to_parse.convert_jjmmyyyy_to_yyyymmjj('25-10-1995'), '1995-10-25')

    def test_set_file_date(self):
        self.project_to_parse.set_file_date()
        self.assertEqual(self.project_to_parse.file_date, '2019-05-27')

    def test_set_project_deadline(self):
        self.project_to_parse.set_project_deadline()
        self.assertEqual(self.project_to_parse.project_deadline, '2020-04-30')

    def test_set_project_startdate(self):
        self.project_to_parse.set_project_startdate()
        self.assertEqual(self.project_to_parse.project_start_date, '2019-05-01')

    def test_get_subproject_namelist(self):
        self.project_to_parse.set_project_name()

        # self.project_to_parse.check_has_subproject()
        liste = self.project_to_parse.get_subproject_namelist()
        liste_mock = ['100592']
        self.assertListEqual(liste, liste_mock)

    def test_set_processor_type(self):
        self.project_to_parse.set_project_name()
        self.project_to_parse.set_processor_type()
        dict1_mock = {'ADA': {}}
        self.assertDictEqual(self.project_to_parse.processor_type_dict, dict1_mock)

    def test_set_subproject(self):
        self.project_to_parse.set_project_name()
        self.project_to_parse.set_processor_type()
        self.project_to_parse.set_subproject()
        dict1_mock = {'sous_projet': {'100592': {}}}
        self.assertDictEqual(self.project_to_parse.processor_type_dict['ADA'], dict1_mock)

    def test_set_subtotals(self):
        self.project_to_parse.set_project_name()

        self.project_to_parse.set_processor_type()
        self.project_to_parse.set_subproject()
        self.project_to_parse.set_subtotals()
        dict1_mock = {'sous_projet': {
                      '100592': {'subtotal': 222538.38}}
                      }
        self.assertDictEqual(self.project_to_parse.processor_type_dict['ADA'], dict1_mock)

    def test_set_total(self):
        self.project_to_parse.set_project_name()

        self.project_to_parse.set_processor_type()
        self.project_to_parse.set_total()
        dict1_mock = {'ADA': {'total': 222538.38}}
        self.assertDictEqual(self.project_to_parse.processor_type_dict, dict1_mock)


    def test_set_allocated(self):
        self.project_to_parse.set_project_name()
        self.project_to_parse.set_processor_type()
        self.project_to_parse.set_allocated()
        dict1_mock = {'ADA': {'allocated': 4700000.0}}

        self.assertDictEqual(self.project_to_parse.processor_type_dict, dict1_mock)

    def test_set_login_for_a_subproject(self):
        self.project_to_parse.set_project_name()
        self.project_to_parse.set_processor_type()
        self.project_to_parse.set_subproject()
        self.project_to_parse.set_subtotals()
        self.project_to_parse.set_login_for_a_subproject('100592')
        dict1_mock = dict()
        sous_dict = self.mock_dict["processor_type"]["ADA"]["sous_projet"]
        dict1_mock["sous_projet"] = sous_dict

        self.assertDictEqual(self.project_to_parse.processor_type_dict['ADA'], dict1_mock)


    def test_set_login_for_all_subproject(self):
        self.project_to_parse.set_project_name()
        self.project_to_parse.set_processor_type()
        self.project_to_parse.set_subproject()
        self.project_to_parse.set_subtotals()
        self.project_to_parse.set_login_for_all_subprojects()

        dict1_mock = dict()
        sous_dict = self.mock_dict["processor_type"]["ADA"]["sous_projet"]
        dict1_mock["sous_projet"] = sous_dict

        self.assertDictEqual(self.project_to_parse.processor_type_dict['ADA'], dict1_mock)

    def test_build_complete_dictionary(self):
        self.project_to_parse.build_complete_dictionary()


        dict1_mock = self.mock_dict
        self.assertDictEqual(self.project_to_parse.complete_dictionary, dict1_mock)



    def test_set_output_name(self):
        self.project_to_parse.set_file_date()
        self.project_to_parse.set_project_name()
        self.project_to_parse.set_project_machine()
        self.project_to_parse.set_output_name()

        self.assertEqual(self.project_to_parse.output_name, 'ADA_100592_20190527.json')

    def test_get_output_path(self):
        self.project_to_parse.set_file_date()
        self.project_to_parse.set_project_name()
        self.project_to_parse.set_project_machine()
        self.project_to_parse.set_output_name()
        path1 = self.project_to_parse.get_output_path()

        self.assertEqual(path1, '/home/edupont/cpt_data/mocks/daily_jsons/ADA_100592_20190527.json')

    #     self.complete_project_to_parse.set_file_date()
    #     self.complete_project_to_parse.set_project_name()
    #     self.complete_project_to_parse.set_project_machine()
    #     self.complete_project_to_parse.set_output_name()
    #     pathc = self.complete_project_to_parse.get_output_path()
    #
    #     self.assertEqual(pathc, '/home/edupont/ccc_myproject_data/ccc_myproject_20190515/Irene_gencmip6_20190514.json')
    #
    #     pathe = self.empty_project_to_parse.get_output_path()
    #
    #     self.assertEqual(pathe, '/home/edupont/ccc_myproject_data/mocks/mock_ccc_myproject/default_output_name')
    #
    #     self.empty_project_to_parse.set_output_name()
    #     pathe = self.empty_project_to_parse.get_output_path()
    #     self.assertEqual(pathe, '/home/edupont/ccc_myproject_data/mocks/mock_ccc_myproject/__19450508.json')
    #
    # def test_dump_dict_to_json(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
