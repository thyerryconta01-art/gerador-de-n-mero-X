import json
import os
import secrets
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty


DATA_FILE = "random_core_x.json"


KV = """
ScreenManager:
    HomeScreen:
    DrawScreen:
    HistoryScreen:
    StatsScreen:
    SettingsScreen:

<HomeScreen>:
    name: "home"

    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "15dp"

        Label:
            text: "RANDOM CORE X"
            font_size: "30sp"
            bold: True
            size_hint_y: None
            height: "60dp"

        Label:
            text: "ADVANCED RANDOM SYSTEM"
            font_size: "14sp"
            size_hint_y: None
            height: "35dp"

        Button:
            text: "🎲 NOVO SORTEIO"
            font_size: "20sp"
            on_release: app.root.current = "draw"

        Button:
            text: "📜 HISTÓRICO"
            font_size: "20sp"
            on_release: app.root.current = "history"

        Button:
            text: "📊 ESTATÍSTICAS"
            font_size: "20sp"
            on_release: app.root.current = "stats"

        Button:
            text: "⚙️ CONFIGURAÇÕES"
            font_size: "20sp"
            on_release: app.root.current = "settings"

        Widget:

        Label:
            text: "RANDOM CORE X • MOBILE"
            size_hint_y: None
            height: "30dp"


<DrawScreen>:
    name: "draw"

    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "12dp"

        Label:
            text: "🎲 NOVO SORTEIO"
            font_size: "26sp"
            bold: True
            size_hint_y: None
            height: "50dp"

        TextInput:
            id: minimum
            hint_text: "Número mínimo"
            text: "1"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: "50dp"

        TextInput:
            id: maximum
            hint_text: "Número máximo"
            text: "100"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: "50dp"

        TextInput:
            id: quantity
            hint_text: "Quantidade"
            text: "1"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: "50dp"

        Button:
            text: "🎯 SORTEAR"
            font_size: "20sp"
            size_hint_y: None
            height: "55dp"
            on_release: app.draw_numbers()

        Label:
            id: result
            text: "Aguardando sorteio..."
            font_size: "26sp"
            bold: True
            text_size: self.width, None

        Widget:

        Button:
            text: "⬅ VOLTAR"
            size_hint_y: None
            height: "50dp"
            on_release: app.root.current = "home"


<HistoryScreen>:
    name: "history"

    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "10dp"

        Label:
            text: "📜 HISTÓRICO"
            font_size: "26sp"
            bold: True
            size_hint_y: None
            height: "50dp"

        ScrollView:
            Label:
                id: history_text
                text: app.get_history()
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
                font_size: "16sp"

        Button:
            text: "🗑 LIMPAR HISTÓRICO"
            size_hint_y: None
            height: "50dp"
            on_release: app.clear_history()

        Button:
            text: "⬅ VOLTAR"
            size_hint_y: None
            height: "50dp"
            on_release: app.root.current = "home"


<StatsScreen>:
    name: "stats"

    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "15dp"

        Label:
            text: "📊 ESTATÍSTICAS"
            font_size: "26sp"
            bold: True
            size_hint_y: None
            height: "60dp"

        Label:
            id: stats
            text: app.get_stats()
            font_size: "19sp"

        Widget:

        Button:
            text: "⬅ VOLTAR"
            size_hint_y: None
            height: "50dp"
            on_release: app.root.current = "home"


<SettingsScreen>:
    name: "settings"

    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "15dp"

        Label:
            text: "⚙️ CONFIGURAÇÕES"
            font_size: "26sp"
            bold: True
            size_hint_y: None
            height: "60dp"

        Label:
            text: "Random Core X\\n\\nGerador de números aleatórios\\ncom histórico e estatísticas.\\n\\nFonte de aleatoriedade: secrets"
            font_size: "18sp"

        Widget:

        Button:
            text: "⬅ VOLTAR"
            size_hint_y: None
            height: "50dp"
            on_release: app.root.current = "home"
"""


class HomeScreen(Screen):
    pass


class DrawScreen(Screen):
    pass


class HistoryScreen(Screen):
    pass


class StatsScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class RandomCoreX(App):

    def build(self):
        self.data = self.load_data()
        return Builder.load_string(KV)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        return {
            "draws": [],
            "total_numbers": 0
        }

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def draw_numbers(self):
        screen = self.root.get_screen("draw")

        try:
            minimum = int(screen.ids.minimum.text)
            maximum = int(screen.ids.maximum.text)
            quantity = int(screen.ids.quantity.text)

            if minimum > maximum:
                raise ValueError

            total = maximum - minimum + 1

            if quantity < 1 or quantity > total:
                raise ValueError

            numbers = secrets.SystemRandom().sample(
                range(minimum, maximum + 1),
                quantity
            )

            numbers.sort()

            result = "  •  ".join(str(n) for n in numbers)

            screen.ids.result.text = result

            self.data["draws"].append({
                "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "numbers": numbers,
                "range": [minimum, maximum]
            })

            self.data["total_numbers"] += quantity

            self.save_data()

        except Exception:
            screen.ids.result.text = "⚠️ VALORES INVÁLIDOS"

    def get_history(self):
        if not self.data["draws"]:
            return "Nenhum sorteio realizado ainda."

        lines = []

        for item in reversed(self.data["draws"]):
            numbers = ", ".join(map(str, item["numbers"]))
            lines.append(
                f"{item['date']}\\n"
                f"→ {numbers}\\n"
            )

        return "\\n".join(lines)

    def get_stats(self):
        draws = len(self.data["draws"])
        numbers = self.data["total_numbers"]

        return (
            f"Sorteios realizados: {draws}\\n\\n"
            f"Números gerados: {numbers}\\n\\n"
            f"Histórico salvo automaticamente."
        )

    def clear_history(self):
        self.data = {
            "draws": [],
            "total_numbers": 0
        }

        self.save_data()

        self.root.get_screen("history").ids.history_text.text = (
            "Histórico limpo."
        )

    def on_start(self):
        pass


if __name__ == "__main__":
    RandomCoreX().run()
