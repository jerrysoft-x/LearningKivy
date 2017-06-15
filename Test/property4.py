from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class MyObject(Widget):

    hello = ObjectProperty(None, allownone=True)

# then later
a = MyObject()
a.hello = 'bleh' # working
a.hello = None # working too, because allownone is True.