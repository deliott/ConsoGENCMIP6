"""
This module parses the ccc_myproject log file and return a/several structured data file/s
At first it should provide a datetime and a numper of cpu hours on skylake for cmip6 projects.
as well as on equal to the total of hours.

logs are stored on /home/edupont/ccc_myproject_data
and ccc_myproject_20190514.log is one we can work on
"""

import bin.settings as settings
import bin.set_paths as set_paths
import os
import datetime

# @TODO : This is not a parser but somethin to get the files_to_parse's directory and list.
class Parser:

    def __init__(self):
        settings.init()
        # settings.path_to_ccc_myproject_raw_data
        self.path_to_raw_data = "/default/path/"
        # self.working_date = datetime.datetime.now().strftime('%Y%m%d')
        self.list_of_possible_files_to_parse = []

        # #init uses the defined methods in the class. Is this conventional ?
        # self.set_path_to_raw_data()
        # self.get_list_of_possible_files_to_parse()
        # print(self.list_of_possible_files_to_parse)


    def set_path_to_raw_data(self):
        set_paths.set_path_to_raw_data_for_parser()
        self.path_to_raw_data = settings.path_to_ccc_myproject_raw_data

    def get_list_of_possible_files_to_parse(self):
        for _file in os.listdir(self.path_to_raw_data):
            if _file.endswith('.log') and _file.startswith('ccc_myproject_20'):
                self.list_of_possible_files_to_parse.append(_file)
        return


    # def open_raw_data_file(self):
    #     open(self.path_to_raw_data, "r")

