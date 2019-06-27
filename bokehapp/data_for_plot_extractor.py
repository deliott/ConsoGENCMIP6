
"""
This module regroups the methods for extracting data for the json timeseries
and allow the plot_project_timeseries.py script to use these data in its plots.


"""


import bokehapp.settings as settings
import bokehapp.set_paths as set_paths

import os
import json
import pandas as pd

import datetime

# # Initialise Global Variables
settings.init()
set_paths.set_path_to_timeseries()
# set_paths.set_path_to_plots()


class ProjectData:
    """This class extracts the project data from the json timeseries file"""
    days_in_advance = 3

    def __init__(self, project_name):
        self.project_name = project_name
        self.path_to_project_timeseries = settings.path_to_timeseries + project_name + '/'
        self.project_timeseries_filename = ''
        self.json_data = None
        self.dates = []
        self.deadline = ''
        self.last_date_of_plot = pd.to_datetime('2000-05-31')
        self.processor_list = []
        self.subproject_list = []
        self.processor_dict = {}
        self.subproject_subtotal_dataframe = pd.DataFrame()
        self.allocated_dict = {}
        self.optimal_daily_consumption = 0.
        self.start_date_dict = {}

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
        """
        Set the project processor list.
        Method set_project_timeseries_filename(), load_project_data() and set_dates() have to be executed first.
        :return:
        """
        self.processor_list = list(self.json_data[self.dates[0]]['processor_type'].keys())
        self.processor_list.sort()
        # print('Les dates sont : ', self.dates)
        # print(list(self.json_data[self.dates[0]]['processor_type'].keys()))

    def set_subproject_list(self):
        """
        Set the subproject_list attributes without duplicates
        and distinction between the different processor type of the project.
        """
        for processor in self.processor_list:
            self.subproject_list = self.subproject_list + list(self.json_data[self.dates[0]]
                                                               ['processor_type'][processor]['sous_projet'].keys())
            self.subproject_list = list(set(self.subproject_list))
            self.subproject_list.sort()

    def set_processor_subproject_list(self, processor):
        """
        Set the subproject list attribute with the subprojects associated to the input given kind of processor.
        :param processor: name of the processor whose subproject are to be listed
        :type processor: str
        """
        self.subproject_list = self.subproject_list + list(self.json_data[self.dates[0]]
                                                           ['processor_type'][processor]['sous_projet'].keys())
        self.subproject_list = list(set(self.subproject_list))
        self.subproject_list.sort()

    # def get_subproject_dataframe(self):
    def get_subproject_subtotal_dataframe(self, processor):
        """
        Creates a pandas dataframe with all the subprojects (MIPs) as columns and the consumed hours as data.

        :param processor: name of the processor whose subproject are to treated
        :type processor: str
        :return df:
        :rtype df: pandas data frame
        """
        mips_data_dict = {}
        for mip in self.subproject_list:
            mips_data_dict[mip] = []
            for date in self.dates:  # dates is a sorted list.
                hour_consumed_on_this_day = \
                    self.json_data[date]['processor_type'][processor]['sous_projet'][mip]['subtotal']
                mips_data_dict[mip].append(hour_consumed_on_this_day)

        # print('MIPs Data Dict : ', mips_data_dict)
        df = pd.DataFrame(mips_data_dict)

        return df

    def set_subproject_subtotal_dataframe(self, processor):
        """
        Setter version of get_subproject_subtotal_dataframe.
        Not tested because quite straight forward
        """
        self.subproject_subtotal_dataframe = self.get_subproject_subtotal_dataframe(processor)

    def sort_df_colomns_according_to_biggest_last_value(self):

        self.subproject_subtotal_dataframe = \
            self.subproject_subtotal_dataframe[
                self.subproject_subtotal_dataframe.iloc[-1, :].sort_values(ascending=False).index
            ]

    def add_dates_to_dataframe(self):
        """
        Set the Date column as the index of the dataframe : self.subproject_subtotal_dataframe
        :return: None
        """
        dates_as_datetime = pd.to_datetime(self.dates)
        self.subproject_subtotal_dataframe.insert(0, "Date", dates_as_datetime, True)

    # def add_total_subprojects(self, processor):

    def add_total_subprojects(self):

        """
        Extract the total of subproject cpu time consumption and add column to self.subproject_subtotal_dataframe

        :param processor: Not used
        :return:
        """
        df_tot = self.subproject_subtotal_dataframe.sum(axis=1, numeric_only=True)
        self.subproject_subtotal_dataframe.insert(loc=1,
                                                  value=df_tot,
                                                  column='Total'
                                                  )

#############################
# Methods for Optimal Curve #
#############################

    def set_allocated_dict(self):
        """
        Set the self.allocated_dict attribute with the values extracted from the json_data attribute.
        Must be ran after load_project_data(), set_dates(), set_processor_list().
        :return:
        """

        for processor in self.processor_list:
            # print(processor)
            # print('DATA ==  ', self.json_data[self.dates[0]]['processor_type'][processor]['allocated'])
            self.allocated_dict[processor] = self.json_data[self.dates[0]]['processor_type'][processor]['allocated']

    def set_deadline(self):
        """
        Set the self.allocated_dict attribute with the values extracted from the json_data attribute.
        Must be ran after load_project_data(), set_dates(), set_processor_list().

        :return: None
        """
        self.deadline = self.json_data[self.dates[0]]['project_deadline']

    def set_start_date_to_dict(self, processor, date):
        """
        Add an entry to the self._dict attribute from input.
        :param processor: name of the processor whose start date we will update. Key of the attribute dictionary
        :type processor: str
        :param date: dd-mm-YYYY describing value associated to the processor in the attribute dictionary
        :type date: str
        :return: None
        """
        self.start_date_dict[processor] = date

    def set_last_date(self, days_in_advance):
        """
        Set the last date for the optimal consumption curve.

        :param days_in_advance: numbers of days the last date must be ahead of the last data we have.
        :type days_in_advance: int
        :return: None
        """
        self.last_date_of_plot = max(pd.to_datetime(self.dates)) + datetime.timedelta(days=int(days_in_advance))

    @staticmethod
    def get_list_of_dates_between_boundaries(start, end):
        """

        :param start: str dd-mm-YYYY describing start boundary of the list
        :param end: str dd-mm-YYYY describing end boundary of the list
        :return:
        :rtype: pandas.core.indexes.datetimes.DatetimeIndex
        """
        return pd.date_range(start=pd.to_datetime(start),
                             end=pd.to_datetime(end),
                             freq='D')

    def set_optimal_daily_consumption(self, processor):
        """
        Sets the self.optimal_daily_consumption attributes to the number of hours
        that should be consummed everyday for optimal use of allocation
        The following attributes have to be set up before using this method:
            - self.start_date_dict
            - self.allocated_dict
            - self.deadline
        :return: None
        """
        delta = pd.to_datetime(self.deadline) - pd.to_datetime(self.start_date_dict[processor])
        self.optimal_daily_consumption = self.allocated_dict[processor] / delta.days

    def get_theoretical_optimal_consumption_curve_dataframe(self, processor):
        """
        Creates the dataframe used to plot the optimal consumption curve for a given processor type of the project.
        The following attributes have to be set up before using this method:
            - self.start_date_dict
            - self.last_date
            - self.optimal_daily_consumption

        :param processor: str, Name of the processor.
        :return: dict with the data to plot the optimal consumption curve
        """
        date_list = self.get_list_of_dates_between_boundaries(self.start_date_dict[processor], self.last_date_of_plot)

        print('Nombres d\'heures à consommer par jour : ', round(self.optimal_daily_consumption, 0))

        liste_consomation_optimale = []
        for indice in range(len(date_list)):
            liste_consomation_optimale.append(indice * self.optimal_daily_consumption)
        return {'Date': date_list, 'Conso_Optimale': liste_consomation_optimale}



    def run_data_for_plot_extractor(self, processor, start_date):
        """
        Sum up all the previous methods to output the dataframe and instanciate all the attributes.
        Only methods to run before plotting a graph.

        :return: measured and optimal dataframe
        """

        self.set_project_timeseries_filename()
        self.load_project_data()
        self.set_dates()
        self.set_processor_list()
        self.set_processor_subproject_list(processor)
        self.set_subproject_subtotal_dataframe(processor)
        self.sort_df_colomns_according_to_biggest_last_value()
        self.add_dates_to_dataframe()
        self.add_total_subprojects()
        self.set_allocated_dict()
        self.set_deadline()


        self.set_last_date(ProjectData.days_in_advance)

        self.set_start_date_to_dict(processor, start_date)  # used to be 'Skylake' and '2019-05-01' for gencmip6
        self.set_optimal_daily_consumption(processor)

        dfOpti = self.get_theoretical_optimal_consumption_curve_dataframe(processor)

        return self.subproject_subtotal_dataframe, dfOpti


