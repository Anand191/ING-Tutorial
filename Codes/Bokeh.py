
#%%
from bokeh.events import Tap
from bokeh.plotting import figure,curdoc
import numpy as np


#%%
N = 5
test = np.zeros((N,3))
test[:,0] = np.arange(N)

test[:,1] = np.random.rand(N)
test[:,2] = np.zeros(N)

x = test[:,0]
y = test[:,1]

p = figure(plot_width=400, plot_height=400)
p.circle(x,y,size=20)


#%%

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]



def onclick_event(event):
    print('Python:Click')
    print int(event.x)
    print (event.y)
    
    x_map = find_nearest(test[:,0],event.x)
    y_map = find_nearest(test[:,1], event.y)
    
    row = np.where(test[:,0]==x_map)[0]
    test[row,2] = 1
        
    print test
    
p.on_event(Tap,onclick_event)


curdoc().add_root(p)

