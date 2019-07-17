# import bin.ccc_myproject_parser as ccc_myproject_parser
from bin.parser.ccc_myproject_fileparser import FileParser

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


class IreneProjectParser(FileParser):

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
        """Set the subprojects name in the subproject dictionary datastructure of the class"""
        processor_list = self.project_processor_list
        liste = self.get_subproject_namelist()
        for processor_name in processor_list:
            self.processor_type_dict[processor_name]['sous_projet'] = {}
            for subproject_name in liste:
                # self.subproject[subproject_name] = {} # Add new entry
                self.processor_type_dict[processor_name]['sous_projet'][subproject_name] = {}  # Add new entry

    def set_processor_type(self):
        """Add a new empty dictionary in the processor_type_dict attribute.
         Do it for each processor type in the list project_processor_list attribute."""
        self.get_processor_type_list()
        liste = self.project_processor_list
        for processor_type in liste:
            self.processor_type_dict[processor_type] = {}  # Add new entry

    def set_subtotals(self):
        """Set the subprojects subtotal in the subproject dictionary datastructure of the class"""
        with open(self.path_to_project_file, "r") as filein:
            key_detected = False

            for processor_name in self.processor_type_dict.keys():
                if self.has_subproject:  # cas avec sous projets
                    for key in self.processor_type_dict[processor_name]['sous_projet'].keys():
                        for ligne in filein:
                            if not key_detected:
                                if key in ligne:
                                    key_detected = True
                            if key not in ligne and 'Subtotal' in ligne:
                                sous_total = ligne.split()[1]
                                self.subproject[key] = {'subtotal': float(sous_total)}
                                self.processor_type_dict[processor_name]['sous_projet'][key] = {'subtotal': float(sous_total)}
                                key_detected = False
                                break

                else:  # cas sans sous projets
                    for key in self.processor_type_dict[processor_name]['sous_projet'].keys():
                        for ligne in filein:
                            if not key_detected:
                                if key in ligne:
                                    key_detected = True
                            if key not in ligne and 'Total' in ligne:
                                sous_total = ligne.split()[1]
                                self.subproject[key] = {'subtotal': float(sous_total)}
                                self.processor_type_dict[processor_name]['sous_projet'][key] = {'subtotal': float(sous_total)}
                                key_detected = False
                                break

    def set_total(self):
        """Set the total consumption to each processor on a project in the processor_type_dict

        has to be run after set_subtotals"""
        with open(self.path_to_project_file, "r") as filein:
            local_processor = ''
            for ligne in filein:
                if 'Accounting' in ligne:
                    local_processor = ligne.split()[6]
                if "Total" in ligne:
                    total_value = float(ligne.split()[1])
                    self.processor_type_dict[local_processor]['total'] = total_value

    def set_allocated(self):
        """Set the allocated time value to each processor on a project in the processor_type_dict

        has to be run after set_subtotals"""
        with open(self.path_to_project_file, "r") as filein:
            local_processor = ''
            for ligne in filein:
                if 'Accounting' in ligne:
                    local_processor = ligne.split()[6]
                if "Allocated" in ligne:
                    allocated_value = float(ligne.split()[1])
                    self.processor_type_dict[local_processor]['allocated'] = allocated_value

    def set_login_for_a_subproject(self, subproject_name):
        """Set the login_conso dictionary inside the data structure for the given subproject.
        Has to be called after self.set_subtotals().
        Modify the processor_type_dict attribute
        """
        with open(self.path_to_project_file, "r") as filein:
            # for each processor in the dictionary

            for processor_name in self.processor_type_dict.keys():
                # create an empty dictionary to store the login conso data
                self.processor_type_dict[processor_name]['sous_projet'][subproject_name]['login_conso'] = {}
                current_file_processor = ''

            if self.has_subproject:
                for ligne in filein:
                    # first set the processor the read lines are about
                    if "Accounting" in ligne:
                        current_file_processor = ligne.split(' ')[6]
                    if len(ligne.split()) > 1 and ligne.split()[1] == subproject_name:
                        # set a new login entry in the dict and associates its consumption data
                        self.processor_type_dict[current_file_processor]['sous_projet']\
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
                        self.processor_type_dict[current_file_processor]['sous_projet']\
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
        self.set_total()
        self.set_allocated()

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

        # outfile = '/'.join(self.path_to_project_file.split('/')[:-1]) + '/' + self.output_name
        outfile = '/'.join(self.path_to_project_file.split('/')[:-2]) + '/daily_jsons/' + self.output_name
        return outfile

    def dump_dict_to_json(self):
        """dumps the complete dictionary to a json file.
        requires the name to be set before."""
        path = self.get_output_path()
        with open(path, 'w') as outfile:
            json.dump(self.complete_dictionary, outfile)

    def dump_dict_to_json(self, dump_path):
        """dumps the complete dictionary to a json file."""
        # path = self.get_output_path()
        with open(dump_path, 'w') as outfile:
            json.dump(self.complete_dictionary, outfile)

# if __name__ == "__main__":
#
#     print("\nBeginning of execution\n")
#     # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mocks/mock_ccc_myproject.log')
#     file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mocks/mock_ccc_myproject_20190514.log')
#     # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190516.log')
#     project_to_parse2 = ProjectParser(file_to_parse.set_path_to_individual_projects_directory() + "/project_2.log")
#     project_to_parse2.build_complete_dictionary()
#
#     project_to_parse2.set_output_name()
#
#     # string = json.dumps(project_to_parse2.complete_dictionary, indent=2)
#     # print(string)
#     project_to_parse2.dump_dict_to_json()
#
#     # complete_file_to_parse = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190515.log')
#
#     complete_file_to_parse = FileParser('/home/edupont/ccc_myproject_data/test_data/p86caub_ccc_myproject.txt')
#     complete_project_to_parse1 = ProjectParser(complete_file_to_parse.set_path_to_individual_projects_directory() + "/project_2.log")
#     complete_project_to_parse1.build_complete_dictionary()
#     complete_project_to_parse1.set_output_name()
#
#     complete_project_to_parse1.dump_dict_to_json()
#
#
#
#     print("\nEnd of execution\n")
