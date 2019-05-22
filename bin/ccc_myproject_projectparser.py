from bin.ccc_myproject_parser import Parser
# import bin.ccc_myproject_parser as ccc_myproject_parser
import os
import shutil
from bin.ccc_myproject_fileparser import FileParser
from datetime import date

import json

"""
The objective of this parser is to create a json file with the data extracted from the project log files.

output should look like this : 
{
  "date": "2019-05-13",
  "projet": "gencmip6",
  "processor_type": {
    "Skylake": {
      "total": 984797.89,
      "alllocated": 27070000,
      "sous_projets": {
        "dcpcmip6": {
          "logins_conso": {
            "pierre": 752.5,
            "paul": 125.4,
            "jacques": 0
          },
          "subtotal": 877.9
        },
        "geocmip6": {
          "logins_conso": {
            "pierre": 552.4,
            "andre": 125.4,
            "jacques": 0
          },
          "subtotal": 677.8
        }
      }
    }    
  },
  "machine": "Irene",
  "project_deadline": "2020-05-02"
}
"""


class ProjectParser(FileParser):

    def __init__(self, path_to_one_file_to_parse):
        """
        :param path_to_one_file_to_parse: absolute path of the file that will be parsed, here it is the last one.
        """
        # super(ProjectParser, self).__init__(path_to_one_file_to_parse)
        # self.path_to_file = "" #Has to be solved if we have one or two path arguments.
        #                         Knowing the this on won't be used here
        self.path_to_project_file = path_to_one_file_to_parse
        self.project_name = ""
        self.project_machine = ""
        self.project_processor_list = []
        # self.file_date = ''
        self.file_date = '1945-05-08'
        self.project_deadline = '1969-07-21'
        self.has_subproject = False
        self.subproject = dict()
        self.processor_type_dict = dict()

        self.complete_dictionary = dict()

        self.output_name = 'default_output_name'

    def set_project_name(self):
        """Get the name of the project from the split log of ccc_myproject.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in filein:
                if "Accounting" in ligne:
                    self.project_name = ligne.split()[3]
                    break

    def set_project_machine(self):
        """Get the name of the machine on which the project is ran from the splitted log of ccc_myproject.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in filein:
                if "Accounting" in ligne:
                    self.project_machine = ligne.split(' ')[5]
                    break

    def get_processor_type_list(self):
        """Get the list of the type of processor for a given project.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in filein:
                if "Accounting" in ligne:
                    self.project_processor_list.append(ligne.split(' ')[6])

    # def set_file_date(self):
    #     """Get the date of the given project log.
    #     """
    #     with open(self.path_to_project_file, "r") as filein:
    #         for ligne in filein:
    #             if "Accounting" in ligne:
    #                 # Convert yyyy-mm-dd format into datetime
    #                 date_projet = ligne.split(' ')[8].split('-')
    #                 self.file_date = date(int(date_projet[0]), int(date_projet[1]), int(date_projet[2]))
    #                 break

    def set_file_date(self):
        """Get the date of the given project log.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in filein:
                if "Accounting" in ligne:
                    # Convert yyyy-mm-dd format into datetime
                    date_projet = ligne.split(' ')[8]
                    self.file_date = date_projet.strip()
                    break

    # def set_project_deadline(self):
    #     """Get the deadline of the given project.
    #     """
    #     with open(self.path_to_project_file, "r") as filein:
    #         for ligne in reversed(list(filein)):
    #             if "deadline" in ligne:
    #                 # Convert yyyy-mm-dd format into datetime
    #                 date_deadline = ligne.split(' ')[2].split('-')
    #                 self.project_deadline = date(int(date_deadline[0]), int(date_deadline[1]), int(date_deadline[2]))
    #                 break

    def set_project_deadline(self):
        """Get the deadline of the given project.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in reversed(list(filein)):
                if "deadline" in ligne:
                    # Convert yyyy-mm-dd format into datetime
                    date_deadline = ligne.split(' ')[2]
                    self.project_deadline = date_deadline.strip()
                    break

    def check_has_subproject(self):
        """Check if the project has subprojects (ex : gencmip6 has mips).
        Update the self.has_subproject attribute to True if there are any.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in filein:
                if "Login" in ligne:
                    liste_mots = ligne.split()
                    if liste_mots[1] == 'Account':
                        self.has_subproject = True
                    break

    def get_subproject_namelist(self):
        """Get the names of the project from the split log of ccc_myproject.
        Warning : if project has no subproject, name has to be set (get_project_name() method)
                  before running this function.
        :returns name_list: List of the names of the subprojects.
        """
        name_list = []
        if not self.has_subproject:
            name_list.append(self.project_name)
        else:
            with open(self.path_to_project_file, "r") as filein:
                store_subproject_name_at_next_line = False
                for ligne in filein:
                    if store_subproject_name_at_next_line:
                        subproject_name = ligne.split()[1]
                        name_list.append(subproject_name)
                        store_subproject_name_at_next_line = False
                    elif "Login" in ligne:
                        store_subproject_name_at_next_line = True

        return name_list

    def set_subproject(self):
        """Sets the subprojects name in the subproject dictionary datastructure of the class"""
        processor_list = self.project_processor_list
        liste = self.get_subproject_namelist()
        for processor_name in processor_list:
            for subproject_name in liste:
                # self.subproject[subproject_name] = {} # Add new entry
                self.processor_type_dict[processor_name][subproject_name] = {}  # Add new entry

    def set_processor_type(self):
        self.get_processor_type_list()
        liste = self.project_processor_list
        for processor_type in liste:
            self.processor_type_dict[processor_type] = {}  # Add new entry

    def set_subtotals(self):
        """Sets the subprojects subtotal in the subproject dictionary datastructure of the class"""
        with open(self.path_to_project_file, "r") as filein:
            key_detected = False

            for processor in self.processor_type_dict.keys():
                if self.has_subproject:  # cas avec sous projets
                    for key in self.processor_type_dict[processor].keys():
                        for ligne in filein:
                            if not key_detected:
                                if key in ligne:
                                    key_detected = True
                            if key not in ligne and 'Subtotal' in ligne:
                                sous_total = ligne.split()[1]
                                self.subproject[key] = {'subtotal': float(sous_total)}
                                self.processor_type_dict[processor][key] = {'subtotal': float(sous_total)}
                                key_detected = False
                                break

                else:  # cas sans sous projets
                    for key in self.processor_type_dict[processor].keys():
                        for ligne in filein:
                            if not key_detected:
                                if key in ligne:
                                    key_detected = True
                            if key not in ligne and 'Total' in ligne:
                                sous_total = ligne.split()[1]
                                self.subproject[key] = {'subtotal': float(sous_total)}
                                self.processor_type_dict[processor][key] = {'subtotal': float(sous_total)}
                                key_detected = False
                                break

    def set_login_for_a_subproject(self, subproject_name):
        """Set the login_conso dictionary inside the data structure for the given subproject.
        Has to be called after self.set_subtotals().
        """
        with open(self.path_to_project_file, "r") as filein:
            # for each processor in the dictionary

            for key in self.processor_type_dict.keys():
                # create an empty dictionary to store the login conso data
                self.processor_type_dict[key][subproject_name]['login_conso'] = {}
                current_file_processor = ''

            if self.has_subproject:
                for ligne in filein:
                    # first set the processor the read lines are about
                    if "Accounting" in ligne:
                        current_file_processor = ligne.split(' ')[6]
                    if len(ligne.split()) > 1 and ligne.split()[1] == subproject_name:
                        # set a new login entry in the dict and associates its consumption data
                        self.processor_type_dict[current_file_processor]\
                            [subproject_name]['login_conso'][ligne.split()[0]] = float(ligne.split()[2])
            else:
                for ligne in filein:
                    # first set the processor the read lines are about
                    if "Accounting" in ligne:
                        current_file_processor = ligne.split(' ')[6]
                    # test to detect the logins lines in the project log file.
                    #   check if lines has at least two words
                    #  and
                    #   check if first word is only lower case (and therefore is a login) (test is a bit weak)
                    if len(ligne.split()) > 1 and ligne.split()[0].islower():
                        # set a new login entry in the dict and associates its consumption data
                        self.processor_type_dict[current_file_processor]\
                            [subproject_name]['login_conso'][ligne.split()[0]] = float(ligne.split()[1])

    def set_login_for_all_subprojects(self):
        """Set the login_conso dictionary inside the data structure
        Call of _login_for_a_subproject on all the subprojects."""
        project_list = self.get_subproject_namelist()
        for project in project_list:
            self.set_login_for_a_subproject(project)

    def build_complete_dictionary(self):

        self.check_has_subproject()
        self.set_project_name()
        self.set_processor_type()
        self.set_subproject()

        self.set_subtotals()
        self.set_login_for_all_subprojects()

        self.set_file_date()
        self.set_project_deadline()
        self.set_project_machine()

        self.complete_dictionary['date'] = self.file_date
        self.complete_dictionary['project'] = self.project_name
        self.complete_dictionary['project_deadline'] = self.project_deadline
        self.complete_dictionary['machine'] = self.project_machine
        self.complete_dictionary['processor_type'] = self.processor_type_dict

    def set_output_name(self):
        """Set the output name attribute before dumping the data structure to a .json file"""
        self.output_name = self.project_machine + '_' + self.project_name + '_' \
                           + ''.join(self.file_date.split('-')) + '.json'

    def get_output_path(self):

        outfile = '/'.join(self.path_to_project_file.split('/')[:-1]) + '/' + self.output_name
        return outfile

    def dump_dict_to_json(self):
        """dumps the complete dictionary to a json file.
        requires the name to be set before."""
        path = self.get_output_path()
        with open(path, 'w') as outfile:
            json.dump(self.complete_dictionary, outfile)

if __name__ == "__main__":

    print("\nBeginning of execution\n")
    file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
    project_to_parse2 = ProjectParser(file_to_parse.set_path_to_individual_projects_directory() + "/project_1.log")


    project_to_parse2.build_complete_dictionary()

    project_to_parse2.set_output_name()

    string = json.dumps(project_to_parse2.complete_dictionary,indent = 2)
    # print(string)

    # project_to_parse2.dump_dict_to_json()

    complete_file_to_parse = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log')
    complete_project_to_parse1 = ProjectParser(complete_file_to_parse.set_path_to_individual_projects_directory() + "/project_1.log")
    complete_project_to_parse1.build_complete_dictionary()
    complete_project_to_parse1.set_output_name()
    string2 = json.dumps(complete_project_to_parse1.complete_dictionary,indent = 2)
    print(string2)
    # project_to_parse2.check_has_subproject()
    # project_to_parse2.get_project_name()
    # project_to_parse2.set_processor_type()
    # project_to_parse2.set_subproject()
    # project_to_parse2.set_subtotals()
    # print(project_to_parse2.has_subproject)
    # project_to_parse2.set_login_for_a_subproject('gen0826')

    # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
    # project_to_parse1 = ProjectParser(self.file_to_parse.set_path_to_individual_projects_directory() +
    #                                            "/project_1.log")

    # # # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
    # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190514.log')
    # print(file_to_parse.path_to_project_file)
    # # print(file_to_parse.get_project_last_line())
    # project_to_parse = ProjectParser(file_to_parse.set_path_to_individual_projects_directory() + "/project_2.log")
    # print(project_to_parse.path_to_project_file)
    # project_to_parse.get_project_name()
    # print(project_to_parse.project_name)
    # # liste = file_to_parse.path_to_file.split('/')[:-1]
    # # print(file_to_parse.set_path_to_individual_projects_directory())
    # #
    # # file_to_parse.create_individual_projects_directory()
    # # file_to_parse.copy_project_from_raw_input()

    print("\nEnd of execution\n")
