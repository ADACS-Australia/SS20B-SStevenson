import numpy as np
import h5py
import sys

from bokeh.plotting import figure
from bokeh.models.widgets import Select, PreText, Button, RangeSlider, RadioGroup, Tabs, Panel
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, LogTicker
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.transform import log_cmap
from bokeh.util.hex import hexbin
from bokeh.models import Range1d, LinearAxis, Paragraph
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.models import Title
from bokeh.palettes import Viridis256, Cividis256, Magma256, Inferno256, Plasma256

from os.path import basename


def get_groups(filename):
    """
    Read in a file and get its keys - which will be groups.

    Parameters
    ----------
    filename : Compas .h5 file.

    Returns
    -------
    all_groups : list of keys - groups.
    """

    with h5py.File(filename, "r") as f:
        # Get groups
        all_groups = list(f.keys())

    return all_groups


def get_keys_from_groups(filename):
    """
    Read in a file and get keys from each group within a file. These keys are properties within the file.

    Parameters
    ----------
    filename : Compas .h5 file.

    Returns
    -------
    sub_keys : Properties which are present in the file.

    """
    with h5py.File(filename, "r") as f:

        # Get keys (columns in datasets) from the main groups
        sub_keys = []
        for j, key in enumerate(get_groups(filename)):
            individual_keys = list(f[key].keys())
            sub_keys.append(individual_keys)

        return sub_keys


def create_dictionary(all_groups, sub_keys):
    """
    Create nested dictionary - each group within a file and its properties.

    Parameters
    ----------
    all_groups : List, groups within .h5 file.
    sub_keys : List, keys for each group within .h5 file.

    Returns
    -------
    dictionary : Dictionary in format: {Group1: [key, Key ...], Group2: [Key, Key ...]}.

    """

    dictionary = {group: [key for key in sub_keys[i]] for i, group in enumerate(all_groups)}

    return dictionary


def update_dropdown(attr, old, new):
    """
    Callback to update a group. As group updates it displays the properties within that group on X and Y axis.
    The X and Y axes will be initialised with the [0]th property. Because the X and Y axis should update at the
    same time - use "hold" and "unhold" to callect all events.

    Parameters
    ----------
    attr : String, changed attribute"s name.
    old : Previous value of the attribute.
    new : Updated value of the attribute.

    Returns
    -------
    old : Previous value of the attribute.
    new : Updated value of the attribute.

    """

    curdoc().hold("combine")

    key_property_x.options = env_dict[group.value]
    key_property_x.value = env_dict[group.value][0]

    key_property_y.options = env_dict[group.value]
    key_property_y.value = env_dict[group.value][0]

    curdoc().unhold()

    return old, new


def file_text_name(filename):
    """
    Retrieve name of the imported file and use it in PreText which will display its name.

    Parameters
    ----------
    filename : Compas .h5 file.

    Returns
    -------
    codefeedback : Bokeh widget containing pre-pformated text.

    """

    file_basename = basename(filename)

    codefeedback = PreText(text=f"{file_basename} file is loaded", width=500, style={"color": "black"})

    return codefeedback


def filter_data(data):
    """
    Define filters for the imported data and filter the data. Each group has its own available filters.

    Parameters
    ----------
    data : Data as numpy.ndarray multiplied with *1 to convert booleans: False into 0 and True into 1.

    Returns
    -------
    filtered_data : Filtered data if filter is used, otherwise it will return just data.

    """

    BH = 14
    NS = 13
    if group.value == "CommonEnvelopes":

        filter_core = np.logical_and(
            np.logical_and(
                np.logical_and(_Core_Mass_1 >= Core_Mass_1.value[0], _Core_Mass_1 <= Core_Mass_1.value[1]),
                _Core_Mass_2 >= Core_Mass_2.value[0],
            ),
            _Core_Mass_2 <= Core_Mass_2.value[1],
        )

        filtered_data = data[filter_core]

    elif group.value == "DoubleCompactObjects":

        if select_type.value == "BHBH":

            filter_BHBH = np.logical_and(_Stellar_Type_1 == BH, _Stellar_Type_2 == BH)
            filtered_data = data[filter_BHBH]

        elif select_type.value == "NSNS":

            filter_NSNS = np.logical_and(_Stellar_Type_1 == NS, _Stellar_Type_2 == NS)
            filtered_data = data[filter_NSNS]

        elif select_type.value == "NSBH":

            filter_NSBH = np.logical_and(_Stellar_Type_1 == NS, _Stellar_Type_2 == BH)
            filtered_data = data[filter_NSBH]

        elif select_type.value == "BHNS":

            filter_BHNS = np.logical_and(_Stellar_Type_1 == BH, _Stellar_Type_2 == NS)
            filtered_data = data[filter_BHNS]

        else:
            filtered_data = data

    elif group.value == "Supernovae":
        filtered_data = data
    elif group.value == "SystemParameters":
        filtered_data = data

    else:
        filtered_data = data

    return filtered_data


def range_slider_visibility(new):
    """
    Visibility options when a certain group is selected. Each group has its own filters which will be seen on the
    dashboard when their radio button is selected, while filters from other groups will be hidden.

    Parameters
    ----------
    new : Updated value of the attribute. In this case updated value of a radio button.

    """

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


def change_nan_inf(data):
    """
    Imported data may contain NaN, Inf and -Inf values, since we are plotting hexbins we need to replace these
    data. This function replaces NaN, Inf and -Inf into the mean values of the given property.

    Parameters
    ----------
    data : Data as numpy.ndarray

    Returns
    -------
    data_array : Data as numpy.ndarray where NaN, Inf and -Inf take the mean values of the given data.

    """

    data_array = np.nan_to_num(
        data * 1,
        nan=np.nanmean(data[np.isfinite(data)], axis=0),
        posinf=np.nanmean(data[np.isfinite(data)], axis=0),
        neginf=np.nanmean(data[np.isfinite(data)], axis=0),
    )

    return data_array


def reformat_data(data):
    """
    This function is normalising the data in range from 0 to 1. In special case, data will be reformated.
    This reformating is needed for the proper display of the hexbin plot.

    Parameters
    ----------
    data : Data as numpy.ndarray.

    Returns
    -------
    data_normed : Reformated data as numpy.ndarray.

    """

    # Normalized data, use MinMax scaling: transform data into the range [0,1]
    # To avoid division with 0, check that Max value is not 0
    if max(data, default=default_max) != 0:
        # Next, check if Max value is equal to Min value
        if max(data, default=default_max) == min(data, default=default_min):
            # If Min and Max are equal, data contains array of const. values
            # so return (data - data.min) -- this will be always 0 and it
            # will scale with extra_y_ranges and extra_x_ranges
            data_normed = data - min(data, default=default_min)
        # In other cases, return MinMax scaling
        else:
            data_normed = (data - min(data, default=default_min)) / (
                max(data, default=default_max) - min(data, default=default_min)
            )
    # If Max value is 0, we need to avoid division with 0
    elif max(data, default=default_max) == 0:
        # Normalize MinMax using value close to 0, since we have much larger
        # hexbin size, this doesn't introduce visible deviations
        data_normed = (data - min(data, default=default_min)) / (0.0001 - min(data, default=default_min))

    return data_normed


def data_bin_change(attr, old, new):
    """
    This function controls what will be displayed on the Figure.

    Parameters
    ----------
    attr : String, changed attribute's name.
    old : Previous value of the attribute.
    new : Updated value of the attribute.

    """

    # Update axis lables based on the selected X, Y properties
    p1.xaxis.axis_label = key_property_x.value
    p1.yaxis.axis_label = key_property_y.value

    with h5py.File(filename, "r") as f:

        # Change_nan_inf: convert NaN, inf, -inf values to mean of the property
        # Placed *1 to convert True/False into 1/0
        x_raw = change_nan_inf(f[group.value][key_property_x.value][:] * 1)

        y_raw = change_nan_inf(f[group.value][key_property_y.value][:] * 1)

        # Obtain filtered data from the RangeSlider
        x = filter_data(x_raw)
        y = filter_data(y_raw)

        # Older version of compas .h5 files doesn"t have all data in one array
        x = np.ravel(x)
        y = np.ravel(y)

        # Adding extra axes, to replace our normalized ones. If min/max
        # are equal e.g. we have const. data in array, e.g. Eccentricity>CE is 0
        # we need to add end+1, otherwise the respective axis will not have ticks.
        if min(y, default=default_min) == max(y, default=default_max) or min(x, default=default_min) == max(
            x, default=default_max
        ):
            p1.extra_y_ranges["yraw"].update(start=min(y, default=default_min), end=max(y, default=default_max) + 1)
            p1.extra_x_ranges["xraw"].update(start=min(x, default=default_min), end=max(x, default=default_max) + 1)

        else:
            p1.extra_y_ranges["yraw"].update(start=min(y, default=default_min), end=max(y, default=default_max))
            p1.extra_x_ranges["xraw"].update(start=min(x, default=default_min), end=max(x, default=default_max))

        # Use reformat_data function
        x_normed = reformat_data(x)
        y_normed = reformat_data(y)

        # Place data into bins of certain hexbin size, this will give (q,r) axial hex coordinate of the tiles.
        bins = hexbin(x_normed, y_normed, hex_size)

        # Populate the ColumnDataSource. Adding +0.0001 onto counts so that if count: max=min=1
        # colorbar doesn't dissapear. This small value will not change real counts, nor color.
        source_bin.data = dict(q=bins.q, r=bins.r, counts=bins.counts + 0.0001)

        # When a property is changed, plot could be zoomed in/moved so reset
        # back to the proper axes ranges
        p1.x_range.start = 0
        p1.y_range.start = 0
        p1.x_range.end = 1
        p1.y_range.end = 1


def redraw_plot(attr):
    """
    Redraw Figure into ranges from min to max of the current property.

    Parameters
    ----------
    attr : String, changed attribute"s name.

    """

    # Redraw the plot, as well as its axes
    p1.x_range.start = 0
    p1.y_range.start = 0
    p1.x_range.end = 1
    p1.y_range.end = 1

    col_max = data_bin_change(None, None, group.value)


def reset_plot_and_filters(attr):
    """
    Reset figure and any filters if they were applied.

    Parameters
    ----------
    attr : String, changed attribute"s name.

    """

    # Redraw the plot, as well as its axes
    p1.x_range.start = 0
    p1.y_range.start = 0
    p1.x_range.end = 1
    p1.y_range.end = 1

    Core_Mass_1.value = (min(_Core_Mass_1), max(_Core_Mass_1))
    Core_Mass_2.value = (min(_Core_Mass_2), max(_Core_Mass_2))
    select_type.value = "None"

    col_max = data_bin_change(None, None, group.value)


def update_stats(attr, old, new):
    """
    This function collects number statistics of NaN, Inf and -Inf values from the loaded data and puts the data in
    the Table which is displayed on the dashboard.

    Parameters
    ----------
    attr : String, changed attribute"s name.
    old : Previous value of the attribute.
    new : Updated value of the attribute.

    """

    with h5py.File(filename, "r") as f:

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


def update_colorbar():
    """
    Callback function to change colormap on the colorbar. Colormaps are defined in cbar.

    """

    for key in colormap_dict:
        if cbar.value == key:
            cmap = log_cmap("counts", palette=colormap_dict[cbar.value], low=1, high=col_max)
            color_bar.color_mapper.palette = colormap_dict[cbar.value]


def layout_and_filters():
    """
    Functions that controls whether filters will be displayed on the dashboard or not, which depends whether the new
    or old .h5 compas file is loaded.

    Returns
    -------
    widgets : List of available widgets.

    """
    try:

        key_present = env_dict["CommonEnvelopes"]

        widgets = [
            table_title,
            data_table,
            select_group_to_filter,
            range_group,
            filters_available,
            Core_Mass_1,
            Core_Mass_2,
            select_type,
            buttons,
        ]

        return widgets

    except KeyError:

        widgets = [table_title, data_table, buttons_no]

    return widgets


url_args = curdoc().session_context.request.arguments
if "is_mobile" in url_args.keys():
    is_mobile = url_args["is_mobile"][0]
    if is_mobile == b"True":
        is_mobile = True
    else:
        is_mobile = False

if "filename" in url_args.keys():
    filename = url_args["filename"][0]
    if isinstance(filename, bytes):
        filename = str(filename, "utf-8")

    # Groups in a list
    group_list = get_groups(filename)

    # Environment Dictionary: {Group1: [keys, ...], Group1: [Keys, ...]}
    env_dict = create_dictionary(get_groups(filename), get_keys_from_groups(filename))

    # Dropdown menues for Groups and Properties (Keys); It will start initialised with the first group and the first Key
    # withing that group.
    group = Select(title="Groups", value=f"{group_list[0]}", options=group_list)

    # Get key for a selected group (properties).
    key_property_x = Select(title="X-axis", value=f"{env_dict[group.value][0]}", options=env_dict[group.value])
    key_property_y = Select(title="Y-axis", value=f"{env_dict[group.value][0]}", options=env_dict[group.value])

    # Update dropdown menues.
    group.on_change("value", update_dropdown)

    # Filename text widgets.
    codefeedback = file_text_name(filename)

    # Defining native Bokeh Figure .
    defaults = "pan,box_zoom,wheel_zoom,save"
    TOOLS = [defaults]

    # Initialise Figure.
    p1 = figure(tools=TOOLS, lod_interval=1000, toolbar_location="above")

    # Initialise ColumnDataSourse
    source_bin = ColumnDataSource(data=dict(r=[], q=[], counts=[]))

    # Hexbin size.
    hex_size = 0.005

    # Default min/max values if the given data array is empty.
    default_min = -999
    default_max = -998

    # Color of the selected range on the RangeFilter.ngeFilter.
    bar_color = "#969696"

    # Define fileters for new .h5 file. If they result in KeyError - old file is used, disable filtering.
    try:
        with h5py.File(filename, "r") as f:

            _Core_Mass_1 = f["CommonEnvelopes"]["Core_Mass_1"][:] * 1

            Core_Mass_1 = RangeSlider(
                title="Core_Mass_1",
                bar_color=bar_color,
                start=min(_Core_Mass_1),
                end=max(_Core_Mass_1),
                value=(min(_Core_Mass_1), max(_Core_Mass_1)),
                step=1,
            )

            _Core_Mass_2 = f["CommonEnvelopes"]["Core_Mass_2"][:] * 1

            Core_Mass_2 = RangeSlider(
                title="Core_Mass_2",
                bar_color=bar_color,
                start=min(_Core_Mass_2),
                end=max(_Core_Mass_2),
                value=(min(_Core_Mass_2), max(_Core_Mass_2)),
                step=1,
            )

            _Stellar_Type_1 = f["DoubleCompactObjects"]["Stellar_Type_1"][:] * 1
            _Stellar_Type_2 = f["DoubleCompactObjects"]["Stellar_Type_2"][:] * 1

            select_type = Select(
                title="Filter by type:", value="None", options=["None", "NSNS", "NSBH", "BHNS", "BHBH"]
            )
    except KeyError:

        Core_Mass_1 = RangeSlider(title="", bar_color=bar_color, start=0, end=1, value=(0, 1), step=1)

        Core_Mass_2 = RangeSlider(title="", bar_color=bar_color, start=0, end=1, value=(0, 1), step=1)

        _Stellar_Type_1 = 0
        _Stellar_Type_2 = 0

        select_type = Select(title="No filters available", value="", options=["", "", "", "", ""])

    # Radio buttons to select available groups which will then show available filters for the selected group.
    range_group = RadioGroup(
        labels=["CommonEnvelopes", "DoubleCompactObjects", "Supernovae", "SystemParameters"], active=0
    )

    range_group.on_click(range_slider_visibility)
    range_slider_visibility(None)

    # Set the original axes as False and then set extra axes as left/below to show real values of the properties.
    p1.xaxis.visible = False
    p1.yaxis.visible = False

    # Initiate the extra axes.
    p1.extra_y_ranges = {"yraw": Range1d(start=0, end=1)}
    p1.add_layout(LinearAxis(y_range_name="yraw", axis_label=key_property_y.value), "left")

    p1.extra_x_ranges = {"xraw": Range1d(start=0, end=1)}
    p1.add_layout(LinearAxis(x_range_name="xraw", axis_label=key_property_x.value), "below")

    # Event handlers with on_change: X, Y axis, Filters and refresh data_bin_change function that controls Figure.
    key_property_x.on_change("value", data_bin_change)
    key_property_y.on_change("value", data_bin_change)

    Core_Mass_1.on_change("value_throttled", data_bin_change)
    Core_Mass_2.on_change("value_throttled", data_bin_change)

    select_type.on_change("value", data_bin_change)

    # Populate the initial data and pass it down for colormap/colorbar change.
    col_max = data_bin_change(None, None, group.value)

    cmap = log_cmap("counts", "Cividis256", 1, col_max)

    h = p1.hex_tile(q="q", r="r", size=hex_size, line_color=None, source=source_bin, fill_color=cmap)

    hover = HoverTool(
        tooltips=[("Counts", "@counts")],
        mode="mouse",
        point_policy="follow_mouse",
        renderers=[h],
    )

    color_bar = ColorBar(
        title="Counts",
        color_mapper=cmap["transform"],
        location=(0, 0),
        ticker=LogTicker(),
        label_standoff=12,
    )

    # Perceptually Uniform Sequential Colormaps - available in Bokeh.
    cbar = Select(
        title="Choose Colormap",
        value="Cividis",
        options=[
            "Cividis",
            "Inferno",
            "Magma",
            "Plasma",
            "Viridis",
            "Cividis_r",
            "Inferno_r",
            "Magma_r",
            "Plasma_r",
            "Viridis_r",
        ],
    )

    # Dictionary containing colormap names and their color sequences
    colormap_dict = {
        "Cividis": Cividis256,
        "Inferno": Inferno256,
        "Magma": Magma256,
        "Plasma": Plasma256,
        "Viridis": Viridis256,
        "Cividis_r": Cividis256[::-1],
        "Inferno_r": Inferno256[::-1],
        "Magma_r": Magma256[::-1],
        "Plasma_r": Plasma256[::-1],
        "Viridis_r": Viridis256[::-1],
    }

    cbar.on_change("value", lambda attr, old, new: update_colorbar())

    p1.add_layout(color_bar, "right")
    color_bar.formatter = PrintfTickFormatter(format="%.0e")

    p1.add_tools(hover)

    # Axes on the layout.
    axes = column(key_property_x, key_property_y)

    # Event handlers for Reset buttons.
    r = Button(label="Reset Figure", min_height=50)
    r.on_click(redraw_plot)

    reset_all = Button(label="Reset Figure & Filters", min_height=50)
    reset_all.on_click(reset_plot_and_filters)

    # Initialise table with NaN, Inf, -Inf values.
    table_source = ColumnDataSource(data=dict(x=[], y=[]))

    # Event handlers for X, Y properties and Table updates.
    key_x = PreText(text="0")
    key_y = PreText(text="0")
    key_property_x.on_change("value", update_stats)
    key_property_y.on_change("value", update_stats)
    update_stats(None, None, key_property_x.value)
    update_stats(None, None, key_property_y.value)

    # Update Table statistics with filtering.
    Core_Mass_1.on_change("value_throttled", update_stats)
    Core_Mass_2.on_change("value_throttled", update_stats)
    select_type.on_change("value", update_stats)

    # Show counts of the inf/nan values.
    columns = [
        TableColumn(field="inf_x", title="X-axis"),
        TableColumn(field="inf_y", title="Y-axis"),
    ]
    data_table = DataTable(source=table_source, columns=columns, width=200, height=150)

    # Define some text on canvas.
    table_title = PreText(text="Table with nan/inf values", style={"color": "black"})

    select_group_to_filter = PreText(text="Select a Group to apply filters to:", style={"color": "black"})

    filters_available = PreText(text="Available filters:", style={"color": "black"})

    # Reset buttons and Colormap Select widget.
    redraw = row(r, width=100)
    reset = row(reset_all, width=150)
    pick_color = row(cbar, width=110)

    # For layout: Reset buttons if filters are present & Select colormap.
    buttons = row(redraw, reset, pick_color, align="center")
    # No filters: reset and select colormap.
    buttons_no = row(redraw, pick_color, align="center")

    # Sorting widgets for layouts.
    available_widgets = column(layout_and_filters())
    figure_widget = column(codefeedback, p1)
    middle_column = column(group, available_widgets)
    layout_data = row(figure_widget, middle_column, axes)

    # Layout on the page - for Computers
    web = Panel(child=layout_data, title="Computer")

    # Layout on the page - for Mobile phones
    mobile = Panel(
        child=column(
            codefeedback,
            group,
            axes,
            available_widgets,
            p1,
        ),
        title="Mobile",
    )

    # I haven't found a way to select an active tab other than placing the desired tab as the first tab
    if is_mobile:
        tabs = Tabs(tabs=[mobile, web])
    else:
        tabs = Tabs(tabs=[web, mobile])

    # Make space between plot and tools/other items
    p1.min_border_right = 30

    # Start server
    curdoc().add_root(tabs)

else:
    info = Paragraph(text="No data for plots was provided")
    layout_data = row(info)
    curdoc().add_root(layout_data)
