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
    # xxx = len(liste)

    print('\n\n\n', df, '\n\n\n')

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
    print('XXXXXXXXXXXXXZZZZZZEDZDSDCSDFVS',  active_subprojects, '\n')
    active_subprojects.sort()
    inactive_subprojects.sort()
    # print('Nombre de Mips : ', xxx - 2)
    # print('Nombre de Mips actifs: ', len(res))
    # print('Nombre de Mips non encore actifs: ', len(res0))

    ll = active_subprojects
    print('Active project : ' , ll)
    # ll.append(res0)
    print('All project : ' ,ll + inactive_subprojects, '\n')

    return active_subprojects, inactive_subprojects

def modify_inactive_project_names(liste):
    """
    Append ' (inactive)' to elements of input list
    :param liste: str list of the inactive subproject names
    :return: List of the changed names (str)
    """
    changed_name_list = [name + ' (incative)' for name in liste]
    return changed_name_list


