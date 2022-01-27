import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from phue import Bridge
from dotenv import dotenv_values
from .widgets.group import GroupBox

class HueView(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self, Gtk.Adjustment(0,0,0,0,0,0))
        self.config = dotenv_values(".env")

        self.content_box = Gtk.Box()
        self.content_box.set_name("hue-box")

        self. bridge_ip = self.config["PHILIPS_HUE_BRIDGE_IP"]
        self.bridge = self.connect_to_hue()

        self.light_groups = self.build_light_groups()

        self.add(self.content_box)
        self.connect_to_hue()


    def connect_to_hue(self):
        bridge = Bridge(self.bridge_ip)
        bridge.connect()
        return bridge

    def build_light_groups(self):
        groups = self.bridge.groups
        group_box = Gtk.FlowBox()
        group_box.set_max_children_per_line(4)
        group_box.set_selection_mode(Gtk.SelectionMode.NONE)
        #group_box.set_homogeneous(True)

        for group in groups:
            group_box.add(GroupBox(self.bridge, group))

        self.content_box.pack_start(group_box, True, True, 1)
