import pandas as pd
import json
import os
import datetime


from bokeh.models import ColumnDataSource


from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Set3
from bokeh.models import HoverTool
from math import pi
from bokeh.models import NumeralTickFormatter
# output_notebook()


# Get path to data
path_to_timeseries = '/home/edupont/ccc_myproject_data/timeseries/gencmip6/'

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

allocated = jl['2019-05-13']['processor_type']['Skylake']["allocated"]
deadline = jl['2019-05-13']['project_deadline']
start_date = '2019-05-01'
last_date = max(dates) + datetime.timedelta(days=int(3))

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
           )

line_list = []

# Ajout des lignes des sous projets au plot :
#Nb de sous projets à ploter :
nb_sousprojets = 10
nb_plot = 1

palette = Set3[nb_sousprojets]

for header in list(df.columns):
    print(header)
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
                           line_width=3,
                           color="black",
                           muted_color="black", muted_alpha=0.2
                           )
                                     )
                else:
                    line_list.append(p.line('Date', header, source=source,
                           legend=header + ' ',
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
                           # small hack to be able to display the name. Otherwise, without the ' ' there is a bug
                           line_width=1,
                           color='black',
                           muted_color='black', muted_alpha=0.2
                           )
)

p.add_tools(HoverTool(
            renderers=line_list,
            tooltips=[
                ('Date', '$x{%F}'),
                ('Hours', '$y{0.2f}'),  # use @{ } for field names with spaces
                #         ( 'volume', '@volume{0.00 a}'      ),
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

print(p)
show(p)








# import pandas as pd
# import json
# import os
# from bokeh.plotting import figure, output_file, show
# from bokeh.palettes import Set3
# from bokeh.models import HoverTool
# from math import pi
# from bokeh.models import NumeralTickFormatter
#
#
# if __name__ == '__main__':
#
#     path_to_timeseries = '/home/edupont/ccc_myproject_data/timeseries/gencmip6/'
#
#     file_list = os.listdir(path_to_timeseries)
#     timeseries_file_name = ''
#     for file in file_list:
#         last_piece = file.split('.')[0].split('_')[-1]
#         if last_piece.isdigit() and 'timeseries' in file:
#             timeseries_file_name = file
#
#
#
#     df = pd.read_json(path_to_timeseries + timeseries_file_name)
#
#
#
#
# ###########################
#
#
#
#     with open(path_to_timeseries + timeseries_file_name) as file:
#
#         jl = json.load(file)
#
#
#
#     dates = list(jl.keys())
#     mips = list(jl[dates[0]]['processor_type']['Skylake']['sous_projet'].keys())
#     # print('\n\n', jl[dates[0]]['processor_type']['Skylake']['sous_projet']['volcmip6']['subtotal'], '\n\n')
#     data = {}
#     data['Date'] = list(jl.keys())
#     for mip in mips:
#         data[mip] = []
#         for date in data['Date']:
#             donnee = jl[date]['processor_type']['Skylake']['sous_projet'][mip]['subtotal']
#             #         donnee = 0#jl[dates]['processor_type']['Skylake']['sous_projet'][mip]['subtotal']
#
#             data[mip].append(donnee)
#
#     # print(mips)
#     # print(test['rcecmip6'])
#
#     data['Date'] = pd.to_datetime(list(jl.keys()))
#     df = pd.DataFrame(data)
#     df.set_index('Date', inplace=True)
#     df = df[df.iloc[-1, :].sort_values(ascending=False).index]
#     # print(df)
#
#     print(df)
#
#     df.reset_index(inplace=True)
#     print(df['Date'])
#     # df
#
#     # TOOLTIPS = [
#     #     # ("index", "$index"),
#     #     ("date", "$x"),
#     #     ("Heures Consommées", "$y{0,} heures")
#     #     ]
#
#
#
#
#
#     # hover_tool.formatters = {"Date": "datetime"}
#     p = figure(title="Consommation de l'allocation CMIP6 - Vue par MIPs",
#                plot_width=1800, plot_height=800,
#                x_axis_type="datetime",
#                x_axis_label="Date",
#                y_axis_label="Irene skylake (millions d'heures)"
#                # , tooltips=TOOLTIPS)
#                # , tools='hover')
#                )
#
#     p.xaxis[0].formatter.days = '%a - %d/%m/%Y'
#     p.xaxis.major_label_orientation = pi / 3
#     p.yaxis.formatter = NumeralTickFormatter(format="0,")
#
#     # hover = p.select(dict(type=HoverTool))
#     # hover.tooltips = [("Heures Consommées", "$y{0,} heures"),
#     #                   ("Date", "@Date{%Y}"),
#     #                   # ("Value", "@y{0.00%}")
#     #                   ]
#
#     # hover.mode = 'mouse'
#     # mypalette = Set3[12]
#
#     # print('DATA === ', df)
#
#
#     i = 0
#     name_list = list(df.columns.values)[1:12]
#     for name, color in zip(name_list, Set3[12]) :
#         ##     p.line(data['Date'], data['pmicmip6'], legend='pmicmip6')
#         ##     if 'Date' not in name:
#         # p.line(data['Date'], df[name],
#         #        legend=name, color=mypalette[i],
#         #        line_width=3)
#         # print(type(name))
#         legend_content = name
#         cr = p.line( x=df['Date'], y=df[name],
#                legend=legend_content,
#                color=color,
#                 muted_color=color, muted_alpha=0.2,
#                line_width=3)
#         # p.line(source=df, x='Date', y=name,
#         #        legend=legend_content,
#         #        color=color, muted_color= color,
#         #        line_width=3)
#         i = i + 1
#
#         p.add_tools(HoverTool(
#             renderers=[cr],
#             tooltips=[
#                 ('Date', '$x{%F}'),
#                 ('Hours', '$y{0.2f}'),  # use @{ } for field names with spaces
#                 #         ( 'volume', '@volume{0.00 a}'      ),
#             ],
#
#             formatters={
#                 '$x': 'datetime',  # use 'datetime' formatter for 'date' field
#             },
#
#             mode='mouse'
#         ))
#
#
#     p.legend.location = "top_left"
#     p.legend.click_policy = "mute"
#
#     output_file("plot_GENCMIP6_MIPs.html", title="test for interractive plot of CMIP6 MIPs")
#
#
#     show(p)