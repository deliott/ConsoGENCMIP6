from unittest import TestCase
import unittest.main
import pandas as pd
from datetime import datetime
import numpy as np

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

    def test_get_subproject_subtotal_dataframe(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_subproject_list('Skylake')
        output = self.gencmip6_data.get_subproject_subtotal_dataframe('Skylake')

        data1 = [[701413.69, 16573.01, 777896.99, 35.01], [761406.56, 16970.07, 801912.78, 35.01], [867443.26, 16970.07, 812899.98, 35.01]]
        df1 = pd.DataFrame(data1, columns=['dcpcmip6', 'devcmip6', 'pmicmip6', 'rcecmip6'])

        try:
            pd.testing.assert_frame_equal(df1, output, check_exact=True)
        except:
            print('\nIssue with the pandas dataframe comparison.\n')
            print('Function\'output  : \n',output)
            print('Must be equal to : \n', df1)
            self.assertTrue(False)

        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.project_timeseries_filename = 'timeseries_gen0826_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gen0826_data.load_project_data()
        self.gen0826_data.set_dates()
        self.gen0826_data.set_processor_subproject_list('Skylake')
        output0826 = self.gen0826_data.get_subproject_subtotal_dataframe('Skylake')

        data2 = [[7319.91], [7319.91], [7319.91]]
        df2 = pd.DataFrame(data2, columns=['gen0826'])
        try:
            pd.testing.assert_frame_equal(df2, output0826, check_exact=True)
        except:
            print('\nIssue with the pandas dataframe comparison.\n')
            print('Function\'output  : \n', output0826)
            print('Must be equal to : \n', df2)
            self.assertTrue(False)
        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.project_timeseries_filename = 'timeseries_gen0826_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gen0826_data.load_project_data()
        self.gen0826_data.set_dates()
        self.gen0826_data.set_processor_subproject_list('KNL')
        output0826 = self.gen0826_data.get_subproject_subtotal_dataframe('KNL')

        data3 = [[60222.24], [60222.24], [60222.24]]
        df3 = pd.DataFrame(data3, columns=['gen0826'])
        try:
            pd.testing.assert_frame_equal(df3, output0826, check_exact=True)
        except:
            print('\nIssue with the pandas dataframe comparison.\n')
            print('Function\'output  : \n', output0826)
            print('Must be equal to : \n', df3)
            self.assertTrue(False)

    def test_sort_df_colomns_according_to_biggest_last_value(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_subproject_list('Skylake')
        # output = self.gencmip6_data.get_subproject_subtotal_dataframe('Skylake')
        self.gencmip6_data.set_subproject_subtotal_dataframe('Skylake')
        self.gencmip6_data.sort_df_colomns_according_to_biggest_last_value()


        sorted_data1 = [[701413.69, 777896.99, 16573.01, 35.01], [761406.56, 801912.78, 16970.07, 35.01], [867443.26, 812899.98, 16970.07, 35.01]]
        sorted_df1 = pd.DataFrame(sorted_data1, columns=['dcpcmip6', 'pmicmip6', 'devcmip6', 'rcecmip6'])

        try:
            pd.testing.assert_frame_equal(sorted_df1, self.gencmip6_data.subproject_subtotal_dataframe, check_exact=True)
        except:
            print('\nIssue with the pandas dataframe comparison.\n')
            print('Function\'output  : \n', self.gencmip6_data.subproject_subtotal_dataframe)
            print('Must be equal to : \n', sorted_df1)
            self.assertTrue(False)

    def test_add_dates_to_dataframe(self):

        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_subproject_list('Skylake')
        # output = self.gencmip6_data.get_subproject_subtotal_dataframe('Skylake')
        self.gencmip6_data.set_subproject_subtotal_dataframe('Skylake')
        self.gencmip6_data.sort_df_colomns_according_to_biggest_last_value()
        self.gencmip6_data.add_dates_to_dataframe()


        sorted_data1 = [[datetime.strptime('2019-05-30', "%Y-%m-%d"), 701413.69, 777896.99, 16573.01, 35.01],
                        [datetime.strptime('2019-05-31', "%Y-%m-%d"), 761406.56, 801912.78, 16970.07, 35.01],
                        [datetime.strptime('2019-06-01', "%Y-%m-%d"), 867443.26, 812899.98, 16970.07, 35.01]]
        sorted_df1 = pd.DataFrame(sorted_data1, columns=['Date', 'dcpcmip6', 'pmicmip6', 'devcmip6', 'rcecmip6'])

        try:
            pd.testing.assert_frame_equal(sorted_df1, self.gencmip6_data.subproject_subtotal_dataframe, check_exact=True)
        except:
            print('\nIssue with the pandas dataframe comparison.\n')
            print('Function\'output  : \n', self.gencmip6_data.subproject_subtotal_dataframe)
            print('Must be equal to : \n', sorted_df1)
            self.assertTrue(False)

    def test_add_total_subprojects(self):

        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_subproject_list('Skylake')
        # output = self.gencmip6_data.get_subproject_subtotal_dataframe('Skylake')
        self.gencmip6_data.set_subproject_subtotal_dataframe('Skylake')
        self.gencmip6_data.sort_df_colomns_according_to_biggest_last_value()
        self.gencmip6_data.add_dates_to_dataframe()

        self.gencmip6_data.add_total_subprojects()


        sorted_data1 = [[datetime.strptime('2019-05-30', "%Y-%m-%d"), 1495918.70, 701413.69, 777896.99, 16573.01, 35.01],
                        [datetime.strptime('2019-05-31', "%Y-%m-%d"), 1580324.42, 761406.56, 801912.78, 16970.07, 35.01],
                        [datetime.strptime('2019-06-01', "%Y-%m-%d"), 1697348.32, 867443.26, 812899.98, 16970.07, 35.01]]
        sorted_df1 = pd.DataFrame(sorted_data1, columns=['Date', 'Total', 'dcpcmip6', 'pmicmip6', 'devcmip6', 'rcecmip6'])

        try:
            pd.testing.assert_frame_equal(sorted_df1, round(self.gencmip6_data.subproject_subtotal_dataframe, 2), check_exact=True)
        except:
            print('\nIssue with the pandas dataframe comparison.\n')
            print('Function\'output  : \n', self.gencmip6_data.subproject_subtotal_dataframe)
            print('Must be equal to : \n', sorted_df1)
            self.assertTrue(False)



    def test_set_allocated_dict(self):

        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_list()
        self.gencmip6_data.set_allocated_dict()

        mock_allocation = {'Skylake': 27070000.0}
        self. assertEqual(self.gencmip6_data.allocated_dict, mock_allocation)

        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.project_timeseries_filename = 'timeseries_gen0826_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gen0826_data.load_project_data()
        self.gen0826_data.set_dates()
        self.gen0826_data.set_processor_list()
        self.gen0826_data.set_allocated_dict()

        mock_allocation2 = {'Skylake':  40000.0, 'KNL': 200000.0}
        self. assertEqual(self.gen0826_data.allocated_dict, mock_allocation2)

    def test_set_deadline(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_deadline()

        mock_deadline1 = '2020-05-02'
        self.assertEqual(self.gencmip6_data.deadline, mock_deadline1)


        self.gen0826_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gen0826/'
        self.gen0826_data.project_timeseries_filename = 'timeseries_gen0826_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gen0826_data.load_project_data()
        self.gen0826_data.set_dates()
        self.gen0826_data.set_deadline()

        mock_deadline2 = '2019-11-04'
        self.assertEqual(self.gen0826_data.deadline, mock_deadline2)

    def test_start_date_to_dict(self):
        self.gencmip6_data.set_start_date_to_dict('Skylake', '19-05-1925')

        test_comparison = {}
        test_comparison['Skylake'] = '19-05-1925'
        self.assertDictEqual(self.gencmip6_data.start_date_dict, test_comparison)

    def test_set_last_date(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_last_date(days_in_advance=3)

        mock_last_date = datetime.strptime('2019-06-04', "%Y-%m-%d")
        self.assertEqual(self.gencmip6_data.last_date_of_plot, mock_last_date)

    def test_get_list_of_dates_between_boundaries(self):
        date1 = '19-05-1925'
        date2 = '28-05-1925'
        output = self.gencmip6_data.get_list_of_dates_between_boundaries(date1, date2)
        test_list = pd.to_datetime(['19-05-1925', '20-05-1925', '21-05-1925', '22-05-1925', '23-05-1925',
                        '24-05-1925', '25-05-1925', '26-05-1925', '27-05-1925', '28-05-1925', ])

        self.assertTrue(all(output == test_list))

    def test_set_optimal_daily_consumption(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()
        self.gencmip6_data.set_processor_list()

        self.gencmip6_data.set_allocated_dict()
        self.gencmip6_data.set_deadline()

        self.gencmip6_data.set_start_date_to_dict('Skylake', '2019-05-01')
        self.gencmip6_data.set_optimal_daily_consumption('Skylake')

        test_result = 73760.0
        self.assertEqual(test_result, round(self.gencmip6_data.optimal_daily_consumption, 0))


    def test_get_theoretical_optimal_consumption_curve_dataframe(self):
        self.gencmip6_data.path_to_project_timeseries = '/home/edupont/ccc_myproject_data/mocks/mock_time_series/gencmip6/'
        self.gencmip6_data.project_timeseries_filename = 'timeseries_gencmip6_Irene_from_20190513_to_20190602_MOCKED.json'
        self.gencmip6_data.load_project_data()
        self.gencmip6_data.set_dates()

        self.gencmip6_data.set_processor_list()
        self.gencmip6_data.set_allocated_dict()
        self.gencmip6_data.set_deadline()
        self.gencmip6_data.set_last_date(days_in_advance=3)
        self.gencmip6_data.set_start_date_to_dict('Skylake', '2019-05-01')
        self.gencmip6_data.set_optimal_daily_consumption('Skylake')

        test = self.gencmip6_data.get_theoretical_optimal_consumption_curve_dataframe('Skylake')

        mock_last_date = [0.0, 73760.21798365122, 147520.43596730244,
                          221280.65395095368, 295040.8719346049, 368801.0899182561,
                          442561.30790190736, 516321.52588555857, 590081.7438692098,
                          663841.961852861, 737602.1798365122, 811362.3978201634,
                          885122.6158038147, 958882.8337874659, 1032643.0517711171,
                          1106403.2697547683, 1180163.4877384196, 1253923.7057220708,
                          1327683.923705722, 1401444.1416893732, 1475204.3596730244,
                          1548964.5776566756, 1622724.7956403268, 1696485.013623978,
                          1770245.2316076295, 1844005.4495912807, 1917765.6675749319,
                          1991525.885558583, 2065286.1035422343, 2139046.3215258853,
                          2212806.5395095367, 2286566.7574931877, 2360326.975476839,
                          2434087.1934604906, 2507847.4114441415]

        self.assertTrue(test['Conso_Optimale'] == mock_last_date)




if __name__ == '__main__':
    # Initialise Global Variables
    settings.init()
    set_paths.set_path_to_timeseries()
    set_paths.set_path_to_plots()

    unittest.main()
