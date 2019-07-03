from os.path import join, dirname
import datetime

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.palettes import Blues4
from bokeh.plotting import figure

from data_for_plot_extractor import ProjectData
import plot_set_up as plot_set_up

import set_paths as set_paths
set_paths.set_path_to_plots()

project_dict = {}
project_dict['gencmip6'] = '2019-05-01'
project_dict['gen0826'] = '2018-10-31'

STATISTICS = ['record_min_temp', 'actual_min_temp', 'average_min_temp', 'average_max_temp', 'actual_max_temp', 'record_max_temp']

def get_dataset_conso(project_name, processor):

    data_for_plot = ProjectData(project_name)

    data_for_plot.set_project_timeseries_filename()
    data_for_plot.load_project_data()
    data_for_plot.set_dates()
    # load_project_data() and set_dates()
    data_for_plot.set_processor_list()
    processor_list = data_for_plot.processor_list

    df_data, df_opti = data_for_plot.run_data_for_plot_extractor(processor, project_dict[str(project_name)])

    # df = src[src.airport == project_name].copy()
    # del df['airport']
    # df['date'] = pd.to_datetime(df.date)
    # # timedelta here instead of pd.DateOffset to avoid pandas bug < 0.18 (Pandas issue #11925)
    # df['left'] = df.date - datetime.timedelta(days=0.5)
    # df['right'] = df.date + datetime.timedelta(days=0.5)
    df_data = df_data.set_index(['Date'])
    df_data.sort_index(inplace=True)
    # if processor == 'Smoothed':
    #     window, order = 51, 3
    #     for key in STATISTICS:
    #         df[key] = savgol_filter(df[key], window, order)

    # return ColumnDataSource(data=df_data)
    return ColumnDataSource(data=df_data)


def make_plot_conso(source, title, processor, project_name):

    plot = plot_set_up.plot_init(processor, project_name, 25000000)

    plot.title.text = title

    plot_set_up.add_subprojects_to_line_list_bis(1, source, plot, line_list=[])

    # fixed attributes
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Temperature (F)"
    plot.axis.axis_label_text_font_style = "bold"
    plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 0.3

    return plot


def update_plot_conso(attrname, old, new):
    project = project_select.value
    processor = processor_select.value
    plot.title.text = "Weather data for " + project_dict[project]

    src = get_dataset_conso(project, processor)

    source.data.update(src.data)


def project_ticker_change(attrname, old, new):
    if project_select.value == 'gencmip6':
        processor_select.value = 'Skylake'


def processor_ticker_change(attrname, old, new):
    if project_select.value == 'gencmip6':
        processor_select.options = ['Skylake']
    else:
        processor_select.options = ['Skylake', 'KNL']


project_name = 'gencmip6'
processor = 'Skylake'


project_select = Select(value=project_name, title='Project Name', options=sorted(project_dict.keys()))
processor_select = Select(value=processor, title='Processor', options=['Skylake'])

source = get_dataset_conso(project_name, 'Skylake')
plot = make_plot_conso(source, "Weather data for " + project_dict[project_name], 'Skylake', project_select.value)

project_select.on_change('value', processor_ticker_change, project_ticker_change, update_plot_conso)
processor_select.on_change('value', update_plot_conso)

# set up layout
controls = column(project_select, processor_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Consomation"
