import pandas as pd
import json
import os
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Set3
from bokeh.models import HoverTool


if __name__ == '__main__':

    path_to_timeseries = '/home/edupont/ccc_myproject_data/timeseries/gencmip6/'

    file_list = os.listdir(path_to_timeseries)
    timeseries_file_name = ''
    for file in file_list:
        last_piece = file.split('.')[0].split('_')[-1]
        if last_piece.isdigit() and 'timeseries' in file:
            timeseries_file_name = file



    df = pd.read_json(path_to_timeseries + timeseries_file_name)




###########################



    with open(path_to_timeseries + timeseries_file_name) as file:

        jl = json.load(file)



    dates = list(jl.keys())
    mips = list(jl[dates[0]]['processor_type']['Skylake']['sous_projet'].keys())
    # print('\n\n', jl[dates[0]]['processor_type']['Skylake']['sous_projet']['volcmip6']['subtotal'], '\n\n')
    data = {}
    data['Date'] = list(jl.keys())
    for mip in mips:
        data[mip] = []
        for date in data['Date']:
            donnee = jl[date]['processor_type']['Skylake']['sous_projet'][mip]['subtotal']
            #         donnee = 0#jl[dates]['processor_type']['Skylake']['sous_projet'][mip]['subtotal']

            data[mip].append(donnee)

    # print(mips)
    # print(test['rcecmip6'])

    data['Date'] = pd.to_datetime(list(jl.keys()))
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    df = df[df.iloc[-1, :].sort_values(ascending=False).index]
    # print(df)

    print(df)

    df.reset_index(inplace=True)
    print(df['Date'])
    # df

    # TOOLTIPS = [
    #     # ("index", "$index"),
    #     ("date", "$x"),
    #     ("Heures Consommées", "$y{0,} heures")
    #     ]





    # hover_tool.formatters = {"Date": "datetime"}
    p = figure(title="Consommation de l'allocation CMIP6 - Vue par MIPs",
               plot_width=1800, plot_height=800,
               x_axis_type="datetime",
               x_axis_label="Date",
               y_axis_label="Irene skylake (millions d'heures)"
               # , tooltips=TOOLTIPS)
               , tools='hover')


    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("Heures Consommées", "$y{0,} heures"),
                      ("Date", "@Date{%Y}"),
                      # ("Value", "@y{0.00%}")
                      ]

    hover.mode = 'mouse'
    # mypalette = Set3[12]

    # print('DATA === ', df)


    i = 0
    name_list = list(df.columns.values)[1:12]
    for name, color in zip(name_list, Set3[12]) :
        ##     p.line(data['Date'], data['pmicmip6'], legend='pmicmip6')
        ##     if 'Date' not in name:
        # p.line(data['Date'], df[name],
        #        legend=name, color=mypalette[i],
        #        line_width=3)
        # print(type(name))
        legend_content = name
        p.line( x=df['Date'], y=df[name],
               legend=legend_content,
               color=color,
                muted_color=color, muted_alpha=0.2,
               line_width=3)
        # p.line(source=df, x='Date', y=name,
        #        legend=legend_content,
        #        color=color, muted_color= color,
        #        line_width=3)
        i = i + 1


    p.legend.location = "top_left"
    p.legend.click_policy = "mute"

    output_file("plot_GENCMIP6_MIPs.html", title="test for interractive plot of CMIP6 MIPs")


    show(p)