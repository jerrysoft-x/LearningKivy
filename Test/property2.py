from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class MyClass(EventDispatcher):
    a = NumericProperty(1)


def callback(instance, value):
    print('My callback is call from', instance)
    print('and the a value changed to', value)

ins = MyClass()
ins.bind(a=callback)

# At this point, any change to the a property will call your callback.
ins.a = 5    # callback called
ins.a = 5    # callback not called, because the value did not change
ins.a = -1   # callback called