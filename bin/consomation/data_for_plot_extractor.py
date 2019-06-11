
"""
This module regroups the methods for extracting data for the json timeseries
and allow the plot_project_timeseries.py script to use these data in its plots.


"""


import bin.consomation.settings as settings
import bin.consomation.set_paths as set_paths

import os

# # Initialise Global Variables
settings.init()
set_paths.set_path_to_timeseries()
# set_paths.set_path_to_plots()

class ProjectData():
    """This class extracts the project data from the json timeseries file"""

    def __init__(self, project_name):
        self.path_to_project_timeseries = settings.path_to_timeseries + project_name + '/'
        self.project_timeseries_filename = ''

    def set_project_timeseries_filename(self):

        file_list = os.listdir(self.path_to_project_timeseries)
        # Sorting is done to get the last timeseries name in the list.
        # We assume this is enough, i.e. the is no modification manual modification of the dates.
        file_list.sort()
        for file in file_list:
            last_piece = file.split('.')[0].split('_')[-1]
            if last_piece.isdigit() and 'timeseries' in file:
                self.project_timeseries_filename = file
