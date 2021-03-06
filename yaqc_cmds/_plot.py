"""GUI for displaying scans in progress, current slice etc."""


import collections

from PySide2 import QtCore, QtWidgets

import yaqc_cmds.project.project_globals as g
import yaqc_cmds.sensors as sensors
import yaqc_cmds.project.widgets as pw
import yaqc_cmds.project.classes as pc
import yaqc_cmds.somatic as somatic


class GUI(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.create_frame()
        self.create_settings()
        self.on_sensors_changed()

    def create_frame(self):
        self.main_widget = g.main_window.read().plot_widget
        # create main daq tab
        main_widget = self.main_widget
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        main_widget.setLayout(layout)
        # display
        # container widget
        display_container_widget = pw.ExpandingWidget()
        display_container_widget.setLayout(QtWidgets.QVBoxLayout())
        display_layout = display_container_widget.layout()
        display_layout.setMargin(0)
        layout.addWidget(display_container_widget)
        # big number
        big_number_container_widget = QtWidgets.QWidget()
        big_number_container_widget.setLayout(QtWidgets.QHBoxLayout())
        big_number_container_layout = big_number_container_widget.layout()
        big_number_container_layout.setMargin(0)
        self.big_display = pw.SpinboxAsDisplay(font_size=100)
        self.big_channel = pw.Label("channel", font_size=72)
        big_number_container_layout.addWidget(self.big_channel)
        big_number_container_layout.addStretch(1)
        big_number_container_layout.addWidget(self.big_display)
        display_layout.addWidget(big_number_container_widget)
        # plot
        self.plot_widget = pw.Plot1D()
        self.plot_scatter = self.plot_widget.add_scatter()
        self.plot_line = self.plot_widget.add_line()
        display_layout.addWidget(self.plot_widget)
        # vertical line
        line = pw.line("V")
        layout.addWidget(line)
        # settings
        settings_container_widget = QtWidgets.QWidget()
        settings_scroll_area = pw.scroll_area()
        settings_scroll_area.setWidget(settings_container_widget)
        settings_scroll_area.setMinimumWidth(300)
        settings_scroll_area.setMaximumWidth(300)
        settings_container_widget.setLayout(QtWidgets.QVBoxLayout())
        self.settings_layout = settings_container_widget.layout()
        self.settings_layout.setMargin(5)
        layout.addWidget(settings_scroll_area)

    def create_settings(self):
        # display settings
        input_table = pw.InputTable()
        input_table.add("Display", None)
        self.channel = pc.Combo()
        input_table.add("Channel", self.channel)
        self.axis = pc.Combo()
        input_table.add("Axis", self.axis)
        self.settings_layout.addWidget(input_table)
        # global daq settings
        input_table = pw.InputTable()
        input_table.add("Settings", None)
        # input_table.add("ms Wait", ms_wait)
        for sensor in sensors.sensors:
            input_table.add(sensor.name, None)
            input_table.add("Status", sensor.busy)
            input_table.add("Freerun", sensor.freerun)
            input_table.add("Time", sensor.measure_time)
        input_table.add("Scan", None)
        # input_table.add("Loop Time", loop_time)
        self.idx_string = pc.String(initial_value="None", display=True)
        input_table.add("Scan Index", self.idx_string)
        self.settings_layout.addWidget(input_table)
        # stretch
        self.settings_layout.addStretch(1)

    def on_channels_changed(self):
        new = list(sensors.get_channels_dict())
        self.channel.set_allowed_values(new)

    def on_data_file_created(self):
        data = somatic._wt5.get_data_readonly()
        self.axis.set_allowed_values(data.axis_expressions)

    def on_data_file_written(self):
        data = somatic._wt5.get_data_readonly()
        last_idx_written = somatic._wt5.last_idx_written
        self.idx_string.write(str(last_idx_written))
        if data is None or last_idx_written is None:
            return
        # data
        idx = last_idx_written
        axis = next(a for a in data.axes if a.expression == self.axis.read())
        channel = data[self.channel.read()]
        xi = axis[idx[:-1]]
        yi = channel[idx[:-1]]
        self.plot_scatter.setData(xi, yi)
        # limits
        self.plot_widget.set_xlim(axis.min(), axis.max())
        self.plot_widget.set_ylim(channel.min(), channel.max())

    def on_sensors_changed(self):
        for s in sensors.sensors:
            s.update_ui.connect(self.update_big_number)
        self.on_channels_changed()

    def stop(self):
        pass

    def update_big_number(self):
        channel = self.channel.read()
        if channel == "None":
            return
        sensor = sensors.get_channels_dict()[channel]
        num = sensor.channels[channel]
        self.big_channel.setText(channel)
        self.big_display.setValue(num)


gui = GUI()
somatic.signals.data_file_written.connect(gui.on_data_file_written)
somatic.signals.data_file_created.connect(gui.on_data_file_created)
sensors.signals.channels_changed.connect(gui.on_channels_changed)
sensors.signals.sensors_changed.connect(gui.on_sensors_changed)
