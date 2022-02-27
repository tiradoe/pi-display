import asyncio

import gi
import snapcast.control

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from dotenv import dotenv_values
from .widgets.group import GroupBox


class SnapCastView(Gtk.ScrolledWindow):
    __gsignals__ = {
        'update_groups': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'toggle_mute': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'stream_changed': (GObject.SIGNAL_RUN_FIRST, None, (Gtk.ComboBox,)),
    }

    def __init__(self, parent, header_bar):
        Gtk.ScrolledWindow.__init__(self, Gtk.Adjustment(0, 0, 0, 0, 0, 0))
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_box.set_name("snapcast-content-box")
        content_box_context = self.content_box.get_style_context()
        content_box_context.add_class("content-box")

        self.parent = parent
        self.row_name = "Snapcontrol"
        self.loop = asyncio.get_event_loop()
        self.config = dotenv_values(".env")
        self.server = self.loop.run_until_complete(
            snapcast.control.create_server(
                self.loop,
                self.config["SNAPCAST_SERVER_IP"],
                self.config["SNAPCAST_TCP_PORT"])
        )
        self.groups_container = Gtk.Box()
        groups_container_context = self.groups_container.get_style_context()
        groups_container_context.add_class("groups-container")
        self.groups_container.set_name("groups-container")
        self.groups = Gtk.FlowBox()

        self.generate_view(header_bar)
        self.connect("stream_changed", self.on_stream_changed)

    def generate_view(self, header_bar):
        self.content_box.pack_start(header_bar(self, "Snapcast"), False, False, 1)
        self.groups.set_valign(Gtk.Align.START)
        self.groups.set_selection_mode(Gtk.SelectionMode.NONE)
        self.groups.set_name("snapcast-grid")

        self.update_group_list()
        self.groups_container.pack_end(self.groups, True, True, 1)
        self.content_box.pack_end(self.groups_container, True, True, 1)

        self.add(self.content_box)

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
        if (player["type"] == 'group'):
            self.loop.run_until_complete(
                self.server.group_mute(player["group"].identifier,
                                       not switch.get_state()
                                       ))
        else:
            self.loop.run_until_complete(self.server.client_volume(
                player["client"], {
                    'muted': not switch.get_state()
                }
            ))

    def on_stream_changed(self, view, combo):
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            group_id, stream_id = model[tree_iter][:2]

            self.loop.run_until_complete(
                self.server.group_stream(group_id, stream_id)
            )

    def update_group_list(self):
        for group in self.server.groups:
            group_box = GroupBox(self, group)
            self.groups.add(group_box)

    def reset_view(self, button):
        self.parent.emit("update_view", "home_view")
