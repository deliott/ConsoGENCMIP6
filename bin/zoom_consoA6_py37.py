import glob
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from libconso_py37 import *

def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-l", "--local", action="store_true",
                        help=" select the config_local.ini file if code ran on local computer ")

    return parser.parse_args()


########################################
if __name__ == '__main__':
    # .. Initialization ..
    # ====================
    # ... Command line arguments ...
    # ------------------------------
    args = get_arguments()

    # ... Files and directories ...
    # -----------------------------

    if args.local:
        config_path = "/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/config_conso_local.ini"
    else:
        config_path = "/ccc/cont003/home/gencmip6/dupontel/deploy_folder/ConsoGENCMIP6_git/ConsoGENCMIP6/bin/config_conso.ini"
#"bin/config_conso.ini"

    project_name, DIR, OUT = parse_config(config_path)

    #files = glob.glob("conso_*.dat")
    files = glob.glob(DIR["SAVEDATA"] + "/conso_*.dat")

    color = ['black', 'red', 'blue', 'green', 'orange', 'cyan', 'grey', 'brown', 'salmon', 'violet', 'yellow']
    xx = {}
    yy = {}
    miplist = []
    for file in files:
        print(file)
        if args.local:
            mip = file[83:91]
        else:
            mip = file[98:106]
        miplist.append(mip)
        xx[mip] = []
        yy[mip] = []
        rfile = open(file, 'r')
        for line in rfile:
            x, y = line.split(' ')
            xx[mip].append(float(x))
            yy[mip].append(float(y) / 1.e6)

    miplist_sorted = [x for y, x in sorted(zip([yy[mip][-1] for mip in miplist], miplist), reverse=True)]
    #plt.xlim(2019. + 4. / 12., 2019 + 6. / 12.)
    plt.xlim(2019. + 4. / 12., 2019 + 5. / 12.)
    plt.xticks([2019 + 4./12  + 2*i/365. for i in range(15)],
               ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29'])

   # plt.xticks([2018 + (9 + i) / 12. for i in range(21)],
   #            ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
   #             'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
    for mip, col in zip(miplist_sorted[0:len(color)], color):
        print(mip, col, yy[mip][-1])
        plt.plot(xx[mip], yy[mip], label=mip, c=col, linewidth=4)

    # plt.plot([2018.+9./12.,2019.+4./12.],[0.,16.1],c='black',linewidth=1) #--16.1 Mh before end of April
    plt.plot([2019. + 4. / 12., 2019. + 4. / 12.], [0., 4.8 + 7.0 + 11.3], c='black',
             linewidth=1)  # --23.1 Mh before end of April
    plt.plot([2019. + 4. / 12., 2020. + 4. / 12.], [0., 27.07], c='black', linewidth=1)  # --27.07 Mh in A6
    plt.xlabel("Mois Mai - Annee 2019 - 2020")
    plt.ylabel("Irene skylake (millions d'heures)")
    #plt.ylim((0, 30))
    plt.ylim((0, 3))
    #plt.yticks([i * 6 for i in range(6)], ['0', '5', '10', '15', '20', '25', '30'])
    plt.yticks([i * 0.6 for i in range(6)], ['0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0'])
    plt.title("Consommation de l'allocation CMIP6")

    leg = plt.legend(bbox_to_anchor=[0.77, 0.01, 1.07, 0.101], loc=3, markerscale=0.3)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(4)
    plt.savefig(DIR["PLOT"] + "/zoom_conso.png")
    plt.savefig(DIR["SAVEPLOT"] + "/zoom_conso.png")
    plt.show()


# import matplotlib.pyplot as plt
# import pandas as pd
# df = pd.read_csv("/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/SORTIES/SAVE/data_conso/pand_conso_totcmip6.dat", sep=";", names=['Date Consummed_Hours TEST'])
# df = pd.read_csv("/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/SORTIES/SAVE/data_conso/pand_conso_totcmip6.dat", sep=";")
#
# df.plot(kind='scatter',x='Date',y='Consummed_Hours',color='red')
# df.plot(x=df[0],y=df[1],color='red')
