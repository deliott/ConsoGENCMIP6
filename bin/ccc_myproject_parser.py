"""
This module parses the ccc_myproject log file and return a/several structured data file/s
At first it should provide a datetime and a numper of cpu hours on skylake for cmip6 projects.
as well as on equal to the total of hours.

logs are stored on /home/edupont/ccc_myproject_data
and ccc_myproject_20190514.log is one we can work on
"""

import bin.settings as settings
import bin.set_config_path as set_config_path
import os
import datetime

# @TODO : Thisis not a parser but somethin to get the files_to_parse's directory and list.
class Parser:

    def __init__(self):
        settings.init()
        # settings.path_to_ccc_myproject_raw_data
        self.path_to_raw_data = "/default/path/"
        # self.working_date = datetime.datetime.now().strftime('%Y%m%d')
        self.list_of_possible_files_to_parse = []



    def set_path_to_raw_data(self):
        set_config_path.set_path_to_raw_data_for_parser()
        self.path_to_raw_data = settings.path_to_ccc_myproject_raw_data

    def get_list_of_possible_files_to_parse(self):
        for _file in os.listdir(self.path_to_raw_data):
            if _file.endswith('.log') and _file.startswith('ccc_myproject_20'):
                self.list_of_possible_files_to_parse.append(_file)
        return


    # def open_raw_data_file(self):
    #     open(self.path_to_raw_data, "r")

# for line in my_text:
#     outputfile.writelines(data_parser(line, reps))

# def parse_myproject(filename, project_name):
#   """
#   If on irene(/curie) the CCCMP file is created from ccc_myproject command
#   Parse the file given by filename to get the relevant data
#
#   :param filename: name of the file containing the ccc_myproject data
#   :type filename: str
#   :param project_name: name of the project (ex gen0212 or dcpcmip6)
#   :type project_name : str
#   :return project: dict with info on the project, name , machine, nb of nodes, time allocated and deadline
#   :rtype project: dict
#   :return logins: ditionary with the consumption associated to the login
#   :rtype logins: dict
#   :return today: date of the given ccc_myproject file
#   :rtype today: datetime
#   :return total: Total consumed timed in hours for the project
#   :rtype total: float
#   :return utheo: percentage of the theorical use of cpu time at this date
#   :rtype utheo: float
#   :return ureal: percentage of the real use of cpu time at this date
#   :rtype ureal: float
#   :raises MyError: Description of my error
#   """
#   project = {}
#   project["name"] = project_name
#   logins= {}
#
#   #If on irene(/curie) the CCCMP file is created from ccc_myproject command
#   if where_we_run() == "irene":
#     try :
#       res = subprocess.check_output("ccc_myproject")
#     except Exception as rc :
#       print(rc)
#       exit(1)
#     with open(os.path.join(DIR["DATA"], OUT["CCCMP"]), "w") as fileout:
#       fileout.write(res)
#
#   with open(filename, "r") as filein:
#     # Skip lines until we find project name.
#     # Then extract script date
#     for ligne in filein:
#       if "Accounting" in ligne and \
#           project["name"] in ligne:
#         today = ligne.split()[-1]
#         today = string_to_date(today)
#         project["machine"] = ligne.split()[5]
#         project["nodes"]   = ligne.split()[6]
#         break
#
#     # Skip until we find login title line
#     for ligne in filein:
#       if "Login" in ligne:
#         if "Account" in ligne:
#           fg_account = True
#         else:
#           fg_account = False
#         break
#
#     # Login list, until Subtotal or blank line
#     for ligne in filein:
#       if not ligne.strip() or \
#          "Subtotal" in ligne:
#         break
#       if fg_account:
#         login, account, conso = ligne.split()
#       else:
#         login, conso = ligne.split()
#       logins[login] = float(conso)
#
#     # Skip until we find consumed time (hours)
#     for ligne in filein:
#       if "Total" in ligne:
#         total = float(ligne.split()[-1])
#         break
#
#     # Skip until we find allocated time (hours)
#     for ligne in filein:
#       if "Allocated" in ligne:
#         project["alloc"] = float(ligne.split()[-1])
#         break
#
#     # Skip until we find theoratical use (%)
#     for ligne in filein:
#       if "Suggested use at this time" in ligne:
#         utheo = float(ligne.split()[-1].strip("%"))
#         break
#
#     # Skip until we find real use (%)
#     for ligne in filein:
#       if "Real use at this time" in ligne:
#         ureal = float(ligne.split()[-1].strip("%"))
#         break
#
#     # Skip until we find deadline
#     for ligne in filein:
#       if "Project deadline" in ligne:
#         project["deadline"] = ligne.split()[-1]
#         break
#
#   return project, logins, today, total, utheo, ureal
