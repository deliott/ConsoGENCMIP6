import glob
#import matplotlib as mpl
import matplotlib.pyplot as plt
from bin.libconso_py37 import *
import bin.settings as settings
import bin.set_paths as set_paths
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Set3


def get_project_name(chemin):
    """
    Get the name of the projectin 8 letters from the path leading to the project data.

    :param chemin: path to conso*.dat file
    :type chemin: str
    :return: name of the project in 8 letters
    :rtype: str

    >>> get_project_name("/home/edupont/data_conso/conso_anacmip6.dat")
    'anacmip6'
    """
    if len(chemin) < 12:
        raise IndexError('Path is too small to contain project_name.dat')
    else :
        return chemin[-12:-4]

########################################

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # .. Initialization ..
    # ====================
    # ... Config Path ...
    # -------------------
    settings.init()
    set_paths.set_config_path()

    project_name, DIR, OUT = parse_config(settings.config_path)

    files = glob.glob(DIR["SAVEDATA"] + "/conso_*.dat")

    df = pd.read_table(files[0], header=None, delim_whitespace=True)
    name = get_project_name(files[0])
    df.columns = ['Date', name]
    output_file(DIR["SAVEPLOT"] + "test.html")

    colormap = Set3[12]
    p = figure(title="Consommation de l'allocation CMIP6", x_axis_label="Année 2018 - 2019 - 2020", y_axis_label="Irene skylake (millions d'heures)")
    #p.line(df['Date'], df[name], legend=name, line_width=2, color=colormap[0])

    for file in files[1:]:
        df1 = pd.read_table(file, header=None, delim_whitespace=True)
        name = get_project_name(file)
        df1.columns = ['Date', name]
        df[name] = df1[name]

#@TODO : sort colulmns according to last value to get only the 10 biggest
#@TODO : Check why we dont get the A6 allocation data

    df=df[df.iloc[-1,:].sort_values(ascending=False).index]
#
#     df.sort_index(level=-1, inplace=True)

    for i in range(12):
        if not df.columns[i] == 'Date':
            p.line(df['Date'], df[df.columns[i]], legend=df.columns[i], line_width=2, color=colormap[i])


# p.line(df['Date'], df.columns[1], legend=df.columns[1], line_width=2)
    p.legend.location = "top_left"
    show(p)