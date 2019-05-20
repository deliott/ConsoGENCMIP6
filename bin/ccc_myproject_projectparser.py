from bin.ccc_myproject_parser import Parser
# import bin.ccc_myproject_parser as ccc_myproject_parser
import os
import shutil
from bin.ccc_myproject_fileparser import FileParser
from datetime import date


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

    def get_project_name(self):
        """Get the name of the project from the split log of ccc_myproject.
        """
        with open(self.path_to_project_file, "r") as filein:
            for ligne in filein:
                if "Accounting" in ligne:
                    self.project_name = ligne.split(' ')[3]
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


if __name__ == "__main__":

    print("\nBeginning of execution\n")

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
