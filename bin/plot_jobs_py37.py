#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this must come first
#TODO: Repair code since switched from python2 to python3


# standard library imports
from argparse import ArgumentParser
import os
import os.path
import datetime as dt
import numpy as np

# Application library imports
from bin.libconso_py37 import *


########################################
class DataDict(dict):
  #---------------------------------------
  def __init__(self):
    self = {}

  #---------------------------------------
  def init_range(self, date_beg, date_end, inc=1):
    """
    """
    delta = date_end - date_beg + dt.timedelta(days=1)

    (deb, fin) = (0, int(delta.total_seconds() / 3600))

    dates = (date_beg + dt.timedelta(hours=i)
             for i in range(deb, fin, inc))

    for date in dates:
      self.add_item(date)

  #---------------------------------------
  def fill_data(self, file_list):
    """
    """
    for filein in sorted(file_list):
      try:
        data = np.genfromtxt(
          filein,
          skip_header=1,
          converters={
            0: string_to_datetime,
            1: float,
            2: float,
          },
          missing_values="nan",
        )
      except Exception as rc:
        print("Problem with file {} :\n{}".format(filein, rc))
        exit(1)

      if len(data) == 24:
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
      else:
        run_mean = np.nan
        pen_mean = np.nan
        run_std  = np.nan
        pen_std  = np.nan

      for date, run, pen in data:
        if date.hour == 0:
          self.add_item(
            date,
            run,
            pen,
            run_mean,
            pen_mean,
            run_std,
            pen_std
          )
        else:
          self.add_item(date, run, pen)
        self[date].fill()

  #---------------------------------------
  def add_item(self, date, run=np.nan, pen=np.nan,
               run_mean=np.nan, pen_mean=np.nan,
               run_std=np.nan, pen_std=np.nan):
    """
    """
    self[date] = Conso(
      date,
      run,
      pen,
      run_mean,
      pen_mean,
      run_std,
      pen_std
    )

  #---------------------------------------
  def get_items_in_range(self, date_beg, date_end, inc=1):
    """
    """
    items = (item for item in self.values()
                   if item.date >= date_beg and
                      item.date <= date_end)
    items = sorted(items, key=lambda item: item.date)

    return items[::inc]

  #---------------------------------------
  def get_items_in_full_range(self, inc=1):
    """
    """
    items = (item for item in self.values()
                   if item.date >= projet.date_init and
                      item.date <= projet.deadline  and
                      item.date.hour == 0)
    items = sorted(items, key=lambda item: item.date)

    return items[::inc]

  #---------------------------------------
  def get_items(self, inc=1):
    """
    """
    items = (item for item in self.values()
                   if item.isfilled())
    items = sorted(items, key=lambda item: item.date)

    return items[::inc]


class Conso(object):
  #---------------------------------------
  def __init__(self, date, run=np.nan, pen=np.nan,
               run_mean=np.nan, pen_mean=np.nan,
               run_std=np.nan, pen_std=np.nan):

    self.date     = date
    self.run      = run
    self.pen      = pen
    self.run_mean = run_mean
    self.pen_mean = pen_mean
    self.run_std  = run_std
    self.pen_std  = pen_std
    self.filled   = False

  #---------------------------------------
  def __repr__(self):
    return "R{:.0f} ({:.0f}/{:.0f}) P{:.0f} ({:.0f}/{:.0f})".format(
      self.run,
      self.run_mean,
      self.run_std,
      self.pen,
      self.pen_mean,
      self.pen_std,
    )

  #---------------------------------------
  def isfilled(self):
    return self.filled

  #---------------------------------------
  def fill(self):
    self.filled = True


########################################
def plot_init():
  paper_size  = np.array([29.7, 21.0])
  fig, ax = plt.subplots(figsize=(paper_size/2.54))

  return fig, ax


########################################
def plot_data(ax, xcoord, dates, run_jobs, pen_jobs, run_std, pen_std):
  """
  """
  line_width = 0.
  width = 1.05

  ax.bar(
    xcoord, run_jobs, width=width, yerr=run_std/2.,
    linewidth=line_width, align="center",
    color="lightgreen", ecolor="green", antialiased=True,
    label="jobs running"
  )
  if args.mode == "machine":
    label = "jobs pending\n(Ressources & Priority)"
  else:
    label = "jobs pending"
  ax.bar(
    xcoord, pen_jobs, bottom=run_jobs, width=width,
    linewidth=line_width, align="center",
    color="firebrick", antialiased=True,
    label=label
  )


########################################
def plot_config(
  fig, ax, xcoord, dates, title, conso_per_day, conso_per_day_2
):
  """
  """
  from matplotlib.ticker import AutoMinorLocator

  # ... Compute useful stuff ...
  # ----------------------------
  multialloc = False

  if args.mode == "machine":
    xi = 0
    xn = xi
    xf = len(dates)
    yi = 80000.
    yf = yi
  else:

    yi = conso_per_day
    yf = conso_per_day
    if projet.date_init in dates:
      xi = dates.index(projet.date_init)
    else:
      xi = 0
    if projet.deadline in dates:
      xf = dates.index(projet.deadline)
    else:
      xf = len(dates) + 1
    xn = xi

    if conso_per_day_2:
      date_inter = projet.date_init + dt.timedelta(days=projet.days//2)
      if projet.date_init in dates:
        xi = dates.index(projet.date_init)
      else:
        xi = 0

      if projet.deadline in dates:
        xf = dates.index(projet.deadline)
      else:
        xf = len(dates) + 1

      if date_inter in dates:
        xn = dates.index(date_inter)
        yi = conso_per_day
        yf = conso_per_day_2
        multialloc = True
      else:
        if dates[-1] < date_inter:
          xn = xf
          yi = conso_per_day
          yf = conso_per_day
        elif dates[0] > date_inter:
          xn = xi
          yi = conso_per_day_2
          yf = conso_per_day_2

  # ... Config axes ...
  # -------------------
  # 1) Range
  xmin, xmax = xcoord[0]-1, xcoord[-1]+1
  if multialloc:
    ymax = 4. * max(yi, yf)
  else:
    ymax = 4. * yi
  ax.set_xlim(xmin, xmax)
  ax.set_ylim(0, ymax)

  # 2) Plot ideal daily consumption
  line_color = "blue"
  line_alpha = 0.5
  line_label = "conso journalière idéale"
  ax.plot(
    [xi, xn, xn, xf], [yi, yi, yf, yf],
    color=line_color, alpha=line_alpha, label=line_label,
  )

  # 3) Ticks labels
  (date_beg, date_end) = (dates[0], dates[-1])

  if date_end - date_beg > dt.timedelta(weeks=9):
    date_fmt = "{:%d-%m}"
    maj_xticks = [x for x, d in zip(xcoord, dates)
                     if d.weekday() == 0 and d.hour == 0]
    maj_xlabs  = [date_fmt.format(d) for d in dates
                     if d.weekday() == 0 and d.hour == 0]
  else:
    date_fmt = "{:%d-%m %Hh}"
    maj_xticks = [x for x, d in zip(xcoord, dates)
                     if d.hour == 0 or d.hour == 12]
    maj_xlabs  = [date_fmt.format(d) for d in dates
                     if d.hour == 0 or d.hour == 12]

  ax.set_xticks(xcoord, minor=True)
  ax.set_xticks(maj_xticks, minor=False)
  ax.set_xticklabels(maj_xlabs, rotation="vertical", size="x-small")

  minor_locator = AutoMinorLocator()
  ax.yaxis.set_minor_locator(minor_locator)

  yticks = list(ax.get_yticks())
  if args.mode == "machine":
    yticks.append(yi)
  else:
    yticks.append(conso_per_day)
    if multialloc:
      yticks.append(conso_per_day_2)
  ax.set_yticks(yticks)

  for x, d in zip(xcoord, dates):
    if d.weekday() == 0 and d.hour == 0:
      ax.axvline(x=x, color="black", linewidth=1., linestyle=":")

  # 4) Define axes title
  ax.set_ylabel("cœurs", fontweight="bold")
  ax.tick_params(axis="y", labelsize="small")

  # 5) Define plot size
  fig.subplots_adjust(
    left=0.08,
    bottom=0.09,
    right=0.93,
    top=0.93,
  )

  # ... Main title and legend ...
  # -----------------------------
  fig.suptitle(title, fontweight="bold", size="large")
  ax.legend(loc="upper right", fontsize="x-small", frameon=False)


########################################
def get_arguments():
  parser = ArgumentParser()
  parser.add_argument("-v", "--verbose", action="store_true",
                      help="verbose mode")
  parser.add_argument("-f", "--full", action="store_true",
                      help="plot the whole period")
  parser.add_argument("-i", "--increment", action="store",
                      type=int, default=1, dest="inc",
                      help="sampling increment")
  parser.add_argument("-r", "--range", action="store", nargs=2,
                      type=string_to_date,
                      help="date range: ssaa-mm-jj ssaa-mm-jj")
  parser.add_argument("-s", "--show", action="store_true",
                      help="interactive mode")
  parser.add_argument("-d", "--dods", action="store_true",
                      help="copy output on dods")
  parser.add_argument("-m", "--mode", action="store",
                      choices=["project", "machine"],
                      default="project",
                      help="copy output on dods")
  parser.add_argument("-l", "--local", action="store_true",
                      help=" select the config_local.ini file if code ran on local computer ")

  return parser.parse_args()


########################################
if __name__ == '__main__':

  # .. Initialization ..
  # ====================
  # ... Command line arguments ...
  # ------------------------------
  args = get_arguments()

  # ... Constants ...
  # -----------------
  WEEK_NB = 3

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

  if args.local:
    config_path = "/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/config_local.ini"
  else:
    config_path = "bin/config.ini"

  project_name, DIR, OUT = parse_config(config_path)

  (file_param, file_utheo) = \
      get_input_files(DIR["SAVEDATA"], [OUT["PARAM"], OUT["UTHEO"]])

  if args.mode == "project":
    pattern = "OUT_JOBS_PENDING_"
  else:
    pattern = "OUT_JOBS_PEN_FULL_"
  file_list = glob.glob(
    os.path.join(DIR["SAVEDATA"], pattern + "*")
  )

  img_name = "jobs_{}".format(args.mode)

  today   = dt.datetime.today()
  weeknum = today.isocalendar()[1]

  if args.verbose:
    fmt_str = "{:10s} : {}"
    print(fmt_str.format("args", args))
    print(fmt_str.format("today", today))
    print(fmt_str.format("file_param", file_param))
    print(fmt_str.format("file_utheo", file_utheo))
    print(fmt_str.format("file_list", file_list))
    print(fmt_str.format("img_name", img_name))

  # .. Get project info ..
  # ======================
  projet = Project(project_name)
  projet.fill_data(file_param)
  projet.get_date_init(file_utheo)

  # .. Fill in data ..
  # ==================
  # ... Initialization ...
  # ----------------------
  bilan = DataDict()
  bilan.init_range(projet.date_init, projet.deadline)
  # ... Extract data from file ...
  # ------------------------------
  bilan.fill_data(file_list)

  # .. Extract data depending on C.L. arguments ..
  # ==============================================
  if args.full:
    selected_items = bilan.get_items_in_full_range(args.inc)
  elif args.range:
    selected_items = bilan.get_items_in_range(
      args.range[0], args.range[1], args.inc
    )
  else:
    range_end   = today
    range_start = (
      range_end + dt.timedelta(weeks=-WEEK_NB) - dt.timedelta(days=1)
    )
    selected_items = bilan.get_items_in_range(
      range_start, range_end, args.inc
    )

  # .. Compute data to be plotted ..
  # ================================
  nb_items = len(selected_items)

  xcoord   = np.linspace(1, nb_items, num=nb_items)
  dates  = [item.date for item in selected_items]

  if args.full:
    run_jobs = np.array([item.run_mean for item in selected_items],
                         dtype=float)
    pen_jobs = np.array([item.pen_mean for item in selected_items],
                         dtype=float)
    run_std  = np.array([item.run_std for item in selected_items],
                         dtype=float)
    pen_std  = np.array([item.pen_std for item in selected_items],
                         dtype=float)
  else:
    run_jobs = np.array([item.run for item in selected_items],
                         dtype=float)
    pen_jobs = np.array([item.pen for item in selected_items],
                         dtype=float)
    run_std  = np.nan
    pen_std  = np.nan

  if args.verbose:
    for i in selected_items:
      if not np.isnan(i.run_mean):
        print(
          "{} {:13.2f} {:13.2f} {:13.2f} {:13.2f}".format(
           i.date,
           i.run_mean, i.pen_mean,
           i.run_std, i.pen_std
          )
        )

  # if projet.project == "gencmip6":
  #   alloc1 = (1 * projet.alloc) / 3
  #   alloc2 = (2 * projet.alloc) / 3
  #   conso_per_day   = 2 * alloc1 / (projet.days * 24.)
  #   conso_per_day_2 = 2 * alloc2 / (projet.days * 24.)
  # else:
  #   conso_per_day = projet.alloc / (projet.days * 24.)
  #   conso_per_day_2 = None
  conso_per_day = projet.alloc / (projet.days * 24.)
  conso_per_day_2 = None

  # .. Plot stuff ..
  # ================
  # ... Initialize figure ...
  # -------------------------
  (fig, ax) = plot_init()

  # ... Plot data ...
  # -----------------
  plot_data(ax, xcoord, dates, run_jobs, pen_jobs, run_std, pen_std)

  # ... Tweak figure ...
  # --------------------
  title = "Suivi des jobs {}\n({:%d/%m/%Y} - {:%d/%m/%Y})".format(
    projet.project.upper(),
    projet.date_init,
    projet.deadline
  )

  plot_config(
    fig, ax, xcoord, dates, title, conso_per_day, conso_per_day_2
  )

  # ... Save figure ...
  # -------------------
  img_in  = os.path.join(DIR["PLOT"], "{}.pdf".format(img_name))
  img_out = os.path.join(DIR["SAVEPLOT"],
                         "{}_w{:02d}.pdf".format(img_name, weeknum))

  plot_save(img_in, img_out, title, DIR)

  # ... Publish figure on dods ...
  # ------------------------------
  if args.dods:
    dods_cp(img_in, DIR)

  if args.show:
    plt.show()

  exit(0)
