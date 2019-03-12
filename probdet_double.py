from ctypes import *

from scipy.stats import gamma

import numpy as np

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, Select, Range1d, TextInput, Spacer, HoverTool
from bokeh.plotting import Figure, curdoc

pd=cdll.LoadLibrary("./libprobdet_double.dylib")
pd.probdet.argtypes=[c_double, c_double, c_double, c_double]
pd.probdet.restype=c_double

pfa=TextInput(title='False Alarm Probability', value='1e-6')
slider1 = Slider(start=1, end=10, value=1, step=1, title="Number of Pulses")
slider2 = Slider(start=.5, end=10, value=1, step=0.5, title="Target Gamma K parameter")
case=Select(title="Swerling Case", value="Case 2", options=["Case 1", "Case 2", "Case 3", "Case 4", "Non-fluctuating"])
space=Spacer(height=30, width=400)

PFA=float(pfa.value)
N=slider1.value
Yb=gamma.ppf(1-PFA,N)
K=1*N;

xdBseries=np.array([x*0.1 for x in range(0, 501)])
xdBseries=xdBseries-10

vprobdet=np.vectorize(pd.probdet)

PDseries=vprobdet(N,Yb,K,xdBseries)

source=ColumnDataSource(data=dict(snr=xdBseries, pd=PDseries))

plot = Figure(plot_width=435, plot_height=400)

plot.line('snr','pd',source=source)

hover=HoverTool(tooltips=[("SNR","@snr"),("Pd","@pd")],mode='vline')
plot.add_tools(hover)

plot.x_range=Range1d(-10 , 40)

def update(attrname, old, new):

    PFA=float(pfa.value)
    N=slider1.value
    Yb=gamma.ppf(1-PFA,N)
    if case.value=="Case 1":
        K=1
    elif case.value=="Case 2":
        K=N
    elif case.value=="Case 3":
        K=2
    elif case.value=="Case 4":
        K=2*N
    else:
        K=1000
    newPDseries=vprobdet(N,Yb,K,xdBseries)
    newdata=dict(snr=xdBseries, pd=newPDseries)
    source.data = newdata

controls=[slider1, case, pfa]

for control in controls:
    control.on_change('value', update)

layout = column(pfa, case, slider1, space, plot)

curdoc().add_root(layout)
