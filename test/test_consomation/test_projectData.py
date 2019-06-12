from unittest import TestCase
import unittest.main

import bin.consomation.settings as settings
import bin.consomation.set_paths as set_paths

from bin.consomation.data_for_plot_extractor import ProjectData

class TestProjectData(TestCase):
    def setUp(self) -> None:

        self.gencmip6_data = ProjectData('gencmip6')
        self.gen0826_data = ProjectData('gen0826')
        # self.empty_project_to_parse = ProjectParser(self.empty_file_to_parse.set_path_to_individual_projects_directory() +
        #                                        "/project_1.log")


    def test_project_parser_init(self):
        self.assertEqual(self.gencmip6_data.path_to_project_timeseries,
                         '/home/edupont/ccc_myproject_data/timeseries/gencmip6/')
        self.assertEqual(self.gen0826_data.path_to_project_timeseries,
                         '/home/edupont/ccc_myproject_data/timeseries/gen0826/')

    def test_set_project_timeseries_json(self):

        # define path to mock gen0826 timeseries
        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.set_project_timeseries_filename()
        gen0826_time_series_filename = self.gen0826_data.project_timeseries_filename

        self. assertEqual(gen0826_time_series_filename, 'timeseries_gen0826_Irene_from_20190513_to_20190602.json')


        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.set_project_timeseries_filename()
        gencmip6_time_series_filename = self.gencmip6_data.project_timeseries_filename

        self. assertEqual(gencmip6_time_series_filename, 'timeseries_gencmip6_Irene_from_20190513_to_20190602.json')

    def test_load_project_data(self):
        pass

    def test_set_dates(self):
        date_list = ['2019-05-13', '2019-05-14', '2019-05-15', '2019-05-16',
                     '2019-05-17', '2019-05-18', '2019-05-19', '2019-05-20',
                     '2019-05-21', '2019-05-22', '2019-05-23', '2019-05-24',
                     '2019-05-25', '2019-05-26', '2019-05-27', '2019-05-28',
                     '2019-05-29', '2019-05-30', '2019-05-31', '2019-06-01',
                     '2019-06-02']

        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.project_timeseries_filename = 'timeseries_gen0826_Irene_from_20190513_to_20190602.json'
        self.gen0826_data.load_project_data()
        self.gen0826_data.set_dates()

        self.assertEqual(self.gen0826_data.dates, date_list)

        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()

        self.assertEqual(self.gencmip6_data.dates, date_list)
        # import json
        # print(json.dumps(self.gen0826_data.json_data, indent=4))

    def test_set_processor_list(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_list()

        self.assertEqual(['Skylake'], self.gencmip6_data.processor_list)

        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.project_timeseries_filename = 'timeseries_gen0826_Irene_from_20190513_to_20190602.json'
        self.gen0826_data.load_project_data()
        self.gen0826_data.set_dates()
        self.gen0826_data.set_processor_list()

        self.assertEqual(['KNL', 'Skylake'], self.gen0826_data.processor_list)

    def test_set_subproject_list(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_list()
        self.gencmip6_data.set_subproject_list()

        mock_list = ['anacmip6', 'c4mcmip6', 'cfmcmip6', 'checmip6', 'cm5cmip6', 'daacmip6', 'dcpcmip6', 'dekcmip6',
                     'devcmip6', 'dmrcmip6', 'fafcmip6', 'geocmip6', 'gmmcmip6', 'hircmip6', 'ismcmip6', 'ls3cmip6',
                     'lumcmip6', 'omicmip6', 'pmicmip6', 'rcecmip6', 'rfmcmip6', 'scecmip6', 'solcmip6', 'strcmip6',
                     'volcmip6']
        self.assertEqual(mock_list, self.gencmip6_data.subproject_list)

        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.project_timeseries_filename = 'timeseries_gen0826_Irene_from_20190513_to_20190602.json'
        self.gen0826_data.load_project_data()
        self.gen0826_data.set_dates()
        self.gen0826_data.set_processor_list()
        self.gen0826_data.set_subproject_list()

        self.assertEqual(['gen0826'], self.gen0826_data.subproject_list)

    def test_set_processor_subproject_list(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_subproject_list('Skylake')

        mock_list = ['anacmip6', 'c4mcmip6', 'cfmcmip6', 'checmip6', 'cm5cmip6', 'daacmip6', 'dcpcmip6', 'dekcmip6',
                     'devcmip6', 'dmrcmip6', 'fafcmip6', 'geocmip6', 'gmmcmip6', 'hircmip6', 'ismcmip6', 'ls3cmip6',
                     'lumcmip6', 'omicmip6', 'pmicmip6', 'rcecmip6', 'rfmcmip6', 'scecmip6', 'solcmip6', 'strcmip6',
                     'volcmip6']
        self.assertEqual(mock_list, self.gencmip6_data.subproject_list)

        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.project_timeseries_filename = 'timeseries_gen0826_Irene_from_20190513_to_20190602.json'
        self.gen0826_data.load_project_data()
        self.gen0826_data.set_dates()
        self.gen0826_data.set_processor_subproject_list('KNL')

        self.assertEqual(['gen0826'], self.gen0826_data.subproject_list)

        self.gen0826_data.set_processor_subproject_list('Skylake')

        self.assertEqual(['gen0826'], self.gen0826_data.subproject_list)


if __name__ == '__main__':
    # Initialise Global Variables
    settings.init()
    set_paths.set_path_to_timeseries()
    set_paths.set_path_to_plots()

    unittest.main()
