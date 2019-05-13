# set_config_path.py

import bin.settings as settings
import socket


def where_we_run():
    """return the name of the computer on which the program is ran"""
    res = ""
    if "irene" in socket.getfqdn():
        res = "irene"

    elif "ipsl" in socket.getfqdn():
        res = "ipsl"
    else:
        res = "default"

    return res

def set_config_path():
    """return the name of the computer on which the program is ran
    changes glob variable config_path according to where the code is ran"""
    res = ""
    if where_we_run() == "irene":
        settings.config_path = "/ccc/cont003/home/gencmip6/dupontel/deploy_folder/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/config_conso.ini"
    elif where_we_run() == "ipsl":
        settings.config_path = "/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/config_conso_local.ini"
    else:
        settings.config_path = "\default"

    return
