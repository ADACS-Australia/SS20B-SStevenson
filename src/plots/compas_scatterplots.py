# -*- coding: utf-8 -*-

import numpy as np
import h5py
import sys
#import scipy.special

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Select, PreText, Button
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import layout, widgetbox, column, row
from bokeh.io import curdoc


filename = 'COMPAS_CHE_30xZ_3000000.h5'
source = ColumnDataSource(data = dict(x = [], y = []) )



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


#Update dropdown values
def update_dropdown(attrname, old, new):
    
    key_property_x.options = env_dict[group.value]
    key_property_y.options = env_dict[group.value]
    #print('group:', new)
    
    
def update_x(attr, old, new):  

    key_property_x.options = env_dict[group.value]
    key_property_x.value = env_dict[group.value][0]
    #print('x', new)
    
def update_y(attr, old, new):  
    key_property_y.options = env_dict[group.value]
    key_property_y.value = env_dict[group.value][0]
    #print('y', new)
    
#Update Data Source
def update_plot():
    codefeedback.text=f"You are currently exploring {filename} file!"
    p1.xaxis.axis_label = key_property_x.value
    p1.yaxis.axis_label = key_property_y.value

    
    #Here data will populate DataColumn by values from Groups/Keys which are 
    #selected from the drop down menue
    with h5py.File(filename, 'r') as f:
        
        source.data = dict(x = f[group.value][key_property_x.value][0:10000],
                           y = f[group.value][key_property_y.value][0:10000],                           
                           )

    
#Stop server Button
def button_callback():
    sys.exit()  # Stop the server

# Button to stop the server
button = Button(label="Stop", button_type="success")
button.on_click(button_callback)  
    


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
key_property_x = Select(title="Keys X", value=f"{env_dict[group.value][0]}", options=env_dict[group.value])
key_property_y = Select(title="Keys Y", value=f"{env_dict[group.value][0]}", options=env_dict[group.value])


#Changing Groups will change available Keys in dropdown menu
group.on_change("value", update_x)

#Updates on x and y. When group is updated, without these lines the Keys
#are not getting update and the system breaks/complains that can not 
#create plot. Its messy setup, but it works at the moment.
key_property_x.on_change("value", update_y)

key_property_y.on_change("value", update_dropdown)

#Text on the top
codefeedback = PreText(text="",width=900)

#Defining Figure Tools
defaults = 'pan,box_zoom,box_select,reset,wheel_zoom, undo,redo,save'
TOOLS = [defaults]#,hover_userdefined]

p1 = figure(tools=TOOLS, lod_interval = 1000)
scatter1 = p1.circle(x='x', y='y' ,source=source, size=7, color='#252525')

#Widget callbacks
plot_axes = [key_property_x,key_property_y]
for ax in plot_axes:
    ax.on_change('value', lambda attr, old, new: update_plot())

#Sort layout
axes = column(*plot_axes, sizing_mode='fixed')

#Defining the layout for the GUI
#Layout on the page
layout = layout([codefeedback],
                #[group, key_property_x, key_property_y],
                [group, axes, p1],
                #[p1],
                button,
                )
#to plot the initial variables immediately
update_plot()


curdoc().add_root(layout)

#Run from command line: bokeh serve --show restructured_compas.py