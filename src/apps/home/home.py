import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from .widgets.clock import ClockLabel
from .widgets.calendar import CalendarBox

class HomeView(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.row_name = "Home"
        self.date_box = self.build_date_box()
        self.picture_box = self.build_picture_box()

        self.add(self.date_box)
        self.attach_next_to(self.picture_box, self.date_box, Gtk.PositionType.RIGHT,3,1)


    def build_date_box(self):
        date_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        date_box.set_name("date-box")
        date_box.set_hexpand(True)
        date_box.set_vexpand(True)

        date_box.pack_start(CalendarBox(), False, False, 2)
        date_box.pack_end(ClockLabel(), False, False, 2)

        return date_box

    def build_picture_box(self):
        picture_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        picture_box.set_name("picture-box")
        picture_box.set_hexpand(True)
        picture_box.set_vexpand(True)

        return picture_box
