#!/usr/env/python
import gi
from dotenv import dotenv_values

from apps.home import HomeView
from apps.huecontrol import HueView
from apps.mycroft import MycroftView
from apps.snapcast import SnapCastView
from layout import build_header_bar

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject


class AppWindow(Gtk.Window):
    __gsignals__ = {
        'update_view': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        super().__init__(title="RPi Display")
        self.config = dotenv_values(".env")
        self.connect("update_view", self.on_update_view)

        if "ENVIRONMENT" in self.config and self.config["ENVIRONMENT"] == "dev":
            self.set_size_request(800, 480)
        else:
            self.fullscreen()

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )
        main_box.set_name('main-box')

        self.content_window = self.build_content_window()
        self.content_window.add_titled(HomeView(self), "home_view", "Home")
        self.content_window.add_titled(SnapCastView(self, build_header_bar), "snapcast_view", "Snapcast")
        self.content_window.add_titled(HueView(self, build_header_bar), "hue_view", "Lights")
        self.content_window.add_titled(MycroftView(self, build_header_bar), "mycroft_view", "Mycroft")

        main_box.pack_start(self.content_window, True, True, 0)

        self.load_css()
        self.add(main_box)

    def build_content_window(self):
        content_box = Gtk.Stack()

        content_box.set_transition_type(Gtk.StackTransitionType.OVER_UP)
        content_box.set_transition_duration(500)

        return content_box

    def on_update_view(self, old_view, new_view):
        self.content_window.set_visible_child_name(new_view)

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
