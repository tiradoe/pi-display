import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from .widgets.clock import ClockLabel
from .widgets.calendar import CalendarBox
from .widgets.app_menu import AppMenu


class HomeView(Gtk.Grid):
    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent
        self.row_name = "Home"
        self.date_stack = self.build_date_box()
        self.date_stack.set_transition_type(Gtk.StackTransitionType.OVER_UP)
        self.picture_box = self.build_picture_box()

        self.add(self.date_stack)
        self.attach_next_to(self.picture_box, self.date_stack, Gtk.PositionType.RIGHT, 3, 1)

    def build_date_box(self):
        date_stack = Gtk.Stack()
        date_stack.set_name("main_menu")

        date_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        date_box.set_name("date-box")
        date_box.set_hexpand(True)
        date_box.set_vexpand(True)

        menu_button = Gtk.Button.new_with_label("Menu")
        menu_button.set_name("menu-button")
        menu_button.connect("clicked", self.toggle_menu)

        date_box.pack_start(CalendarBox(), False, False, 2)
        date_box.pack_start(ClockLabel(), False, False, 2)
        date_box.pack_end(menu_button, False, False, 2)

        main_menu = AppMenu(self, self.parent)
        date_stack.add_titled(date_box, "date_box", "Date")
        date_stack.add_titled(main_menu, "main_menu", "Menu")

        return date_stack

    def build_picture_box(self):
        picture_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        picture_box.set_name("picture-box")
        picture_box.set_hexpand(True)
        picture_box.set_vexpand(True)

        return picture_box

    def toggle_menu(self, button):
        self.date_stack.set_visible_child_name('main_menu')
