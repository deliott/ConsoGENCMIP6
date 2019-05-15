from bin.ccc_myproject_parser import Parser

class FileParser():

    def __init__(self):
        parser = Parser()
        parser.set_path_to_raw_data()
        self.path_to_file = parser.path_to_raw_data + parser.get_list_of_possible_files_to_parse()[0]

    # def __init__(self, date):
    #     self.path_to_file = self.path_to_raw_data + self.get_list_of_possible_files_to_parse()[0]


