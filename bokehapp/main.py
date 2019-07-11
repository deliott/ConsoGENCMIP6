from os.path import join, dirname
import datetime

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, MultiSelect

from data_for_plot_extractor import ProjectData

import plot_set_up as plot_set_up

import subprojects_display_methods as sdm

import set_paths as set_paths
set_paths.set_path_to_plots()

project_dict = {}
project_dict['gencmip6'] = '2019-05-01'
project_dict['gen0826'] = '2018-10-31'


def get_dataset_conso(project_name, processor, subproject_list):
    """
    Check the usages of this function.
    -> in the definition of the initialisation of the plot.
    -> in create_figure
    """
    data_for_plot = ProjectData(project_name)

    data_for_plot.set_project_timeseries_filename()
    data_for_plot.load_project_data()
    data_for_plot.set_dates()
    data_for_plot.set_processor_list()

    df_data, df_opti = data_for_plot.run_data_for_plot_extractor_selected_list(
        processor,
        project_dict[str(project_name)],
        subproject_list
    )
    df_data = df_data.set_index(['Date'])
    df_data.sort_index(inplace=True)

    return ColumnDataSource(data=df_data), ColumnDataSource(data=df_opti)


def create_figure():
    plot = plot_set_up.plot_init(processor_select.value, project_select.value, 27070000)
    plot.title.text = "Consomation data for " + project_select.value + ' on ' + processor_select.value + ' nodes.'

    selected_subproject_list = subproject_multiselect.value
    source_data, source_opti = get_dataset_conso(project_select.value, processor_select.value, selected_subproject_list)

    line_list = []

    add_data_lines(plot, source_data, line_list, selected_subproject_list)
    add_opti_curve(plot, source_opti, line_list)

    # Set up plot display details (legend, axis types, etc)
    plot_set_up.plot_config(plot)

    return plot


def add_data_lines(plot, source_data, line_list, selected_subproject_list):
    nb_plot = 1
    nb_sousprojets = len(selected_subproject_list)
    df_data = source_data.to_df()
    from bokeh.palettes import Spectral
    palette = list(reversed(Spectral[min(nb_sousprojets + 2, 11)]))
    for header in selected_subproject_list:
        if not header == 'Date':
            # Conditions pour afficher le sous projet :
            # sa dernière valeure n'est pas nulle
            # On pourrait rajouter d'autres conditions, telles que :
            # - si la valeur a varié depuis longtemps.
            # if not df_data[header].iloc[-1] == 0:
            if nb_plot <= nb_sousprojets:
                if header == 'Total':
                    if len(list(df_data.columns)) > 3:
                        line_list.append(plot.line('Date', header, source=source_data,  # issue with this source
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
                    line_list.append(plot.line('Date', header, source=source_data, # issue with the source
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


def update(attr, old, new):
    layout.children[1] = create_figure()


# Define variables for initialisation plot.
project_name = 'gencmip6'
processor = 'Skylake'
subproject_list = ['dcpcmip6', 'pmicmip6', 'devcmip6', 'ls3cmip6', 'volcmip6',
                   'rfmcmip6', 'dekcmip6', 'scecmip6', 'geocmip6', 'checmip6',
                   'rcecmip6', 'anacmip6', 'c4mcmip6', 'cfmcmip6', 'cm5cmip6',
                   'daacmip6', 'dmrcmip6', 'fafcmip6', 'gmmcmip6', 'hircmip6', 'ismcmip6']

source_data_gencmip6, source_opti_gencmip6 = get_dataset_conso(project_name, processor, subproject_list)
active_subproject_list_gencmip6, inactive_subproject_list_gencmip6 = sdm.get_subproject_list(source_data_gencmip6)
subproject_list_gencmip6 = active_subproject_list_gencmip6 + inactive_subproject_list_gencmip6


# Define the Widgets
project_select = Select(value=project_name, title='Project Name', options=sorted(project_dict.keys()))
processor_select = Select(value=processor, title='Processor', options=['Skylake'])
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
subproject_multiselect.on_change('value', update)

# Set up layout
controls = column(project_select, processor_select, subproject_multiselect)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Consomation"
