
from bin.consomation.data_for_plot_extractor import ProjectData






# processor = 'Skylake'
# project_name = 'gencmip6'
# data_for_plot = ProjectData('gencmip6')
# df_data, df_opti = data_for_plot.run_data_for_plot_extractor('Skylake', '2019-05-01')

#
# processor = 'KNL'
processor = 'Skylake'
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


set_paths.set_path_to_plots()


#############################
# Configuration du Plot :

source = ColumnDataSource(df_data)
p = figure(title="Consommation de l'allocation " + project_name.swapcase() + " - Vue par MIPs/sous-projets",
           x_axis_label="Date",
           y_axis_label="Irene " + processor + " (heures)",
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

for header in list(df_data.columns):
    # print(header)
    if not header == 'Date':
        # Conditions pour afficher le sous projet :
            # sa dernière valeure n'est pas nulle
            # On pourrait rajouter d'autres conditions, telles que :
                # - si la valeur a varié depuis longtemps.
        if not df_data[header].iloc[-1] == 0:
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
source_opt = ColumnDataSource(df_opti)
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
# delai_avant_penalite = 14
delai_avant_penalite = 60
volume_avant_penalite = df_opti['Conso_Optimale'][delai_avant_penalite]

xx = [df_opti['Date'][0],
      df_opti['Date'][-1],
      df_opti['Date'][-1],
      df_opti['Date'][delai_avant_penalite],
      df_opti['Date'][0]]

yy = [df_opti['Conso_Optimale'][0],
      df_opti['Conso_Optimale'][-1],
      df_opti['Conso_Optimale'][-1] - volume_avant_penalite,
      0,
      0]
p.patch(xx, yy, alpha=0.2, line_width=2)

# Ajout de la difference Optimale/Réelle:

print(df_data['Total'].iloc[-1])

last_opti = df_opti['Conso_Optimale'][-(ProjectData.days_in_advance + 1)]
last_real = df_data['Total'].iloc[-1]
last_date = df_data['Date'].iloc[-1]
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



output_file(settings.path_to_plots + "/" + project_name + "_mips_timeseries.html", title= project_name + " mips timeseries")

save(p)

print('Bokeh plot saved on : ', settings.path_to_plots + "/" + project_name + "_mips_timeseries.html")
