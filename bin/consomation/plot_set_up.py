
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.palettes import Spectral

import datetime
from math import pi
import pandas as pd

# from bin.consomation.data_for_plot_extractor import ProjectData.days_in_advance


def plot_init(processor, project_name, allocation):
    """
    Initialize the bokeh plot
    :param processor: str name of the processor type whose data will be plotted
    :param project_name: str, name of the project plotted
    :param allocation: float, number of hours allocated in this project to this processor type.
    :return p: bokeh figure
    """
    p = figure(title="Consommation de l'allocation " + project_name.swapcase() + ' - ' + processor + ' (' + str(int(allocation))
                     + ' heures)' + " - Vue par MIPs/sous-projets",
               x_axis_label=None,
               y_axis_label="Irene " + processor + " (heures)",
               x_axis_type="datetime",
               plot_width=900, plot_height=400,
               sizing_mode='scale_width'
               )

    return p

def set_plot_axis_default_range(plot, df_data, df_opti, start_date, vertical_margin_coef):
    """
    Set the axis range of the plot.

    :param plot: bokeh figure
    :param df_data: dataframe with the cpu time consumption per project and total as columns. Indexed by dates.
    :param df_opti:
    :param vertical_margin_coef: float representing the precentage of margin to be taken on vertical axis
    :return:
    """
    fin = pd.to_datetime(df_opti['Date'][-1] + pd.Timedelta(2.5, unit='D'))
    debut = max(fin - pd.Timedelta(60, unit='D'), pd.to_datetime(start_date))

    plot.x_range.start = debut
    plot.x_range.end = fin

    plot.y_range.end = max(
        df_opti['Conso_Optimale'][-1] * 1.25,  # 1.25 stands for the 25% bonus that can be gained at TGCC
        max(df_data['Total'])
    ) * vertical_margin_coef


def add_subprojects_to_line_list(nb_sousprojets, df_data, p, line_list):
    """
    Append Bokeh Line Glyphs corresponding to subprojects data to the list (line_list) to be added to the figure (p).

    :param nb_sousprojets: max number of subprojects to be plotted on the figure.
    :param df_data: dataframe with the cpu time consumption per project and total as columns. Indexed by dates.
    :param p: bokeh figure that will render the glyphs
    :param line_list: list with the bokeh glyphs to be added to the p figure.
    # :return line_list: updated list of bokeh glyphs added to be added to the figure.
    :return: None
    """
    nb_plot = 1

    source = ColumnDataSource(df_data)

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
                        if len(list(df_data.columns)) > 3:
                            line_list.append(p.line('Date', header, source=source,
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
                        line_list.append(p.line('Date', header, source=source,
                                                legend=header + ' ',
                                                name=header + ' ',
                                                # small hack to be able to display the name.
                                                # Otherwise, without the ' ' there is a bug
                                                line_width=3,
                                                color=palette[nb_plot],
                                                muted_color=palette[nb_plot], muted_alpha=0.2
                                                )
                                         )
                        nb_plot = nb_plot + 1

    # return line_list


def add_optimal_consumption_curve(df_opti, p, line_list):
    """
    Append Bokeh Line Glyphs corresponding to the optimal consumption of the allocation to the list (line_list)
    to be added to the figure (p).

    :param df_opti: dataframe with the optimal cpu time consumption as column. Indexed by dates.
    :type df_opti: python dict
    :param p: bokeh figure that will render the glyphs
    :param line_list: list with the bokeh glyphs to be added to the p figure.
    :return: None
    """
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


def add_possible_bonus_curve(df_opti, p, line_list):
    """
    Append Bokeh Line Glyphs corresponding to the optimal consumption multiplied by  of the allocation to the list (line_list)
    to be added to the figure (p).

    :param df_opti: dataframe with the optimal cpu time consumption as column. Indexed by dates.
    :type df_opti: python dict
    :param p: bokeh figure that will render the glyphs
    :param line_list: list with the bokeh glyphs to be added to the p figure.
    :return: None
    """

    df_opti['Conso_Bonus'] = [i * 1.25 for i in df_opti['Conso_Optimale']]
    # because df_opti is a python dict and not a pandas dataframe ... TO CHANGE ...
    # Ajout de la courbe de consomation théorique :
    source_opt = ColumnDataSource(df_opti)
    line_list.append(
        p.line('Date', 'Conso_Bonus', source=source_opt,
               legend='125% Consomation Optimale ',
               name='125% Conso Optimale ',
               line_width=1,
               color='pink',
               muted_color='pink', muted_alpha=0.2
               )
    )



def add_optimal_consumption_patch(delai_avant_penalite, df_opti, p, color):
    """
    Add Bokeh Patch Glyph to the figurte (p) corresponding to the security area
    before risk restriction of the allocation.

    :param delai_avant_penalite: Number of days before Computing Centers decides to take back part of the allocation.
    60 Days at TGCC.
    :param df_opti: dataframe with the optimal cpu time consumption as column. Indexed by dates.
    :param p: bokeh figure that will render the glyphs.
    :param color: string describing the color of the patch.
    :return: None
    """
    # delai_avant_penalite = 14
    # delai_avant_penalite = 60

    if len(df_opti['Date']) <= delai_avant_penalite:
        delai_avant_penalite = min(len(df_opti['Date'])-1, 30)
        color = 'green'

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
    p.patch(xx, yy, alpha=0.1, line_width=2, legend=str(delai_avant_penalite) + ' days security area', color=color)


def add_optimal_total_difference_ticks(df_data, df_opti, p, days_in_advance):
    """
    Add ticks to show difference between optimal curve and total of consumption.

    :param df_data: dataframe with the cpu time consumption per project and total as columns. Indexed by dates.
    :param df_opti: dataframe with the optimal cpu time consumption as column. Indexed by dates.
    :param p: bokeh figure that will render the glyphs.
    :param days_in_advance: Number of days the optimal curv
    :return: None
    """
    last_opti = df_opti['Conso_Optimale'][-(days_in_advance + 1)]
    last_real = df_data['Total'].iloc[-1]
    last_date = df_data['Date'].iloc[-1]
    delta_conso = '{:,.0f}'.format(abs(last_opti - last_real)) + ' heures'

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
                            name=delta_conso
                            )
    p.add_tools(HoverTool(
        tooltips=[
            (statut, '$name'),
            ],
        renderers=[retard_warning],
        mode='hline'
    ))


def add_optimal_total_difference_ticks_bis(df_data, df_opti, p):
    """
    Add ticks to show difference between optimal curve and total of consumption.

    :param df_data: dataframe with the cpu time consumption per project and total as columns. Indexed by dates.
    :param df_opti: dataframe with the optimal cpu time consumption as column. Indexed by dates.
    :param p: bokeh figure that will render the glyphs.
    :param days_in_advance: Number of days the optimal curv
    :return: None
    """

    days_in_start_difference_between_data_and_opti = (df_data['Date'].iloc[0] - df_opti['Date'][0]).days

    retard_warning = []

    for i in range(len(df_data['Date'])):
        opti_value = df_opti['Conso_Optimale'][days_in_start_difference_between_data_and_opti + i]
        total_value = df_data['Total'].iloc[i]

        delta_conso = '{:,.0f}'.format(abs(opti_value - total_value)) + ' heures'

        left = df_data['Date'].iloc[i]
        right = df_data['Date'].iloc[i] + datetime.timedelta(days=0.1)

        if opti_value > total_value:
            statut = 'Retard'
            statut_color = 'firebrick'
            statut_top = opti_value
            statut_bottom = total_value
        else:
            statut = 'Avance'
            statut_color = 'lightgreen'
            statut_top = total_value
            statut_bottom = opti_value

        source = ColumnDataSource(dict(
            left=[left],
            top=[statut_top],
            right=[right],
            bottom=[statut_bottom],
            color=[statut_color],

        ))
        retard_warning.append(p.quad(left="left", right="right", top="top", bottom="bottom",
                                     color=None,
                                     hover_color="color",
                                     source=source,
                                     alpha=0.3,
                                     name=statut + ' de ' + delta_conso
                                     )
                              )
    return retard_warning


def add_warnings_hovertool(p, warning_list):

    p.add_tools(HoverTool(
        renderers=warning_list,
        tooltips=[
            ('', '$name'),
        ],
        mode='mouse'
    ))


def add_curves_hovertool(p, line_list):
    """
    Adds the bokeh hover tool associated to the different consomation data lines to the figure (p).

    :param p:  bokeh figure that will render the glyphs
    :param line_list: list with the bokeh glyphs to be added to the p figure.
    :return: None
    """
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


def plot_config(p):
    """

    :param p:
    :return:
    """
    p.legend.location = "top_left"
    p.legend.click_policy = "mute"

    p.xaxis[0].formatter.days = '%a - %d/%m/%Y'
    p.xaxis.major_label_orientation = pi / 3
    p.yaxis.formatter = NumeralTickFormatter(format="0,")
    p.axis.axis_label_text_font_style = "bold"
