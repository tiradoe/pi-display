import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from mycroft_bus_client import MessageBusClient
from time import sleep


class MycroftView(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.set_name("mycroft-box")
        self.content_box = Gtk.Box()
        self.display_in_use = False

        self.build_default_view()
        self.pack_start(self.content_box, True, True, 1)

        self.client = MessageBusClient()
        self.client.run_in_thread()
        self.client.on("speak", self.handle_utterance)


    def build_default_view(self):
        view = Gtk.Label("Say \"Hey, Mycroft\" to activate Mycroft")
        self.content_box.pack_start(view, True, True, 1)


    def handle_utterance(self, message):
        # Ignore requests that come in while another
        # is displayed until a queue has been implemented
        if self.display_in_use == True:
            return

        skills = {
            "QuestionsAnswersSkill": self.handle_questions_and_answers_skill,
            "WeatherSkill": self.handle_questions_and_answers_skill,
            "JokingSkill": self.handle_joking_skill,
            "TimerSkill": self.handle_timer_skill,
        }

        if message.data["meta"]["skill"] in skills:
            main_window = self.get_toplevel().content_window
            if main_window.get_visible_child_name() != "mycroft_view":
                main_window.set_visible_child_name("mycroft_view")

            run_skill = skills[message.data["meta"]["skill"]]
            run_skill(message)
            self.reset_view()


    def handle_joking_skill(self, message):
        view = MycroftTextResponse(message)
        self.update_view(view)


    def handle_questions_and_answers_skill(self, message):
        view = MycroftTextResponse(message)
        self.update_view(view)


    def handle_timer_skill(self, message):
        view = MycroftTextResponse(message)
        self.update_view(view)


    def reset_view(self):
        sleep(15)
        self.display_in_use = False
        self.get_toplevel().content_window.set_visible_child_name("home_view")


    def update_view(self, new_view):
        self.display_in_use = True
        for child in self.content_box:
            self.content_box.remove(child)

        self.content_box.pack_start(new_view, True, True, 1)
        self.content_box.show_all()


class MycroftTextResponse(Gtk.Box):
    def __init__(self, message):
        Gtk.Box.__init__(self)
        self.utterance_label = Gtk.Label(message.data["utterance"])
        self.utterance_label.set_line_wrap(True)
        self.pack_start(self.utterance_label, True, True, 1)

