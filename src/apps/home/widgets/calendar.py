import gi
from datetime import datetime
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

class CalendarBox(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        GLib.timeout_add_seconds(1, self.update_date)
        self.set_name("calendar-box")

        self.day_label = Gtk.Label("")
        self.month_label = Gtk.Label("")
        self.year_label = Gtk.Label("")

        self.pack_start(self.day_label, False, False, 2)
        self.pack_start(self.month_label, False, False, 2)
        self.pack_start(self.year_label, False, False, 2)

        self.update_date()

    def update_date(self):
        date = datetime.today()

        self.day_label.set_text(str(date.day))
        self.month_label.set_text(date.strftime("%b").upper())
        self.year_label.set_text(str(date.year))

        return GLib.SOURCE_CONTINUE
