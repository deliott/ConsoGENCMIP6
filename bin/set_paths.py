# set_config_path.py

import bin.settings as settings
import socket


def where_we_run():
    """return the name of the computer on which the program is ran"""
    res = ""
    if "irene" in socket.getfqdn():
        res = "irene"

    elif "jussieu" in socket.getfqdn():
        res = "jussieu"
    elif "ciclad" in socket.getfqdn():
        res = "ciclad"
    else:
        res = "default"

    return res

def set_config_path():
    """return the name of the computer on which the program is ran
    changes glob variable config_path according to where the code is ran"""
    res = ""
    if where_we_run() == "irene":
        settings.config_path = "/ccc/cont003/home/gencmip6/dupontel/deploy_folder/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/config_conso.ini"
    elif where_we_run() == "jussieu":
        settings.config_path = "/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/config_conso_local.ini"
    else:
        settings.config_path = "\default"

    return

def set_path_to_raw_data_for_parser():
    """changes glob variable path_to_ccc_myproject_raw_data according to where the code is ran"""
    res = ""
    if where_we_run() == "irene":
        settings.path_to_ccc_myproject_raw_data = "/ccc/cont003/home/drf/p86ipsl/Suivi_Consomation_Eliott/ccc_myproject_data/"
    elif where_we_run() == "jussieu":
        settings.path_to_ccc_myproject_raw_data = "/home/edupont/ccc_myproject_data/"
    elif where_we_run() == "ciclad":
        settings.path_to_ccc_myproject_raw_data = "/home/eldupont/ccc_myproject_data/"
    else:
        settings.path_to_ccc_myproject_raw_data = "\wrong\computer"

    return

def set_path_to_timeseries():
    """changes glob variable path_to_timeseries according to where the code is ran"""
    res = ""
    if where_we_run() == "irene":
        settings.path_to_timeseries = "/ccc/cont003/home/drf/p86ipsl/Suivi_Consomation_Eliott/ccc_myproject_data/timeseries/"
    elif where_we_run() == "jussieu":
        settings.path_to_timeseries = "/home/edupont/ccc_myproject_data/timeseries/"
    elif where_we_run() == "ciclad":
        settings.path_to_timeseries = "/home/eldupont/ccc_myproject_data/timeseries/"
    else:
        settings.path_to_timeseries = "\wrong\computer"

    return