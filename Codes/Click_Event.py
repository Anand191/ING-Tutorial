#%%
from matplotlib import pyplot as plt
import numpy as np

#%%
fig = plt.figure()
ax = fig.add_subplot(111)
N = 5
test = np.zeros((N,3))
test[:,0] = np.arange(N)

test[:,1] = np.random.rand(N)
test[:,2] = np.zeros(N)

ax.plot(test[:,0],test[:,1])

#%%
def onclick(event):
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))
    if (np.any(test[:,0]==int(event.xdata))):
        row = np.where(test[:,0]==int(event.xdata))[0]
        test[row,2] = 1
        
    print test

cid = fig.canvas.mpl_connect('button_press_event', onclick)
