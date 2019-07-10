from os.path import join, dirname
import datetime

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, MultiSelect
from bokeh.palettes import Blues4
from bokeh.plotting import figure

from data_for_plot_extractor import ProjectData
import plot_set_up as plot_set_up

import subprojects_display_methods as sdm

import set_paths as set_paths
set_paths.set_path_to_plots()

project_dict = {}
project_dict['gencmip6'] = '2019-05-01'
project_dict['gen0826'] = '2018-10-31'

STATISTICS = ['record_min_temp', 'actual_min_temp', 'average_min_temp', 'average_max_temp', 'actual_max_temp',
              'record_max_temp']

def get_dataset_conso(project_name, processor, subproject_list):

    data_for_plot = ProjectData(project_name)

    data_for_plot.set_project_timeseries_filename()
    data_for_plot.load_project_data()
    data_for_plot.set_dates()
    # load_project_data() and set_dates()
    data_for_plot.set_processor_list()
    processor_list = data_for_plot.processor_list

    df_data, df_opti = data_for_plot.run_data_for_plot_extractor_selected_list(
        processor,
        project_dict[str(project_name)],
        subproject_list
    )

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
    # print('get_dataset_conso - DF_DATA : ', df_data)
    return ColumnDataSource(data=df_data), ColumnDataSource(data=df_opti)


# def make_plot_conso(source, line_list):
#
#     plot = plot_set_up.plot_init(processor_select.value,  project_select.value, 27070000)
#
#     plot.title.text ="Consomation data for " + project_select.value + ' on ' + processor_select.value + ' nodes.'
#
#     # line_list = []
#     # plot_set_up.add_subprojects_to_line_list_bis(1, source, plot, line_list=line_list)
#
#     plot_set_up.add_subprojects_to_line_list_ter(['Total'], source, plot, line_list=line_list)
#     # plot_set_up.add_subprojects_to_line_list_ter(['Total'], source, plot, line_list=line_liste)
#
#     # plot_set_up.add_optimal_consumption_curve(source_opt, plot, line_list)
#
#     # fixed attributes
#     if processor_select.value == 'Skylake':
#         plot.axis.axis_label_text_font_style = "bold"
#     else:
#         plot.axis.axis_label_text_font_style = "italic"
#
#
#     plot.x_range = DataRange1d(range_padding=0.0)
#     plot.grid.grid_line_alpha = 0.3
#
#     plot_set_up.plot_config(plot)
#
#     return plot

def create_figure():
    plot = plot_set_up.plot_init(processor_select.value, project_select.value, 27070000)
    plot.title.text ="Consomation data for " + project_select.value + ' on ' + processor_select.value + ' nodes.'

    subproject_list = subproject_multiselect.value
    source_data, source_opti = get_dataset_conso(project_select.value, processor_select.value, subproject_list)

    line_list = []
    plot_set_up.add_subprojects_to_line_list_ter(['Total'], source_data, plot, line_list=line_list)

    # add_data_lines(plot, source_data, line_list)

    nb_plot = 1
    nb_sousprojets = len(subproject_list)
    df_data = source_data.to_df()
    # line_list = []
    from bokeh.palettes import Spectral
    palette = list(reversed(Spectral[min(nb_sousprojets + 2, 11)]))
    for header in subproject_list:
        # print(header)
        if not header == 'Date':
            # Conditions pour afficher le sous projet :
            # sa dernière valeure n'est pas nulle
            # On pourrait rajouter d'autres conditions, telles que :
            # - si la valeur a varié depuis longtemps.
            # if not df_data[header].iloc[-1] == 0:
            if nb_plot <= nb_sousprojets:
                if header == 'Total':
                    if len(list(df_data.columns)) > 3:
                        line_list.append(plot.line('Date', header, source=source,
                                                legend=header + ' ',
                                                # small hack to be able to display the name.
                                                # Otherwise, without the ' ' there is a bug
                                                name=header + ' ',
                                                # small hack to be able to display the name.
                                                # Otherwise, without the ' ' there is a bug
                                                line_width=3,
                                                color="black",
                                                muted_color="black", muted_alpha=0.2
                                                )
                                         )
                else:
                    print((nb_plot - 1) % 11)
                    line_list.append(plot.line('Date', header, source=source,
                                               legend=header + ' ',
                                               name=header + ' ',
                                               # small hack to be able to display the name.
                                               # Otherwise, without the ' ' there is a bug
                                               # line_width=3,
                                               color=palette[(nb_plot-1) % 11],
                                               muted_color=palette[(nb_plot-1 )% 11], muted_alpha=0.2
                                               )
                                     )
                nb_plot = nb_plot + 1

    add_opti_curve(plot, source_opti, line_list)

    # Set up plot display details (legend, axis types, etc)
    plot_set_up.plot_config(plot)

    return plot


def add_data_lines(plot, source_data, line_list):
    nb_plot = 1
    nb_sousprojets = len(subproject_list)
    df_data = source_data.to_df()
    # line_list = []
    from bokeh.palettes import Spectral
    palette = list(reversed(Spectral[min(nb_sousprojets + 2, 11)]))
    for header in subproject_list:
        # print(header)
        if not header == 'Date':
            # Conditions pour afficher le sous projet :
            # sa dernière valeure n'est pas nulle
            # On pourrait rajouter d'autres conditions, telles que :
            # - si la valeur a varié depuis longtemps.
            # if not df_data[header].iloc[-1] == 0:
            if nb_plot <= nb_sousprojets:
                if header == 'Total':
                    if len(list(df_data.columns)) > 3:
                        line_list.append(plot.line('Date', header, source=source,
                                                legend=header + ' ',
                                                # small hack to be able to display the name.
                                                # Otherwise, without the ' ' there is a bug
                                                name=header + ' ',
                                                # small hack to be able to display the name.
                                                # Otherwise, without the ' ' there is a bug
                                                line_width=3,
                                                color="black",
                                                muted_color="black", muted_alpha=0.2
                                                )
                                         )
                else:
                    print((nb_plot - 1) % 11)
                    line_list.append(plot.line('Date', header, source=source,
                                               legend=header + ' ',
                                               name=header + ' ',
                                               # small hack to be able to display the name.
                                               # Otherwise, without the ' ' there is a bug
                                               # line_width=3,
                                               color=palette[(nb_plot-1) % 11],
                                               muted_color=palette[(nb_plot-1 )% 11], muted_alpha=0.2
                                               )
                                     )
                nb_plot = nb_plot + 1

def add_opti_curve(plot, source_opt, line_list):
    plot_set_up.add_optimal_consumption_curve_bis(source_opt, plot, line_list)


def update_plot_conso(attrname, old, new):
    """
    Update the main time series plot depending on the tickers selected.
    Executed when tickers are changed.

    :return: None
    """
    project = project_select.value
    processor = processor_select.value
    column_names_to_remove = source.column_names
    column_names_to_remove.remove('Date')
    column_names_to_remove.remove('Total')
    print('\nColonnes à supprimer : ', column_names_to_remove)

    # plot.title.text = "Consomation data for " + project_select.value + ' on ' + processor_select.value + ' nodes.'

    src, src_opti = get_dataset_conso(project, processor, subproject_multiselect.value)
    source.data.update(src.data)

    # print(source.to_df())

    # print('\nColonnes à supprimer : ', column_names_to_remove)
    [source.remove(name) for name in column_names_to_remove]
    source_opti.data.update(src_opti.data)
    # print(source.to_df())


def project_ticker_change(attrname, old, new):
    """
    Change the processor tickers value depending on the project selected in order to avoid selecting non-existent data.
    :return: None
    """
    if project_select.value == 'gencmip6':
        processor_select.value = 'Skylake'


def processor_ticker_change(attrname, old, new):
    """
    Change the processor tickers options depending on the processor selected in order to avoid selecting
    non-existent data.
    :return: None
    """
    if project_select.value == 'gencmip6':
        processor_select.options = ['Skylake']
    else:
        processor_select.options = ['Skylake', 'KNL']


def subproject_multiselect_change(attrname, old, new):
    # subproject_list, res0 = sdm.get_subproject_list(source)

    active_subproject_list, inactive_subproject_list = sdm.get_subproject_list(source)
    subproject_list = active_subproject_list + inactive_subproject_list

    # subproject_multiselect.value = ['Total']
    subproject_multiselect.value = ['Total']
    subproject_multiselect.options = list(zip(subproject_list,
                                         active_subproject_list
                                              + sdm.modify_inactive_project_names(inactive_subproject_list)
                                              )
                                          )

def update(attr, old, new):
    layout.children[1] = create_figure()


project_name = 'gencmip6'
processor = 'Skylake'
subproject_list = ['dcpcmip6', 'pmicmip6', 'devcmip6', 'ls3cmip6', 'volcmip6',
                   'rfmcmip6', 'dekcmip6', 'scecmip6', 'geocmip6', 'checmip6',
                   'rcecmip6', 'anacmip6', 'c4mcmip6', 'cfmcmip6', 'cm5cmip6',
                   'daacmip6', 'dmrcmip6', 'fafcmip6', 'gmmcmip6', 'hircmip6', 'ismcmip6']

# Define the Widgets
project_select = Select(value=project_name, title='Project Name', options=sorted(project_dict.keys()))
processor_select = Select(value=processor, title='Processor', options=['Skylake'])


plotted_line_liste = []

source, source_opti = get_dataset_conso(project_name, 'Skylake', subproject_list)
# plot = make_plot_conso(source, line_list=plotted_line_liste)
# plot = add_opti_curve(plot, source_opti, line_list=plotted_line_liste)

# Define more widget
active_subproject_list, inactive_subproject_list = sdm.get_subproject_list(source)
subproject_list = active_subproject_list + inactive_subproject_list

subproject_multiselect = MultiSelect(title="Subprojects:",
                                     value=active_subproject_list,
                                     options=list(zip(
                                         subproject_list,
                                         active_subproject_list
                                         + sdm.modify_inactive_project_names(inactive_subproject_list)
                                     )),
                                     size=8
                                     )


# Define widget actions
project_select.on_change('value',
                         processor_ticker_change,
                         project_ticker_change,
                         update_plot_conso,
                         subproject_multiselect_change
                         )
# project_select.on_change('value',
#                          processor_ticker_change,
#                          project_ticker_change,
#                          update,
#                          subproject_multiselect_change
#                          )

# processor_select.on_change('value', update_plot_conso)
processor_select.on_change('value', update)
subproject_multiselect.on_change('value', update,
                                 # subproject_multiselect_change,
                                 )

# set up layout
controls = column(project_select, processor_select, subproject_multiselect)

# layout = row(controls, plot)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Consomation"
