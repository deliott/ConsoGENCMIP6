#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this must come first
#TODO: Repair code since switched from python2 to python3 when used with plot_jobs*

# standard library imports
import socket
import os
import os.path
import glob
import shutil
import subprocess
import datetime as dt
import numpy as np
import configparser as cp

# Application library imports


########################################
def dods_cp(filein, DIR):
  """
  """
  if not DIR["DODS"]:
    print("DODS directory not defined")
    return

  basefile = os.path.basename(filein)

  fileout = os.path.join(DIR["DODS"], basefile)
  filepng = os.path.join(DIR["DODS"], "img", basefile.split(".")[0] + ".png")

  # Copy file
  shutil.copy(filein, fileout)

  # Convert it to png for web page
  command = ["convert", "-density", "200", fileout, filepng]

  try :
    subprocess.call(command)
  except Exception as rc :
    print("Error in convert for {}:\n{}".format(fileout, rc))

  return


########################################
def parse_config(filename):
  """
  Extract relevant data from the config*.ini files.

  :param filename: path to the relevant config*.ini according to where and what the program will run
  :type filename: str
  :return project_name: name of the project worked on. ex: gencmip6
  :rtype project_name: str
  :return DIR: dictionary with the paths of the [directories] section of the config file
  :rtype DIR: dict
  :return OUT: dictionary with the paths of the [files] section of the config file
  :rtype OUT: dict
  """
  DIR = {}
  OUT = {}

  config = cp.ConfigParser(allow_no_value=True)
  config.optionxform = str
  config.read(filename)

  for section in ("projet", "directories", "files"):
    if not config.has_section(section):
      print("Missing section {} in {}, we stop".format(section, filename))
      exit(1)

  # .. Project name ..
  # ------------------
  section = "projet"
  option  = "name"
  project_name = config.get(section, option)

  # ..Common directories ..
  # -----------------------
  section = "directories"
  for option in config.options(section):
    DIR[option] = config.get(section, option)

    if DIR[option] and not os.path.isdir(DIR[option]):
      print("mkdir {}".format(DIR[option]))
      try :
        os.makedirs(DIR[option])
      except Exception as rc :
        print("Could not create {}:\n{}".format(DIR[option], rc))

  # ..Common files ..
  # -----------------
  section = "files"
  for option in config.options(section):
    OUT[option] = config.get(section, option)

  return (project_name, DIR, OUT)


########################################
def string_to_percent(x):
  """
  """
  return float(x.strip("%"))/100.


########################################
def string_to_size_unit(x):
  """
  """
  if x == "None":
    x = "0o"

  if str(x).isdecimal():
    x = x + "o"

  (size, unit) = (float(x[:-1]), x[-1])

  return SizeUnit(size, unit)


########################################
def string_to_float(x):
  """
  """
  return float(x.strip("h"))


########################################
def string_to_date(ssaammjj, fmt="%Y-%m-%d"):
  """
  """
  return dt.datetime.strptime(ssaammjj, fmt)


########################################
def string_to_datetime(string, fmt="%Y-%m-%d-%H:%M"):
  """Convert a string in the proper format into a datetime  """
  return dt.datetime.strptime(string, fmt)


# ########################################
# def date_to_string(dtdate, fmt="%Y-%m-%d"):
#   """
#   """
#   return dt.datetime.strftime(dtdate, fmt)


########################################
def where_we_run():
  """return the name of the computer on which the program is ran"""
  res = ""
  if "curie" in socket.getfqdn():
    res = "curie"
  elif "ipsl" in socket.getfqdn():
    res = "ipsl"
  else:
    res = "default"

  return res


########################################
def get_last_file(dir_data, pattern):
  """
  Extract relevant data from the config*.ini files.

  :param filename: path to the relevant config*.ini according to where and what the program will run
  :type filename: str
  :return project_name: name of the project worked on. ex: gencmip6
  :rtype project_name: str
  :return DIR: dictionary with the paths of the [directories] section of the config file
  :rtype DIR: dict
  :return OUT: dictionary with the paths of the [files] section of the config file
  :rtype OUT: dict
  """
  current_dir = os.getcwd()
  os.chdir(dir_data)
  filename = pattern + "*"
  file_list = glob.glob(os.path.join(dir_data, filename))
  if file_list:
    res = sorted(file_list)[-1]
  else:
    res = None
  os.chdir(current_dir)
  return res


########################################
def get_input_files(dir_data, file_list, date=None):
  """
  """
  res = []

  for filebase in file_list:
    if date:
      filename = "_".join((filebase, date))
    else:
      filename = filebase

    res.append(get_last_file(dir_data, filename))

  if None in res:
    print("\nMissing one or more input files, we stop.")
    for f_in, f_out in zip(file_list, res):
      print("=> {}: {}".format(f_in, f_out))
    exit(1)

  return res


########################################
def plot_save(img_in, img_out, title, DIR):
  """
  """
  from matplotlib.backends.backend_pdf import PdfPages

  dpi = 200.

  # img_in  = os.path.join(DIR["PLOT"], "{}.pdf".format(img_name))

  with PdfPages(img_in) as pdf:
    pdf.savefig(dpi=dpi)

    # pdf file's metadata
    d = pdf.infodict()
    d["Title"]   = title
    d["Author"]  = os.path.basename(__file__)
    # d["Subject"] = "Time spent over specific commands during create_ts \
    #                 jobs at IDRIS and four configurations at TGCC"
    # d["Keywords"] = "bench create_ts TGCC IDRIS ncrcat"
    # d["CreationDate"] = dt.datetime(2009, 11, 13)
    # d["ModDate"] = dt.datetime.today()

  if os.path.isdir(DIR["SAVEPLOT"]):
    # img_out = os.path.join(DIR["SAVEPLOT"],
    #                        "{}_{}.pdf".format(img_name, suffix))
    shutil.copy(img_in, img_out)


########################################
class Project(object):

  #---------------------------------------
  def __init__(self, project_name):
    self.project   = project_name
    self.date_init = ""
    self.deadline  = ""
    self.alloc     = 0

  #---------------------------------------
  def fill_data(self, filein):
    import json
    dico = json.load(open(filein, "r"))
    self.deadline = string_to_date(dico["deadline"]) + \
                    dt.timedelta(days=-1)
    self.alloc = dico["alloc"]

  #---------------------------------------
  def get_date_init(self, filein):
    data = np.genfromtxt(
      filein,
      skip_header=1,
      converters={
        0: string_to_date,
        1: string_to_percent,
      },
      missing_values="nan",
    )
    dates, utheos = list(zip(*data))

    x2 = len(utheos) - 1
    x1 = x2
    for nb, elem in enumerate(utheos[-2::-1]):
      if elem >= utheos[x2]:
        break
      x1 = x2 - nb + 1

    m = np.array([[x1, 1.], [x2, 1.]])
    n = np.array([utheos[x1], utheos[x2]])

    poly_ok = True
    try:
      polynome = np.poly1d(np.linalg.solve(m, n))
    except np.linalg.linalg.LinAlgError:
      poly_ok = False

    if poly_ok:
      delta = x1 - int(round(polynome.r[0]))
      d1 = dates[x1]
      self.date_init = d1 - dt.timedelta(days=delta)
    else:
      self.date_init = dt.datetime(self.deadline.year, 1, 1)

    delta = self.deadline - self.date_init
    self.days = delta.days + 1


########################################
class SizeUnit(object):
  #---------------------------------------
  def __init__(self, size, unit):
    self.size = size
    self.unit = unit

  #---------------------------------------
  def __repr__(self):
    return "{:6.2f}{}o".format(self.size, self.unit)

  #---------------------------------------
  def convert_size(self, unit_out):
    """
    """
    prefixes = ["o", "K", "M", "G", "T", "P", "H"]

    if not self.size or \
      self.unit == unit_out:
      size_out = self.size
    else:
      idx_deb = prefixes.index(self.unit)
      idx_fin = prefixes.index(unit_out)
      size_out = self.size
      for i in range(abs(idx_fin-idx_deb)):
        if idx_fin > idx_deb:
          size_out = size_out / 1024
        else:
          size_out = size_out * 1024

    return SizeUnit(size_out, unit_out)


########################################
if __name__ == '__main__':
  pass

