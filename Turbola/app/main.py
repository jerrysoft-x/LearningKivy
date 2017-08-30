from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import json
import kivy

from Turbola.app.taskitem import TaskItem, TaskList


class LabForm(StackLayout):
    def __init__(self, **kwargs):
        super(LabForm, self).__init__(**kwargs)

        self.font = self.getFont()
        self.newTask = StringProperty('')
        self.taskPopup = TaskPopup(self.font)

        self.newBtn = TaskBtn(rowid=0, text='New task', font_name=self.font, size_hint=(1, 0.1), background_color=[0, 153/255., 51/255., 1])
        self.add_widget(self.newBtn)
        self.newBtn.bind(on_release=self.task_btn_pressed)

        self.mainTaskList = TaskList(r'tasklist.json')
        self.mainTaskList.loadFromFile()
        self.taskPopup.setCurrentTaskList(self.mainTaskList)
        self.taskPopup.setForm(self)
        for rowid in self.mainTaskList.taskList:
            taskItem = self.mainTaskList.taskList[rowid]
            taskBtn = TaskBtn(rowid=taskItem.rowid ,text=taskItem.name, font_name=self.font, size_hint=(1, 0.1))
            taskBtn.bind(on_release=self.task_btn_pressed)
            self.add_widget(taskBtn)

    def getFont(self):
        ''' 在Android下面要用这个字体显示中文
        kivy.resources.resource_add_path(‘/system/fonts/’)  #指字字体路径
        p=kivy.resources.resource_find(‘DroidSansFallback.ttf’)    #指定字体
        '''
        kivy.resources.resource_add_path(r'C:\Windows\Fonts')  # 指字字体路径
        return kivy.resources.resource_find('msyhbd.ttf')  # 指定字体 微软雅黑粗体

    def task_btn_pressed(self, instance):
        # print ('instance', instance, 'have:', value)
        # print('Task button is pressed and its content is {content}'.format(content=instance.text))
        if instance.rowid == 0:
            self.taskPopup.setContent('')
        else:
            self.taskPopup.setContent(instance.text)
        self.taskPopup.setCurrentButton(instance)
        self.taskPopup.open()

class TaskBtn(Button):
    def __init__(self, rowid, **kwargs):
        super(TaskBtn, self).__init__(**kwargs)
        self.rowid = rowid

class TaskPopup(Popup):
    def __init__(self, font, **kwargs):
        super(TaskPopup, self).__init__(**kwargs)

        # Initialize the popup window
        self.title = 'Update task content'
        self.title_font = font
        self.size_hint = (None, None)
        self.size = (256, 256)
        self.disabled = False

        self.font = font

        # Setup popup window's layout
        self.content = GridLayout(cols=1)

        self.content_text_input = TextInput(font_name=font)
        self.content.add_widget(self.content_text_input)

        # Button area
        self.button_area = GridLayout(rows=1, size_hint_y=None, height=40)
        self.content.add_widget(self.button_area)
        self.save_btn = Button(text='Save')
        self.button_area.add_widget(self.save_btn)
        self.save_btn.bind(on_release=self.on_save_callback)
        self.cancel_btn = Button(text='Cancel')
        self.button_area.add_widget(self.cancel_btn)
        self.cancel_btn.bind(on_release=self.on_cancel_callback)

        # Set the focus to the textinput when popup window is open,
        # setting the focus during textinput initialization will disable keyboard input by test.
        self.bind(on_open=self.on_open_callback)

        # Need to remember the instance of button
        self.currentButton = None

        # Need to have a reference to the task list
        self.currentTaskList = None

        self.form = None

    def on_open_callback(self, instance):
        self.content_text_input.focus = True

    def on_save_callback(self, instance):
        if self.currentButton.rowid == 0:
            if self.getContent() != '':
                newRowId = self.currentTaskList.generateRowID()
                taskItem = TaskItem(newRowId, self.getContent())
                self.currentTaskList.taskList[newRowId] = taskItem
                self.currentTaskList.flushToFile()
                taskBtn = TaskBtn(rowid=taskItem.rowid, text=taskItem.name, font_name=self.font, size_hint=(1, 0.1))
                taskBtn.bind(on_release=self.form.task_btn_pressed)
                self.form.add_widget(taskBtn)
        else:
            if self.currentButton.text != self.getContent():
                self.currentButton.text = self.getContent()
                self.currentTaskList.taskList[self.currentButton.rowid].name = self.getContent()
                self.currentTaskList.flushToFile()
        self.dismiss()

    def on_cancel_callback(self, instance):
        self.dismiss()

    def setContent(self, text):
        self.content_text_input.text = text

    def getContent(self):
        return self.content_text_input.text

    def setCurrentButton(self, btn):
        self.currentButton = btn

    def setCurrentTaskList(self, taskList):
        self.currentTaskList = taskList

    def setForm(self, form):
        self.form = form

class TurbolaApp(App):
    def build(self):
        return LabForm()


if __name__ == '__main__':
    TurbolaApp().run()
