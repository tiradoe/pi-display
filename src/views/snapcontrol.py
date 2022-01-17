import gi
import asyncio
import snapcast.control

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from dotenv import dotenv_values

class SnapControlView(Gtk.FlowBox):
    def __init__(self):
        self.row_name = "Snapcontrol"
        self.loop = asyncio.get_event_loop()
        self.config = dotenv_values(".env")
        self.server = self.loop.run_until_complete(
                snapcast.control.create_server(
                    self.loop,
                    self.config["SNAPCAST_SERVER_IP"],
                    self.config["SNAPCAST_TCP_PORT"])
                )

    def generate_view(self):
        display = Gtk.FlowBox()

        display.set_valign(Gtk.Align.START)
        display.set_selection_mode(Gtk.SelectionMode.NONE)
        display.set_name("snapcontrol-grid")

        self.get_group_list(display)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(display)

        return scrolled_window


    def get_group_list(self, flowbox):

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

            group_name = Gtk.Label(group.friendly_name)

            group_header_box.pack_start(group_name, False, False, 20)
            group_header_box.pack_end(group_switch, False, False, 1)

            group_box.pack_start(group_header_box, False, False, 1)

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

            source_container = Gtk.Box()
            source_container.pack_start(Gtk.Label("Source"), False, False, 1)
            source_container.pack_end(source_dropdown, False, False, 1)
            source_container.set_name("source-container")

            group_box.pack_start(source_container, False, False, 1)
            separator = Gtk.Separator()
            group_box.pack_start(separator, False, False, 1)

            separator_context = separator.get_style_context()
            separator_context.add_class("separator")

            #CLIENTS

            group_box.pack_start(Gtk.Label("Clients"), False, False, 1)

            for client_name in group.clients:
                client_box = Gtk.Box()
                client_box.set_name("client-box")

                client_switch = Gtk.Switch()
                client_switch.connect("notify::active", self.on_mute_toggle,  {"type": "client", "client": client_name})
                client_switch.set_state(not self.server.client(client_name).muted)

                name = Gtk.Label(self.server.client(client_name).friendly_name)


                client_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                client_context = client_container.get_style_context()
                client_context.add_class("client-container")

                client_box.pack_start(name, False, False, 10)
                client_box.pack_end(client_switch, False, False, 1)

                client_container.pack_start(client_box, False, False, 0)

                group_box.pack_start(client_container, False, False, 1)

            flowbox.add(group_box)

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
