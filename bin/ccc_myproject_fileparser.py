from bin.ccc_myproject_parser import Parser
# import bin.ccc_myproject_parser as ccc_myproject_parser
import os
import shutil


class FileParser:

    def __init__(self):
        # """
        # :param path_to_file: absolute path of the file that will be parsed, here it is the last one.
        # """
        parser = Parser()
        # parser = ccc_myproject_parser.Parser()
        parser.set_path_to_raw_data()
        parser.get_list_of_possible_files_to_parse()
        # print(parser.path_to_raw_data)
        # print(parser.list_of_possible_files_to_parse)
        self.path_to_file = parser.path_to_raw_data + parser.list_of_possible_files_to_parse[-1]


    def __init__(self,path_to_one_file_to_parse):
        """
        :param path_to_one_file_to_parse: absolute path of the file that will be parsed, here it is the last one.
        """
        self.path_to_file = path_to_one_file_to_parse

    def get_projects_last_line_list(self):
        """Get a list of indexes of the lines after the deadlines of a project are told"""
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
        Determine the path, and the name of the directory where the splitted ccc_myproject files will be written.

        :return path: path to the directory where to store temp splitted ccc_myproject data
        :rtype path: str
        """

        splitted_path = self.path_to_file.split('/')[:-1]
        new_folder_name = self.path_to_file.split('/')[-1][:-4]
        # Add the name of the new directory
        splitted_path.append(new_folder_name)
        # Reconstruct the path to the new directory
        path = '/'.join(splitted_path)
        return path

    def create_individual_projects_directory(self):
        """
        Create the directory to store the project splitted ccc_myproject files.
        Not tested.
        :return: None
        """
        dirpath = self.set_path_to_individual_projects_directory()
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)

    def delete_individual_projects_directory(self):
        """
        Delete the directory to store the project splitted ccc_myproject files. If it exists.
        Not tested.
        :return: None
        """
        dirpath = self.set_path_to_individual_projects_directory()
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)

    def copy_project_from_raw_input(self):
        """
        Split the raw ccc_my_project data into subfiles, one per project
        Not tested.
        :return: None
        """
        project_number = 0
        end_of_projects_line_list = self.get_projects_last_line_list()
        length_of_project_to_parse_list = [end_of_projects_line_list[0]] + [x - y for x, y in
                                                                            zip(end_of_projects_line_list[1:],
                                                                                end_of_projects_line_list)]
        # print(length_of_project_to_parse_list)
        try:
            raw_ccc_myproject_file = open(self.path_to_file, "r")
        except IOError:
            print("Failed to open " + self.path_to_file + " file in copy_project_from_raw_input. ")
        while len(length_of_project_to_parse_list) > 0:
            project_number = project_number + 1
            path_to_new_file = self.set_path_to_individual_projects_directory() + '/project_' + \
                               str(project_number) + '.log'

            # Update of the length of the file
            length_of_project_to_parse = length_of_project_to_parse_list.pop(0)
            # print(length_of_project_to_parse_list)

            try:
                project_specific_file = open(path_to_new_file, "wt")
            except IOError:
                print("Failed to open " + path_to_new_file + " file in copy_project_from_raw_input. ")

            for ligne in range(length_of_project_to_parse):
                line_to_copy = raw_ccc_myproject_file.readline()
                project_specific_file.write(str(line_to_copy))
            project_specific_file.close()

        raw_ccc_myproject_file.close()



if __name__ == "__main__":

    print("\nBeginning of execution\n")

    # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/mock_ccc_myproject.log')
    # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/test_data/oboucher_ccc_myproject.txt')
    file_to_parse = FileParser('/home/edupont/ccc_myproject_data/test_data/p86caub_ccc_myproject.txt')
    # file_to_parse = FileParser('/home/edupont/ccc_myproject_data/ccc_myproject_20190514.log')
    print(file_to_parse.path_to_file)
    print(file_to_parse.get_projects_last_line_list())

    liste = file_to_parse.path_to_file.split('/')[:-1]
    print(liste)
    print(file_to_parse.set_path_to_individual_projects_directory())

    file_to_parse.create_individual_projects_directory()
    file_to_parse.copy_project_from_raw_input()

    print("\nEnd of execution\n")
