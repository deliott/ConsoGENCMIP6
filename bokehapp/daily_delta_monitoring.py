"""
This scripts plots the daily consumption monitoring.
It gives a bar plot timeserie of the difference between daily total consumption and optimal consumption.
It is plotted for each processor, etc.
"""
from data_for_plot_extractor import ProjectData
###############################################################
from bokeh.plotting import figure, output_file, save

import settings as settings
import set_paths as set_paths

import plot_set_up as plot_set_up

from bokeh.layouts import gridplot
import datetime
from math import pi

from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter



set_paths.set_path_to_plots()
###############################################################

def delta_plot(project_name, processor):
    pass

def plot_init_delta(processor, project_name):
    """
    Initialize the bokeh plot
    :param processor: str name of the processor type whose data will be plotted
    :param project_name: str, name of the project plotted
    :return p: bokeh figure
    """
    p = figure(title="Daily Delta Monitoring : " + project_name.swapcase(),
               x_axis_label="Date",
               y_axis_label="Irene " + processor + " (heures)",
               x_axis_type="datetime",
               plot_width=900, plot_height=400,
               sizing_mode='scale_width'
               )

    return p


def plot_config_delta(p):
    """

    :param p:
    :return:
    """
    p.legend.location = "top_left"
    p.legend.click_policy = "mute"

    p.xaxis[0].formatter.days = '%a - %d/%m/%Y'
    p.xaxis.major_label_orientation = pi / 3
    p.yaxis.formatter = NumeralTickFormatter(format="0,")


def test_add_optimal_total_difference_ticks_bis(data_for_plot, df_data, df_opti, p):
    """
    Add ticks to show difference between optimal curve and total of consumption.

    :param df_data: dataframe with the cpu time consumption per project and total as columns. Indexed by dates.
    :param df_opti: dataframe with the optimal cpu time consumption as column. Indexed by dates.
    :param p: bokeh figure that will render the glyphs.
    :param days_in_advance: Number of days the optimal curv
    :return: None
    """

    days_in_start_difference_between_data_and_opti = (df_data['Date'].iloc[0] - df_opti['Date'][0]).days

    # print(data_for_plot.optimal_daily_consumption)

    retard_warning = []

    print(len(df_data['Date']))
    for i in range(len(df_data['Date'])):
        print(i)
        if i > 0:
            # opti_value = df_opti['Conso_Optimale'][days_in_start_difference_between_data_and_opti + i]
            opti_value = data_for_plot.optimal_daily_consumption
            total_value = df_data['Total'].iloc[i] - df_data['Total'].iloc[i-1]

            delta_conso = '{:,.0f}'.format(abs(opti_value - total_value)) + ' heures'

            left = df_data['Date'].iloc[i]
            right = df_data['Date'].iloc[i] + datetime.timedelta(days=0.95)

            if opti_value > total_value:
                statut = 'Prise de retard'
                statut_color = 'firebrick'
                statut_top = 0
                statut_bottom = total_value - opti_value
                # statut_bottom = 0
            else:
                statut = 'Prise d\'avance'
                statut_color = 'lightgreen'
                statut_top = total_value - opti_value
                statut_bottom = 0

            source = ColumnDataSource(dict(
                left=[left],
                top=[statut_top],
                right=[right],
                bottom=[statut_bottom],
                color=[statut_color],

            ))
            retard_warning.append(p.quad(left="left", right="right", top="top", bottom="bottom",
                                         color="color",
                                         hover_color="color",
                                         source=source,
                                         alpha=0.5,
                                         name=statut + ' de ' + delta_conso
                                         )
                                  )


    # dates = df_data['Date'][1:].append(df_data['Date'][-1]  + + datetime.timedelta(days=1))

    # print('Dates : ' , df_data['Date'][0])
    #
    # import pandas as pd
    # print('Dates : ' , pd.date_range(start='2019-05-13', end='2019-05-16', freq='D'))

    p.line(df_data['Date'], [-data_for_plot.optimal_daily_consumption]*len(df_data['Date']), line_color="#ff8888", line_width=2, alpha=0.7, legend="200 % Optimal daily consumption")
    p.line(df_data['Date'], [ data_for_plot.optimal_daily_consumption]*len(df_data['Date']), line_color="lime", line_width=2, alpha=0.7, legend="Maximum daily delay ")

    return retard_warning


def test_add_optimal_total_difference_ticks_ter(data_for_plot, df_data, df_opti, p):
    """
    Add ticks to show difference between optimal curve and total of consumption.

    :param df_data: dataframe with the cpu time consumption per project and total as columns. Indexed by dates.
    :param df_opti: dataframe with the optimal cpu time consumption as column. Indexed by dates.
    :param p: bokeh figure that will render the glyphs.
    :param days_in_advance: Number of days the optimal curv
    :return retard_waring : list of Bokeh glyphs (quad) representing the daily consumption. An element represent a day.
    """
    # print('\n\n\n\nDF_OPTI : ', len(df_opti.index))
    # print('DF_DATA : ', type(df_data.index), '\n\n\n\n')

    days_in_start_difference_between_data_and_opti = (df_data.index[0] - df_opti.index[0]).days
    # print('Time delta between start of minitoring and begining of allocation : ' , days_in_start_difference_between_data_and_opti)
    # print('Daily hours amount : ', data_for_plot.optimal_daily_consumption)

    p.line(df_data.index, [3 * data_for_plot.optimal_daily_consumption]*len(df_data.index),
           line_color="olive", line_width=2, alpha=0.7, legend="300 % Optimal daily consumption")
    p.line(df_data.index, [2 * data_for_plot.optimal_daily_consumption]*len(df_data.index),
           line_color="green", line_width=2, alpha=0.7, legend="200 % Optimal daily consumption")
    p.line(df_data.index, [    data_for_plot.optimal_daily_consumption]*len(df_data.index),
           line_color="midnightblue", line_width=2, alpha=0.7, legend="100 % Optimal daily consumption")


    retard_warning = []

    for i in range(len(df_data.index)):
        if i > 0:
            # opti_value = df_opti['Conso_Optimale'][days_in_start_difference_between_data_and_opti + i]
            opti_value = data_for_plot.optimal_daily_consumption
            total_value = df_data['Total'].iloc[i] - df_data['Total'].iloc[i-1]

            delta_conso = '{:,.0f}'.format(abs(opti_value - total_value)) + ' heures'

            left = df_data.index[i] - datetime.timedelta(days=0.95)
            right = df_data.index[i]

            if opti_value < total_value:
                # statut = 'Prise d\'avance'
                statut = 'Consomation quotidienne de ' + '{:,.0f}'.format(abs(total_value)) + ' heures'
                statut_color = 'lightgreen'
                # statut_top = abs(total_value - opti_value)
                statut_top = total_value
                statut_bottom = 0

                # name = statut + ' de ' + delta_conso
                name = statut
                source_bis = ColumnDataSource(dict(
                    left=[left],
                    top=[opti_value],
                    right=[right],
                    bottom=[statut_top],
                    color=['lightgreen'],

                ))
                retard_warning.append(p.quad(left="left", right="right", top="top", bottom="bottom",
                                             color="color",
                                             hover_color="color",
                                             source=source_bis,
                                             alpha=0.5,
                                             # name='Consomation quotidienne de ' + '{:,.0f}'.format(abs(total_value)) + ' heures'
                                             name='Prise d\'avance de '  + '{:,.0f}'.format(abs(total_value - opti_value)) + ' heures'
                                             )
                                      )


            else:

                # statut = 'Prise de retard'
                statut = 'Consomation quotidienne de ' + '{:,.0f}'.format(abs(total_value)) + ' heures'
                # statut_color = 'firebrick'
                statut_color = 'lightgreen'
                # statut_top = abs(opti_value - total_value)
                statut_top =  total_value
                statut_bottom = 0
                # statut_bottom = 0

                name = statut

                source_bis = ColumnDataSource(dict(
                    left=[left],
                    top=[opti_value],
                    right=[right],
                    # bottom=[statut_top],
                    bottom=[total_value],
                    # color=['lightgreen'],
                    color=['firebrick'],

                ))
                retard_warning.append(p.quad(left="left", right="right", top="top", bottom="bottom",
                                             color="color",
                                             hover_color="color",
                                             source=source_bis,
                                             alpha=0.5,
                                             name='Prise de retard de ' + '{:,.0f}'.format(abs(opti_value - total_value)) + ' heures'
                                             )
                                      )


            source = ColumnDataSource(dict(
                left=[left],
                top=[statut_top],
                right=[right],
                bottom=[statut_bottom],
                color=[statut_color],

            ))


            retard_warning.append(p.quad(left="left", right="right", top="top", bottom="bottom",
                                         color="color",
                                         hover_color="color",
                                         source=source,
                                         alpha=0.5,
                                         # name=statut + ' de ' + delta_conso
                                         name=name
                                         )
                                  )

    return retard_warning

def add_difference_hovertool(p, warning_list):

    p.add_tools(HoverTool(
        renderers=warning_list,
        tooltips=[
            # ('Date', '$x{%F}'),
            ('', '$name'),
        ],
        formatters={
            '$x': 'datetime',  # use 'datetime' formatter for 'date' field
        },
        mode='vline'
    ))

# project_dict={}
# project_dict['gencmip6'] = '2019-05-01'
# project_dict['gen0826'] = '2018-10-31'
#
# for project_name in list(project_dict.keys()):
#     start_date = project_dict[project_name]
#     print('\nPlotting ' + project_name + '. It started on ' + start_date + '.')
#
#     data_for_plot = ProjectData(project_name)
#
#     data_for_plot.set_project_timeseries_filename()
#     data_for_plot.load_project_data()
#     data_for_plot.set_dates()
#     # load_project_data() and set_dates()
#     data_for_plot.set_processor_list()
#     processor_list = data_for_plot.processor_list
#
#     print('Processor list : ', processor_list)
#
#     # Creation of the each processor type's figure.
#
#     figure_liste = []
#
#     for processor in processor_list:
#
#         df_data, df_opti = data_for_plot.run_data_for_plot_extractor(processor, start_date)
#
#         print(data_for_plot.optimal_daily_consumption)
#
#         #############################
#         # Configuration du Plot :
#
#         p = plot_init_delta(processor, project_name)
#
#         retard_warning = test_add_optimal_total_difference_ticks_ter(df_data, df_opti, p)
#         # retard_warning = test_add_optimal_total_difference_ticks_bis(df_data, df_opti, p)
#
#         add_difference_hovertool(p, retard_warning)
#
#         plot_set_up.plot_config(p)
#
#         figure_liste.append(p)
#
#
#     output_file(settings.path_to_plots + "/" + project_name + "_DELTA_PLOT.html", title= project_name + " DELTA_PLOT")
#
#     if len(figure_liste) == 1:
#         save(gridplot([figure_liste], plot_width=1800, plot_height=800, sizing_mode='scale_width'))
#     else:
#         save(gridplot([figure_liste], plot_width=600, plot_height=400, sizing_mode='scale_width'))
#
#
#     print('Bokeh plot saved on : ', settings.path_to_plots + "/" + project_name + "_DELTA_PLOT.html")
