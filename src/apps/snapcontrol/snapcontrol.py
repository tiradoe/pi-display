import gi
import asyncio
import snapcast.control

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GObject
from dotenv import dotenv_values
from .widgets.group import GroupBox

class SnapControlView(Gtk.ScrolledWindow):
    __gsignals__ = {
        'update_groups': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'toggle_mute': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'stream_changed': (GObject.SIGNAL_RUN_FIRST, None, (Gtk.ComboBox,)),
    }

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
        self.connect("stream_changed", self.on_stream_changed)
        #for group in self.groups:
        #    print(group.get_child().title)

    def generate_view(self):
        self.groups.set_valign(Gtk.Align.START)
        self.groups.set_selection_mode(Gtk.SelectionMode.NONE)
        self.groups.set_name("snapcontrol-grid")

        self.update_group_list()
        self.add(self.groups)


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
