import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

class GroupBox(Gtk.Box):
    def __init__(self, group, parent):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        GLib.timeout_add_seconds(1, self.update_data, group)
        self.title = Gtk.Label("")

        self.mute_switch = Gtk.Switch()
        self.mute_switch.connect("notify::active", self.on_mute_toggle, {"type": "group", "group": group}, parent)
        self.pack_start(self.title, False, False, 1)
        self.pack_start(self.mute_switch, False, False, 1)
        self.update_data(group, parent)

    def update_data(self, group, parent):
        self.mute_switch.set_state(not group.muted)
        for parent_group in parent.groups:
            if parent_group.identifier == group.identifier:
                self.title.set_text(parent_group.friendly_name)

        print(parent.groups)


        return GLib.SOURCE_CONTINUE

    def on_mute_toggle(self, switch, gparam, player, parent):
        if(player["type"] == 'group'):
            self.server = parent.server
            parent.loop.run_until_complete(
                parent.server.group_mute( player["group"].identifier,
                not switch.get_state()
            ))
        else:
            loop.run_until_complete(server.client_volume(
                player["client"], {
                    'muted': not switch.get_state()
                    }
                ))
