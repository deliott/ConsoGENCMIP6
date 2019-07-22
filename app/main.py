from os.path import join, dirname
import datetime

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column, layout, widgetbox, Spacer
from bokeh.models import ColumnDataSource, Select, MultiSelect, CustomJS

from data_for_plot_extractor import ProjectData

import plot_set_up as plot_set_up

import subprojects_display_methods as sdm


from daily_delta_monitoring import plot_init_delta, plot_config_delta, test_add_optimal_total_difference_ticks_bis,\
    test_add_optimal_total_difference_ticks_ter, add_difference_hovertool


import set_paths as set_paths
set_paths.set_path_to_plots()

project_dict = dict()
project_dict['gencmip6'] = '2019-05-01'
project_dict['gen0826'] = '2018-10-31'


def instance_data_for_plot(project_name):
    """
    Check the usages of this function.
    -> in the definition of the initialisation of the plot.
    -> in create_figure
    """
    # print("\n\nCall of get_dataset_conso with : ", project_name, " - ", processor, " - ", subproject_list , "\n\n")
    data_for_plot = ProjectData(project_name)

    data_for_plot.set_project_timeseries_filename()
    data_for_plot.load_project_data()
    data_for_plot.set_dates()
    data_for_plot.set_processor_list()

    return data_for_plot


def get_dataset_conso(project_name, processor, subproject_list, data_for_plot):
    """
    Same as bis just different output type.
    Check the usages of this function.
    -> in the definition of the initialisation of the plot.
    -> in create_figure
    """

    df_data, df_opti = data_for_plot.run_data_for_plot_extractor_selected_list(
        processor,
        project_dict[str(project_name)],
        subproject_list
    )
    # df_data = df_data.set_index(['Date'], inplace=True)
    df_data = df_data.set_index(['Date'])
    df_data.sort_index(inplace=True)

    # df_opti = df_opti.set_index(['Date'], inplace=True)
    df_opti = df_opti.set_index(['Date'])

    return df_data, df_opti


def create_figure():
    plot = plot_set_up.plot_init(processor_select.value, project_select.value, 27070000)
    plot.title.text = "Consomation data for " + project_select.value + ' on ' + processor_select.value + ' nodes.'

    selected_subproject_list = subproject_multiselect.value
    if project_select.value == 'gencmip6':
        selected_subproject_list = ['Total'] + selected_subproject_list

    # source_data, source_opti = get_dataset_conso(project_select.value, processor_select.value, selected_subproject_list)
    df_data, df_opti = get_dataset_conso(project_select.value,
                                                     processor_select.value,
                                                     selected_subproject_list,
                                                     instance_data_for_plot(project_select.value))
    # source_data, source_opti = get_dataset_conso(project_select.value,
    #                                                  processor_select.value,
    #                                                  selected_subproject_list,
    #                                                  instance_data_for_plot(project_select.value))
    # df_opti = source_opti.to_df()

    line_list = []

    add_data_lines(plot, ColumnDataSource(data=df_data), line_list, selected_subproject_list)

    # # Nouvelle version
    retard_warning = plot_set_up.add_optimal_total_difference_ticks_bis(df_data, df_opti, plot)
    plot_set_up.add_warnings_hovertool(plot, retard_warning)

    add_opti_curve_patch_and_bonus(plot, df_opti, line_list)

    plot_set_up.add_curves_hovertool(plot, line_list)

    # Set up plot display details (legend, axis types, etc)

    plot_set_up.set_plot_xaxis_default_range(plot, df_opti, project_dict[str(project_select.value)])
    plot_set_up.plot_config(plot)

    return plot


def create_delta():
    """Don't forget to refactor this function."""
    q = plot_init_delta(processor_select.value, project_select.value)

    data_for_plot = instance_data_for_plot(project_select.value)

    df_data, df_opti = get_dataset_conso(project_select.value,
                                                     processor_select.value,
                                                     subproject_multiselect.value,
                                                     data_for_plot
                                                     )

    retard_warning = test_add_optimal_total_difference_ticks_ter(data_for_plot,
                                                                 df_data,
                                                                 df_opti,
                                                                 q
                                                                 )
    # retard_warning = test_add_optimal_total_difference_ticks_bis(data_for_plot, df_data, df_opti, q)

    add_difference_hovertool(q, retard_warning)

    # plot_set_up.set_plot_xaxis_default_range(q, source_opti.to_df(), project_dict[str(project_select.value)])
    # q.x_range = plots.children[0].x_range
    q.x_range = layout.children[0].children[1].children[0].x_range
    plot_config_delta(q)

    return q


def add_data_lines(plot, source_data, line_list, selected_subproject_list):
    plot_set_up.add_subprojects_to_line_list_bis(plot, source_data, line_list, selected_subproject_list)


def add_opti_curve_patch_and_bonus(plot, df_opti, line_list):
    plot_set_up.add_optimal_consumption_curve(df_opti, plot, line_list)  # runs a CDS() bis uses source directly
    delai_avant_penalite = 60
    plot_set_up.add_optimal_consumption_patch_bis(delai_avant_penalite, df_opti, plot, 'orange')  # does not uses source
    plot_set_up.add_possible_bonus_curve(df_opti, plot, line_list)  # runs a CDS()


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
    if project_select.value == 'gencmip6':
        liste_sousprojets = active_subproject_list_gencmip6 + inactive_subproject_list_gencmip6
        subproject_multiselect.value = ['Total']
        subproject_multiselect.options = list(zip(liste_sousprojets,
                                                  active_subproject_list_gencmip6
                                                  + sdm.modify_inactive_project_names(inactive_subproject_list_gencmip6)
                                                  )
                                              )
    else:
        liste_sousprojets = [project_select.value]
        subproject_multiselect.value = [project_select.value]
        subproject_multiselect.options = list(zip(liste_sousprojets,liste_sousprojets))


def update(attrname, old, new):
    # p = create_figure()
    # q = create_delta()
    # layout.children[0].children[1] = column(p, q,
    #                                        # sizing_mode='scale_height',
    #                                        sizing_mode='scale_width',
    #                                        )
    layout.children[0].children[1].children[0] = create_figure()  # p
    print('\nUpdate de P done ')
    layout.children[0].children[1].children[1] = create_delta()   # q
    print('\nUpdate de Q done')
    print('OLD : ', old)
    print('NEW : ', new)

def update_conso(attrname, old, new):
    """
    Can be used to speed up the update when multiselct is used.
    So far it breaks the x-axis link between the plots.
    """

    print(layout.children[0].children[1].children[0].x_range)

    p = create_figure()  #
    layout.children[0].children[1].children[0] = p

    print(p.x_range)
    print('Update of top plot : done ')

    # Re-create the link between the x-axis. (Since the conso plot has been changed.)

    # print(layout.children[0].children[1].children[1].x_range)

    # layout.children[0].children[1].children[1].x_range = layout.children[0].children[1].children[0].x_range
    layout.children[0].children[1].children[1].x_range = p.x_range

    print(layout.children[0].children[1].children[1].x_range)


    print('\nX-axis link : recreated. --> So far there is a issue.')
    print('OLD : ', old)
    print('NEW : ', new)



# Define variables for initialisation plot.
init_project_name = 'gencmip6'
init_processor = 'Skylake'
subproject_list = ['dcpcmip6', 'pmicmip6', 'devcmip6', 'ls3cmip6', 'volcmip6',
                   'rfmcmip6', 'dekcmip6', 'scecmip6', 'geocmip6', 'checmip6',
                   'rcecmip6', 'anacmip6', 'c4mcmip6', 'cfmcmip6', 'cm5cmip6',
                   'daacmip6', 'dmrcmip6', 'fafcmip6', 'gmmcmip6', 'hircmip6', 'ismcmip6']

df_data_gencmip6, df_opti_gencmip6 = get_dataset_conso(init_project_name,
                                                                   init_processor,
                                                                   subproject_list,
                                                                   instance_data_for_plot(init_project_name))

source_data_gencmip6 = ColumnDataSource(data=df_data_gencmip6)

active_subproject_list_gencmip6, inactive_subproject_list_gencmip6 = sdm.get_subproject_list(source_data_gencmip6)
subproject_list_gencmip6 = active_subproject_list_gencmip6 + inactive_subproject_list_gencmip6


# Define the Widgets
project_select = Select(value=init_project_name, title='Project Name', options=sorted(project_dict.keys()))
processor_select = Select(value=init_processor, title='Processor', options=['Skylake'])
subproject_multiselect = MultiSelect(title="Subprojects:",
                                     value=active_subproject_list_gencmip6,
                                     options=list(zip(
                                         subproject_list_gencmip6,
                                         active_subproject_list_gencmip6
                                         + sdm.modify_inactive_project_names(inactive_subproject_list_gencmip6)
                                     )),
                                     size=8
                                     )

# Define widget actions
project_select.on_change('value',
                         processor_ticker_change,
                         project_ticker_change,
                         update,
                         subproject_multiselect_change
                         )
processor_select.on_change('value', update)
# subproject_multiselect.on_change('value', update)
subproject_multiselect.on_change('value', update_conso)

# Set up layout
controls = widgetbox(project_select, processor_select, subproject_multiselect, width=200)

# Create first plot and layout structure
p = create_figure()
plots = column(p, Spacer(), sizing_mode='scale_both')

layout = layout(row(controls, plots), sizing_mode='scale_both')

# Insert second plot in layout structure.
layout.children[0].children[1].children[1] = create_delta()


curdoc().add_root(layout)
curdoc().title = "Consomation"
