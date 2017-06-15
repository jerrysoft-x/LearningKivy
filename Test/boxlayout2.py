from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyApp(App):

    def build(self):
        layout = BoxLayout(spacing=10)
        btn1 = Button(text='Hello', size_hint=(.7, 1))
        btn2 = Button(text='World', size_hint=(.3, 1))
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        return layout

if __name__ == '__main__':
    MyApp().run()
