# Plot Temperature in real-time from two TSYS01 sensors on i2c bus
# TSYS01 a is on address 0x76, TSYS01 b is on 0x77



# sudo apt-get install python-gi-cairo



# Brian Glazer, 27 Nov 2018, based on code from

# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# 2017

import time,sys,traceback,logging
from os.path import expanduser
sys.path.append(expanduser('~'))
import matplotlib.pyplot as plt
from matplotlib import animation
from datetime import datetime
from tsys01.drivers.tsys01_0x76 import TSYS01_0x76
from tsys01.drivers.tsys01_0x77 import TSYS01_0x77

logging.basicConfig(level=logging.WARNING)

#fast
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
#xdata_0x76 = []
tempdata_0x77 = []
tempdata_0x76 = []
plt.ylabel('Temperature_0x77, Deg.C',color='r',fontsize=16)
for t in ax1.get_yticklabels():
    t.set_color('r')

ax2 = ax1.twinx()
line2, = ax2.plot([],[],'orangered.-',lw=4,markersize=10)
ax2.set_xlim(0,length)
ax2.set_ylim(10,35)
ax2.set_ylabel('Temperature_0x76, Deg.C',color='orangered',fontsize=16)
for t in ax2.get_yticklabels():
    t.set_color('orangered')

plt.xlabel('Index')
plt.title('Dual TSYS01 Demo')

def update_line(num,line1,line2):
    s_0x77 = TSYS01_0x77(bus=1)
    s_0x76 = TSYS01_0x76(bus=1)
    #print(s._read_prom())
    temp_0x77 = (s_0x77.read())
    temp_0x76 = (s_0x76.read())

    print('{} Deg.C'.format(temp_0x77))
    print('{} Deg.C'.format(temp_0x76))

    tempdata_0x77.append(temp_0x77)
    tempdata_0x76.append(temp_0x76)
    
    while len(tempdata_0x77) > length:
        tempdata_0x77.pop(0)

    while len(tempdata_0x76) > length:
        tempdata_0x76.pop(0)

    xdata = range(0,len(tempdata_0x77))
    

    #ax1.figure.canvas.draw()
    line1.set_xdata(xdata)
    line1.set_ydata(tempdata_0x77)

    line2.set_xdata(xdata)
    line2.set_ydata(tempdata_0x76)
    return line1,line2

    
line_ani = animation.FuncAnimation(fig,update_line,fargs=(line1,line2),
                                   interval=interval,blit=False)

plt.show()
