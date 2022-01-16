import gi
import time
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

class ClockLabel(Gtk.Label):
    def __init__(self):
        Gtk.Label.__init__(self, "")
        GLib.timeout_add_seconds(1, self.update_time)
        self.set_name("clock")
        self.update_time()

    def update_time(self):
        time = self.get_time()
        self.set_text(time)
        return GLib.SOURCE_CONTINUE

    def get_time(self):
        return time.strftime("%H:%M")
