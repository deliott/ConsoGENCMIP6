from bin.ccc_myproject_parser import Parser
# import bin.ccc_myproject_parser as ccc_myproject_parser
import os
import shutil
from bin.ccc_myproject_fileparser import FileParser
from datetime import date


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

    def __init__(self,path_to_one_file_to_parse):
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
        self.file_date = date(1945, 5, 8)
        self.project_deadline = date(1969, 7, 21)
        self.has_subproject = False
        self.subproject = dict()
        self.processor_type_dict = dict()




    def get_project_name(self):
        """Get the name of the project from the split log of ccc_myproject.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in filein:
                if "Accounting" in ligne:
                    self.project_name = ligne.split()[3]
                    break

    def get_project_machine(self):
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

    def get_file_date(self):
        """Get the date of the given project log.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in filein:
                if "Accounting" in ligne:
                    # Convert yyyy-mm-dd format into datetime
                    date_projet = ligne.split(' ')[8].split('-')
                    self.file_date = date(int(date_projet[0]), int(date_projet[1]), int(date_projet[2]))
                    break

    def get_project_deadline(self):
        """Get the deadline of the given project.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in reversed(list(filein)):
                if "deadline" in ligne:
                    # Convert yyyy-mm-dd format into datetime
                    date_deadline = ligne.split(' ')[2].split('-')
                    self.project_deadline = date(int(date_deadline[0]), int(date_deadline[1]), int(date_deadline[2]))
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
                        #
                        subproject_name = ligne.split()[1]
                        # print(subproject_name)
                        name_list.append(subproject_name)
                        store_subproject_name_at_next_line = False
                        # self.subproject[subproject_name] = {} # Add new entry
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
                self.processor_type_dict[processor_name][subproject_name] = {} # Add new entry

    def set_processor_type(self):
        self.get_processor_type_list()
        liste = self.project_processor_list
        for processor_type in liste:
            self.processor_type_dict[processor_type] = {} # Add new entry




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
                            if not key in ligne and 'Subtotal' in ligne:
                                sous_total = ligne.split()[1]
                                self.subproject[key] = {'subtotal': float(sous_total)}
                                self.processor_type_dict[processor][key] = {'subtotal': float(sous_total)}
                                key_detected = False
                                break

                else: # cas sans sous projets
                    for key in self.processor_type_dict[processor].keys():
                        for ligne in filein:
                            if not key_detected:
                                if key in ligne:
                                    key_detected = True
                            if not key in ligne and 'Total' in ligne:
                                sous_total = ligne.split()[1]
                                self.subproject[key] = {'subtotal': float(sous_total)}
                                self.processor_type_dict[processor][key] = {'subtotal': float(sous_total)}
                                key_detected = False
                                break








if __name__ == "__main__":

    print("\nBeginning of execution\n")
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
