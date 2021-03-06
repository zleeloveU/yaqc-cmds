import pathlib

import appdirs
import toml

from . import signals
from ._sensors import Sensor, Driver, SensorWidget


sensors = []
config = toml.load(pathlib.Path(appdirs.user_config_dir("yaqc-cmds", "yaqc-cmds")) / "config.toml")
for section in config["sensors"].keys():
    if section == "settings":
        continue
    if config["sensors"][section]["enable"]:
        # collect arguments
        kwargs = dict()
        for option in config["sensors"][section].keys():
            if option in ["enable", "model", "serial", "path", "__name__"]:
                continue
            else:
                kwargs[option] = config["sensors"][section][option]
                sensor = Sensor(Driver, kwargs, None, Widget=SensorWidget, name=section, model="Virtual",)
                sensors.append(sensor)
                sensor.initialize()


def get_channels_dict():
    channels = dict()
    for sensor in sensors:
        for name in sensor.channel_names:
            channels[name] = sensor
    if not channels:
        raise Exception("you must have at least one sensor with channels to run yaqc-cmds")
    return channels
