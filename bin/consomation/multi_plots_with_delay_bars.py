"""
This scripts plots the projects time series
and the bar plot showing daily consumption relatively to optimal consumption.

It uses settings, set_paths, plot_set_up and daily_delta_monitoring .py


"""
from bin.consomation.data_for_plot_extractor import ProjectData
###############################################################
from bokeh.plotting import figure, output_file, save

import bin.consomation.settings as settings
import bin.consomation.set_paths as set_paths

import bin.consomation.plot_set_up as plot_set_up

from bokeh.layouts import gridplot

from bin.consomation.daily_delta_monitoring import plot_init_delta, plot_config_delta, test_add_optimal_total_difference_ticks_bis,\
    test_add_optimal_total_difference_ticks_ter, add_difference_hovertool

set_paths.set_path_to_plots()
###############################################################


# Define the project dictionary :
project_dict = {}
project_dict['gencmip6'] = '2019-05-01'
project_dict['gen0826'] = '2018-10-31'

for project_name in list(project_dict.keys()):
    start_date = project_dict[project_name]
    print('\nPlotting ' + project_name + '. It started on ' + start_date + '.')



    data_for_plot = ProjectData(project_name)

    data_for_plot.set_project_timeseries_filename()
    data_for_plot.load_project_data()
    data_for_plot.set_dates()
    # load_project_data() and set_dates()
    data_for_plot.set_processor_list()
    processor_list = data_for_plot.processor_list

    print('Processor list : ', processor_list)

    # Creation of the each processor type's figure.

    figure_ligne1 = []
    figure_ligne2 = []

    for processor in processor_list:
        df_data, df_opti = data_for_plot.run_data_for_plot_extractor(processor, start_date)

        #############################
        # Configuration du Plot :
        p = plot_set_up.plot_init(processor, project_name)

        # Ajout des glyphs à la liste
        nb_sousprojets = 10
        line_list = []

        # line_list = plot_set_up.add_subprojects_to_line_list(nb_sousprojets, df_data, p, line_list)
        plot_set_up.add_subprojects_to_line_list(nb_sousprojets, df_data, p, line_list)

        plot_set_up.add_optimal_consumption_curve(df_opti, p, line_list)

        # Ajout de la surface de sécurité de consomation théorique :

        delai_avant_penalite=60
        plot_set_up.add_optimal_consumption_patch(delai_avant_penalite, df_opti, p, 'orange')

        # print('Last Total : ', df_data['Total'].iloc[-1])

        # Ajout des ticks de difference entre Conso Optimale et Totale
        # # Ancienne version
        # # days_in_advance = ProjectData.days_in_advance
        # #plot_set_up.add_optimal_total_difference_ticks(df_data, df_opti, p, days_in_advance)

        # # Nouvelle version
        retard_warning = plot_set_up.add_optimal_total_difference_ticks_bis(df_data, df_opti, p)
        plot_set_up.add_warnings_hovertool(p, retard_warning)

        # Ajout du HoverTool pour les courbes de données

        plot_set_up.add_curves_hovertool(p, line_list)

        plot_set_up.plot_config(p)

        figure_ligne1.append(p)


        q = plot_init_delta(processor, project_name)
        # q = plot_set_up.plot_init(processor, project_name)
        print('DF_OPTI : ', df_opti)
        print('DF_DATA : ', df_data)

        retard_warning = test_add_optimal_total_difference_ticks_ter(data_for_plot, df_data, df_opti, q)
        # retard_warning = test_add_optimal_total_difference_ticks_bis(data_for_plot, df_data, df_opti, q)

        add_difference_hovertool(q, retard_warning)

        plot_config_delta(q)
        figure_ligne2.append(q)


    # output_file(settings.path_to_plots + "/" + project_name + "_mips_timeseries.html", title= project_name + " mips timeseries")
    output_file(settings.path_to_plots + "/" + project_name + "_DELTA_PLOT.html", title= project_name + " DELTA_PLOT")



    if len(figure_ligne1) == 1:
        # save(gridplot([figure_liste], plot_width=1800, plot_height=800, sizing_mode='scale_width'))
        save(gridplot([figure_ligne1, figure_ligne2], plot_width=900, plot_height=400, sizing_mode='scale_width'))
    else:
        save(gridplot([figure_ligne1, figure_ligne2], plot_width=500, plot_height=350, sizing_mode='scale_width'))


    # print('Bokeh plot saved on : ', settings.path_to_plots + "/" + project_name + "_mips_timeseries.html")
    print('Bokeh plot saved on : ', settings.path_to_plots + "/" + project_name + "_DELTA_PLOT.html")
