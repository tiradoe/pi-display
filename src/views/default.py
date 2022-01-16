import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from datetime import datetime
from widgets.clock import ClockLabel
from widgets.calendar import CalendarBox

class DefaultView(Gtk.Grid):
    def __init__(self):
        self.row_name = "Default"
        self.generate_view()

    def generate_view(self):
        display = Gtk.Grid()

        date_box = self.date_box()
        picture_box = self.picture_box()

        display.add(date_box)
        display.attach_next_to(picture_box, date_box, Gtk.PositionType.RIGHT,3,1)

        return display

    def date_box(self):
        date_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        date_box.set_name("date-box")
        date_box.set_hexpand(True)
        date_box.set_vexpand(True)

        date_box.pack_start(CalendarBox(), False, False, 2)
        date_box.pack_end(ClockLabel(), False, False, 2)

        return date_box

    def picture_box(self):
        picture_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        picture_box.set_name("picture-box")
        picture_box.set_hexpand(True)
        picture_box.set_vexpand(True)

        return picture_box
