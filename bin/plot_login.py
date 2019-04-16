#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this must come first
from __future__ import print_function, unicode_literals, division

# standard library imports
from argparse import ArgumentParser
import os
import os.path
import numpy as np

# Application library imports
from libconso import *


########################################
class LoginDict(dict):
  #---------------------------------------
  def __init__(self):
    self = {}

  #---------------------------------------
  def fill_data(self, filein):
    """
    """
    try:
      data = np.genfromtxt(
        filein,
        skip_header=1,
        converters={
          0: string_to_date,
          1: str,
        },
        missing_values="nan",
      )
    except:
      print("Empty file {}".format(filein))
      exit(1)

    for date, login, conso in data:
      self.add_item(date, login, conso)

  #---------------------------------------
  def add_item(self, date, login, conso):
    """
    """
    self[login] = Login(date, login, conso)

  #---------------------------------------
  def get_items(self):
    """
    """
    items = (item for item in self.itervalues())
    items = sorted(items, key=lambda item: item.login)

    return items

  #---------------------------------------
  def get_items_not_null(self):
    """
    """
    items = (item for item in self.itervalues()
                   if item.conso > 0.)
    items = sorted(items, key=lambda item: item.login)

    return items


class Login(object):
  #---------------------------------------
  def __init__(self, date, login, conso):
    self.date  = date
    self.login = login
    self.conso = conso

  #---------------------------------------
  def __repr__(self):
    return "{} ({:.2}h)".format(self.login, self.conso)


########################################
def get_aliases(alias_file):

  res = {}

  if os.path.isfile(alias_file):
    try:
      data = np.genfromtxt(
        os.path.join(alias_file),
        skip_header=2,
        converters={
          0: str,
          1: str,
          2: str,
          3: str,
        },
        missing_values="",
      )
    except Exception as rc:
      print("Empty file {}:\n{}".format(filein, rc))
      exit(1)

  for alias, login, _, _ in data:
    res[login] = alias

  return res


########################################
def plot_init():
  paper_size  = np.array([29.7, 21.0])
  fig, ax = plt.subplots(figsize=(paper_size/2.54))

  return fig, ax


########################################
def plot_data(ax, ycoord, ylabels, consos):
  """
  """
  ax.barh(ycoord, consos, align="center", color="linen",
          linewidth=0.2, label="conso (heures)")


########################################
def plot_config(fig, ax, ycoord, ylabels, title):
  """
  """
  from matplotlib.ticker import AutoMinorLocator

  # ... Config axes ...
  # -------------------
  # 1) Range
  ymin, ymax = ycoord[0]-1, ycoord[-1]+1
  ax.set_ylim(ymin, ymax)

  # 2) Ticks labels
  ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
  ax.set_yticks(ycoord, minor=False)
  ax.set_yticklabels(ylabels, size="xx-small", fontweight="bold")
  ax.invert_yaxis()

  minor_locator = AutoMinorLocator()
  ax.xaxis.set_minor_locator(minor_locator)

  # 3) Define axes title
  ax.set_xlabel("heures", fontweight="bold")

  # 4) Define plot size
  fig.subplots_adjust(
    left=0.08,
    bottom=0.09,
    right=0.93,
    top=0.93,
  )

  # ... Main title and legend ...
  # -----------------------------
  ax.set_title(title, fontweight="bold", size="large")
  ax.legend(loc="best", fontsize="x-small", frameon=False)


########################################
def get_arguments():
  parser = ArgumentParser()
  parser.add_argument("-v", "--verbose", action="store_true",
                      help="verbose mode")
  parser.add_argument("-f", "--full", action="store_true",
                      help="plot all the logins" +
                           " (default: plot only non-zero)")
  parser.add_argument("-s", "--show", action="store_true",
                      help="interactive mode")
  parser.add_argument("-d", "--dods", action="store_true",
                      help="copy output on dods")

  return parser.parse_args()


########################################
if __name__ == '__main__':

  # .. Initialization ..
  # ====================
  # ... Command line arguments ...
  # ------------------------------
  args = get_arguments()

  # ... Turn interactive mode off ...
  # ---------------------------------
  if not args.show:
    import matplotlib
    matplotlib.use('Agg')

  import matplotlib.pyplot as plt
  # from matplotlib.backends.backend_pdf import PdfPages

  if not args.show:
    plt.ioff()

  # ... Files and directories ...
  # -----------------------------
  project_name, DIR, OUT = parse_config("bin/config.ini")

  (file_param, file_utheo, file_data) = get_input_files(
    DIR["SAVEDATA"],
    [OUT["PARAM"], OUT["UTHEO"], OUT["LOGIN"]]
  )

  alias_file = os.path.join(
    "bin",
    "alias_catalog.dat",
  )

  img_name = os.path.splitext(
               os.path.basename(__file__)
             )[0].replace("plot_", "")

  today = os.path.basename(file_param).strip(OUT["PARAM"])

  if args.verbose:
    fmt_str = "{:10s} : {}"
    print(fmt_str.format("args", args))
    print(fmt_str.format("today", today))
    print(fmt_str.format("file_param", file_param))
    print(fmt_str.format("file_utheo", file_utheo))
    print(fmt_str.format("file_data", file_data))
    print(fmt_str.format("img_name", img_name))

  # .. Get alias info ..
  # ====================
  alias_dict = get_aliases(alias_file)

  # .. Get project info ..
  # ======================
  projet = Project(project_name)
  projet.fill_data(file_param)
  projet.get_date_init(file_utheo)

  # .. Fill in data ..
  # ==================
  logins = LoginDict()
  logins.fill_data(file_data)

  # .. Extract data depending on C.L. arguments ..
  # ==============================================
  if args.full:
    selected_items = logins.get_items()
  else:
    selected_items = logins.get_items_not_null()

  if args.verbose:
    for login in selected_items:
      print(login)

  # .. Compute data to be plotted ..
  # ================================
  nb_items = len(selected_items)

  ycoord  = np.linspace(1, nb_items, num=nb_items)
  ylabels = [
    alias_dict[item.login] 
    if item.login in alias_dict 
    else str(hash(item.login)) 
    for item in selected_items
  ]
  consos  = np.array([item.conso for item in selected_items],
                      dtype=float)
  date = selected_items[0].date

  # .. Plot stuff ..
  # ================
  # ... Initialize figure ...
  # -------------------------
  (fig, ax) = plot_init()

  # ... Plot data ...
  # -----------------
  plot_data(ax, ycoord, ylabels, consos)

  # ... Tweak figure ...
  # --------------------
  title = "Consommation {} par login\n{:%d/%m/%Y}".format(
    projet.project.upper(),
    date
  )
  plot_config(fig, ax, ycoord, ylabels, title)

  # ... Save figure ...
  # -------------------
  img_in  = os.path.join(DIR["PLOT"], "{}.pdf".format(img_name))
  img_out = os.path.join(DIR["SAVEPLOT"],
                         "{}_{}.pdf".format(img_name, today))

  plot_save(img_in, img_out, title, DIR)

  # ... Publish figure on dods ...
  # ------------------------------
  if args.dods:
    if args.verbose:
      print("Publish figure on dods")
    dods_cp(img_in, DIR)

  if args.show:
    plt.show()

  exit(0)
