import gi
from datetime import datetime
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

class CalendarBox(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        GLib.timeout_add_seconds(1, self.update_date)
        self.set_name("calendar-box")

        self.month_label= Gtk.Label("")
        self.day_of_month_label= Gtk.Label("")
        self.day_of_month_label.set_name("day-of-month-label")
        self.day_of_week_label= Gtk.Label("")

        self.pack_start(self.month_label, False, False, 2)
        self.pack_start(self.day_of_month_label, False, False, 2)
        self.pack_start(self.day_of_week_label, False, False, 2)

        self.update_date()

    def update_date(self):
        date = datetime.today()

        self.month_label.set_text(date.strftime("%B"))
        self.day_of_month_label.set_text(date.strftime("%d").upper())
        self.day_of_week_label.set_text(date.strftime("%A"))

        return GLib.SOURCE_CONTINUE
