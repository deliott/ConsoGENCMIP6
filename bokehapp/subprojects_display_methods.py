"""
This script contains the differents methods used by the bokeh server to display the subprojects.

"""




def get_subproject_list(source, project_name, processor_name):
    print('\n', type(source.to_df().columns))
    print(source.to_df().columns)
    res = []
    liste = list(source.to_df().columns)
    # while liste != []:
    while liste:
        element = liste.pop()
        if element == 'Date' or element == 'Total':
            continue
        else:
            res.append(element)
    print(res, '\n')
    res.sort()
    return res