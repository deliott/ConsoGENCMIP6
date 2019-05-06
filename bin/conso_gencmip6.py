#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this must come first
from __future__ import print_function, unicode_literals, division

# standard library imports
from argparse import ArgumentParser
import json
import shutil
import os
import os.path
import subprocess
# import datetime as dt

# Application library imports
from libconso import *


########################################
def get_storedir(login):

  print("get_storedir")

  command = ["ccc_home", "-A", "-u", login]
  try :
    res = subprocess.check_output(command)
    print("res", res)
  except Exception as rc:
    print("exception", rc)
    res = None

  return res.strip()


########################################
def get_dirsize(dirname):

  command = ["du", "-sbh", dirname]
  try :
    res = subprocess.check_output(command)
    res = res.split()[0]
  except Exception as rc :
    print(rc)
    res = None

  return res


# ########################################
# def get_dirlist(dirname):


#   return output


########################################
def parse_myproject(filename, project_name):

  project = {}
  project["name"] = project_name
  logins  = {}

  if where_we_run() == "curie":
    try :
      res = subprocess.check_output("ccc_myproject")
    except Exception as rc :
      print(rc)
      exit(1)
    with open(os.path.join(DIR["DATA"], OUT["CCCMP"]), "w") as fileout:
      fileout.write(res)

  with open(filename, "r") as filein:
    # Skip lines until we find project name.
    # Then extract script date
    for ligne in filein:
      if "Accounting" in ligne and \
          project["name"] in ligne:
        today = ligne.split()[-1]
        today = string_to_date(today)
        project["machine"] = ligne.split()[5]
        project["nodes"]   = ligne.split()[6]
        break

    # Skip until we find login title line
    for ligne in filein:
      if "Login" in ligne:
        if "Account" in ligne:
          fg_account = True
        else:
          fg_account = False
        break

    # Login list, until Subtotal or blank line
    for ligne in filein:
      if not ligne.strip() or \
         "Subtotal" in ligne:
        break
      if fg_account:
        login, account, conso = ligne.split()
      else:
        login, conso = ligne.split()
      logins[login] = float(conso)

    # Skip until we find consumed time (hours)
    for ligne in filein:
      if "Total" in ligne:
        total = float(ligne.split()[-1])
        break

    # Skip until we find allocated time (hours)
    for ligne in filein:
      if "Allocated" in ligne:
        project["alloc"] = float(ligne.split()[-1])
        break

    # Skip until we find theoratical use (%)
    for ligne in filein:
      if "Suggested use at this time" in ligne:
        utheo = float(ligne.split()[-1].strip("%"))
        break

    # Skip until we find real use (%)
    for ligne in filein:
      if "Real use at this time" in ligne:
        ureal = float(ligne.split()[-1].strip("%"))
        break

    # Skip until we find deadline
    for ligne in filein:
      if "Project deadline" in ligne:
        project["deadline"] = ligne.split()[-1]
        break

  return project, logins, today, total, utheo, ureal


########################################
def write_param(filename, project):

  if args.dryrun:
    print(json.dumps(project, indent=2))
  else:
    with open(filename, "w") as fileout:
      json.dump(project, fileout, indent=2)


########################################
def write_bilan(
  filename, today, total, ureal, utheo,
  runp_mean, penp_mean, runp_std, penp_std,
  runf_mean, penf_mean, runf_std, penf_std
):
  """
  Conso totale par jour
  ---------------------
  on garde le total, date en tete en accumulant dans le fichier :
  OUT_CONSO_BILAN
  """

  fmt_str = (
    "{:10s} {:12s} {:11s} {:11s} "
    "{:14s} {:14s} {:14s} {:14s} "
    "{:14s} {:14s} {:14s} {:14s} "
    "\n"
  )

  title_str = fmt_str.format(
    "date",
    "conso(hours)",
    "real_use(%)",
    "theo_use(%)",
    "runningP(core)",
    "pendingP(core)",
    "run_stdP(core)",
    "pen_stdP(core)",
    "runningF(core)",
    "pendingF(core)",
    "run_stdF(core)",
    "pen_stdF(core)",
  )

  fmt_str = (
    "{:%Y-%m-%d} {:12.2f} {:11.2f} {:11.2f} "
    "{:14.2f} {:14.2f} {:14.2f} {:14.2f} "
    "{:14.2f} {:14.2f} {:14.2f} {:14.2f} "
    "\n"
  )

  result_str = fmt_str.format(
    today,
    total,
    ureal,
    utheo,
    runp_mean,
    penp_mean,
    runp_std,
    penp_std,
    runf_mean,
    penf_mean,
    runf_std,
    penf_std,
  )

  if args.dryrun:
    print(title_str.strip())
    print(result_str.strip())
  else:
    if not os.path.isfile(filename):
      with open(filename, "w") as fileout:
        fileout.write(title_str)
    with open(filename, "a") as fileout:
      fileout.write(result_str)


########################################
def write_utheo(filename, today, utheo):
  """
  Conso théorique par jour
  ------------------------
  OUT_CONSO_THEO
  """

  title_str  = "{:10s} {:11s}\n".format(
                 "date",
                 "theo_use(%)",
               )
  result_str = "{:%Y-%m-%d} {:11.2f}\n".format(
                 today,
                 utheo,
               )

  if args.dryrun:
    print(title_str.strip())
    print(result_str.strip())
  else:
    if not os.path.isfile(filename):
      with open(filename, "w") as fileout:
        fileout.write(title_str)
    with open(filename, "a") as fileout:
      fileout.write(result_str)


########################################
def write_login(filename, today, logins):
  """
  Conso par login (HOME)
  ----------------------
  on garde la trace de chaque login, date en tete, en remplacant
  le fichier a chaque fois : OUT_CONSO_LOGIN
  """

  title_str  = "{:10s} {:10s} {:12s}\n".format(
                 "date",
                 "login",
                 "conso(hours)",
               )

  with open(filename, "w") as fileout:
    if args.dryrun:
      print(title_str.strip())
    else:
      fileout.write(title_str)

    for key in sorted(logins):
      result_str = "{:%Y-%m-%d} {:10s} {:12.2f}\n".format(
                     today,
                     key,
                     logins[key],
                   )
      if args.dryrun:
        print(result_str.strip())
      else:
        fileout.write(result_str)


########################################
def write_store(filename, today, logins):
  """
  volume cree sur STORE
  ---------------------
  par login qui a consomme, en remplacant le fichier a chaque fois :
  OUT_CONSO_STORE
  """

  items = (login for login, conso in logins.iteritems()
                  if conso > 0.)

  title_str = "{:10s} {:10s} {:>7s} {:s}\n".format(
                "date",
                "login",
                "dirsize",
                "dirname",
              )

  with open(filename, "w") as fileout:
    if args.dryrun:
      print(title_str.strip())
    else:
      fileout.write(title_str)

    for login in items:
      if args.verbose:
        print(login)
      storedir = get_storedir(login)
      if not storedir:
        print("storedir not found for {}".format(storedir))
        break
      igcm_out = os.path.join(storedir, "IGCM_OUT")

      if not os.path.isdir(igcm_out):
        print("no {}".format(igcm_out))
        continue

      dirlist = []
      try:
        dirlist = os.listdir(igcm_out)
      except OSError as rc:
        print("Error on os.listdir({}):\n{}".format(igcm_out, rc))

      for dirname in dirlist:
        result_str = "{:%Y-%m-%d} {:10s} {:>7s} {:s}\n".format(
                       today,
                       login,
                       get_dirsize(os.path.join(igcm_out, dirname)),
                       os.path.join(igcm_out, dirname)
                     )

        if args.dryrun or args.verbose:
          print(result_str.strip())

        if not args.dryrun:
          fileout.write(result_str)


########################################
def save_files(file_list, today):

  if not args.dryrun:
    suffix = "{:%Y%m%d}".format(today)
    for filename in file_list:
      filein  = os.path.join(DIR["DATA"], filename)
      if os.path.isfile(filein):
        fileout = os.path.join(DIR["SAVEDATA"],
                               "_".join((filename, suffix)))
        shutil.copy(filein, fileout)


########################################
if __name__ == '__main__':

  # Get arguments from command line
  # ===============================
  parser = ArgumentParser()
  parser.add_argument("-v", "--verbose", action="store_true",
                      help="Verbose mode")
  parser.add_argument("-d", "--dryrun", action="store_true",
                      help="dry run, no file produced")
  parser.add_argument("-a", "--all", action="store_false",
                      help="produce all files (default)")
  parser.add_argument("-b", "--bilan", action="store_true",
                      help="produce all files (default)")
  parser.add_argument("-l", "--login", action="store_true",
                      help="produce all files (default)")
  parser.add_argument("-s", "--store", action="store_true",
                      help="produce all files (default)")
  parser.add_argument("-L", "--local", action="store_true",
                      help=" select the config_local.ini file if code ran on local computer ")

  args = parser.parse_args()


  if args.local:
    config_path = "/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/config_local.ini"
  else:
    config_path = "bin/config.ini"



  if args.verbose:
    print(os.path.basename(__file__))
    print(where_we_run())
    print(args)

  if args.bilan or args.login or args.store:
    args.all = False

  project_name, DIR, OUT = parse_config(config_path)

  if args.verbose:
    print(DIR["DATA"])
    print(DIR["SAVEDATA"])

  (project, logins, today, total, utheo, ureal) = parse_myproject(
    os.path.join(DIR["DATA"], OUT["CCCMP"]),
    project_name
  )

  if args.verbose:
    print(today, utheo, ureal)
    print(project)
    print(logins)

  # Produce files
  # =============

  # 1- Parametres du projet
  # -----------------------
  if args.verbose:
    print("=> write_param")

  write_param(os.path.join(DIR["DATA"], OUT["PARAM"]), project)

  # 2- Conso totale par jour
  # ------------------------

  if args.verbose:
    print("=> write_bilan")

  file_jobs = get_last_file(
      DIR["SAVEDATA"],
      "{}_{:%Y%m%d}".format(OUT["JOBS"], today)
  )
  if args.verbose:
    print(file_jobs)

  run_mean = np.nan
  pen_mean = np.nan
  run_std  = np.nan
  pen_std  = np.nan

  if file_jobs:
    try:
      data = np.genfromtxt(
        file_jobs,
        skip_header=1,
        converters={
          0: string_to_datetime,
          1: float,
          2: float,
        },
        missing_values="nan",
      )
    except Exception as rc:
      print("Problem with file {} :\n{}".format(file_jobs, rc))
      exit(1)

    run_mean = np.nanmean(
        np.array([run for _, run, _ in data])
    )
    pen_mean = np.nanmean(
        np.array([pen for _, _, pen in data])
    )

    run_std = np.nanstd(
        np.array([run for _, run, _ in data])
    )
    pen_std = np.nanstd(
        np.array([pen for _, _, pen in data])
    )

  if args.verbose:
    print(run_mean, pen_mean, run_std, pen_std)

  write_bilan(
    os.path.join(DIR["DATA"], OUT["BILAN"]),
    today,
    total,
    ureal,
    utheo,
    run_mean,
    pen_mean,
    run_std,
    pen_std,
    runf_mean,
    penf_mean,
    runf_std,
    penf_std,
  )

  # 2b- Conso théorique par jour
  # ----------------------------
  if args.verbose:
    print("=> write_utheo")

  write_utheo(os.path.join(DIR["DATA"], OUT["UTHEO"]), today, utheo)

  # 3- Conso par login (HOME)
  # -------------------------
  if args.verbose:
    print("=> write_login")

  write_login(os.path.join(DIR["DATA"], OUT["LOGIN"]), today, logins)

  # 4- volume cree sur STORE
  # ------------------------
  if args.verbose:
    print("=> write_store")

  if where_we_run() == "curie":
    write_store(os.path.join(DIR["DATA"], OUT["STORE"]), today, logins)

  # Save files (on WORKDIR)
  # =======================
  if args.verbose:
    print("=> Save files")
  if not args.dryrun:
    file_list = [
        OUT["PARAM"],
        OUT["BILAN"],
        OUT["UTHEO"],
        OUT["LOGIN"],
        OUT["STORE"],
        OUT["CCCMP"],
    ]

    save_files(file_list, today)

  exit(0)

