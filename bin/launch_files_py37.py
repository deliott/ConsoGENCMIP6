# import sys
import os
# import logging as log
# import bin.conso_A6_py37
# import bin.settings as settings
import bin.set_config_path as set_config_path

########################################
if __name__ == '__main__':
    # settings.init()
    # print(settings.config_path)
    # set_config_path.set_config_path()
    # print(settings.config_path)

    if set_config_path.where_we_run() == "jussieu":
        os.system("/home/edupont/.conda/envs/env3.7_loc/bin/python \
        /home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/conso_A6_py37.py")
    elif set_config_path.where_we_run() == "ciclad":
        os.system("/home/eldupont/.conda/envs/env3.7/bin/python \
        /home/eldupont/ConsoGENCMIP6/bin/conso_A6_py37.py")
    #     log.error("Running on IRENE : conda env has to be set up to be able tu run next command.\
    #      \nRun on local with -l CL Argument instead")
    #     #os.system("/home/edupont/.conda/envs/env3.7_loc/bin/python /home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/conso_A6_py37.py -l")
