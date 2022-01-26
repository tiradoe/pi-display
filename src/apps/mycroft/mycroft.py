import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from mycroft_bus_client import MessageBusClient
from time import sleep
from .responses.text_response import MycroftTextResponse


class MycroftView(Gtk.ScrolledWindow):
    def __init__(self, parent):
        Gtk.ScrolledWindow.__init__(self, Gtk.Adjustment(0,0,0,0,0,0))
        self.display_in_use = False
        self.parent = parent
        self.stack = Gtk.Stack()
        self.stack.set_name("mycroft-stack")

        self.default_message = {"text":"Say \"Hey, Mycroft\" to activate Mycroft" }
        self.text_response = MycroftTextResponse(self.default_message)

        self.build_stack()
        self.add(self.stack)

        self.client = MessageBusClient()
        self.client.run_in_thread()
        self.client.on("speak", self.handle_utterance)


    def build_stack(self):
        self.stack.add_titled(self.text_response, "text_response", "Text")


    def handle_utterance(self, message):
        # Ignore requests that come in while another
        # is displayed until a queue has been implemented
        if self.display_in_use == True:
            return

        self.handle_text_response(message)
        self.reset_view()


    def handle_text_response(self, message):
        self.text_response.set_label(message)
        self.update_view("text_response")


    def reset_view(self):
        self.display_in_use = False
        self.text_response.set_label(self.default_message)
        self.parent.emit("update_view", "home_view")


    def update_view(self, new_view):
        self.display_in_use = True
        self.stack.set_visible_child_name(new_view)
        self.parent.emit("update_view", "mycroft_view")
        sleep(15)

