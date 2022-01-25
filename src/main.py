#!/usr/env/python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from apps.home import HomeView
from apps.snapcontrol import SnapControlView
from apps.mycroft import MycroftView
from dotenv import dotenv_values

class AppWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="RPi Display")
        self.config = dotenv_values(".env")

        if "ENVIRONMENT" in self.config and self.config["ENVIRONMENT"] == "dev":
            self.set_size_request(800,480)
        else:
            self.fullscreen()

        main_box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                )
        main_box.set_name('main-box')

        self.content_window = self.build_content_window()
        self.content_window.add_titled(HomeView(), "home_view", "Home")
        self.content_window.add_titled(SnapControlView(), "snapcontrol_view", "Snapcast")
        self.content_window.add_titled(MycroftView(), "mycroft_view", "Mycroft")

        switcher = Gtk.StackSwitcher(can_focus=False)
        switcher.set_name("menu")
        switcher.set_stack(self.content_window)

        main_box.pack_start(self.content_window, True, True, 0)
        main_box.pack_end(switcher, False, False, 0)

        self.load_css()
        self.add(main_box)


    def build_content_window(self):
        content_box = Gtk.Stack()

        content_box.set_transition_type(Gtk.StackTransitionType.OVER_UP)
        content_box.set_transition_duration(500)

        return content_box


    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)


window = AppWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
