from kivy.event import EventDispatcher
from kivy.properties import StringProperty


class MyClass(EventDispatcher):
    my_string = StringProperty('default')

    def __init__(self, **kwargs):
        super(MyClass, self).__init__(**kwargs)

print(MyClass(my_string='value').my_string)