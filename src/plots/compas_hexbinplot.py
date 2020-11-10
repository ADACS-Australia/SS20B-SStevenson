import numpy as np
import h5py
import sys

from bokeh.plotting import figure
from bokeh.models.widgets import Select, PreText, Button, RangeSlider, RadioGroup
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, LogTicker
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.transform import log_cmap
from bokeh.util.hex import hexbin
from bokeh.models import Range1d, LinearAxis
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.models import Title

filename = 'COMPAS_CHE_30xZ_3000000.h5'
# filename = 'testing.h5'
# filename = 'COMPASOutput.h5'
# filename = 'COMPAS_CHE_30xZ_3000000_5percent.h5' #5% of the full COMPASS file
# filename = 'COMPAS_CHE_30xZ_3000000_10percent.h5'
# filename = './Datasets/0Fiducial/COMPASOutput_0Fiducial.h5'

import configparser

config = configparser.ConfigParser()
# COMPASS_TOP_DIR = config.get('', 'topdir')

# def update_file():
#    filename = COMPASS_TOP_DIR
#    return filename

# filename = update_file()


def get_groups(filename):

    with h5py.File(filename, 'r') as f:
        # Get groups
        all_groups = list(f.keys())

    return all_groups


def get_keys_from_groups(filename):
    with h5py.File(filename, 'r') as f:

        # Get keys (columns in datasets) from the main groups
        sub_keys = []
        for j, key in enumerate(get_groups(filename)):
            individual_keys = list(f[key].keys())
            sub_keys.append(individual_keys)

        return sub_keys


def create_dictionary(all_groups, sub_keys):

    dictionary = {group: [key for key in sub_keys[i]] for i, group in enumerate(all_groups)}

    return dictionary


def update_dropdown(attr, old, new):

    key_property_x.options = env_dict[group.value]
    key_property_y.options = env_dict[group.value]

    return old, new


def update_x(attr, old, new):

    key_property_x.options = env_dict[group.value]
    key_property_x.value = env_dict[group.value][0]

    return old, new


def update_y(attr, old, new):
    key_property_y.options = env_dict[group.value]
    key_property_y.value = env_dict[group.value][0]

    return old, new


# Groups in a list
group_list = get_groups(filename)

# Environment Dictionary: {Group1: [keys, ...], Group1: [Keys, ...]}
env_dict = create_dictionary(get_groups(filename), get_keys_from_groups(filename))


# Dropdown menues for Groups and Properties (Keys); It will start initialised
# with the first group 'CommonEnvelopes' and the first Key withing that group
# Select a group
group = Select(title="Groups", value=f"{group_list[0]}", options=group_list)

# Get key for a selected group (properties)
key_property_x = Select(title="X-axis", value=f"{env_dict[group.value][0]}", options=env_dict[group.value])
key_property_y = Select(title="Y-axis", value=f"{env_dict[group.value][0]}", options=env_dict[group.value])


# Changing Groups will change available Keys in dropdown menu
group.on_change("value", update_x)

# Need to update x and y when a group updates; goes into circular updates.
key_property_x.on_change("value", update_y)
key_property_y.on_change("value", update_dropdown)

# Text on the top
def file_text_name(filename):

    codefeedback = PreText(text=f"{filename} file is loaded", width=500, style={'color': 'black'})

    return codefeedback


codefeedback = file_text_name(filename)

# Defining Figure Tools
defaults = 'pan,box_zoom,box_select,reset,wheel_zoom, undo,redo,save'
TOOLS = [defaults]  # ,hover_userdefined]

p1 = figure(tools=TOOLS, lod_interval=1000, toolbar_location="above")
p1.add_layout(Title(text="Normalized", align="center", text_font_style='normal'), "left")
p1.add_layout(Title(text="Normalized", align="center", text_font_style='normal'), "below")

source_bin = ColumnDataSource(data=dict(r=[], q=[], counts=[]))

hex_size = 0.005

bar_color = '#969696'

try:
    with h5py.File(filename, 'r') as f:

        _Core_Mass_1 = f['CommonEnvelopes']['Core_Mass_1'][:] * 1

        Core_Mass_1 = RangeSlider(
            title='Core_Mass_1',
            bar_color=bar_color,
            start=min(_Core_Mass_1),
            end=max(_Core_Mass_1),
            value=(min(_Core_Mass_1), max(_Core_Mass_1)),
            step=1,
        )

        _Core_Mass_2 = f['CommonEnvelopes']['Core_Mass_2'][:] * 1

        Core_Mass_2 = RangeSlider(
            title='Core_Mass_2',
            bar_color=bar_color,
            start=min(_Core_Mass_2),
            end=max(_Core_Mass_2),
            value=(min(_Core_Mass_2), max(_Core_Mass_2)),
            step=1,
        )

        _Stellar_Type_1 = f['DoubleCompactObjects']['Stellar_Type_1'][:] * 1
        _Stellar_Type_2 = f['DoubleCompactObjects']['Stellar_Type_2'][:] * 1

        select_type = Select(title="Filter by type:", value="", options=["", "NSNS", "NSBH", "BHNS", "BHBH"])
except KeyError:

    Core_Mass_1 = RangeSlider(title='', bar_color=bar_color, start=0, end=1, value=(0, 1), step=1)

    Core_Mass_2 = RangeSlider(title='', bar_color=bar_color, start=0, end=1, value=(0, 1), step=1)

    _Stellar_Type_1 = 0
    _Stellar_Type_2 = 0

    select_type = Select(title="No filters available", value="", options=["", "", "", "", ""])

# Filtering data
def filter_data(data):

    BH = 14
    NS = 13
    if group.value == 'CommonEnvelopes':

        filter_core = np.logical_and(
            np.logical_and(
                np.logical_and(_Core_Mass_1 >= Core_Mass_1.value[0], _Core_Mass_1 <= Core_Mass_1.value[1]),
                _Core_Mass_2 >= Core_Mass_2.value[0],
            ),
            _Core_Mass_2 <= Core_Mass_2.value[1],
        )

        filtered_data = data[filter_core]

    elif group.value == 'DoubleCompactObjects':

        if select_type.value == 'BHBH':

            filter_BHBH = np.logical_and(_Stellar_Type_1 == BH, _Stellar_Type_2 == BH)
            filtered_data = data[filter_BHBH]

        elif select_type.value == 'NSNS':

            filter_NSNS = np.logical_and(_Stellar_Type_1 == NS, _Stellar_Type_2 == NS)
            filtered_data = data[filter_NSNS]

        elif select_type.value == 'NSBH':

            filter_NSBH = np.logical_and(_Stellar_Type_1 == NS, _Stellar_Type_2 == BH)
            filtered_data = data[filter_NSBH]

        elif select_type.value == 'BHNS':

            filter_BHNS = np.logical_and(_Stellar_Type_1 == BH, _Stellar_Type_2 == NS)
            filtered_data = data[filter_BHNS]

        else:
            filtered_data = data

    elif group.value == 'Supernovae':
        filtered_data = data
    elif group.value == 'SystemParameters':
        filtered_data = data

    else:
        filtered_data = data

    return filtered_data


# Visibility options -- each group has its own RangeSliders
def range_slider_visibility(new):
    active_radio_button = range_group.active

    if active_radio_button == 0:
        Core_Mass_1.visible = True
        Core_Mass_2.visible = True
        select_type.visible = False

    elif active_radio_button == 1:
        Core_Mass_1.visible = False
        Core_Mass_2.visible = False
        select_type.visible = True

    elif active_radio_button == 2:
        Core_Mass_1.visible = False
        Core_Mass_2.visible = False
        select_type.visible = False
    else:
        active_radio_button == 3
        Core_Mass_1.visible = False
        Core_Mass_2.visible = False
        select_type.visible = False


range_group = RadioGroup(
    labels=["CommonEnvelopes", "DoubleCompactObjects", "Supernovae", "SystemParameters"], active=0
)

range_group.on_click(range_slider_visibility)
range_slider_visibility(None)


def change_nan_inf(data):

    data_array = np.nan_to_num(
        data * 1,
        nan=np.nanmean(data[np.isfinite(data)], axis=0),
        posinf=np.nanmean(data[np.isfinite(data)], axis=0),
        neginf=np.nanmean(data[np.isfinite(data)], axis=0),
    )

    return data_array


def reformat_data(data):

    # Normalized data, use MinMax scaling: transform data into the range [0,1]
    # To avoid division with 0, check that Max value is not 0
    if data.max(axis=0) != 0:
        # Next, check if Max value is equal to Min value
        if data.max(axis=0) == data.min(axis=0):
            # If Min and Max are equal, data contains array of const. values
            # so return (data - data.min) -- this will be always 0 and it
            # will scale with extra_y_ranges and extra_x_ranges
            data_normed = data - data.min(axis=0)
        # In other cases, return MinMax scaling
        else:
            data_normed = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
    # If Max value is 0, we need to avoid division with 0
    elif data.max(axis=0) == 0:
        # Normalize MinMax using value close to 0, since we have much larger
        # hexbin size, this doesn't introduce visible deviations
        data_normed = (data - data.min(axis=0)) / (0.0001 - data.min(axis=0))

    return data_normed


# Extra x/y axis, needed to show the real values beside the normalized ones

with h5py.File(filename, 'r') as f:

    x = change_nan_inf(f[group.value][key_property_x.value][:] * 1)

    y = change_nan_inf(f[group.value][key_property_y.value][:] * 1)

    # Older version of compas .h5 files doesn't have all data in one array
    x = np.ravel(x)
    y = np.ravel(y)

    # Start the extra axes
    p1.extra_y_ranges = {"yraw": Range1d(start=min(y), end=max(y))}
    p1.add_layout(LinearAxis(y_range_name="yraw", axis_label=key_property_y.value), 'right')

    p1.extra_x_ranges = {"xraw": Range1d(start=min(x), end=max(x))}
    p1.add_layout(LinearAxis(x_range_name="xraw", axis_label=key_property_x.value), 'above')


def data_bin_change(attr, old, new):

    p1.xaxis.axis_label = key_property_x.value
    p1.yaxis.axis_label = key_property_y.value

    with h5py.File(filename, 'r') as f:

        # Change_nan_inf: convert NaN, inf, -inf values to mean of the property
        # Placed *1 to convert True/False into 1/0
        x_raw = change_nan_inf(f[group.value][key_property_x.value][:] * 1)

        y_raw = change_nan_inf(f[group.value][key_property_y.value][:] * 1)

        # Obtain filtered data from the RangeSlider
        x = filter_data(x_raw)
        y = filter_data(y_raw)

        # Older version of compas .h5 files doesn't have all data in one array
        x = np.ravel(x)
        y = np.ravel(y)

        # Adding extra axes, to replace our normalized ones. If min/max
        # are equal e.g. we have const. data in array, e.g. Eccentricity>CE is 0
        # we need to add end = 1, otherwise the respective axis will not have ticks.
        if min(y) == max(y):
            p1.extra_y_ranges['yraw'].update(start=min(y), end=min(y) + 1)
            p1.extra_x_ranges['xraw'].update(start=min(x), end=max(x))

        elif min(x) == max(x):
            p1.extra_x_ranges['xraw'].update(start=min(x), end=min(y) + 1)
            p1.extra_y_ranges['yraw'].update(start=min(y), end=max(y))

        else:
            p1.extra_y_ranges['yraw'].update(start=min(y), end=max(y))
            p1.extra_x_ranges['xraw'].update(start=min(x), end=max(x))

        x_normed = reformat_data(x)
        y_normed = reformat_data(y)

        bins = hexbin(x_normed, y_normed, hex_size)

        source_bin.data = dict(q=bins.q, r=bins.r, counts=bins.counts)


key_property_x.on_change("value", data_bin_change)
key_property_y.on_change("value", data_bin_change)

Core_Mass_1.on_change("value_throttled", data_bin_change)
Core_Mass_2.on_change("value_throttled", data_bin_change)

select_type.on_change('value', data_bin_change)


# Populate the initial data and pass it down for colormap/colorbar change
col_max = data_bin_change(None, None, group.value)

cmap = log_cmap('counts', 'Cividis256', 1, col_max)

h = p1.hex_tile(q="q", r="r", size=hex_size, line_color=None, source=source_bin, fill_color=cmap)

hover = HoverTool(tooltips=[('Counts', '@counts')], mode='mouse', point_policy='follow_mouse', renderers=[h],)

color_bar = ColorBar(
    title="Counts", color_mapper=cmap['transform'], location=(0, 0), ticker=LogTicker(), label_standoff=12,
)

p1.add_layout(color_bar, 'right')
color_bar.formatter = PrintfTickFormatter(format="%.0e")

p1.add_tools(hover)

plot_axes = [key_property_x, key_property_y]

# Sort layout
axes = column(*plot_axes, sizing_mode='fixed')

# Stop server Button
def button_callback():
    sys.exit()


# Types: default-white, primary-blue, success-green, warning-orange, danger-red
button = Button(label="Stop", button_type="success")
button.on_click(button_callback)

# Figure needs to redraw previous self after Bokeh Reset option - to get axes
def redraw_plot(attr):
    col_max = data_bin_change(None, None, group.value)


r = Button(label="Redraw Figure After Reset")
r.on_click(redraw_plot)


table_source = ColumnDataSource(data=dict(x=[], y=[]))


def update_stats(attr, old, new):

    with h5py.File(filename, 'r') as f:

        x_r = f[group.value][key_property_x.value][:]
        y_r = f[group.value][key_property_y.value][:]

        x_stat = filter_data(x_r)
        y_stat = filter_data(y_r)

        x_inf = len(np.argwhere(np.isinf(x_stat)))
        y_inf = len(np.argwhere(np.isinf(y_stat)))

        x_neginf = len(np.argwhere(np.isneginf(x_stat)))
        y_neginf = len(np.argwhere(np.isneginf(y_stat)))

        x_nan = len(np.argwhere(np.isnan(x_stat)))
        y_nan = len(np.argwhere(np.isnan(y_stat)))

        stat_x = f"inf: {x_inf}"
        stat_x_neg = f"-inf: {x_neginf}"
        stat_x_nan = f"nan: {x_nan}"

        stat_y = f"inf: {y_inf}"
        stat_y_neg = f"-inf: {y_neginf}"
        stat_y_nan = f"nan: {y_nan}"

        table_source.data = dict(inf_x=[stat_x, stat_x_neg, stat_x_nan], inf_y=[stat_y, stat_y_neg, stat_y_nan])


key_x = PreText(text='0')
key_y = PreText(text='0')
key_property_x.on_change("value", update_stats)
key_property_y.on_change("value", update_stats)
update_stats(None, None, key_property_x.value)
update_stats(None, None, key_property_y.value)

# Update Table statistics with filtering
Core_Mass_1.on_change("value_throttled", update_stats)
Core_Mass_2.on_change("value_throttled", update_stats)
select_type.on_change('value', update_stats)

# Show counts of the inf/nan values
columns = [
    TableColumn(field='inf_x', title='X-axis'),
    TableColumn(field='inf_y', title='Y-axis'),
]
data_table = DataTable(source=table_source, columns=columns, width=400, height=150)


# Define some text on canvas
table_title = PreText(text="Table with nan/inf values", style={'color': 'black'})

select_group_to_filter = PreText(text="Select a Group to apply filters to:", style={'color': 'black'})

filters_available = PreText(text="Available filters:", style={'color': 'black'})

# Layout on the page

drop_down = column(
    group,
    table_title,
    data_table,
    select_group_to_filter,
    range_group,
    filters_available,
    Core_Mass_1,
    Core_Mass_2,
    select_type,
    button,
    r,
)
stat_dd = row(axes)
fig_file = column(codefeedback, p1)
layout_data = row(fig_file, drop_down, stat_dd)

# Make space between plot and tools/other items
p1.min_border_right = 30
# Start on 0, extra_y/x_range will be aligned
p1.x_range.start = 0
p1.y_range.start = 0
p1.x_range.end = 1
p1.y_range.end = 1

# Start server
curdoc().add_root(layout_data)

# Start server: url based file
# url_args = curdoc().session_context.request.arguments
# update_file()

# Run from command line: bokeh serve --show compas_hexbinplot.py
