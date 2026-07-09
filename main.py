import random
import colorsys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp

sensors = {}
next_id = 0


def color_for_index(index):
    hue = (index * 0.6180339887498949) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.75, 1.0)
    return (r, g, b, 1)


class SensorCard(BoxLayout):
    def __init__(self, sid, on_remove, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, height=dp(120),
                          padding=dp(8), spacing=dp(2), **kwargs)
        self.sid = sid
        s = sensors[sid]

        with self.canvas.before:
            Color(*s["color"], 0.15)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.name_label = Label(text=s["name"], bold=True, color=s["color"], size_hint_y=None, height=dp(24))
        self.hr_label = Label(text="---", font_size=dp(32), bold=True, size_hint_y=None, height=dp(40))
        self.status_label = Label(text="Демо-режим", font_size=dp(12), size_hint_y=None, height=dp(20))
        self.battery_label = Label(text="", font_size=dp(12), size_hint_y=None, height=dp(20))

        remove_btn = Button(text="Удалить", size_hint_y=None, height=dp(30))
        remove_btn.bind(on_release=lambda *_: on_remove(sid))

        self.add_widget(self.name_label)
        self.add_widget(self.hr_label)
        self.add_widget(self.battery_label)
        self.add_widget(self.status_label)
        self.add_widget(remove_btn)

    def _update_bg(self, *_):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def refresh(self):
        s = sensors.get(self.sid)
        if not s:
            return
        self.hr_label.text = str(s["hr"])
        self.battery_label.text = f"Заряд: {s['battery']}%"


class AddSensorPopup(Popup):
    def __init__(self, on_confirm, **kwargs):
        super().__init__(title="Добавить демо-датчик", size_hint=(0.85, 0.4), **kwargs)
        layout = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        self.name_input = TextInput(hint_text="Имя датчика", multiline=False, size_hint_y=None, height=dp(40))
        confirm_btn = Button(text="Добавить", size_hint_y=None, height=dp(44))
        confirm_btn.bind(on_release=lambda *_: self._confirm(on_confirm))
        layout.add_widget(self.name_input)
        layout.add_widget(confirm_btn)
        self.content = layout

    def _confirm(self, on_confirm):
        name = self.name_input.text.strip() or "Датчик"
        on_confirm(name)
        self.dismiss()


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.cards = {}

        header = BoxLayout(size_hint_y=None, height=dp(48), padding=dp(8), spacing=dp(8))
        title = Label(text="XOSS Heart Monitor (demo)", bold=True)
        add_btn = Button(text="+ Датчик", size_hint_x=None, width=dp(110))
        add_btn.bind(on_release=self.open_add_popup)
        header.add_widget(title)
        header.add_widget(add_btn)
        self.add_widget(header)

        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(8), padding=dp(8))
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

        self.empty_label = Label(text="Нет датчиков. Нажми '+ Датчик'.")
        self.grid.add_widget(self.empty_label)

        Clock.schedule_interval(self.tick, 1.0)

    def open_add_popup(self, *_):
        AddSensorPopup(on_confirm=self.add_sensor).open()

    def add_sensor(self, name):
        global next_id
        sid = next_id
        next_id += 1
        sensors[sid] = {
            "id": sid,
            "name": name,
            "hr": 70,
            "battery": 100,
            "color": color_for_index(sid),
        }
        if self.empty_label.parent:
            self.grid.remove_widget(self.empty_label)
        card = SensorCard(sid, self.remove_sensor)
        self.cards[sid] = card
        self.grid.add_widget(card)

    def remove_sensor(self, sid):
        if sid in self.cards:
            self.grid.remove_widget(self.cards.pop(sid))
        sensors.pop(sid, None)
        if not sensors:
            self.grid.add_widget(self.empty_label)

    def tick(self, *_):
        for sid, s in sensors.items():
            s["hr"] = max(50, min(180, s["hr"] + random.randint(-4, 4)))
            s["battery"] = max(0, s["battery"] - random.choice([0, 0, 0, 1]))
            if sid in self.cards:
                self.cards[sid].refresh()


class XossHeartMonitorApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    XossHeartMonitorApp().run()
