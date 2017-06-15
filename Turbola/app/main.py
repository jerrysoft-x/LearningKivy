from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
import json

from Turbola.app.taskitem import TaskItem


class LabForm(StackLayout):
    def __init__(self, **kwargs):
        super(LabForm, self).__init__(**kwargs)

        with open(r'tasklist.json', 'r') as f:
            for task in f.readlines():
                taskitem = json.loads(task, object_hook=TaskItem.dict2taskitem)
                self.add_widget(Button(text=taskitem.name, size_hint=(1, 0.08)))


class TurbolaApp(App):
    def build(self):
        return LabForm()


if __name__ == '__main__':
    TurbolaApp().run()
