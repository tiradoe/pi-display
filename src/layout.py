import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


def build_header_bar(display, title):
    header_bar = Gtk.Box()
    header_bar.set_hexpand(True)
    header_bar_context = header_bar.get_style_context()
    header_bar_context.add_class("title-box")

    home_button = Gtk.Button.new_with_label("<-")
    home_button_context = home_button.get_style_context()
    home_button_context.add_class("home-button")
    home_button.connect("clicked", display.reset_view)

    app_label = Gtk.Label(title)
    app_label_context = app_label.get_style_context()
    app_label_context.add_class("header")

    header_bar.pack_start(home_button, False, False, 5)
    header_bar.pack_end(app_label, False, False, 5)

    return header_bar
