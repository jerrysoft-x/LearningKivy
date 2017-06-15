from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button


class MyApp(App):

    def build(self):
        layout = AnchorLayout(anchor_x='right', anchor_y='bottom')
        btn1 = Button(text='Button 1', size_hint=(0.1, 0.1))
        layout.add_widget(btn1)
        btn2 = Button(text='Button 2', size_hint=(0.1, 0.3))
        layout.add_widget(btn2)
        return layout

if __name__ == '__main__':
    MyApp().run()
