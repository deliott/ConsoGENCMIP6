#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this must come first
from __future__ import print_function, unicode_literals, division

# standard library imports
from argparse import ArgumentParser
import os
import os.path
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages

# Application library imports
from libconso import *


########################################
class DirVolume(object):
  #---------------------------------------
  def __init__(self, date, login, dirname, size, date_init, dirsize_init):
    self.date = date
    self.login = login
    self.dirname = dirname
    self.dirsize = size
    self.date_init = date_init
    self.dirsize_init = dirsize_init

  #---------------------------------------
  def __repr__(self):
    return "{}={}-{}".format(self.dirname, self.dirsize, self.dirsize_init)


########################################
class StoreDict(dict):
  #---------------------------------------
  def __init__(self):
    self = {}

  #---------------------------------------
  def fill_data(self, filein, fileinit):
    """
    """
    try:
      data = np.genfromtxt(
        filein,
        skip_header=1,
        converters={
          0: string_to_date,
          1: str,
          2: string_to_size_unit,
          3: str,
        },
        missing_values="nan",
      )
    except Exception as rc:
      print("Problem with file {} :\n{}".format(filein, rc))
      exit(1)

    try:
      init = np.genfromtxt(
        fileinit,
        skip_header=1,
        converters={
          0: string_to_date,
          1: str,
          2: string_to_size_unit,
          3: str,
        },
        missing_values="nan",
      )
    except Exception as rc:
      print("Problem with file {} :\n{}".format(filein, rc))
      exit(1)

    for (date, login, dirsize, dirname), \
        (date_init, _, dirsize_init, _) in zip(data, init):
      self.add_item(
        date, login, dirsize, dirname,
        date_init, dirsize_init
      )

  #---------------------------------------
  def add_item(self, date, login, dirsize, dirname, date_init, dirsize_init):
    """
    """
    if login not in self:
      self[login] = Login(date, login)
    self[login].add_directory(
      date, login, dirsize, dirname,
      date_init, dirsize_init
    )

  #---------------------------------------
  def get_items(self):
    """
    """
    items = (subitem for item in self.itervalues()
                     for subitem in item.listdir)
    items = sorted(items, key=lambda item: item.login)

    return items

  #---------------------------------------
  def get_items_by_name(self, pattern):
    """
    """
    items = (subitem for item in self.itervalues()
                     for subitem in item.listdir
                      if pattern in subitem.dirname)
    items = sorted(items, key=lambda item: item.login)

    return items


########################################
class Login(object):
  #---------------------------------------
  def __init__(self, date, login):
    self.date  = date
    self.login = login
    self.total = SizeUnit(0., "K")
    self.listdir = []

  #---------------------------------------
  def __repr__(self):
    return "{}/{:%F}: {}".format(self.login, self.date, self.listdir)

  #---------------------------------------
  def add_to_total(self, dirsize):
    """
    """
    somme = self.total.convert_size("K").size + \
            dirsize.convert_size("K").size
    self.total = SizeUnit(somme, "K")

  #---------------------------------------
  def add_directory(self, date, login, dirsize, dirname,
                    date_init, dirsize_init):
    """
    """
    self.listdir.append(DirVolume(date, login, dirname, dirsize,
                                  date_init, dirsize_init))
    if isinstance(dirsize, SizeUnit):
      self.add_to_total(dirsize)
    elif args.verbose:
      print("No size for {}, {}".format(login, dirname))


########################################
def plot_init():
  paper_size  = np.array([29.7, 21.0])
  fig, ax = plt.subplots(figsize=(paper_size/2.54))

  return fig, ax


########################################
def plot_data(ax, coords, ylabels, values, values_init):
  """
  """
  ax.barh(coords, values, align="center", color="orange",
          linewidth=0.1, label="volume sur STORE ($To$)")
  ax.barh(coords, values_init, align="center", color="linen",
          linewidth=0.1, label="volume initial sur STORE ($To$)")


########################################
def plot_config(ax, coords, ylabels, dirnames, title,
                tot_volume, tot_volume_init, delta):
  """
  """
  from matplotlib.ticker import AutoMinorLocator

  # ... Config axes ...
  # -------------------
  # 1) Range
  ymin, ymax = coords[0]-1, coords[-1]+1
  ax.set_ylim(ymin, ymax)

  # 2) Ticks labels
  ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
  ax.set_yticks(coords, minor=False)
  ax.set_yticklabels(ylabels, size="xx-small", fontweight="bold")
  ax.invert_yaxis()

  minor_locator = AutoMinorLocator()
  ax.xaxis.set_minor_locator(minor_locator)

  xmin, xmax = ax.get_xlim()
  xpos = xmin + (xmax-xmin)/50.
  for (ypos, text) in zip(coords, dirnames):
    ax.text(s=text, x=xpos, y=ypos, va="center", ha="left",
                size="xx-small", color="gray", style="italic")

  # 3) Define axes title
  ax.set_xlabel("$To$", fontweight="bold")

  # ... Main title and legend ...
  # -----------------------------
  ax.set_title(title, fontweight="bold", size="large")
  ax.legend(loc="best", fontsize="x-small", frameon=False)

  tot_label = "prod {} = {}\n({} - {})".format(
    projet.project.upper(),
    delta,
    tot_volume,
    tot_volume_init,
  )
  plt.figtext(x=0.95, y=0.93, s=tot_label, backgroundcolor="linen",
              ha="right", va="bottom", fontsize="small")


########################################
def get_arguments():
  parser = ArgumentParser()
  parser.add_argument("-v", "--verbose", action="store_true",
                      help="verbose mode")
  parser.add_argument("-f", "--full", action="store_true",
                      help="plot all the directories in IGCM_OUT" +
                           "(default: plot IPSLCM6 directories)")
  parser.add_argument("-p", "--pattern", action="store",
                      default="IPSLCM6",
                      help="plot the whole period")
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

  (file_param, file_utheo, file_data) = \
      get_input_files(DIR["SAVEDATA"],
                      [OUT["PARAM"], OUT["UTHEO"], OUT["STORE"]])

  (file_init, ) = \
      get_input_files(DIR["DATA"], [OUT["SINIT"]])

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
    print(fmt_str.format("file_init", file_init))
    print(fmt_str.format("img_name", img_name))

  # .. Get project info ..
  # ======================
  projet = Project(project_name)
  projet.fill_data(file_param)
  projet.get_date_init(file_utheo)



  exit()


  # .. Fill in data ..
  # ==================
  stores = StoreDict()
  stores.fill_data(file_data, file_init)

  # .. Extract data depending on C.L. arguments ..
  # ==============================================
  if args.full:
    selected_items = stores.get_items()
  else:
    selected_items = stores.get_items_by_name(args.pattern)

  if args.verbose:
    for item in selected_items:
      fmt_str = "{:8s} " + 2*"{:%F} {} {:>18s} " + "{} "
      print(
        fmt_str.format(
          item.login,
          item.date,
          item.dirsize,
          item.dirsize.convert_size("K"),
          item.date_init,
          item.dirsize_init,
          item.dirsize_init.convert_size("K"),
          item.dirname,
        )
      )

  # .. Compute data to be plotted ..
  # ================================
  # ylabels = [item.login for item in selected_items]
  ylabels = [str(hash(item.login)) for item in selected_items]
  values = np.array(
    [item.dirsize.convert_size("T").size for item in selected_items],
    dtype=float
  )
  values_init = np.array(
    [item.dirsize_init.convert_size("T").size for item in selected_items],
    dtype=float
  )
  dirnames = [
    # item.dirname for item in selected_items
    "/".join(item.dirname.split("/")[6:]) for item in selected_items
  ]
  date = selected_items[0].date

  nb_items = len(ylabels)
  coords  = np.linspace(1, nb_items, num=nb_items)

  # .. Plot stuff ..
  # ================
  # ... Initialize figure ...
  # -------------------------
  (fig, ax) = plot_init()

  # ... Plot data ...
  # -----------------
  plot_data(ax, coords, ylabels, values, values_init)

  # ... Tweak figure ...
  # --------------------
  title = "Occupation {} de STORE par login\n{:%d/%m/%Y}".format(
    projet.project.upper(),
    date
  )

  tot_volume = np.sum(values)
  tot_volume_init = np.sum(values_init)
  delta = tot_volume - tot_volume_init

  plot_config(ax, coords, ylabels, dirnames, title,
              SizeUnit(tot_volume, "T"),
              SizeUnit(tot_volume_init, "T"),
              SizeUnit(delta, "T"))

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