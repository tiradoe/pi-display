import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class MycroftTextResponse(Gtk.Box):
    def __init__(self, message):
        Gtk.Box.__init__(self)

        self.utterance_label = Gtk.Label()
        self.set_label(message)
        self.pack_start(self.utterance_label, True, True, 1)


    def set_label(self, message):
        try:
            self.utterance_label.set_text(message.data["utterance"])
        except:
            self.utterance_label.set_text(message["text"])

        self.utterance_label.set_line_wrap(True)
        self.utterance_label.set_max_width_chars(50)
