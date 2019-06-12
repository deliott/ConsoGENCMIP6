
"""
This module regroups the methods for extracting data for the json timeseries
and allow the plot_project_timeseries.py script to use these data in its plots.


"""


import bin.consomation.settings as settings
import bin.consomation.set_paths as set_paths

import os
import json

# # Initialise Global Variables
settings.init()
set_paths.set_path_to_timeseries()
# set_paths.set_path_to_plots()

class ProjectData():
    """This class extracts the project data from the json timeseries file"""

    def __init__(self, project_name):
        self.path_to_project_timeseries = settings.path_to_timeseries + project_name + '/'
        self.project_timeseries_filename = ''
        self.json_data = None
        self.dates = []
        self.processor_list = []
        self.subproject_list = []
        self.processor_dict = {}

    def set_project_timeseries_filename(self):
        """
        Sets the self.project_timeseries_filename attribute by checking the folder pointed by
        the self.path_to_timeseries attribute.

        :return:
        """
        file_list = os.listdir(self.path_to_project_timeseries)
        # Sorting is done to get the last timeseries name in the list.
        # We assume this is enough, i.e. the is no modification manual modification of the dates.
        file_list.sort()
        for file in file_list:
            last_piece = file.split('.')[0].split('_')[-1]
            if last_piece.isdigit() and 'timeseries' in file:
                self.project_timeseries_filename = file


    def load_project_data(self):
        """Load the data in the timeseries files. Not tested"""
        with open(self.path_to_project_timeseries + self.project_timeseries_filename) as file:
            self.json_data = json.load(file)

    def set_dates(self):
        self.dates = list(self.json_data.keys())
        self.dates.sort()

    def set_processor_list(self):
        self.processor_list = list(self.json_data[self.dates[0]]['processor_type'].keys())
        self.processor_list.sort()
        # print('Les dates sont : ', self.dates)
        # print(list(self.json_data[self.dates[0]]['processor_type'].keys()))

    def set_subproject_list(self):
        """Set the subproject_list attributes without duplicates and distinction between the different processor type of the project"""
        for processor in self.processor_list:
            self.subproject_list = self.subproject_list + list(self.json_data[self.dates[0]]
                                                               ['processor_type'][processor]['sous_projet'].keys())
            self.subproject_list = list(set(self.subproject_list))
            self.subproject_list.sort()

    def set_processor_subproject_list(self,processor):
        """Set the subproject list attribute with the subprojects associated to the input given kind of processor"""
        self.subproject_list = self.subproject_list + list(self.json_data[self.dates[0]]
                                                           ['processor_type'][processor]['sous_projet'].keys())
        self.subproject_list = list(set(self.subproject_list))
        self.subproject_list.sort()






# mips = list(jl[self.dates[0]]['processor_type']['Skylake']['sous_projet'].keys())

