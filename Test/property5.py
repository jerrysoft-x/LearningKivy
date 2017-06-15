from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, ReferenceListProperty


class MyWidget(EventDispatcher):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)

mw = MyWidget()
print(mw.pos)
