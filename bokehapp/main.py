from os.path import join, dirname
import datetime

import pandas as pd
from scipy.signal import savgol_filter

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
    return ColumnDataSource(df_data)


def plot_initialisation( processor, project_name):
    plot = plot_set_up.plot_init(processor, project_name, 25000000)

    return plot
def make_plot_conso(source, title, processor, project_name):

    # print(source.to_df())

    # plot = plot_set_up.plot_init(processor, project_name, data_for_plot.allocated_dict[processor])


    # plot = plot_set_up.plot_init(processor, project_name, 25000000)

    print('plot initiated\n')
    # plot = figure(x_axis_type="datetime", plot_width=800, tools="", toolbar_location=None)
    plot.title.text = title

    line_list = []
    plot_set_up.add_subprojects_to_line_list_bis(1, source, plot, line_list)

    # fixed attributes
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Temperature (F)"
    plot.axis.axis_label_text_font_style = "bold"
    plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 0.3

    # return plot


def update_plot_conso(attrname, old, new):
    city = city_select.value
    plot.title.text = "Weather data for " + project_dict[city]

    src = get_dataset_conso(city, 'Skylake')

    source.data.update(src.data)



city = 'gencmip6'
distribution = 'Discrete'


city_select = Select(value=city, title='Project Name', options=sorted(project_dict.keys()))
distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smoothed'])

# df = pd.read_csv(join(dirname(__file__), 'data/2015_weather.csv'))
source = get_dataset_conso(city, 'Skylake')


plot = plot_initialisation( 'Skylake', city_select.value)
# plot = make_plot_conso(source, "Weather data for " + project_dict[city], 'Skylake', city_select.value)
make_plot_conso(source, "Weather data for " + project_dict[city], 'Skylake', city_select.value)

city_select.on_change('value', update_plot_conso)
distribution_select.on_change('value', update_plot_conso)

controls = column(city_select, distribution_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Consomation"
