import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

class GroupBox(Gtk.Box):
    def __init__(self, parent, group):
        self.parent = parent
        self.streams = []

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.context = self.get_style_context()
        self.context.add_class("group-box")

        #GLib.timeout_add_seconds(1, self.update_fields, parent.server.group(group.identifier))

        # GROUP NAME
        self.name = Gtk.Label("")

        # GROUP MUTE SWITCH
        self.mute_switch = Gtk.Switch()
        self.mute_switch.set_state(not group.muted)
        self.mute_switch.connect("notify::active", parent.on_mute_toggle, {"type": "group", "group": group})

        #self.clients = self.build_clients_box(group)
        self.build_header()
        self.build_source_dropdown(group)
        self.build_separator()
        self.build_clients_box(group)

        self.update_fields(group)


    def update_fields(self, group):
        self.name.set_text(group.friendly_name)
        self.mute_switch.set_state(not group.muted)

        #return GLib.SOURCE_CONTINUE


    def build_header(self):
        # HEADER
        group_header_box = Gtk.Box()
        group_header_context = group_header_box.get_style_context()
        group_header_context.add_class("group-header")

        group_header_box.pack_start(self.name, False, False, 1)
        group_header_box.pack_end(self.mute_switch, False, False, 1)

        self.pack_start(group_header_box, False, False, 1)


    def build_source_dropdown(self, group):
        self.streams = []

        # DROPDOWN
        stream_store = Gtk.ListStore(str, str)
        for stream in self.parent.server.streams:
            self.streams.append(stream.friendly_name)
            stream_store.append([group.identifier, stream.friendly_name])

        source_dropdown = Gtk.ComboBox.new_with_model_and_entry(stream_store)
        source_dropdown.set_entry_text_column(1)

        # If the stream isn't found, just use the first one
        # This can be caused by changing the stream name on the server
        try:
            source_dropdown.set_active(self.streams.index(group.stream))
        except:
            source_dropdown.set_active(0)

        source_dropdown.connect("changed", self.on_stream_changed)

        source_dropdown_context = source_dropdown.get_style_context()
        source_dropdown_context.add_class("dropdown")

        source_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        source_label = Gtk.Label("Source")
        source_label_context = source_label.get_style_context()
        source_label_context.add_class("title")
        source_label.set_halign(Gtk.Align.START)

        source_container.pack_start(source_label, False, False, 1)
        source_container.pack_end(source_dropdown, False, False, 1)
        source_container_context = source_container.get_style_context()
        source_container_context.add_class("source-container")

        self.pack_start(source_container, False, False, 1)


    def build_clients_box(self, group):
        client_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        client_context = client_container.get_style_context()
        client_context.add_class("client-container")

        clients_label = Gtk.Label("Clients")
        clients_label_context = clients_label.get_style_context()
        clients_label_context.add_class("title")
        clients_label.set_halign(Gtk.Align.START)
        client_container.pack_start(clients_label, False, False, 0)

        for client_name in group.clients:
            client_box = Gtk.Box()
            client_box_context = client_box.get_style_context()
            client_box_context.add_class("client-box")

            client_switch = Gtk.Switch()
            client_switch.set_state(not self.parent.server.client(client_name).muted)
            client_switch.connect(
                "notify::active",
                self.parent.on_mute_toggle,
                {"type": "client", "client": client_name}
            )

            name = Gtk.Label(self.parent.server.client(client_name).friendly_name)

            client_box.pack_start(name, False, False, 1)
            client_box.pack_end(client_switch, False, False, 1)

            client_container.pack_start(client_box, False, False, 0)

        self.pack_start(client_container, False, False, 1)

    def build_separator(self):
        # SEPARATOR
        separator = Gtk.Separator()
        separator_context = separator.get_style_context()
        separator_context.add_class("separator")

        self.pack_start(separator, False, False, 1)

    def on_stream_changed(self, source_dropdown):
        self.parent.emit("stream_changed", source_dropdown)
