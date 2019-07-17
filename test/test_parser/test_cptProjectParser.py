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

        # # @TODO : check if we need to import Parent and Child classes or if just Child is enough.
        # self.file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mocks/mock_ccc_myproject.log')
        # self.project_to_parse1 = AdaProjectParser(self.file_to_parse.set_path_to_individual_projects_directory() +
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


    # # def test_set_subproject(self):
    # #     self.project_to_parse1.check_has_subproject()
    # #     self.project_to_parse1.set_subproject()
    # #     dict1_mock = {'dcpcmip6': {}, 'rcecmip6': {}, 'scecmip6': {}, 'pmicmip6': {}, 'devcmip6': {}}
    # #     self.assertDictEqual(self.project_to_parse1.subproject, dict1_mock)
    # #
    # #     self.project_to_parse2.check_has_subproject()
    # #     self.project_to_parse2.get_project_name()
    # #     self.project_to_parse2.set_subproject()
    # #     dict2_mock = {'gen0826': {}}
    # #     self.assertDictEqual(self.project_to_parse2.subproject, dict2_mock)
    #
    # def test_set_subproject(self):
    #     self.project_to_parse1.check_has_subproject()
    #     self.project_to_parse1.set_processor_type()
    #     self.project_to_parse1.set_subproject()
    #     dict1_mock = {'sous_projet': {'dcpcmip6': {}, 'rcecmip6': {}, 'scecmip6': {}, 'pmicmip6': {}, 'devcmip6': {}}}
    #
    #     # print(self.project_to_parse1.processor_type_dict)
    #     self.assertDictEqual(self.project_to_parse1.processor_type_dict['Skylake'], dict1_mock)
    #
    #     self.project_to_parse2.check_has_subproject()
    #     self.project_to_parse2.set_project_name()
    #     self.project_to_parse2.set_processor_type()
    #     self.project_to_parse2.set_subproject()
    #     #
    #     dict2_mock = {'Skylake': {'sous_projet': {'gen0826': {}}}, 'KNL': {'sous_projet': {'gen0826': {}}}}
    #     self.assertDictEqual(self.project_to_parse2.processor_type_dict, dict2_mock)
    #
    # def test_set_subtotals(self):
    #     self.project_to_parse1.check_has_subproject()
    #     self.project_to_parse1.set_processor_type()
    #     self.project_to_parse1.set_subproject()
    #     self.project_to_parse1.set_subtotals()
    #     dict1_mock = {'sous_projet': {
    #                   'dcpcmip6': {'subtotal': 665437.81},
    #                   'rcecmip6': {'subtotal': 0.0},
    #                   'scecmip6': {'subtotal': 61794.4},
    #                   'pmicmip6': {'subtotal': 125172.41},
    #                   'devcmip6': {'subtotal': 6026.07}}
    #                   }
    #     self.assertDictEqual(self.project_to_parse1.processor_type_dict['Skylake'], dict1_mock)
    #
    #     self.project_to_parse2.check_has_subproject()
    #     self.project_to_parse2.set_project_name()
    #     self.project_to_parse2.set_processor_type()
    #     self.project_to_parse2.set_subproject()
    #     self.project_to_parse2.set_subtotals()
    #     dict2_mock = {
    #         'KNL': {'sous_projet': {'gen0826': {'subtotal': 59460.32}}},
    #         'Skylake': {'sous_projet': {'gen0826': {'subtotal': 6935.07}}}
    #     }
    #     self.assertDictEqual(self.project_to_parse2.processor_type_dict, dict2_mock)
    #
    # # def test_get_total(self):
    # #         self.project_to_parse1.check_has_subproject()
    # #         self.project_to_parse1.set_subproject()
    # #         total = self.project_to_parse1.get_total()
    # #
    # #         self.assertEqual(total, 984797.89)
    # #
    # #         self.project_to_parse1.check_has_subproject()
    # #         self.project_to_parse1.set_subproject()
    # #         total = self.project_to_parse1.get_total()
    # #
    # #         self.assertEqual(total, 984797.89)
    #
    # def test_set_processor_type(self):
    #     self.project_to_parse1.check_has_subproject()
    #     self.project_to_parse1.set_processor_type()
    #     dict1_mock = {'Skylake': {}}
    #     self.assertDictEqual(self.project_to_parse1.processor_type_dict, dict1_mock)
    #
    #     self.project_to_parse2.check_has_subproject()
    #     # self.project_to_parse2.get_project_name()
    #     self.project_to_parse2.set_processor_type()
    #     dict2_mock = {'Skylake': {}, 'KNL': {}}
    #     self.assertDictEqual(self.project_to_parse2.processor_type_dict, dict2_mock)
    #
    # def test_set_total(self):
    #     self.project_to_parse1.check_has_subproject()
    #     self.project_to_parse1.set_processor_type()
    #     self.project_to_parse1.set_total()
    #     dict1_mock = {'Skylake': {'total': 984797.89}}
    #     self.assertDictEqual(self.project_to_parse1.processor_type_dict, dict1_mock)
    #
    #     self.project_to_parse2.check_has_subproject()
    #     self.project_to_parse2.set_processor_type()
    #     self.project_to_parse2.set_total()
    #     dict2_mock = {'Skylake': {'total': 6935.07}, 'KNL': {'total': 59460.32}}
    #     self.assertDictEqual(self.project_to_parse2.processor_type_dict, dict2_mock)
    #
    # def test_set_allocated(self):
    #     self.project_to_parse1.check_has_subproject()
    #     self.project_to_parse1.set_processor_type()
    #     self.project_to_parse1.set_allocated()
    #     dict1_mock = {'Skylake': {'allocated': 27070000.00}}
    #     self.assertDictEqual(self.project_to_parse1.processor_type_dict, dict1_mock)
    #
    #     self.project_to_parse2.check_has_subproject()
    #     self.project_to_parse2.set_processor_type()
    #     self.project_to_parse2.set_allocated()
    #     dict2_mock = {'Skylake': {'allocated': 40000.00}, 'KNL': {'allocated': 200000.00}}
    #     self.assertDictEqual(self.project_to_parse2.processor_type_dict, dict2_mock)
    #
    # def test_set_login_for_a_subproject(self):
    #     self.project_to_parse1.check_has_subproject()
    #     self.project_to_parse1.set_processor_type()
    #     self.project_to_parse1.set_subproject()
    #     self.project_to_parse1.set_subtotals()
    #     self.project_to_parse1.set_login_for_a_subproject('dcpcmip6')
    #     dict1_mock = {'sous_projet': {'dcpcmip6': {'subtotal': 665437.81,
    #                                'login_conso': {
    #                                    'andrezwt': 0.00,
    #                                    'bobby': 0.00,
    #                                    'corrine': 0.00,
    #                                    'damiens': 0.00,
    #                                    'p86ffas': 3444.85,
    #                                    'p86ticl': 135472.06,
    #                                    'quoranti': 526520.90,
    #                                }
    #
    #                                },
    #                   'rcecmip6': {'subtotal': 0.0},
    #                   'scecmip6': {'subtotal': 61794.4},
    #                   'pmicmip6': {'subtotal': 125172.41},
    #                   'devcmip6': {'subtotal': 6026.07}}
    #                   }
    #     self.assertDictEqual(self.project_to_parse1.processor_type_dict['Skylake'], dict1_mock)
    #
    #     self.project_to_parse2.check_has_subproject()
    #     self.project_to_parse2.set_project_name()
    #     self.project_to_parse2.set_processor_type()
    #     self.project_to_parse2.set_subproject()
    #     self.project_to_parse2.set_subtotals()
    #     self.project_to_parse2.set_login_for_a_subproject('gen0826')
    #     dict2_mock = {'KNL': {'sous_projet': {'gen0826': {'login_conso': {'desroche': 59460.32,
    #                                                       'derickin': 0.00,
    #                                                       'pierre': 0.00,
    #                                                       'p24demus': 0.00,
    #                                                       'p86fisa': 0.00,
    #                                                       'p86mno': 0.00,
    #                                                       'p86mnop': 0.00,
    #                                                       'p86fann': 0.00,
    #                                                       'francesc': 0.00
    #                                                       },
    #                                       'subtotal': 59460.32}}},
    #                   'Skylake': {'sous_projet': {'gen0826': {'login_conso': {'desroche': 6295.58,
    #                                                           'derickin': 3.13,
    #                                                           'pierre': 0.00,
    #                                                           'p24demus': 4.00,
    #                                                           'p86fisa': 4.12,
    #                                                           'p86mno': 622.33,
    #                                                           'p86mnop': 1.04,
    #                                                           'p86fann': 4.85,
    #                                                           'francesc': 0.02
    #                                                           },
    #                                           'subtotal': 6935.07}}}}
    #     self.assertDictEqual(self.project_to_parse2.processor_type_dict, dict2_mock)
    #
    # def test_set_login_for_all_subproject(self):
    #     self.project_to_parse1.check_has_subproject()
    #     self.project_to_parse1.set_processor_type()
    #     self.project_to_parse1.set_subproject()
    #     self.project_to_parse1.set_subtotals()
    #     self.project_to_parse1.set_login_for_all_subprojects()
    #     dict1_mock = {'sous_projet':
    #                   {'dcpcmip6': {'subtotal': 665437.81,
    #                                'login_conso': {
    #                                    'andrezwt': 0.00,
    #                                    'bobby': 0.00,
    #                                    'corrine': 0.00,
    #                                    'damiens': 0.00,
    #                                    'p86ffas': 3444.85,
    #                                    'p86ticl': 135472.06,
    #                                    'quoranti': 526520.90
    #                                }
    #                                },
    #                   'rcecmip6': {'subtotal': 0.0,
    #                                'login_conso': {
    #                                    'andrezwt': 0.00,
    #                                    'bobby': 0.00,
    #                                    'corrine': 0.00
    #                                }
    #                                },
    #                   'scecmip6': {'subtotal': 61794.4,
    #                                'login_conso': {
    #                                    'andrezwt': 0.00,
    #                                    'bobby': 0.00,
    #                                    'corrine': 0.00,
    #                                    'damiens': 0.00,
    #                                    'edgards': 61794.40,
    #                                    'francesc': 0.00,
    #                                    'guozhe': 0.00,
    #                                    'habzhani': 0.00
    #                                }
    #                                },
    #                   'pmicmip6': {'subtotal': 125172.41,
    #                                'login_conso': {
    #                                    'andrezwt': 0.00,
    #                                    'bobby': 0.00,
    #                                    'corrine': 0.00,
    #                                    'damiens': 0.00,
    #                                    'p25dede': 125171.95
    #                                }
    #                                },
    #                   'devcmip6': {'subtotal': 6026.07,
    #                                'login_conso': {
    #                                    'andrezwt': 0.00,
    #                                    'bobby': 0.00,
    #                                    'corrine': 0.00,
    #                                    'damiens': 0.00,
    #                                    'derickin': 1583.51,
    #                                    'edgards': 5.09,
    #                                    'p48elle': 1658.67,
    #                                    'p86confi': 28.27,
    #                                    'p86derou': 1515.33,
    #                                    'p86cnrs': 1235.20
    #                                }
    #                                }}
    #                  }
    #     # print(self.project_to_parse1.processor_type_dict)
    #     self.assertDictEqual(self.project_to_parse1.processor_type_dict['Skylake'], dict1_mock)
    #
    #     self.project_to_parse2.check_has_subproject()
    #     self.project_to_parse2.set_project_name()
    #     self.project_to_parse2.set_processor_type()
    #     self.project_to_parse2.set_subproject()
    #     self.project_to_parse2.set_subtotals()
    #     self.project_to_parse2.set_login_for_all_subprojects()
    #     dict2_mock = {'KNL': {'sous_projet':
    #                              {'gen0826': {'login_conso': {'desroche': 59460.32,
    #                                                           'derickin': 0.00,
    #                                                           'pierre': 0.00,
    #                                                           'p24demus': 0.00,
    #                                                           'p86fisa': 0.00,
    #                                                           'p86mno': 0.00,
    #                                                           'p86mnop': 0.00,
    #                                                           'p86fann': 0.00,
    #                                                           'francesc': 0.00,
    #                                                           },
    #                                           'subtotal': 59460.32}}
    #                           },
    #                   'Skylake': {'sous_projet':
    #                                  {'gen0826': {'login_conso': {'desroche': 6295.58,
    #                                                               'derickin': 3.13,
    #                                                               'pierre': 0.00,
    #                                                               'p24demus': 4.00,
    #                                                               'p86fisa': 4.12,
    #                                                               'p86mno': 622.33,
    #                                                               'p86mnop': 1.04,
    #                                                               'p86fann': 4.85,
    #                                                               'francesc': 0.02,
    #                                                               },
    #                                               'subtotal': 6935.07}
    #                                   }
    #                               }
    #                   }
    #
    #     # print(self.project_to_parse2.processor_type_dict)
    #
    #     self.assertDictEqual(self.project_to_parse2.processor_type_dict, dict2_mock)
    #
    # def test_build_complete_dictionary(self):
    #     self.project_to_parse1.build_complete_dictionary()
    #     dict1_mock = {
    #         'date': '2019-05-13',
    #         'project': 'gencmip6',
    #         'machine': 'Irene',
    #         'project_deadline': '2020-05-02',
    #         'processor_type': {'Skylake': {
    #                   'total': 984797.89,
    #                   'allocated': 27070000.00,
    #                   'sous_projet': {
    #                       'dcpcmip6': {'subtotal': 665437.81,
    #                                    'login_conso': {
    #                                        'andrezwt': 0.00,
    #                                        'bobby': 0.00,
    #                                        'corrine': 0.00,
    #                                        'damiens': 0.00,
    #                                        'p86ffas': 3444.85,
    #                                        'p86ticl': 135472.06,
    #                                        'quoranti': 526520.90
    #                                    }
    #                                    },
    #                       'rcecmip6': {'subtotal': 0.0,
    #                                    'login_conso': {
    #                                        'andrezwt': 0.00,
    #                                        'bobby': 0.00,
    #                                        'corrine': 0.00
    #                                    }
    #                                    },
    #                       'scecmip6': {'subtotal': 61794.4,
    #                                    'login_conso': {
    #                                        'andrezwt': 0.00,
    #                                        'bobby': 0.00,
    #                                        'corrine': 0.00,
    #                                        'damiens': 0.00,
    #                                        'edgards': 61794.40,
    #                                        'francesc': 0.00,
    #                                        'guozhe': 0.00,
    #                                        'habzhani': 0.00
    #                                    }
    #                                    },
    #                       'pmicmip6': {'subtotal': 125172.41,
    #                                    'login_conso': {
    #                                        'andrezwt': 0.00,
    #                                        'bobby': 0.00,
    #                                        'corrine': 0.00,
    #                                        'damiens': 0.00,
    #                                        'p25dede': 125171.95
    #                                    }
    #                                    },
    #                       'devcmip6': {'subtotal': 6026.07,
    #                                    'login_conso': {
    #                                        'andrezwt': 0.00,
    #                                        'bobby': 0.00,
    #                                        'corrine': 0.00,
    #                                        'damiens': 0.00,
    #                                        'derickin': 1583.51,
    #                                        'edgards': 5.09,
    #                                        'p48elle': 1658.67,
    #                                        'p86confi': 28.27,
    #                                        'p86derou': 1515.33,
    #                                        'p86cnrs': 1235.20
    #                                    }
    #                                    }
    #                   }
    #         }
    #         }
    #     }
    #     self.assertDictEqual(self.project_to_parse1.complete_dictionary, dict1_mock)
    #
    #     self.project_to_parse2.build_complete_dictionary()
    #     dict2_mock = {
    #         'date': '2019-05-13',
    #         'project': 'gen0826',
    #         'machine': 'Irene',
    #         'project_deadline': '2019-11-04',
    #         'processor_type': {
    #             'KNL': {
    #                 'total': 59460.32,
    #                 'allocated': 200000.00,
    #                 'sous_projet': {
    #                     'gen0826': {
    #                         'login_conso': {
    #                             'desroche': 59460.32,
    #                             'derickin': 0.00,
    #                             'pierre': 0.00,
    #                             'p24demus': 0.00,
    #                             'p86fisa': 0.00,
    #                             'p86mno': 0.00,
    #                             'p86mnop': 0.00,
    #                             'p86fann': 0.00,
    #                             'francesc': 0.00,
    #                             },
    #                         'subtotal': 59460.32}
    #                 }
    #             },
    #             'Skylake': {
    #                 'total': 6935.07,
    #                 'allocated': 40000.00,
    #                 'sous_projet': {
    #                     'gen0826': {
    #                         'login_conso': {
    #                             'desroche': 6295.58,
    #                             'derickin': 3.13,
    #                             'pierre': 0.00,
    #                             'p24demus': 4.00,
    #                             'p86fisa': 4.12,
    #                             'p86mno': 622.33,
    #                             'p86mnop': 1.04,
    #                             'p86fann': 4.85,
    #                             'francesc': 0.02,
    #                             },
    #                         'subtotal': 6935.07}
    #                 }
    #             }
    #         }
    #     }
    #     self.assertDictEqual(self.project_to_parse2.complete_dictionary, dict2_mock)
    #
    # def test_set_output_name(self):
    #     self.project_to_parse1.set_file_date()
    #     self.project_to_parse1.set_project_name()
    #     self.project_to_parse1.set_project_machine()
    #     self.project_to_parse1.set_output_name()
    #
    #     self.assertEqual(self.project_to_parse1.output_name, 'Irene_gencmip6_20190513.json')
    #
    #     self.project_to_parse2.set_file_date()
    #     self.project_to_parse2.set_project_name()
    #     self.project_to_parse2.set_project_machine()
    #     self.project_to_parse2.set_output_name()
    #
    #     self.assertEqual(self.project_to_parse2.output_name, 'Irene_gen0826_20190513.json')
    #
    #     self.complete_project_to_parse.set_file_date()
    #     self.complete_project_to_parse.set_project_name()
    #     self.complete_project_to_parse.set_project_machine()
    #     self.complete_project_to_parse.set_output_name()
    #
    #     self.assertEqual(self.complete_project_to_parse.output_name, 'Irene_gencmip6_20190514.json')
    #
    # def test_get_output_path(self):
    #     self.project_to_parse1.set_file_date()
    #     self.project_to_parse1.set_project_name()
    #     self.project_to_parse1.set_project_machine()
    #     self.project_to_parse1.set_output_name()
    #     path1 = self.project_to_parse1.get_output_path()
    #     self.assertEqual(path1, '/home/edupont/ccc_myproject_data/mocks/mock_ccc_myproject/Irene_gencmip6_20190513.json')
    #
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
