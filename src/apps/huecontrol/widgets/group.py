import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

class GroupBox(Gtk.Box):
    def __init__(self, bridge, group):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.context = self.get_style_context()
        self.context.add_class("group-box")
        self.context.add_class("groups-container")
        self.bridge = bridge

        # GROUP NAME
        self.name = Gtk.Label("")

        # GROUP ON/OFF SWITCH
        #self.group_switch = Gtk.Switch()
        #self.mute_switch.set_state(not group.muted)
        #self.mute_switch.connect("notify::active", parent.on_mute_toggle, {"type": "group", "group": group})

        #self.clients = self.build_clients_box(group)
        self.build_header()
        self.build_separator()
        self.build_lights_box(group)

        self.update_fields(group)


    def update_fields(self, group):
        self.name.set_text(group.name)


    def build_header(self):
        # HEADER
        group_header_box = Gtk.Box()
        group_header_context = group_header_box.get_style_context()
        group_header_context.add_class("group-header")

        group_header_box.pack_start(self.name, False, False, 1)

        self.pack_start(group_header_box, False, False, 1)


    def build_lights_box(self, group):
        lights_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        lights_container_context = lights_container.get_style_context()
        lights_container_context.add_class("client-container")

        lights_label = Gtk.Label("Lights")
        lights_label_context = lights_label.get_style_context()
        lights_label_context.add_class("title")
        lights_label.set_halign(Gtk.Align.START)
        lights_container.pack_start(lights_label, False, False, 0)

        for light in group.lights:
            light_box = Gtk.Box()
            light_box_context = light_box.get_style_context()
            light_box_context.add_class("client-box")

            light_switch = Gtk.Switch()
            light_switch.set_state(light.on)
            light_switch.connect(
                "notify::active",
                self.on_light_toggle,
                light
            )

            name = Gtk.Label(light.name)

            light_box.pack_start(name, False, False, 1)
            light_box.pack_end(light_switch, False, False, 1)

            lights_container.pack_start(light_box, False, False, 0)

        self.pack_start(lights_container, False, False, 1)

    def build_separator(self):
        # SEPARATOR
        separator = Gtk.Separator()
        separator_context = separator.get_style_context()
        separator_context.add_class("separator")

        self.pack_start(separator, False, False, 1)


    def on_light_toggle(self, switch, gparam, light):
        self.bridge.set_light(light.light_id, 'on', switch.get_state())
