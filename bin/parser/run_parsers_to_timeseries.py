import os
import shutil
# from bin.ccc_myproject_parser import Parser
from bin.parser.ccc_myproject_fileparser import FileParser
from bin.parser.ccc_myproject_projectparser import IreneProjectParser
from bin.parser.cpt_projectparser import AdaProjectParser

from bin.parser.concatenate_into_time_serie import TimeSeriesConcatenator


import bin.consomation.settings as settings
import bin.consomation.set_paths as set_paths

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

def get_list_of_cpt_raw_logs(path):
    """

    :param path: path to raw_data logs directory
    :return liste_of_files:
    """

    liste = os.listdir(path)
    liste_of_files = []
    for name in liste :
        if 'cpt_' in name and name.endswith('.log'):
            liste_of_files.append(name)
    return liste_of_files

def get_list_of_projects(path):
    """
    Give the list of projects names corresponding to the raw log in available at path destination
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
    set_paths.set_path_to_timeseries()
    print('Initialisation réussite\n')

    # raw_data_path = '/home/edupont/ccc_myproject_data/'
    raw_ccc_data_path = settings.path_to_ccc_myproject_raw_data

    print('raw_ccc_data_path = ', raw_ccc_data_path)

    raw_cpt_data_path = settings.path_to_cpt_raw_data


    ccc_file_liste = get_list_of_ccc_raw_logs(raw_ccc_data_path)
    cpt_file_liste = get_list_of_cpt_raw_logs(raw_cpt_data_path)

    file_dict = dict()
    file_dict['ccc'] = ccc_file_liste
    file_dict['cpt'] = cpt_file_liste


    print('cptfilelist = ', cpt_file_liste)

    project_daily_jsons_path_dict = dict()

    for file_name in cpt_file_liste: #[0:5]:

        project_to_parse = AdaProjectParser(raw_cpt_data_path + file_name)
        project_to_parse.build_complete_dictionary()
        project_to_parse.set_output_name()

        # Create the appropriate folders to store the daily jsons, (if does not exist)
        daily_jsons_project_directory_list = os.listdir(raw_cpt_data_path + 'daily_jsons/')

        project_daily_jsons_path = raw_cpt_data_path + 'daily_jsons/' + project_to_parse.project_name
        if project_to_parse.project_name not in daily_jsons_project_directory_list:
            os.makedirs(project_daily_jsons_path)

        # Dump the daily json parsed files into the appropriate folders.
        project_to_parse.dump_dict_to_json(project_daily_jsons_path + '/' + project_to_parse.output_name)

        # Store into dictionary the project names and path where daily json data is dumped.
        if project_to_parse.project_name not in [*project_daily_jsons_path_dict.keys()]:
            project_daily_jsons_path_dict[project_to_parse.project_name] = project_daily_jsons_path #+ '/' + project_to_parse.output_name


    for file_name in ccc_file_liste: #[0:5]:
        # Create directories and split the log into project logs
        file_to_parse = FileParser(raw_ccc_data_path + file_name)
        # print('new_directory : ', file_to_parse.set_path_to_individual_projects_directory())
        file_to_parse.create_individual_projects_directory()
        file_to_parse.copy_project_from_raw_input()

        # Parse the different projects

        projects_path = file_to_parse.set_path_to_individual_projects_directory()

        project_list = get_list_of_projects(projects_path)


        for name_of_project_file in project_list:
            # print('PROJECT NAME : ', name_of_project_file)
            project_to_parse = IreneProjectParser(projects_path + '/' + name_of_project_file)
            project_to_parse.build_complete_dictionary()
            project_to_parse.set_output_name()

            # Create the appropriate folders to store the daily jsons, (if does not exist)
            daily_jsons_project_directory_list = os.listdir(raw_ccc_data_path + 'daily_jsons/')
            project_daily_jsons_path = raw_ccc_data_path + 'daily_jsons/' + project_to_parse.project_name
            if project_to_parse.project_name not in daily_jsons_project_directory_list:
                os.makedirs(project_daily_jsons_path)


            # Dump the daily json parsed files into the appropriate folders.
            project_to_parse.dump_dict_to_json(project_daily_jsons_path + '/' + project_to_parse.output_name)

            # Store into dictionary the project names and path where daily json data is dumped.
            if project_to_parse.project_name not in [*project_daily_jsons_path_dict.keys()]:
                project_daily_jsons_path_dict[project_to_parse.project_name] = project_daily_jsons_path #+ '/' + project_to_parse.output_name



    for name_of_project_file in [*project_daily_jsons_path_dict.keys()]:
        # print('PROJECT PATH NAME  : ', project_timeseries_path)

        project_concat = TimeSeriesConcatenator(project_daily_jsons_path_dict[name_of_project_file])
        project_concat.create_timeseries()
        project_concat.suppress_zeroes_from_timeseries()
        # project_concat.dump_dict_to_json()

        if name_of_project_file not in os.listdir(settings.path_to_timeseries):
            os.makedirs(settings.path_to_timeseries + name_of_project_file)

        project_concat.dump_dict_to_json(settings.path_to_timeseries + name_of_project_file)

    print("\nFin de l'Execution du parser et de la creation de la série temporelle JSON\n")
    print("\nEnd of execution\n")

