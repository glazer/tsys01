# Plot Temperature in real-time from two TSYS01 sensors on i2c bus
# TSYS01 a is on address 0x76, TSYS01 b is on 0x77

#aticus.py doesn't need separate driver files for different addresses, but treats address
#like a variable in calling TSYS01

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
from node.drivers.tsys01 import TSYS01
logging.basicConfig(level=logging.WARNING)

#fast
interval = 500     #ms
length = 2*60

#long
#interval = 30000     #ms
#length = 16*60

fig,ax1 = plt.subplots()
line1, = ax1.plot([],[],'C0^-',lw=4,markersize=10)
ax1.set_xlim(0,length)
ax1.set_ylim(20,25)
ax1.grid()
xdata = []
tempdata_0x77 = []
tempdata_0x76 = []
plt.ylabel('Temperature_0x77, Deg.C',color='C0',fontsize=16)
for t in ax1.get_yticklabels():
    t.set_color('C0')

ax2 = ax1.twinx()
line2, = ax2.plot([],[],'C1v-',lw=4,markersize=10)
ax2.set_xlim(0,length)
ax2.set_ylim(20,25)
ax2.set_ylabel('Temperature_0x76, Deg.C',color='C1',fontsize=16)
for t in ax2.get_yticklabels():
    t.set_color('C1')

plt.xlabel('Index')
plt.title('Dual TSYS01 Demo')

def update_line(num,line1,line2):
    s_0x77 = TSYS01(address=0x77)
    s_0x76 = TSYS01(address=0x76)
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
    
    line1.set_xdata(xdata)
    line1.set_ydata(tempdata_0x77)

    line2.set_xdata(xdata)
    line2.set_ydata(tempdata_0x76)
    return line1,line2
    
line_ani = animation.FuncAnimation(fig,update_line,fargs=(line1,line2),
                                   interval=interval,blit=False)

plt.show()
