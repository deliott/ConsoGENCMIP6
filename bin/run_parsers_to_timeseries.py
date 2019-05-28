import os
import shutil
# from bin.ccc_myproject_parser import Parser
from bin.ccc_myproject_fileparser import FileParser
from bin.ccc_myproject_projectparser import ProjectParser

from bin.concatenate_into_time_serie import TimeSeriesConcatenator


import bin.settings as settings
import bin.set_paths as set_paths

# Initialise Global Variables
settings.init()
set_paths.set_path_to_timeseries()


def get_list_of_ccc_raw_logs(path):
    """

    :param path: path to raw_data logs directory
    :return liste_of_files:
    """

    liste = os.listdir(path)
    liste_of_files = []
    for name in liste :
        if 'ccc_myproject' in name and name.endswith('.log'):
            liste_of_files.append(name)
    return liste_of_files

def get_list_of_projects(path):
    """

    :param path: path to raw_data logs directory
    :return liste_of_files:
    """

    liste = os.listdir(path)
    liste_of_files = []
    for name in liste:
        if name.endswith('.log'):
            liste_of_files.append(name)
    return liste_of_files


if __name__ == "__main__":


    print("\nBeginning of execution\n")
    print("Don't forget to update the raw logs database : \n    On ciclad run : dataCCCMYPROJECTS_update and give"
          "password, \n    On local machine run dataCCCMYPROJECTS_update \nThis will update our "
          "ccc_myproject log repository.\n")
    print("So far this script seems to work with data from ccc_myproject run on shared account.")



    # Initialise Global Variables
    print('\nInitialisation of Global Variables (paths)\n')

    settings.init()
    set_paths.set_path_to_raw_data_for_parser()
    print('Initialisation réussite\n')

    # raw_data_path = '/home/edupont/ccc_myproject_data/'
    raw_data_path = settings.path_to_ccc_myproject_raw_data

    file_liste = get_list_of_ccc_raw_logs(raw_data_path)

    projects_name_list = []

    for file_name in file_liste:
        # Create directories and split the lob into project logs
        file_to_parse = FileParser(raw_data_path + file_name)
        # print('new_directory : ', file_to_parse.set_path_to_individual_projects_directory())
        file_to_parse.create_individual_projects_directory()
        file_to_parse.copy_project_from_raw_input()

        # Parse the different projects

        projects_path = file_to_parse.set_path_to_individual_projects_directory()
        project_list =get_list_of_projects(projects_path)


        for name_of_project_file in project_list:
            # print('PROJECT NAME : ', name_of_project_file)
            project_to_parse = ProjectParser(projects_path + '/' + name_of_project_file)
            project_to_parse.build_complete_dictionary()
            project_to_parse.set_output_name()
            # print(project_to_parse.project_name)
            if project_to_parse.project_name not in projects_name_list:
                projects_name_list.append(project_to_parse.project_name)

            project_to_parse.dump_dict_to_json()


            # Create the appropriate folders to store the daily jsons, (if does not exist)
            time_series_project_directory_list = os.listdir(raw_data_path + 'timeseries/')

            project_timeseries_path = raw_data_path + 'timeseries/' + project_to_parse.project_name
            if project_to_parse.project_name not in time_series_project_directory_list:
                os.makedirs(project_timeseries_path)

            # Cut and paste the json files to the appropriate timeseries file
            # @TODO : (should write them directly in the right place ... )

            shutil.move(project_to_parse.get_output_path(), project_timeseries_path + '/' + project_to_parse.output_name)

    for name_of_project_file in projects_name_list:

        project_timeseries_path = raw_data_path + 'timeseries/' + name_of_project_file
        # print('PROJECT PATH NAME  : ', project_timeseries_path)

        project_concat = TimeSeriesConcatenator(project_timeseries_path)
        project_concat.create_timeseries()
        project_concat.suppress_zeroes_from_timeseries()
        project_concat.dump_dict_to_json()

    print("\nEnd of execution\n")
