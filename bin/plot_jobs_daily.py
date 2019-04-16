#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this must come first
from __future__ import print_function, unicode_literals, division

# standard library imports
from argparse import ArgumentParser
import os
import os.path
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np

# Application library imports
from libconso import *


########################################
class DataDict(dict):
  #---------------------------------------
  def __init__(self):
    self = {}

  #---------------------------------------
  def init_range(self, date_beg, date_end, inc=1):
    """
    """
    delta = date_end - date_beg

    (deb, fin) = (0, delta.days+1)

    dates = (date_beg + dt.timedelta(days=i)
             for i in xrange(deb, fin, inc))

    for date in dates:
      self.add_item(date)

  #---------------------------------------
  def fill_data(self, filein):
    """
    """
    try:
      data = np.genfromtxt(
        filein,
        skip_header=1,
        converters={
          0:  string_to_date,
          1:  string_to_float,
          2:  string_to_percent,
          3:  string_to_percent,
          4:  string_to_float,
          5:  string_to_float,
          6:  string_to_float,
          7:  string_to_float,
          8:  string_to_float,
          9:  string_to_float,
          10: string_to_float,
          11: string_to_float,
        },
        missing_values="nan",
      )
    except Exception as rc:
      print("Empty file {}:\n{}".format(filein, rc))
      exit(1)

    for date, conso, real_use, theo_use, \
        runp_mean, penp_mean, runp_std, penp_std, \
        runf_mean, penf_mean, runf_std, penf_std in data:
      if date in self:
        self.add_item(
          date,
          conso,
          real_use,
          theo_use,
          runp_mean,
          penp_mean,
          runp_std,
          penp_std,
          runf_mean,
          penf_mean,
          runf_std,
          penf_std,
        )
        self[date].fill()

  #---------------------------------------
  def add_item(self, date, conso=np.nan,
               real_use=np.nan, theo_use=np.nan,
               runp_mean=np.nan, penp_mean=np.nan,
               runp_std=np.nan, penp_std=np.nan,
               runf_mean=np.nan, penf_mean=np.nan,
               runf_std=np.nan, penf_std=np.nan):
    """
    """
    self[date] = Conso(
      date, conso, real_use, theo_use,
      runp_mean, penp_mean, runp_std, penp_std,
      runf_mean, penf_mean, runf_std, penf_std,
    )

  #---------------------------------------
  def theo_equation(self):
    """
    """
    (dates, theo_uses) = \
      zip(*((item.date, item.theo_use)
            for item in self.get_items_in_full_range()))

    (idx_min, idx_max) = \
        (np.nanargmin(theo_uses), np.nanargmax(theo_uses))

    x1 = dates[idx_min].timetuple().tm_yday
    x2 = dates[idx_max].timetuple().tm_yday

    y1 = theo_uses[idx_min]
    y2 = theo_uses[idx_max]

    m = np.array([[x1, 1.], [x2, 1.]], dtype="float")
    n = np.array([y1, y2], dtype="float")

    poly_ok = True
    try:
      poly_theo = np.poly1d(np.linalg.solve(m, n))
    except np.linalg.linalg.LinAlgError:
      poly_ok = False

    if poly_ok:
      delta = (dates[0] + relativedelta(months=2) - dates[0]).days

      poly_delay = np.poly1d(
        [poly_theo[1], poly_theo[0] - poly_theo[1] * delta]
      )

      self.poly_theo = poly_theo
      self.poly_delay = poly_delay

  #---------------------------------------
  def get_items_in_range(self, date_beg, date_end, inc=1):
    """
    """
    items = (item for item in self.itervalues()
                   if item.date >= date_beg and
                      item.date <= date_end)
    items = sorted(items, key=lambda item: item.date)

    return items[::inc]

  #---------------------------------------
  def get_items_in_full_range(self, inc=1):
    """
    """
    items = (item for item in self.itervalues())
    items = sorted(items, key=lambda item: item.date)

    return items[::inc]

  #---------------------------------------
  def get_items(self, inc=1):
    """
    """
    items = (item for item in self.itervalues()
                   if item.isfilled())
    items = sorted(items, key=lambda item: item.date)

    return items[::inc]


class Conso(object):
  #---------------------------------------
  def __init__(
    self, date, conso=np.nan,
    real_use=np.nan, theo_use=np.nan,
    runp_mean=np.nan, penp_mean=np.nan,
    runp_std=np.nan, penp_std=np.nan,
    runf_mean=np.nan, penf_mean=np.nan,
    runf_std=np.nan, penf_std=np.nan,
  ):
    self.date     = date
    self.conso    = conso
    self.real_use = real_use
    self.theo_use = theo_use
    self.poly_theo = np.poly1d([])
    self.poly_delay = np.poly1d([])
    self.runp_mean = runp_mean
    self.penp_mean = penp_mean
    self.runp_std  = runp_std
    self.penp_std  = penp_std
    self.runf_mean = runf_mean
    self.penf_mean = penf_mean
    self.runf_std  = runf_std
    self.penf_std  = penf_std
    self.filled   = False

  #---------------------------------------
  def __repr__(self):
    return "{:.2f} ({:.2%})".format(self.conso, self.real_use)

  #---------------------------------------
  def isfilled(self):
    return self.filled

  #---------------------------------------
  def fill(self):
    self.filled = True


########################################
def plot_init():
  paper_size  = np.array([29.7, 21.0])
  fig, (ax_jobsp, ax_jobsf) = plt.subplots(
    nrows=2,
    ncols=1,
    sharex=True,
    squeeze=True,
    figsize=(paper_size/2.54)
  )

  return fig, ax_jobsp, ax_jobsf


########################################
def plot_data(ax_jobsp, ax_jobsf, xcoord, dates,
              runp_mean, penp_mean, runp_std, penp_std,
              runf_mean, penf_mean, runf_std, penf_std):
  """
  """

  line_width = 0.
  width = 1.05

  ax_jobsp.bar(
    xcoord, runp_mean, width=width, align="center",
    # yerr=runp_std/2, ecolor="green",
    color="lightgreen", linewidth=line_width,
    antialiased=True, label="jobs running"
  )
  ax_jobsp.bar(
    xcoord, penp_mean, bottom=runp_mean, width=width, align="center",
    # yerr=penp_std/2, ecolor="darkred",
    color="firebrick", linewidth=line_width,
    antialiased=True, label="jobs pending"
  )

  ax_jobsf.bar(
    xcoord, runf_mean, width=width, align="center",
    # yerr=runf_std/2, ecolor="green",
    color="lightgreen", linewidth=line_width,
    antialiased=True, label="jobs running"
  )
  ax_jobsf.bar(
    xcoord, penf_mean, bottom=runf_mean, width=width, align="center",
    # yerr=penf_std/2, ecolor="darkred",
    color="firebrick", linewidth=line_width,
    antialiased=True, label="jobs pending\n(Ressources & Priority)"
  )


########################################
def plot_config(fig, ax_conso, ax_theo, xcoord, dates, title,
                conso_per_day, conso_per_day_2):
  """
  """
  from matplotlib.ticker import AutoMinorLocator

  # ... Config axes ...
  # -------------------
  # 1) Range
  jobsp_max = np.nanmax(runp_mean)
  jobsf_max = np.nanmax(runf_mean)
  conso_jobsf = 80000.
  if args.max:
    ymax_jobsp = jobsp_max  # * 1.1
    ymax_jobsf = jobsf_max  # * 1.1
  else:
    ymax_jobsp = 2. * (max(conso_per_day, conso_per_day_2)/24.)
    ymax_jobsf = 3. * conso_jobsf

  xmin, xmax = xcoord[0]-1, xcoord[-1]+1
  ax_jobsp.set_xlim(xmin, xmax)
  ax_jobsp.set_ylim(0., ymax_jobsp)
  ax_jobsf.set_ylim(0., ymax_jobsf)

  # 2) Plot ideal daily consumption in hours
  line_color = "blue"
  line_alpha = 0.5
  line_label = "conso journalière\nidéale ({})"
  for ax, y_div, label in (
    (ax_jobsp, 24., line_label.format("cœurs")),
  ):
    if conso_per_day_2:
      list_x = [0, xmax/2, xmax/2, xmax]
      list_y = np.array(
        [conso_per_day, conso_per_day, conso_per_day_2, conso_per_day_2],
        dtype=float
      )
      ax.plot(
        list_x, list_y/y_div,
        color=line_color, alpha=line_alpha, label=label,
      )
    else:
      ax.axhline(
        y=conso_per_day/y_div,
        color=line_color, alpha=line_alpha, label=label,
      )
  ax_jobsf.axhline(
    y=conso_jobsf,
    color=line_color, alpha=line_alpha
  )

  # 3) Ticks labels
  (date_beg, date_end) = (dates[0], dates[-1])
  date_fmt = "{:%d-%m}"

  if date_end - date_beg > dt.timedelta(weeks=9):
    maj_xticks = [x for x, d in zip(xcoord, dates)
                     if d.weekday() == 0]
    maj_xlabs  = [date_fmt.format(d) for d in dates
                     if d.weekday() == 0]
  else:
    maj_xticks = [x for x, d in zip(xcoord, dates)]
    maj_xlabs  = [date_fmt.format(d) for d in dates]

  ax_jobsf.set_xticks(xcoord, minor=True)
  ax_jobsf.set_xticks(maj_xticks, minor=False)
  ax_jobsf.set_xticklabels(
    maj_xlabs, rotation="vertical", size="x-small"
  )

  for ax, y, label in (
    (ax_jobsp, conso_per_day / 24., "cœurs (projet)"),
    (ax_jobsf, conso_jobsf, "cœurs (machine)"),
  ):
    minor_locator = AutoMinorLocator()
    ax.yaxis.set_minor_locator(minor_locator)

    yticks = list(ax.get_yticks())
    yticks.append(y)
    ax.set_yticks(yticks)

  if conso_per_day_2:
    yticks.append(conso_per_day_2)

  for x, d in zip(xcoord, dates):
    if d.weekday() == 0 and d.hour == 0:
      for ax in (ax_jobsp, ax_jobsf):
        ax.axvline(x=x, color="black", alpha=0.5,
                   linewidth=0.5, linestyle=":")

  # 4) Define axes title
  for ax, label in (
    (ax_jobsp, "cœurs (projet)"),
    (ax_jobsf, "cœurs (machine)"),
  ):
    ax.set_ylabel(label, fontweight="bold")
    ax.tick_params(axis="y", labelsize="small")

  # 5) Define plot size
  fig.subplots_adjust(
    left=0.08,
    bottom=0.09,
    right=0.93,
    top=0.93,
    hspace=0.1,
    wspace=0.1,
  )

  # ... Main title and legend ...
  # -----------------------------
  fig.suptitle(title, fontweight="bold", size="large")
  for ax, subtitle, loc_legend in (
    (ax_jobsp, "Projet", "upper right"),
    (ax_jobsf, "Tout Curie", "upper right"),
  ):
    ax.legend(loc=loc_legend, fontsize="x-small", frameon=False)
    ax.set_title(subtitle, loc="left")


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
  parser.add_argument("-m", "--max", action="store_true",
                      help="plot with y_max = allocation")
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
                      [OUT["PARAM"], OUT["UTHEO"], OUT["BILAN"]])

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
  bilan.fill_data(file_data)
  # ... Compute theoratical use from known data  ...
  # ------------------------------------------------
  bilan.theo_equation()

  # .. Extract data depending on C.L. arguments ..
  # ==============================================
  if args.full:
    selected_items = bilan.get_items_in_full_range(args.inc)
  elif args.range:
    selected_items = bilan.get_items_in_range(
      args.range[0], args.range[1], args.inc
    )
  else:
    selected_items = bilan.get_items(args.inc)

  # .. Compute data to be plotted ..
  # ================================
  nb_items = len(selected_items)

  xcoord = np.linspace(1, nb_items, num=nb_items)
  dates = [item.date for item in selected_items]

  if projet.project == "gencmip6":
    alloc1 = (1 * projet.alloc) / 3
    alloc2 = (2 * projet.alloc) / 3
    conso_per_day   = 2 * alloc1 / projet.days
    conso_per_day_2 = 2 * alloc2 / projet.days
  else:
    conso_per_day = projet.alloc / projet.days
    conso_per_day_2 = None

  runp_mean = np.array(
    [item.runp_mean for item in selected_items], dtype=float
  )
  penp_mean = np.array(
    [item.penp_mean for item in selected_items], dtype=float
  )
  runp_std  = np.array(
    [item.runp_std for item in selected_items], dtype=float
  )
  penp_std  = np.array(
    [item.penp_std for item in selected_items], dtype=float
  )

  runf_mean = np.array(
    [item.runf_mean for item in selected_items], dtype=float
  )
  penf_mean = np.array(
    [item.penf_mean for item in selected_items], dtype=float
  )
  runf_std  = np.array(
    [item.runf_std for item in selected_items], dtype=float
  )
  penf_std  = np.array(
    [item.penf_std for item in selected_items], dtype=float
  )

  # .. Plot stuff ..
  # ================
  # ... Initialize figure ...
  # -------------------------
  (fig, ax_jobsp, ax_jobsf) = plot_init()

  # ... Plot data ...
  # -----------------
  plot_data(
    ax_jobsp, ax_jobsf, xcoord, dates,
    runp_mean, penp_mean, runp_std, penp_std,
    runf_mean, penf_mean, runf_std, penf_std,
  )

  # ... Tweak figure ...
  # --------------------
  title = (
    "{} : Suivi des jobs (moyenne journalière)\n"
    "({:%d/%m/%Y} - {:%d/%m/%Y})"
  ).format(
    projet.project.upper(),
    projet.date_init,
    projet.deadline
  )

  plot_config(
    fig, ax_jobsp, ax_jobsf,
    xcoord, dates, title, 
    conso_per_day, conso_per_day_2
  )

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

