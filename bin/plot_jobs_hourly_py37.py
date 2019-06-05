#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this must come first
# TODO: Repair code since switched from python2 to python3


# standard library imports
from argparse import ArgumentParser
import os
import os.path
import datetime as dt
import numpy as np
import pprint

# Application library imports
from bin.libconso_py37 import *

pp = pprint.PrettyPrinter(indent=2)


########################################
class DataDict(dict):
    # ---------------------------------------
    def __init__(self):
        self = {}

    # ---------------------------------------
    def init_range(self, date_beg, date_end, inc=1):
        """
        """
        delta = date_end - date_beg + dt.timedelta(days=1)

        (deb, fin) = (0, int(delta.total_seconds() / 3600))

        dates = (date_beg + dt.timedelta(hours=i)
                 for i in range(deb, fin, inc))

        for date in dates:
            self.add_item(date)

    # ---------------------------------------
    def fill_data(self, file_list, projet, mode="project"):
        """
        """

        for filein in sorted(file_list):
            filedate = dt.datetime.strptime(
                os.path.basename(filein).split("_")[-1],
                "%Y%m%d"
            )
            if filedate < projet.date_init or \
                    filedate > projet.deadline:
                continue

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

            for date, run, pen in data:
                date = dt.datetime(
                    date.year,
                    date.month,
                    date.day,
                    date.hour,
                    0
                )

                if mode == "project":
                    # self.add_item(
                    #   date=date,
                    #   runp=run,
                    #   penp=pen,
                    # )
                    self[date].runp = run
                    self[date].penp = pen
                elif mode == "machine":
                    # self.add_item(
                    #   date=date,
                    #   runf=run,
                    #   penf=pen,
                    # )
                    self[date].runf = run
                    self[date].penf = pen
                self[date].fill()

    # ---------------------------------------
    def add_item(self, date, runp=np.nan, penp=np.nan, runf=np.nan, penf=np.nan):
        """
        """
        self[date] = Conso(
            date,
            runp,
            penp,
            runf,
            penf,
        )

    # ---------------------------------------
    def get_items_in_range(self, date_beg, date_end, inc=1):
        """
        """
        items = (item for item in self.values()
                 if item.date >= date_beg and
                 item.date <= date_end)
        items = sorted(items, key=lambda item: item.date)

        return items[::inc]

    # ---------------------------------------
    def get_items(self, inc=1):
        """
        """
        items = (item for item in self.values()
                 if item.isfilled())
        items = sorted(items, key=lambda item: item.date)

        return items[::inc]


class Conso(object):
    # ---------------------------------------
    def __init__(self, date, runp=np.nan, penp=np.nan, runf=np.nan, penf=np.nan):
        self.date = date
        self.runp = runp
        self.penp = penp
        self.runf = runf
        self.penf = penf
        self.filled = False

    # ---------------------------------------
    def __repr__(self):
        return "R{:.0f} P{:.0f}".format(
            self.runp,
            self.penp,
        )

    # ---------------------------------------
    def isfilled(self):
        return self.filled

    # ---------------------------------------
    def fill(self):
        self.filled = True


########################################
def plot_init():
    paper_size = np.array([29.7, 21.0])
    fig, (ax_jobsp, ax_jobsf) = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        squeeze=True,
        figsize=(paper_size / 2.54)
    )

    return fig, ax_jobsp, ax_jobsf


########################################
def plot_data(
        ax_jobsp, ax_jobsf, xcoord, dates,
        runp, penp, runf, penf
):
    """
    """
    line_width = 0.
    width = 1.05

    # max_cores = 80000.

    ax_jobsp.bar(
        # xcoord, penp, bottom=runp, width=width,
        # xcoord, penp, bottom=max(runp), width=width,
        # xcoord, penp, bottom=8000., width=width,
        xcoord, penp, bottom=3082., width=width,  # This change is not sure. Maybe it is bad
        linewidth=line_width, align="center",
        color="firebrick", antialiased=True,
        label="jobs pending"
    )
    ax_jobsp.bar(
        xcoord, runp, width=width,
        linewidth=line_width, align="center",
        color="lightgreen", ecolor="green", antialiased=True,
        label="jobs running"
    )

    ax_jobsf.bar(
        # xcoord, penf, bottom=runf, width=width,
        xcoord, penf, bottom=MAX_CORES, width=width,
        linewidth=line_width, align="center",
        color="firebrick", antialiased=True,
        label="jobs pending\n(Ressources & Priority)"
    )
    ax_jobsf.bar(
        xcoord, runf, width=width,
        linewidth=line_width, align="center",
        color="lightgreen", ecolor="green", antialiased=True,
        label="jobs running"
    )


########################################
def plot_config(
        fig, ax_jobsp, ax_jobsf, xcoord, dates,
        title, conso_per_day, conso_per_day_2
):
    """
    """
    from matplotlib.ticker import AutoMinorLocator

    # ... Compute useful stuff ...
    # ----------------------------
    # conso_jobsf = 80000.
    conso_jobsf = MAX_CORES

    multialloc = False

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
        date_inter = projet.date_init + dt.timedelta(days=projet.days // 2)
        if projet.date_init in dates:
            xi = dates.index(projet.date_init)
        else:
            xi = 0

        if projet.deadline in dates:
            xf = dates.index(projet.deadline)
        else:
            xf = len(dates)

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
    xmin, xmax = xcoord[0] - 1, xcoord[-1] + 1
    if multialloc:
        ymax_jobsp = 4. * max(yi, yf)
    else:
        ymax_jobsp = 4. * yi
    ymax_jobsf = 4. * conso_jobsf
    ax_jobsp.set_xlim(xmin, xmax)
    ax_jobsp.set_ylim(0, ymax_jobsp)
    ax_jobsf.set_ylim(0, ymax_jobsf)

    # 2) Plot ideal daily consumption
    line_color = "blue"
    line_alpha = 0.5
    line_label = "conso journalière idéale"
    ax_jobsp.plot(
        [xi, xn, xn, xf], [yi, yi, yf, yf],
        color=line_color, alpha=line_alpha, label=line_label,
    )
    ax_jobsf.axhline(
        y=conso_jobsf,
        color=line_color, alpha=line_alpha
    )

    # 3) Ticks labels
    (date_beg, date_end) = (dates[0], dates[-1])

    if date_end - date_beg > dt.timedelta(weeks=9):
        date_fmt = "{:%d-%m}"
        maj_xticks = [x for x, d in zip(xcoord, dates)
                      if d.weekday() == 0 and d.hour == 0]
        maj_xlabs = [date_fmt.format(d) for d in dates
                     if d.weekday() == 0 and d.hour == 0]
    else:
        date_fmt = "{:%d-%m %Hh}"
        maj_xticks = [x for x, d in zip(xcoord, dates)
                      if d.hour == 0 or d.hour == 12]
        maj_xlabs = [date_fmt.format(d) for d in dates
                     if d.hour == 0 or d.hour == 12]

    ax_jobsf.set_xticks(xcoord, minor=True)
    ax_jobsf.set_xticks(maj_xticks, minor=False)
    ax_jobsf.set_xticklabels(maj_xlabs, rotation="vertical", size="x-small")

    for ax in (ax_jobsp, ax_jobsf):
        minor_locator = AutoMinorLocator()
        ax.yaxis.set_minor_locator(minor_locator)

    yticks = list(ax_jobsp.get_yticks())
    # yticks.append(conso_per_day)
    # if multialloc:
    #   yticks.append(conso_per_day_2)
    yticks.extend([yi, yf])
    ax_jobsp.set_yticks(yticks)

    yticks = list(ax_jobsf.get_yticks())
    yticks.append(conso_jobsf)
    ax_jobsf.set_yticks(yticks)

    for x, d in zip(xcoord, dates):
        if d.weekday() == 0 and d.hour == 0:
            for ax in (ax_jobsp, ax_jobsf):
                ax.axvline(x=x, color="black", linewidth=1., linestyle=":")

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
    # ax_jobsp.legend(loc="upper right", fontsize="x-small", frameon=False)
    for ax, subtitle, loc_legend in (
            (ax_jobsp, "Projet", "upper right"),
            (ax_jobsf, "Tout Irene", "upper right"),
    ):
        ax.legend(loc=loc_legend, fontsize="x-small", frameon=False)
        ax.set_title(subtitle, loc="left")


########################################
def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="verbose mode")
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
    MAX_CORES = 79200

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

    jobsp_file_list = glob.glob(
        os.path.join(DIR["SAVEDATA"], "OUT_JOBS_PENDING_*")
    )
    jobsf_file_list = glob.glob(
        os.path.join(DIR["SAVEDATA"], "OUT_JOBS_PEN_FULL_*")
    )

    img_name = os.path.splitext(
        os.path.basename(__file__)
    )[0].replace("plot_", "")

    today = dt.datetime.today()
    weeknum = today.isocalendar()[1]

    if args.verbose:
        fmt_str = "{:10s} : {}"
        print(fmt_str.format("args", args))
        print(fmt_str.format("today", today))
        print(fmt_str.format("file_param", file_param))
        print(fmt_str.format("file_utheo", file_utheo))
        print(fmt_str.format("jobsp", jobsp_file_list))
        print(fmt_str.format("jobsf", jobsf_file_list))
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
    bilan.fill_data(jobsp_file_list, projet, mode="project")
    bilan.fill_data(jobsf_file_list, projet, mode="machine")

    # .. Extract data depending on C.L. arguments ..
    # ==============================================
    if args.range:
        selected_items = bilan.get_items_in_range(
            args.range[0], args.range[1], args.inc
        )
    else:
        range_end = today
        range_start = (
                range_end + dt.timedelta(weeks=-WEEK_NB) - dt.timedelta(days=1)
        )
        selected_items = bilan.get_items_in_range(
            range_start, range_end, args.inc
        )

    # .. Compute data to be plotted ..
    # ================================
    nb_items = len(selected_items)

    xcoord = np.linspace(1, nb_items, num=nb_items)
    dates = [item.date for item in selected_items]

    runp = np.array([item.runp for item in selected_items],
                    dtype=float)
    penp = np.array([item.penp for item in selected_items],
                    dtype=float)
    runf = np.array([item.runf for item in selected_items],
                    dtype=float)
    penf = np.array([item.penf for item in selected_items],
                    dtype=float)

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
    (fig, ax_jobsp, ax_jobsf) = plot_init()

    # ... Plot data ...
    # -----------------
    plot_data(
        ax_jobsp, ax_jobsf, xcoord, dates,
        runp, penp, runf, penf
    )

    # ... Tweak figure ...
    # --------------------
    title = "Suivi des jobs {}\n({:%d/%m/%Y} - {:%d/%m/%Y})".format(
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
    img_in = os.path.join(DIR["PLOT"], "{}.pdf".format(img_name))
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
