
from bin.consomation.data_for_plot_extractor import ProjectData






# processor = 'Skylake'
# project_name = 'gencmip6'
# data_for_plot = ProjectData('gencmip6')
# df_data, df_opti = data_for_plot.run_data_for_plot_extractor('Skylake', '2019-05-01')
# #

processor = 'KNL'
# processor = 'Skylake'
project_name = 'gen0826'
data_for_plot = ProjectData(project_name)
df_data, df_opti = data_for_plot.run_data_for_plot_extractor(processor, '2018-10-31')

#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
import datetime
from math import pi


from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure, output_file, save
from bokeh.palettes import Spectral

import bin.consomation.settings as settings
import bin.consomation.set_paths as set_paths

import bin.consomation.plot_set_up as plot_set_up

set_paths.set_path_to_plots()


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

output_file(settings.path_to_plots + "/" + project_name + "_mips_timeseries.html", title= project_name + " mips timeseries")

save(p)

print('Bokeh plot saved on : ', settings.path_to_plots + "/" + project_name + "_mips_timeseries.html")
