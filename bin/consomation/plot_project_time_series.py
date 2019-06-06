import pandas as pd
import json
import os
import datetime


from bokeh.models import ColumnDataSource


from bokeh.plotting import figure, output_file, save, show
from bokeh.palettes import Spectral
from bokeh.models import HoverTool
from math import pi
from bokeh.models import NumeralTickFormatter
# output_notebook()

import bin.consomation.settings as settings
import bin.consomation.set_paths as set_paths

# Initialise Global Variables
settings.init()
set_paths.set_path_to_timeseries()
set_paths.set_path_to_plots()


# Get path to data
path_to_timeseries = settings.path_to_timeseries + 'gencmip6/'


file_list = os.listdir(path_to_timeseries)
timeseries_file_name = ''
for file in file_list:
    last_piece = file.split('.')[0].split('_')[-1]
    if last_piece.isdigit() and 'timeseries' in file:
        timeseries_file_name = file


# Load data
with open(path_to_timeseries + timeseries_file_name) as file:

    jl = json.load(file)

    # print(json.dumps(jl, indent=4))

# Extract dates from data
dates = list(jl.keys())
dates.sort()
# print(dates)

# Extract Subprojects (MIPs) Names

mips = list(jl[dates[0]]['processor_type']['Skylake']['sous_projet'].keys())
# print(mips)

#############################
# Create a pandas_dataframe with al the subprojects (MIPs) as columns
mips_data_dict = {}
for mip in mips:
    mips_data_dict[mip] = []
    for date in dates: # dates is a sorted list.
        hour_consumed_on_this_day = jl[date]['processor_type']['Skylake']['sous_projet'][mip]['subtotal']
        mips_data_dict[mip].append(hour_consumed_on_this_day)

# print('MIPs Data Dict : ', mips_data_dict)
df = pd.DataFrame(mips_data_dict)


# Set the Date column as the index of the dataframe


# Sort the columns according to their biggest last value
df = df[df.iloc[-1, :].sort_values(ascending=False).index]

dates = pd.to_datetime(dates)

df.insert(0, "Date", dates, True)

#############################
# Extract the total of subproject value and add column to dataframe

dfTot = df.sum(axis=1, numeric_only=True)
df.insert(loc=1, value=dfTot, column='Total')


#############################
# Extract Theoretical Optimal Consumption Curve
days_in_advance = 3


allocated = jl['2019-05-13']['processor_type']['Skylake']["allocated"]
deadline = jl['2019-05-13']['project_deadline']
start_date = '2019-05-01'
last_date = max(dates) + datetime.timedelta(days=int(days_in_advance))

date_list = pd.date_range(start=pd.to_datetime(start_date),
                          end=pd.to_datetime(last_date),
                          freq='D')

delta = pd.to_datetime(deadline) - pd.to_datetime(start_date)

deltaH = allocated / delta.days
print('Nombres d\'heures à consommer par jour : ' , deltaH )
liste_consomation_optimale = []
for indice in range(len(date_list)):
    liste_consomation_optimale.append(indice*deltaH)

dfOpti = {'Date': date_list, 'Conso_Optimale': liste_consomation_optimale}



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
#Nb de sous projets à ploter :
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
delai_avant_penalite = 14
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
        ))

# Ajout de quelsues paramètres pour le graph

p.legend.location = "top_left"
p.legend.click_policy = "mute"

p.xaxis[0].formatter.days = '%a - %d/%m/%Y'
p.xaxis.major_label_orientation = pi / 3
p.yaxis.formatter = NumeralTickFormatter(format="0,")



output_file(settings.path_to_plots + "/gencmip6_mips_timeseries.html", title="gencmip6 mips timeseries")

show(p)

print('Bokeh plot saved on : ', settings.path_to_plots + "/gencmip6_mips_timeseries.html")