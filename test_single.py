from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text='Test: Python files ARE included!', font_size=20)

TestApp().run()
