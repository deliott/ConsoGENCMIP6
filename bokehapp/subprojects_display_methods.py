"""
This script contains the differents methods used by the bokeh server to display the subprojects.

"""




def get_subproject_list(source):
    """

    :param source:
    :return res: list of the subproject names (str) in alphabetical order
    """
    active_subprojects = []
    inactive_subprojects = []

    df = source.to_df()
    liste = list(df.columns)

    # print('\n\n\n', df, '\n\n\n')

    while liste:
        element = liste.pop()
        if element == 'Date' or element == 'Total':
            continue
        else:
            if df[element].iloc[-1] > 0:
                # print('\n ', element, df[element].iloc[-1] )
                active_subprojects.append(element)
            else:
                inactive_subprojects.append(element)
    # print('XXXXXXXXXXXXXZZZZZZEDZDSDCSDFVS',  active_subprojects, '\n')
    # active_subprojects.sort()
    active_subprojects = sort_active_subprojects(active_subprojects, df)
    inactive_subprojects.sort()

    # ll = active_subprojects
    # print('Active project : ' , ll)
    # ll.append(res0)
    # print('All project : ' ,ll + inactive_subprojects, '\n')

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
    # print(last_conso_value_dict)

    tuple_list = sorted(last_conso_value_dict.items(), key=lambda t: t[1], reverse=True)
    result = [tuple_element[0] for tuple_element in tuple_list]
    # print('Sorted Dict : ', result)


    return result
