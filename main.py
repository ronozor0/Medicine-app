import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

# Dark background
Window.clearcolor = (0.08, 0.1, 0.13, 1)

class StyledButton(Button):
    def __init__(self, bg_color=(0.15, 0.45, 0.85, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bold = True
        self.font_size = '16sp'
        self.color = (1, 1, 1, 1)
        self.bg_color = bg_color
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(55)
        self.font_size = '16sp'
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0.16, 0.20, 0.26, 1)
        self.foreground_color = (1, 1, 1, 1)
        self.hint_text_color = (0.6, 0.65, 0.7, 1)
        self.cursor_color = (0, 0.8, 1, 1)
        self.padding = [dp(15), dp(15), dp(15), dp(15)]

class MedicineApp(App):
    def build(self):
        self.init_db()
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Title
        header = Label(
            text="[b]Medicine Manager[/b] [color=00d1b2](IQD)[/color]",
            markup=True,
            font_size='22sp',
            size_hint_y=None,
            height=dp(45),
            halign='center',
            valign='middle'
        )
        header.bind(size=header.setter('text_size'))
        main_layout.add_widget(header)

        # Inputs
        self.name_input = CustomTextInput(hint_text="Medicine Name")
        self.price_input = CustomTextInput(hint_text="Price in IQD", input_filter='int')

        main_layout.add_widget(self.name_input)
        main_layout.add_widget(self.price_input)

        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(12))
        search_btn = StyledButton(text="Search", bg_color=(0.15, 0.45, 0.85, 1), on_press=self.search_medicine)
        add_btn = StyledButton(text="Save / Update", bg_color=(0.0, 0.7, 0.45, 1), on_press=self.add_medicine)
        
        btn_layout.add_widget(search_btn)
        btn_layout.add_widget(add_btn)
        main_layout.add_widget(btn_layout)

        # Results area
        self.result_label = Label(
            text="[color=7f8c8d]Search results or status messages will appear here.[/color]",
            markup=True,
            size_hint_y=None,
            font_size='16sp',
            line_height=1.3,
            halign='left',
            valign='top'
        )
        self.result_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.result_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))

        scroll = ScrollView(bar_width=dp(4))
        scroll.add_widget(self.result_label)
        main_layout.add_widget(scroll)

        return main_layout

    def init_db(self):
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                price INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def search_medicine(self, instance):
        query = self.name_input.text.strip()
        if not query:
            self.result_label.text = "[color=e74c3c]Please enter a medicine name to search.[/color]"
            return

        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM inventory WHERE name LIKE ?", (f"%{query}%",))
        results = cursor.fetchall()
        conn.close()

        if results:
            text = "[b][color=00d1b2]Search Results:[/color][/b]\n\n"
            for name, price in results:
                text += f"[color=ffffff]• [b]{name.capitalize()}[/b]:[/color] [color=2ecc71]{price:,} IQD[/color]\n\n"
            self.result_label.text = text
        else:
            self.result_label.text = f"[color=e67e22]No matching medicines found for '[b]{query}[/b]'.[/color]"

    def add_medicine(self, instance):
        name = self.name_input.text.strip().lower()
        price_text = self.price_input.text.strip()

        if not name or not price_text:
            self.result_label.text = "[color=e74c3c]Please fill in both Name and Price to save.[/color]"
            return

        price = int(price_text)
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (name, price) VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET price = excluded.price
        ''', (name, price))
        conn.commit()
        conn.close()

        self.result_label.text = f"[color=2ecc71]✔ Saved Successfully:[/color]\n[b]{name.capitalize()}[/b] -> {price:,} IQD"
        self.name_input.text = ""
        self.price_input.text = ""

if __name__ == "__main__":
    MedicineApp().run()
