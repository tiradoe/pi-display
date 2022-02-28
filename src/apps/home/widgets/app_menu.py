import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class AppMenu(Gtk.ScrolledWindow):
    def __init__(self, parent, main_window):
        super().__init__()
        self.parent = parent
        self.main_window = main_window
        self.apps = {
            "Snapcast": "snapcast_view",
            "Lights": "hue_view",
            "Mycroft": "mycroft_view"
        }

        self.app_grid = self.build_grid()
        self.add(self.app_grid)

    def build_grid(self):
        app_grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        app_grid.set_hexpand(True)
        app_grid_context = app_grid.get_style_context()
        app_grid_context.add_class("main-menu")

        home_app_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        home_app_box.set_hexpand(True)
        home_app_box_context = home_app_box.get_style_context()
        home_app_box_context.add_class("app-box")

        home_app_button = Gtk.Button.new_with_label("Home")
        home_app_button_context = home_app_button.get_style_context()
        home_app_button_context.add_class("menu-button")
        home_app_button.connect('clicked', self.reset_home_view)

        home_app_box.pack_start(home_app_button, False, False, 0)

        app_grid.add(home_app_box)

        for name, app in self.apps.items():
            app_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            app_box_context = app_box.get_style_context()
            app_box_context.add_class("app-box")

            app_button = Gtk.Button.new_with_label(name)
            app_button_context = app_button.get_style_context()
            app_button_context.add_class("menu-button")
            app_button.connect('clicked', self.update_view, app)

            app_box.pack_start(app_button, False, False, 0)

            app_grid.add(app_box)

        return app_grid

    def update_view(self, button, view):
        self.main_window.emit("update_view", view)
        self.reset_home_view()

    def reset_home_view(self, button=None):
        self.parent.date_stack.set_visible_child_name("date_box")
