from flask import Flask
import yaml

class Web:
    def __init__(self, name):
        self.app = Flask(name)

    def route(self, path):
        return self.app.route(path)

    def run(self):
        self.app.run(debug=True)


class UI:
    @staticmethod
    def load_ted(name):
        with open(f"{name}.ted", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f.read())

        root = data.get("</>")
        html = ""

        for widget_name, props in root.items():
            if widget_name == "Label":
                html += Label(props).render()

        return f"""
        <html>
        <body style="position:relative;">
            {html}
        </body>
        </html>
        """


class Label:
    def __init__(self, props):
        self.text = props.get("text", "")
        pos = props.get("pos", {})
        size = props.get("size", {})

        self.x = pos.get("x", 0)
        self.y = pos.get("y", 0)
        self.w = size.get("x", 100)
        self.h = size.get("y", 30)

    def render(self):
        return f"""
        <div style="
            position:absolute;
            left:{self.x}px;
            top:{self.y}px;
            width:{self.w}px;
            height:{self.h}px;
        ">
            {self.text}
        </div>
        """