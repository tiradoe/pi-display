import gi
from dotenv import dotenv_values
from gi.repository import Gtk
from phue import Bridge

from .widgets.group import GroupBox

gi.require_version("Gtk", "3.0")


class HueView(Gtk.ScrolledWindow):
    def __init__(self, parent, header_bar):
        Gtk.ScrolledWindow.__init__(self, Gtk.Adjustment(0, 0, 0, 0, 0, 0))
        header_bar = header_bar(self, "Lights")
        self.config = dotenv_values(".env")
        self.parent = parent

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_box.set_name("hue-content-box")

        content_box_context = self.content_box.get_style_context()
        content_box_context.add_class("content-box")
        self.content_box.pack_start(header_bar, False, False, 1)

        self.bridge_ip = self.config["PHILIPS_HUE_BRIDGE_IP"]
        self.bridge = self.connect_to_hue()

        self.build_light_groups()
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

        for group in groups:
            group_box.add(GroupBox(self.bridge, group))

        self.content_box.pack_start(group_box, True, True, 1)

    def reset_view(self, button):
        self.parent.emit("update_view", "home_view")
