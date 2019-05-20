from bin.ccc_myproject_parser import Parser
# import bin.ccc_myproject_parser as ccc_myproject_parser
import os
import shutil


class FileParser():

    def __init__(self):
        """
        :param path_to_file: absolute path of the file that will be parsed, here it is the last one.
        """
        parser = Parser()
        # parser = ccc_myproject_parser.Parser()
        parser.set_path_to_raw_data()
        parser.get_list_of_possible_files_to_parse()

        # print(parser.path_to_raw_data)
        # print(parser.list_of_possible_files_to_parse)

        self.path_to_file = parser.path_to_raw_data + parser.list_of_possible_files_to_parse[-1]

    def __init__(self,path_to_one_file_to_parse):
        """
        :param path_to_file: absolute path of the file that will be parsed, here it is the last one.
        """

        self.path_to_file = path_to_one_file_to_parse
        self.project_name = ""

    def get_project_name(self):
        """method to get the name of the project from the raw log of ccc_myproject"""

    # with open( self.path_to_file, "r") as filein:
    #     # Skip lines until we find project name.
    #     # Then extract script date
    #     for ligne in filein:
    #       if "Accounting" in ligne:
    #         today = ligne.split()[-1]
    #         today = string_to_date(today)
    #         project["machine"] = ligne.split()[5]
    #         project["nodes"]   = ligne.split()[6]
    #         break

    def get_project_last_line(self):
        """Method to get a list of indexes of the lines after the deadlinesof a project are told"""
        end_of_project_line_list = []

        with open(self.path_to_file, "r") as filein:
            line_number = 0
            for ligne in filein:
                line_number = line_number + 1
                if "Project deadline" in ligne:
                    end_of_project_line_list.append(line_number + 1)

        return end_of_project_line_list

    def set_path_to_individual_projects_directory(self):
        """
        Determines the path, and the name of the directory where the splitted ccc_myproject files will be written.

        :return path: path to the directory where to store temp splitted ccc_myproject data
        :rtype path: str
        """

        splitted_path = self.path_to_file.split('/')[:-1]
        new_folder_name = self.path_to_file.split('/')[-1][:-4]
        # add the name of the new directory
        # splitted_path.append(new_folder_name[-1][:-4])
        splitted_path.append(new_folder_name)
        # reconstruct the path to the new directory
        path = '/'.join(splitted_path)
        return path

    def create_individual_projects_directory(self):
        """
        Method to create the directory to store the project splitted ccc_myproject files.
        Not tested.
        :return: None
        """
        dirpath = self.set_path_to_individual_projects_directory()
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)

    def delete_individual_projects_directory(self):
        """
        Method to delete the directory to store the project splitted ccc_myproject files.
        Not tested.
        :return: None
        """
        dirpath = self.set_path_to_individual_projects_directory()
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)


    def copy_project_from_raw_input(self):

        beginning_of_project_line = 0
        project_number = 0

        end_of_project_line = self.get_project_last_line()

        f = open(self.path_to_file,"r")
        while len(end_of_project_line) > 0:
            project_number = project_number + 1
            print(end_of_project_line)
            end_line = end_of_project_line.pop(0)

            path_to_new_file = self.set_path_to_individual_projects_directory() + '/project_' + \
                               str(project_number) + '.log'
            w = open(path_to_new_file, "wt")

            for ligne in range(beginning_of_project_line,end_line):
                line_to_copy = f.readline()
                w.write(str(line_to_copy))



# def __init__(self, date):
    #     """

    #     :param path_to_file: absolute path of the file that will be parsed, here it is the one indicated by the date.
    #     """
    #     self.path_to_file = self.path_to_raw_data + self.get_list_of_possible_files_to_parse()[0]




if __name__ == "__main__":

    print("\nBeginning of execution\n")

    # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
    file_to_parse = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190514.log')


    print(file_to_parse.path_to_file)
    print(file_to_parse.get_project_last_line())
    liste = file_to_parse.path_to_file.split('/')[:-1]


    print(file_to_parse.set_path_to_individual_projects_directory())

    file_to_parse.create_individual_projects_directory()
    file_to_parse.copy_project_from_raw_input()
    # number = 3
    # print(file_to_parse.path_to_file[:(-4)] + '/project_'+ str(number) + '.log')
    # file_to_parse.copy_project_from_raw_imput()
    print("\nEnd of execution\n")


