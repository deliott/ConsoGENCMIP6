"""
This script contains the differents methods used by the bokeh server to display the subprojects.

"""


def get_subproject_list(source):
    """
    Get the subproject lists separated depending on if it is active or not and sorted accordingly.

    :param source:
    :return active_subprojects: list of the active subproject names (str)
    sorted by decreasing associated last time value
    :return inactive_subprojects: list of the inactive subproject names (str) in alphabetical order
    """
    active_subprojects = []
    inactive_subprojects = []

    df = source.to_df()
    liste = list(df.columns)

    while liste:
        element = liste.pop()
        if element == 'Date' : #or element == 'Total':
            continue
        else:
            if df[element].iloc[-1] > 0:
                active_subprojects.append(element)
            else:
                inactive_subprojects.append(element)
    active_subprojects = sort_active_subprojects(active_subprojects, df)
    inactive_subprojects.sort()

    return active_subprojects, inactive_subprojects


def modify_inactive_project_names(liste):
    """
    Append ' (inactive)' to elements of input list
    :param liste: str list of the inactive subproject names
    :return: List of the changed names (str)
    """
    changed_name_list = [name + ' (incative)' for name in liste]
    return changed_name_list


def sort_active_subprojects(liste, df):
    """
    Sort the active project list according to the last consumption value.
    :param liste: active subproject name list (str)
    :param df:
    :return:
    """
    last_conso_value_dict = {}
    for name in liste:
        last_conso_value_dict[name] = df[name].iloc[-1]
    tuple_list = sorted(last_conso_value_dict.items(), key=lambda t: t[1], reverse=True)
    result = [tuple_element[0] for tuple_element in tuple_list]

    return result




def update_plot_conso(attrname, old, new):
    """
    Update the main time series plot depending on the tickers selected.
    Executed when tickers are changed.

    :return: None
    """
    project = project_select.value
    processor = processor_select.value
    column_names_to_remove = source.column_names
    column_names_to_remove.remove('Date')
    column_names_to_remove.remove('Total')
    print('\nColonnes à supprimer : ', column_names_to_remove)

    plot.title.text = "Consomation data for " + project_select.value + ' on ' + processor_select.value + ' nodes.'

    src, src_opti = get_dataset_conso(project, processor)
    source.data.update(src.data)



    # print('\nColonnes à supprimer : ', column_names_to_remove)
    [source.remove(name) for name in column_names_to_remove]
    source_opti.data.update(src_opti.data)





def update_plot_multiselect_subproject(attrname, old, new):
    # selected_subprojects = ['Total'] + subproject_multiselect.value
    selected_subprojects = subproject_multiselect.value
    print('\n MULTISELECT selection - new Value = ', subproject_multiselect.value, '\n')
    print('PLOT : ', plot, '\n')
    # print(plot.__doc__)
    print(plot.renderers)
    # print(plot.renderers.remove(id=1006))
    from inspect import signature
    print("Test to remove line from plot")
    # [print(line) plot.renderers.remove[line] for line in plotted_line_liste]
    [print(line.name) for line in plotted_line_liste]
    print(plotted_line_liste)

    for line in plotted_line_liste:
        line2 = plot.select_one({'name': line.name})
        plot.renderers.remove(line2)
    # [plot.renderers.remove[line.name] for line in plotted_line_liste]
    print(plotted_line_liste)

    print("Test to removed line from plot")












