from bin.ccc_myproject_parser import Parser
# import bin.ccc_myproject_parser as ccc_myproject_parser
import os
import shutil
import glob
from bin.ccc_myproject_fileparser import FileParser

import json

"""
The objective of module is to concatenate the daily json files of a project 
into a bigger json file representing the timeserie.
"""


class TimeSeriesConcatenator():

    def __init__(self, path_to_daily_json_data_folder):
        """
        :param path_to_daily_json_data_folder: absolute path of the file that will be parsed, here it is the last one.
        """

        self.path_to_project_daily_json_files_directory = path_to_daily_json_data_folder
        self.daily_dict = dict()
        self.time_series_dict = dict()
        # self.time_series_dict = {'data': {}}
        self.file_list = []
        self.daily_time = ''

        #
        self.project_name = ""
        self.project_machine = ""
        self.debut = ""
        self.fin = ""
        # self.project_processor_list = []
        # # self.file_date = ''
        # self.file_date = '1945-05-08'
        # self.project_deadline = '1969-07-21'
        # self.has_subproject = False
        #
        # self.complete_dictionary = dict()
        #
        # self.output_name = 'default_output_name'

    def load_daily_data(self,file):
        """ Load data from on json file that have the data structure for a day.
        The data dictionnary is stored in the daily_dict attribute.

        :param file: name of the json file with the data from the day we want.
        :type file: str
        :return: None
        """
        with open(self.path_to_project_daily_json_files_directory + '/' + file) as file_object:
            # store file data in object
            self.daily_dict = dict()

            self.daily_dict = json.load(file_object)

        # print(self.daily_dict)

    def set_daily_time(self):
        # print('Execution de set_daily_time() : ')
        # print('le dico : ', self.daily_dict)
        # print('La date : ', self.daily_dict['date'])
        self.daily_time = self.daily_dict['date']

    def remove_date_from_dailydict(self):
        del self.daily_dict['date']

    def add_dailydict_to_timeseries(self):
        """
        Adds the daily_dict dictionary into the bigger one : time_series_dict.
        Daily dict is added in as a new item with a key containing the date of the data.
        'date' entry is removed from dailydict before insertion
        :return: None
        """
        self.remove_date_from_dailydict()
        self.time_series_dict[self.daily_time] = self.daily_dict

    def set_file_list(self):
        """
        Set the file_list attribute with all the daily json files
        in the path_to_project_daily_json_files_directory.
        """
        full_list = os.listdir(self.path_to_project_daily_json_files_directory)
        for file in full_list:
            if file.endswith('.json') and not file.startswith('timeseries'):
                # print('Selected file : ', file)
                self.file_list.append(file)

        # self.file_list = os.listdir(self.path_to_project_daily_json_files_directory)

    def create_timeseries(self):
        """
        Create the timeseries in the time_series_dict attribute by calling add_dailydict_to_timeseries on each file of
        path_to_daily_json_data_folder attribute

        """
        self.set_file_list()
        for file in self.file_list:
            # print('Le FICHIER : ', file, '\n')
            self.load_daily_data(file)
            # print('local dico : ', self.daily_dict)
            self.set_daily_time()
            self.add_dailydict_to_timeseries()
            # print('la série temporelle : ', self.time_series_dict)

    def suppress_zeroes_from_timeseries(self):
        for dates in self.time_series_dict.keys():
            print('\n', dates)
            for processor_type in self.time_series_dict[dates]['processor_type'].keys():
                print(processor_type)
                for subproject in self.time_series_dict[dates]['processor_type'][processor_type].keys():
                    print(subproject, '\nxxxXXXxxx')

    def get_timeseries_name(self):
        """
        Get the name of the timeseries output json file from time_series_dict attribute.

        :return output_name: complete name of the json file in which to dump our time_series_dict
        :rtype output_name: str
        """
        output_name = 'timeseries.json'
        if self.time_series_dict == {}:
            pass
        else:
            dates = list(self.time_series_dict.keys())
            dates.sort()
            debut = dates[0]
            self.project_name = self.time_series_dict[debut]["project"]
            self.machine_name = self.time_series_dict[debut]["machine"]

            self.debut = ''.join(debut.split('-'))
            self.fin = ''.join(dates[-1].split('-'))
            output_name = 'timeseries_' + self.project_name + '_' + self.machine_name + '_from_' + self.debut + '_to_' + self.fin + '.json'
        return output_name

    def backup_former_timeseries(self):
        # # Copy former timeseries to a backup folder
        # origin_path = self.path_to_project_daily_json_files_directory + '/' + 'timeseries'
        # dest_path = self.path_to_project_daily_json_files_directory + '/backups_ts/'
        # for file in glob.glob(origin_path + r'/*.json'):
        #     shutil.copy(origin_path, dest_path)
        pass

    def dump_dict_to_json(self):
        """
        Dumps the complete dictionary to a json file.
        Requires the name to be set before.
        Not tested
        """
        path = self.path_to_project_daily_json_files_directory + '/' + self.get_timeseries_name()# self.get_output_path()
        print('Le path est :', path)

        with open(path, 'w') as outfile:
            json.dump(self.time_series_dict, outfile)
            pass

if __name__ == "__main__":

    print("\nBeginning of execution\n")
    mock_concat = TimeSeriesConcatenator('/home/edupont/ccc_myproject_data/mocks/mock_time_series')
    mock_concat.create_timeseries()
    mock_concat.dump_dict_to_json()

    gencmip6_concat = TimeSeriesConcatenator('/home/edupont/ccc_myproject_data/time_series_gencmip6')
    gencmip6_concat.create_timeseries()
    gencmip6_concat.dump_dict_to_json()
    # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
    # project_to_parse2 = ProjectParser(file_to_parse.set_path_to_individual_projects_directory() + "/project_1.log")
    # project_to_parse2.build_complete_dictionary()
    #
    # project_to_parse2.set_output_name()
    #
    # # string = json.dumps(project_to_parse2.complete_dictionary, indent=2)
    # # print(string)
    # # project_to_parse2.dump_dict_to_json()

    # time_series = TimeSeriesConcatenator('/home/edupont/ccc_myproject_data/time_series')
    #
    # print(os.listdir(time_series.path_to_project_daily_json_files_directory))
    #
    # time_series.create_timeseries()
    # time_series.dump_dict_to_json()

# #     # time_seriesb = TimeSeriesConcatenator('/home/edupont/ccc_myproject_data/time_seriesb')
# #     # time_seriesb.load_daily_data('/Irene_gen0826_20190513.json')
# #     # time_seriesb.set_daily_time()
# #     # print(os.listdir(time_seriesb.path_to_project_daily_json_files_directory))
# #     #
# #     # time_seriesb.create_timeseries()
# #     #
# #     # # time_seriesb.set_daily_time()
# #     # time_seriesb.dump_dict_to_json()
# #
    # complete_project_to_parse1 = ProjectParser(complete_file_to_parse.set_path_to_individual_projects_directory() + "/project_1.log")
    # complete_project_to_parse1.build_complete_dictionary()
    # complete_project_to_parse1.set_output_name()
    # # string2 = json.dumps(complete_project_to_parse1.complete_dictionary, indent=2)
    # # print(string2)
    # complete_project_to_parse1.dump_dict_to_json()

    print("\nEnd of execution\n")
    # print("\nEnd of execution\n")
    # import pandas as pd
    # with open('/home/edupont/ccc_myproject_data/time_seriesb/time_series.json') as file_object:
    #     # store file data in object
    #     # data = json.load(file_object)
    #     df = pd.read_json(file_object)
    #     # string = json.dumps(data, indent= 2)
    #     print(df.head(5))
    #
    # print("\nEnd of execution\n")
