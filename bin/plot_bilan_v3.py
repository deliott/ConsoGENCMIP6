#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this must come first
from __future__ import print_function, unicode_literals, division

# standard library imports
from argparse import ArgumentParser
import os
import os.path
import datetime as dt
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
          0: string_to_date,
          1: string_to_float,
          2: string_to_percent,
          3: string_to_percent,
          4: string_to_float,
          5: string_to_float,
          6: string_to_float,
          7: string_to_float,
        },
        missing_values="nan",
      )
    except Exception as rc:
      print("Empty file {}:\n{}".format(filein, rc))
      exit(1)

    for date, conso, real_use, theo_use, \
        run_mean, pen_mean, run_std, pen_std in data:
      if date in self:
        self.add_item(
          date,
          conso,
          real_use,
          theo_use,
          run_mean,
          pen_mean,
          run_std,
          pen_std,
        )
        self[date].fill()

  #---------------------------------------
  def add_item(self, date, conso=np.nan,
               real_use=np.nan, theo_use=np.nan,
               run_mean=np.nan, pen_mean=np.nan,
               run_std=np.nan, pen_std=np.nan):
    """
    """
    self[date] = Conso(date, conso, real_use, theo_use,
                       run_mean, pen_mean, run_std, pen_std)

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

    m = np.array([
      [x1, 1.],
      [x2, 1.]
    ], dtype="float")
    n = np.array([
      y1,
      y2
    ], dtype="float")

    try:
      (a, b) = np.linalg.solve(m, n)
    except np.linalg.linalg.LinAlgError:
      (a, b) = (None, None)

    if a and b:
      for date in dates:
        self[date].theo_equ = date.timetuple().tm_yday*a + b

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
  def __init__(self, date, conso=np.nan,
               real_use=np.nan, theo_use=np.nan,
               run_mean=np.nan, pen_mean=np.nan,
               run_std=np.nan, pen_std=np.nan):
    self.date     = date
    self.conso    = conso
    self.real_use = real_use
    self.theo_use = theo_use
    self.theo_equ = np.nan
    self.run_mean = run_mean
    self.pen_mean = pen_mean
    self.run_std  = run_std
    self.pen_std  = pen_std
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
  fig, (ax_c2, ax_conso) = \
      plt.subplots(2, 1, sharex=True, figsize=(paper_size/2.54))
  ax_theo = ax_c2.twinx()

  return fig, ax_conso, ax_theo, ax_c2


########################################
def plot_data(ax_conso, ax_theo, ax_c2, xcoord, dates,
              consos, theo_uses, real_uses, theo_equs,
              run_mean, pen_mean, run_std, pen_std):
  """
  """
  line_style = "-"
  if args.full:
    line_width = 0.05
  else:
    # line_style = "+-"
    line_width = 0.1

  for ax_c in (ax_conso, ax_c2):
    ax_c.bar(xcoord, consos, width=1, align="center", color="linen",
                 linewidth=line_width, label="conso (heures)")

  ax_theo.plot(xcoord, theo_equs, "--",
               color="firebrick", linewidth=0.5,
               solid_capstyle="round", solid_joinstyle="round")
  ax_theo.plot(xcoord, theo_uses, line_style, color="firebrick",
               linewidth=1, markersize=8,
               solid_capstyle="round", solid_joinstyle="round",
               label="conso théorique (%)")
  ax_theo.plot(xcoord, real_uses, line_style, color="forestgreen",
               linewidth=1, markersize=8,
               solid_capstyle="round", solid_joinstyle="round",
               label="conso réelle (%)")


########################################
def plot_config(fig, ax_conso, ax_theo, ax_c2, xcoord, dates,
                title, conso_per_day):
  """
  """
  # ... Config axes ...
  # -------------------
  # 1) Range
  if args.max:
    ymax = projet.alloc
  else:
    ymax = np.nanmax(consos) + np.nanmax(consos) * .05

  xmin, xmax = xcoord[0]-1, xcoord[-1]+1
  ax_conso.set_xlim(xmin, xmax)

  ax_conso.set_ylim(0., 2. * conso_per_day)
  ax_c2.set_ylim(6. * conso_per_day, ymax)

  ax_theo.set_ylim(0., 100)

  # 2) Ticks labels
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

  # ax_conso.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
  # ax_c2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

  ax_conso.set_xticks(xcoord, minor=True)
  ax_conso.set_xticks(maj_xticks, minor=False)
  ax_conso.set_xticklabels(
    maj_xlabs, rotation="vertical", size="x-small"
  )

  yticks = list(ax_conso.get_yticks())
  yticks.append(conso_per_day)
  ax_conso.set_yticks(yticks)

  # hide the spines between ax and ax2
  ax_c2.spines["bottom"].set_visible(False)
  ax_conso.spines["top"].set_visible(False)
  ax_theo.spines["bottom"].set_visible(False)
  # ax_theo.spines["top"].set_visible(False)

  # don't put tick labels at the top
  ax_c2.xaxis.tick_top()
  ax_c2.tick_params(labeltop=False)
  ax_conso.xaxis.tick_bottom()
  # ax_conso.yaxis.set_ticks_position('left')

  ax_theo.spines["right"].set_color("indianred")
  ax_theo.tick_params(colors="indianred")
  ax_theo.yaxis.label.set_color("indianred")

  # how big to make the diagonal lines in axes coordinates
  d = .015
  # arguments to pass plot, just so we don't keep repeating them
  kwargs = dict(transform=ax_c2.transAxes, color='k', clip_on=False)
  ax_c2.plot((-d, +d), (-d, +d), **kwargs)      # top-left diagonal
  # ax_c2.plot((1-d, 1+d), (-d, +d), **kwargs)    # top-right diagonal

  # switch to the bottom axes
  kwargs.update(transform=ax_conso.transAxes)
  # - bottom-left diagonal
  ax_conso.plot((-d, +d), (1-d, 1+d), **kwargs)
  # - bottom-right diagonal
  ax_conso.plot((1-d, 1+d), (1-d, 1+d), **kwargs)

  ax_conso.axhline(y=conso_per_day, color="blue", alpha=0.5,
                   label="conso journalière idéale (heures)")

  for ax_c in (ax_conso, ax_c2):
    for x, d in zip(xcoord, dates):
      if d.weekday() == 0 and d.hour == 0:
        ax_c.axvline(x=x, color="black", alpha=0.5,
                     linewidth=0.5, linestyle=":")

  # 3) Define axes title
  for ax, label in (
    (ax_conso, ""),
    (ax_c2, "heures"),
    (ax_theo, "%"),
  ):
    ax.set_ylabel(label, fontweight="bold")
    ax.tick_params(axis="y", labelsize="small")

  # 4) Define plot size
  fig.subplots_adjust(
    left   = 0.08,
    bottom = 0.09,
    right  = 0.93,
    top    = 0.93,
    hspace = 0.07,
  )

  # ... Main title and legend ...
  # -----------------------------
  fig.suptitle(title, fontweight="bold", size="large")
  for ax, loc in (
    # (ax_c2, "upper right"),
    (ax_c2, "upper left"),
    (ax_theo, "upper right"),
  ):
    ax.legend(loc=loc, fontsize="x-small", frameon=False)


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
  if args.verbose:
    print(args)

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

  img_name = "bilan_v3"
  today = os.path.basename(file_param).strip(OUT["PARAM"])

  if args.verbose:
    print(file_param)
    print(file_utheo)
    print(file_data)
    print(img_name)
    print(today)

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

  xcoord    = np.linspace(1, nb_items, num=nb_items)
  dates   = [item.date for item in selected_items]

  cumul     = np.array([item.conso for item in selected_items],
                        dtype=float)
  consos    = []
  consos.append(cumul[0])
  consos[1:nb_items] = cumul[1:nb_items] - cumul[0:nb_items-1]
  consos    = np.array(consos, dtype=float)

  conso_per_day = projet.alloc / projet.days

  theo_uses = np.array([100.*item.theo_use for item in selected_items],
                       dtype=float)
  real_uses = np.array([100.*item.real_use for item in selected_items],
                       dtype=float)
  theo_equs = np.array([100.*item.theo_equ for item in selected_items],
                       dtype=float)

  run_mean = np.array([item.run_mean for item in selected_items],
                       dtype=float)
  pen_mean = np.array([item.pen_mean for item in selected_items],
                       dtype=float)
  run_std  = np.array([item.run_std for item in selected_items],
                       dtype=float)
  pen_std  = np.array([item.pen_std for item in selected_items],
                       dtype=float)

  # .. Plot stuff ..
  # ================
  # ... Initialize figure ...
  # -------------------------
  (fig, ax_conso, ax_theo, ax_c2) = plot_init()

  # ... Plot data ...
  # -----------------
  plot_data(ax_conso, ax_theo, ax_c2, xcoord, dates,
            consos, theo_uses, real_uses, theo_equs,
            run_mean, pen_mean, run_std, pen_std)

  # ... Tweak figure ...
  # --------------------
  title = "Consommation {}\n({:%d/%m/%Y} - {:%d/%m/%Y})".format(
    projet.project.upper(),
    projet.date_init,
    projet.deadline
  )

  plot_config(
    fig, ax_conso, ax_theo, ax_c2, xcoord, dates, title, conso_per_day
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
    dods_cp(img_in, DIR)

  if args.show:
    plt.show()

  exit(0)