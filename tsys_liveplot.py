import time,sys,traceback,logging
from os.path import expanduser
sys.path.append(expanduser('~'))
import matplotlib.pyplot as plt
from matplotlib import animation
from datetime import datetime
from node.drivers.tsys01 import TSYS01

logging.basicConfig(level=logging.WARNING)
#short
interval = 500     #ms
length = 2*60

#long
#interval = 30000     #ms
#length = 16*60


fig,ax1 = plt.subplots()
line1, = ax1.plot([],[],'r.-',lw=4,markersize=10)
ax1.set_xlim(0,length)
ax1.set_ylim(10,35)
ax1.grid()
xdata = []
tempdata = []
plt.ylabel('Temperature, Deg.C',color='r',fontsize=16)
for t in ax1.get_yticklabels():
    t.set_color('r')

plt.xlabel('Index')
plt.title('TSYS01 Demo')

def update_line(num,line1):
    s = TSYS01(bus=1)
    #print(s._read_prom())
    temp = (s.read())

    print('{} Deg.C'.format(temp))

    tempdata.append(temp)
    
    while len(tempdata) > length:
        tempdata.pop(0)

    xdata = range(0,len(tempdata))

    #ax1.figure.canvas.draw()
    line1.set_xdata(xdata)
    line1.set_ydata(tempdata)

    return line1,

    
line_ani = animation.FuncAnimation(fig,update_line,fargs=(line1,),
                                   interval=interval,blit=False)

plt.show()
