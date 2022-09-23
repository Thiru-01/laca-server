import asyncio
import os
from pathlib import Path
from svgtrace import trace, doTrace
import numpy as np
from PIL import Image, ImageOps
from unicorn import inkex
from unicorn.svg_parser import SvgParser
from unicorn.context import GCodeContext


class MyEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.context = None
        self.OptionParser.add_option("--pen-up-angle",
                                     action="store", type="float",
                                     dest="pen_up_angle", default="50.0",
                                     help="Pen Up Angle")
        self.OptionParser.add_option("--pen-down-angle",
                                     action="store", type="float",
                                     dest="pen_down_angle", default="30.0",
                                     help="Pen Down Angle")
        self.OptionParser.add_option("--start-delay",
                                     action="store", type="float",
                                     dest="start_delay", default="150.0",
                                     help="Delay after pen down command before movement in milliseconds")
        self.OptionParser.add_option("--stop-delay",
                                     action="store", type="float",
                                     dest="stop_delay", default="150.0",
                                     help="Delay after pen up command before movement in milliseconds")
        self.OptionParser.add_option("--xy-feedrate",
                                     action="store", type="float",
                                     dest="xy_feedrate", default="3500.0",
                                     help="XY axes feedrate in mm/min")
        self.OptionParser.add_option("--z-feedrate",
                                     action="store", type="float",
                                     dest="z_feedrate", default="150.0",
                                     help="Z axis feedrate in mm/min")
        self.OptionParser.add_option("--z-height",
                                     action="store", type="float",
                                     dest="z_height", default="0.0",
                                     help="Z axis print height in mm")
        self.OptionParser.add_option("--finished-height",
                                     action="store", type="float",
                                     dest="finished_height", default="0.0",
                                     help="Z axis height after printing in mm")
        self.OptionParser.add_option("--register-pen",
                                     action="store", type="string",
                                     dest="register_pen", default="true",
                                     help="Add pen registration check(s)")
        self.OptionParser.add_option("--x-home",
                                     action="store", type="float",
                                     dest="x_home", default="0.0",
                                     help="Starting X position")
        self.OptionParser.add_option("--y-home",
                                     action="store", type="float",
                                     dest="y_home", default="0.0",
                                     help="Starting Y position")
        self.OptionParser.add_option("--num-copies",
                                     action="store", type="int",
                                     dest="num_copies", default="1")
        self.OptionParser.add_option("--continuous",
                                     action="store", type="string",
                                     dest="continuous", default="false",
                                     help="Plot continuously until stopped.")
        self.OptionParser.add_option("--pause-on-layer-change",
                                     action="store", type="string",
                                     dest="pause_on_layer_change", default="false",
                                     help="Pause on layer changes.")
        self.OptionParser.add_option("--tab",
                                     action="store", type="string",
                                     dest="tab")

    def output(self):
        return self.context.generate()

    def effect(self):
        self.context = GCodeContext(self.options.xy_feedrate, self.options.z_feedrate,
                                    self.options.start_delay, self.options.stop_delay,
                                    self.options.pen_up_angle, self.options.pen_down_angle,
                                    self.options.z_height, self.options.finished_height,
                                    self.options.x_home, self.options.y_home,
                                    self.options.register_pen,
                                    self.options.num_copies,
                                    self.options.continuous,
                                    self.svg_file)
        parser = SvgParser(self.document.getroot(), self.options.pause_on_layer_change)
        parser.parse()
        for entity in parser.entities:
            entity.get_gcode(self.context)


if __name__ == '__main__':
    name = "th.jpg"
    currentDir = os.getcwd()
    fullPath = "{}\{}".format(currentDir, name)

    print(f"{name.split('.')[0]}.svg")
#    Path(f"{name.split('.')[0]}.svg").write_text(trace(fullPath, True), encoding="utf-8")
    print(trace(fullPath))
    print("thiru")
    gcode = MyEffect()
    gcode.affect([f"{name.split('.')[0]}.svg"])

    print(gcode.output())
