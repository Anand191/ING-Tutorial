#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 10:55:28 2017

@author: anand
"""
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown
from bokeh.plotting import curdoc

menu = [("Quaterly", "a"), ("Half Yearly", "b"),("Yearly", "c")]
dropdown = Dropdown(label="Time Period", button_type="warning", menu=menu)

def function_to_call(attr, old, new):
    print dropdown.value

dropdown.on_change('value', function_to_call)

curdoc().add_root(widgetbox(dropdown))
#show(dropdown)