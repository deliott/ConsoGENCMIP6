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





if __name__ == '__main__':
    # Initialise Global Variables
    settings.init()
    set_paths.set_path_to_timeseries()
    set_paths.set_path_to_plots()

    unittest.main()
