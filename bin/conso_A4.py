import glob
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

files=glob.glob("conso_*.dat")
color=['black','red','blue','green','orange','cyan','grey','brown','salmon','violet','yellow']
xx={}
yy={}
miplist=[]
for file in files: 
  print file
  mip=file[6:14]
  miplist.append(mip)
  xx[mip]=[]
  yy[mip]=[]
  rfile=open(file,'r') 
  for line in rfile: 
     x,y=line.split(' ')
     xx[mip].append(float(x))
     yy[mip].append(float(y)/1.e6)

miplist_sorted=[x for y,x in sorted(zip([yy[mip][-1] for mip in miplist],miplist),reverse=True)]
plt.xlim(2018.+9./12.,2019+6./12.)
plt.xticks([2018+(9+i)/12. for i in range(9)],['Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun'])
for mip,col in zip(miplist_sorted[0:len(color)],color):
   print mip,col,yy[mip][-1]
   plt.plot(xx[mip],yy[mip],label=mip,c=col,linewidth=4)

#plt.plot([2018.+9./12.,2019.+4./12.],[0.,16.1],c='black',linewidth=1) #--16.1 Mh before end of April
plt.plot([2018.+9./12.,2019.+4./12.],[0.,4.8+7.0+11.3],c='black',linewidth=1) #--23.1 Mh before end of April
plt.xlabel("Annee 2018 - 2019")
plt.ylabel("Irene skylake (millions d'heures)")
plt.ylim((0,25))
plt.yticks([i*5 for i in range (6)], ['0','5','10','15','20', '25'])
plt.title("Consommation de l'allocation CMIP6")

leg=plt.legend(bbox_to_anchor=[0.77,0.01,1.07,0.101],loc=3,markerscale=0.3)
for legobj in leg.legendHandles:
    legobj.set_linewidth(4)
plt.savefig('conso.png')
plt.show()
