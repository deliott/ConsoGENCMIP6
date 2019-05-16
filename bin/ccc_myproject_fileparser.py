from bin.ccc_myproject_parser import Parser
# import bin.ccc_myproject_parser as ccc_myproject_parser

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


    # def __init__(self, date):
    #     """

    #     :param path_to_file: absolute path of the file that will be parsed, here it is the one indicated by the date.
    #     """
    #     self.path_to_file = self.path_to_raw_data + self.get_list_of_possible_files_to_parse()[0]


