import pandas as pd
import json
import os
import datetime
from math import pi


from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, save
from bokeh.palettes import Spectral
from bokeh.models import HoverTool
from bokeh.models import NumeralTickFormatter

import bin.consomation.settings as settings
import bin.consomation.set_paths as set_paths

from bin.consomation.data_for_plot_extractor import ProjectData

"""
This script is run by a bash script executed by a cron on ciclad. 
So far it extract the data from the json timeseries of project GENCMIP6 on Irene.

It has to be refactored to take into account other projects.
So far there are no test associated with this scirpt.  

"""

# Initialise Global Variables
# settings.init()
# set_paths.set_path_to_timeseries()

# Get path to data
set_paths.set_path_to_plots()

p0826 = ProjectData('gen0826')
p0826.set_project_timeseries_filename()

# Load data
p0826.load_project_data()
jl = p0826.json_data

# Extract dates from data
p0826.set_dates()

# # Extract Processor List
p0826.set_processor_list()
# processor_list = pcmip6.processor_list

# Extract Subprojects (MIPs) Names
p0826.set_processor_subproject_list('Skylake')
mips = p0826.subproject_list

#############################
# Create a pandas_dataframe with all the subprojects (MIPs) as columns
p0826.set_subproject_subtotal_dataframe('Skylake')


# Sort the columns according to their biggest last value
p0826.sort_df_colomns_according_to_biggest_last_value()
df = p0826.subproject_subtotal_dataframe

# Set the Date column as the index of the dataframe
p0826.add_dates_to_dataframe()

#############################
# Extract the total of subproject value and add column to dataframe

dfTot = df.sum(axis=1, numeric_only=True)
df.insert(loc=1, value=dfTot, column='Total')


#############################
# Extract Theoretical Optimal Consumption Curve
# @TODO : refactor in a different module than data_for_plot_extractor.py ?
days_in_advance = 3

p0826.set_allocated_dict()
p0826.set_deadline()
start_date = '2018-10-31'
allocated = p0826.allocated_dict['Skylake']

p0826.set_last_date(days_in_advance)
last_date = p0826.last_date

p0826.set_start_date_to_dict('Skylake', '2018-10-31')
p0826.set_optimal_daily_consumption('Skylake')

dfOpti = p0826.get_theoretical_optimal_consumption_curve_dataframe('Skylake')


#############################
# Configuration du Plot :

source = ColumnDataSource(df)
p = figure(title="Consommation de l'allocation CMIP6 - Vue par MIPs",
           x_axis_label="Date",
           y_axis_label="Irene skylake (heures)",
           x_axis_type="datetime",
           plot_width=1800, plot_height=800,
           sizing_mode='scale_width'
           )

line_list = []

# Ajout des lignes des sous projets au plot :
# Nb de sous projets à ploter :
nb_sousprojets = 10
nb_plot = 1

palette = list(reversed(Spectral[nb_sousprojets]))

for header in list(df.columns):
    # print(header)
    if not header == 'Date':
        # Conditions pour afficher le sous projet :
            # sa dernière valeure n'est pas nulle
            # On pourrait rajouter d'autres conditions, telles que :
                # - si la valeur a varié depuis longtemps.
        if not df[header].iloc[-1] == 0:
            if nb_plot < nb_sousprojets:
                if header == 'Total':
                    line_list.append(p.line('Date', header, source=source,
                           legend=header + ' ', # small hack to be able to display the name. Otherwise, without the ' ' there is a bug
                           name=header + ' ', # small hack to be able to display the name. Otherwise, without the ' ' there is a bug
                           line_width=3,
                           color="black",
                           muted_color="black", muted_alpha=0.2
                           )
                                     )
                else:
                    line_list.append(p.line('Date', header, source=source,
                           legend=header + ' ',
                           name=header + ' ',
                           # small hack to be able to display the name. Otherwise, without the ' ' there is a bug
                           line_width=3,
                           color=palette[nb_plot],
                           muted_color=palette[nb_plot], muted_alpha=0.2
                           )
                                     )
                    nb_plot = nb_plot + 1





# Ajout de la courbe de consomation théorique :
source_opt = ColumnDataSource(dfOpti)
line_list.append(
    p.line('Date', 'Conso_Optimale', source=source_opt,
                           legend='Conso_Optimale ',
                            name='Conso_Optimale ',
                           # small hack to be able to display the name. Otherwise, without the ' ' there is a bug
                           line_width=1,
                           color='black',
                           muted_color='black', muted_alpha=0.2
                           )
)

# Ajout de la courbe de consomation théorique :
delai_avant_penalite = 60
volume_avant_penalite = dfOpti['Conso_Optimale'][delai_avant_penalite]

xx = [dfOpti['Date'][0],
      dfOpti['Date'][-1],
      dfOpti['Date'][-1],
      dfOpti['Date'][delai_avant_penalite],
      dfOpti['Date'][0]]

yy = [dfOpti['Conso_Optimale'][0],
      dfOpti['Conso_Optimale'][-1],
      dfOpti['Conso_Optimale'][-1] - volume_avant_penalite,
      0,
      0]
p.patch(xx, yy, alpha=0.2, line_width=2)

# Ajout de la difference Optimale/Réelle:

print(df['Total'].iloc[-1])

last_opti = dfOpti['Conso_Optimale'][-(days_in_advance+1)]
last_real = df['Total'].iloc[-1]
last_date = df['Date'].iloc[-1]
deltaConso = '{:,.0f}'.format(abs(last_opti - last_real)) + ' heures'


if last_opti > last_real:
    statut = 'Retard'
    statut_color = 'red'
    statut_top = last_opti
    statut_bottom = last_real
else:
    statut = 'Avance'
    statut_color = 'green'
    statut_top = last_real
    statut_bottom = last_opti


source = ColumnDataSource(dict(
        left=[last_date],
        top=[statut_top],
        right=[last_date + datetime.timedelta(days=0.01)],
        bottom=[statut_bottom],
        color=[statut_color],
    )
)
retard_warning = p.quad(left="left", right="right", top="top", bottom="bottom",
              color=None,
              hover_color="color",
              source=source,
              alpha=0.3,
              name=deltaConso
                        )
p.add_tools(HoverTool(
    tooltips=[
                (statut, '$name'),
                # ('Courbe', '$name'),
                # ('Hours', '$y{0,2f}'),  # use @{ } for field names with spaces
            ],
    renderers=[retard_warning],
    mode='hline'))

# Ajout du HoverTool
p.add_tools(HoverTool(
    renderers=line_list,
    tooltips=[
        ('Date', '$x{%F}'),
        ('Courbe', '$name'),
        ('Hours', '$y{0,2f}'),  # use @{ } for field names with spaces
        ],
    formatters={
        '$x': 'datetime',  # use 'datetime' formatter for 'date' field
        },
    mode='mouse'
                    )
            )

# Ajout de quelsues paramètres pour le graph

p.legend.location = "top_left"
p.legend.click_policy = "mute"

p.xaxis[0].formatter.days = '%a - %d/%m/%Y'
p.xaxis.major_label_orientation = pi / 3
p.yaxis.formatter = NumeralTickFormatter(format="0,")



output_file(settings.path_to_plots + "/" + p0826.project_name +  "_mips_timeseries.html", title="gencmip6 mips timeseries")

save(p)

print('Bokeh plot saved on : ', settings.path_to_plots +"/" + p0826.project_name +  "_mips_timeseries.html")