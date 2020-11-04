# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import numpy as np
import h5py
import sys
from numpy import inf

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Select, PreText, Button, Slider, TextInput
from bokeh.models import (ColumnDataSource, HoverTool, ColorBar, LogTicker)
from bokeh.layouts import layout, widgetbox, column, row
from bokeh.io import curdoc
from bokeh.transform import log_cmap
from bokeh.util.hex import hexbin
from bokeh.models import Range1d, LinearAxis
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models.formatters import PrintfTickFormatter


filename = 'COMPAS_CHE_30xZ_3000000.h5'



def get_groups(filename):
    
    with h5py.File(filename, 'r') as f:
        #Get groups
        all_groups = list(f.keys())
            
    return all_groups
   
    
def get_keys_from_groups(filename):
    with h5py.File(filename, 'r') as f:

        #get keys (columns in datasets) from the main groups (there are 4)
        sub_keys = []      
        for j, key in enumerate(get_groups(filename)):
            individual_keys = list(f[key].keys())
            sub_keys.append(individual_keys)
            
        return sub_keys
    
def create_dictionary(all_groups, sub_keys):

    dictionary = {group: [key for key in sub_keys[i]] 
                  for i, group in enumerate(all_groups)}
    
    return dictionary


def update_dropdown(attr, old, new):
    
    key_property_x.options = env_dict[group.value]
    key_property_y.options = env_dict[group.value]

    return old, new
    
def update_x(attr, old, new):  

    key_property_x.options = env_dict[group.value]
    key_property_x.value = env_dict[group.value][13]
    #print('x', new)
    return old, new
    
def update_y(attr, old, new):  
    key_property_y.options = env_dict[group.value]
    key_property_y.value = env_dict[group.value][13]
    #print('y', new)
    return old, new
    
    

# Groups in a list
group_list = get_groups(filename)

# Environment Dictionary: {Group1: [keys, ...], Group1: [Keys, ...]}
env_dict = create_dictionary(get_groups(filename),
                             get_keys_from_groups(filename))


#Dropdown menues for Groups and Properties (Keys); It will start initialised
#with the first group 'CommonEnvelopes' and the first Key withing that group
#Select a group
group = Select(title="Groups", value=f"{group_list[0]}", options=group_list)

# Get key for a selected group (properties)
key_property_x = Select(title="X-axis", value=f"{env_dict[group.value][13]}", options=env_dict[group.value])
key_property_y = Select(title="Y-axis", value=f"{env_dict[group.value][13]}", options=env_dict[group.value])


#Changing Groups will change available Keys in dropdown menu
group.on_change("value", update_x)

#Updates on x and y. When group is updated, without these lines the Keys
#are not getting update and the system breaks/complains that can not 
#create plot. It looks messy setup, but it works.
key_property_x.on_change("value", update_y)
key_property_y.on_change("value", update_dropdown)



def update_plot():
    
    
    with h5py.File(filename, 'r') as f:
        data = dict(
                x = f[group.value][key_property_x.value][:],
                y = f[group.value][key_property_y.value][:],
                ) 
        
    return data

data = update_plot()

#Text on the top
codefeedback = PreText(text=f"{filename} file is loaded",width=500,
                       style={'color': 'black'})

#Defining Figure Tools
defaults = 'pan,box_zoom,box_select,reset,wheel_zoom, undo,redo,save'
TOOLS = [defaults]#,hover_userdefined]

p1 = figure(tools=TOOLS, lod_interval = 1000, toolbar_location="above")

source_bin = ColumnDataSource(data=dict(r=[], q=[], counts=[]))

hex_size = 0.01


def data_bin_change(attr, old, new):
    
        
    p1.xaxis.axis_label = key_property_x.value
    p1.yaxis.axis_label = key_property_y.value
    
    
    with h5py.File(filename, 'r') as f:
        
        #Placed *1 to convert True/False into 1/0
        #Placed np.nan_to_num to convert NaN, inf, -inf values to 0

        x = np.nan_to_num(f[group.value][key_property_x.value][:]*1,
                          nan=0, posinf=0, neginf=0)
        
        y = np.nan_to_num(f[group.value][key_property_y.value][:]*1,
                          nan=0, posinf=0, neginf=0)

    
        #Normalized data to max
        # If data is all 0, then just parse the data
        if (x.max(axis=0) != 0):
            x_normed = x / x.max(axis=0)
        else:
            x_normed = x

        if (y.max(axis=0) != 0):
            y_normed = y / y.max(axis=0)            
        else:
            y_normed = y

        
        bins = hexbin(x_normed, y_normed, hex_size)
        

        source_bin.data = dict(q=bins.q, r=bins.r, counts=bins.counts)
              

key_property_x.on_change("value", data_bin_change)
key_property_y.on_change("value", data_bin_change)

# Populate the initial data.
data_bin_change(None, None, key_property_x.value)
data_bin_change(None, None, key_property_y.value)

#`cmap` should be updating with `data_bin_change`.
cmap = log_cmap('counts', 'Cividis256', 1, max(source_bin.data['counts']))
        
h = p1.hex_tile(q="q", r="r", size=hex_size, line_color=None,
               source=source_bin, fill_color=cmap)
               

hover = HoverTool(
    tooltips=[('Counts', '@counts')],
    mode='mouse',
    point_policy='follow_mouse',
    renderers=[h],
)

color_bar = ColorBar(
                color_mapper=cmap['transform'],
                location=(0, 0),
                ticker=LogTicker(),
                label_standoff=12,
                )
color_bar.formatter = PrintfTickFormatter(format="%.0e")



p1.add_tools(hover)
p1.add_layout(color_bar, 'right')


#Widget callbacks
plot_axes = [key_property_x,key_property_y]
for ax in plot_axes:
    ax.on_change('value', lambda attr, old, new: update_plot())

#Sort layout
axes = column(*plot_axes, sizing_mode='fixed')


#Stop server Button
def button_callback():
    sys.exit()  # Stop the server

# Button to stop the server
button = Button(label="Stop", button_type="success")
button.on_click(button_callback) 
 
table_source = ColumnDataSource(data = dict(x = [], y = []) )

def update_stats(attr, old, new):
    with h5py.File(filename, 'r') as f:
        
        x_inf =  len(
            np.argwhere(np.isinf(f[group.value][key_property_x.value][:])) 
                    )
        y_inf =  len(
            np.argwhere(np.isinf(f[group.value][key_property_y.value][:]))
                    )
        
        x_neginf =  len(
            np.argwhere(np.isneginf(f[group.value][key_property_x.value][:]))
                    )
        y_neginf =  len(
            np.argwhere(np.isneginf(f[group.value][key_property_y.value][:]))
                    )
        
        x_nan =  len(
            np.argwhere(np.isnan(f[group.value][key_property_x.value][:])) 
                    )
        y_nan =  len(
            np.argwhere(np.isnan(f[group.value][key_property_y.value][:]))
                    )

        stat_x = f"inf: {x_inf}"
        stat_x_neg = f"-inf: {x_neginf}"
        stat_x_nan = f"nan: {x_nan}"

        
        stat_y =f"inf: {y_inf}"
        stat_y_neg = f"-inf: {y_neginf}"
        stat_y_nan = f"nan: {y_nan}"
        
        
        table_source.data = dict(inf_x = [stat_x, stat_x_neg, stat_x_nan],
                  inf_y = [stat_y, stat_y_neg, stat_y_nan])
        


key_x = PreText(text='0')
key_y = PreText(text='0')
key_property_x.on_change("value", update_stats)
key_property_y.on_change("value", update_stats)
update_stats(None, None, key_property_x.value)
update_stats(None, None, key_property_y.value)

columns = [
            TableColumn(field='inf_x', title='X-axis'),
            TableColumn(field='inf_y', title='Y-axis'),
            ]
data_table = DataTable(source=table_source, columns=columns, 
                       width=400, height=150)

drop_down = column(group, data_table, button)
stat_dd = row(axes)
fig_file = column(codefeedback, p1)
layout_data = row(fig_file, drop_down, stat_dd)


#make space between plot and tools/other items
p1.min_border_right = 30


curdoc().add_root(layout_data)

#Run from command line: bokeh serve --show restructured_compas.py
