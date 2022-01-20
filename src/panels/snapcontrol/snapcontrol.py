import gi
import asyncio
import snapcast.control

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from dotenv import dotenv_values

class SnapControlView(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self, Gtk.Adjustment(0,0,0,0,0,0))
        self.row_name = "Snapcontrol"
        self.loop = asyncio.get_event_loop()
        self.config = dotenv_values(".env")
        self.server = self.loop.run_until_complete(
                snapcast.control.create_server(
                    self.loop,
                    self.config["SNAPCAST_SERVER_IP"],
                    self.config["SNAPCAST_TCP_PORT"])
                )
        self.groups = Gtk.FlowBox()
        self.generate_view()
        GLib.timeout_add_seconds(1, self.update_groups)

    def generate_view(self):
        self.groups.set_valign(Gtk.Align.START)
        self.groups.set_selection_mode(Gtk.SelectionMode.NONE)
        self.groups.set_name("snapcontrol-grid")

        self.update_group_list()
        self.add(self.groups)

    def update_groups(self):
        for group in self.groups:
            wtf = group.get_children()
            for child in wtf:
                print(child)
            return GLib.SOURCE_CONTINUE


    def get_clients_box(self, group):
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
            client_switch.connect(
                "notify::active",
                self.on_mute_toggle,
                {"type": "client", "client": client_name}
            )

            client_switch.set_state(not self.server.client(client_name).muted)
            name = Gtk.Label(self.server.client(client_name).friendly_name)

            client_box.pack_start(name, False, False, 1)
            client_box.pack_end(client_switch, False, False, 1)

            client_container.pack_start(client_box, False, False, 0)

        return client_container


    def get_source_dropdown(self, group):
        streams = []
        # DROPDOWN
        stream_store = Gtk.ListStore(str, str)
        for stream in self.server.streams:
            streams.append(stream.friendly_name)
            stream_store.append([group.identifier, stream.friendly_name])

        source_dropdown = Gtk.ComboBox.new_with_model_and_entry(stream_store)
        source_dropdown.set_entry_text_column(1)

        # If the stream isn't found, just use the first one
        # This can because by changing the stream name on the server
        try:
            source_dropdown.set_active(streams.index(group.stream))
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
        source_container.set_name("source-container")

        return source_container


    def set_volume(self, volume):
        # set volume for client #0 to 50%
        client = self.server.clients[1]
        self.loop.run_until_complete(self.server.client_volume(
            client.identifier, {
                'percent': volume,
                'muted': False
                })
            )

    def on_mute_toggle(self, switch, gparam, player):
        if(player["type"] == 'group'):
            self.loop.run_until_complete(
                self.server.group_mute( player["group"].identifier,
                not switch.get_state()
            ))
        else:
            self.loop.run_until_complete(self.server.client_volume(
                player["client"], {
                    'muted': not switch.get_state()
                    }
                ))

    def on_stream_changed(self, combo):
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            group_id, stream_id = model[tree_iter][:2]

            self.loop.run_until_complete(
                self.server.group_stream(group_id, stream_id)
            )


    def update_group_list(self):
        for group in self.server.groups:
            group_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            group_box.set_name("group-box")

            # HEADER
            group_header_box = Gtk.Box()
            group_header_box.set_name("group-header")

            group_switch = Gtk.Switch()
            group_switch.set_name("switch")
            group_switch.connect("notify::active", self.on_mute_toggle, {"type": "group", "group": group})
            group_switch.set_state(not group.muted)

            group_name_label = Gtk.Label(group.friendly_name)

            group_header_box.pack_start(group_name_label, False, False, 1)
            group_header_box.pack_end(group_switch, False, False, 1)

            group_box.pack_start(group_header_box, False, False, 1)

            # SOURCE DROPDOWN
            source_container = self.get_source_dropdown(group)

            # SEPARATOR
            group_box.pack_start(source_container, False, False, 1)
            separator = Gtk.Separator()
            group_box.pack_start(separator, False, False, 1)

            separator_context = separator.get_style_context()
            separator_context.add_class("separator")

            # CLIENT LIST
            clients = self.get_clients_box(group)
            group_box.pack_start(clients, False, False, 1)

            self.groups.add(group_box)
