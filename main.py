from fractions import Fraction
import random
import os.path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import urllib.request
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

class API(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_components = parse_qs(parsed_path.query)
        path = parsed_path.path

        if path == "/api/rankcard":
            self.handle_rankcard(query_components)
        elif path == "/api/ejected":
            self.handle_amongus(query_components)
        else:
            self.send_error(404, "Page not found, check API documentation")
    def handle_rankcard(self, query_components):
        background = Image.open("backgrounds/Background-Rankcard.png")
        draw = ImageDraw.Draw(background)
        for key, values in query_components.items():
            if key == "username":
                username = values[0]
            elif key == "avatar":
                if "gif" in values[0]:
                    os.system(f"curl {values[0]} -o avatar.gif")
                else:
                    os.system(f"curl {values[0]} -o avatar.png")
            elif key == "currentxp":
                currentxp = int(values[0])
            elif key == "nextlevelxp":
                nextlevelxp = int(values[0])
            elif key == "level":
                level = int(values[0])
        if nextlevelxp and currentxp:
            xpfrac = Fraction(currentxp, nextlevelxp)
        font = ImageFont.truetype("fonts/Roboto-BoldItalic.ttf", 40)
        try:
            x = 10
            y = 150
            progress = 0
            color_progressbar = (225, 225, 225)
            height = 30
            width = 5.5
            if username:
              draw.text((10, 10), username, font=font)
            if xpfrac:
              progress = xpfrac * 100
        except:
            pass
        draw.rectangle(
                (x + (height / 2), y, x + width + (height / 2), y + height),
                fill = color_progressbar,
                width=10,
        )
        draw.ellipse(
                (x + width, y, x + height + width, y + height),
                fill = color_progressbar,
                width=10,
        )
        draw.ellipse(
                (x, y, x + height, y + height),
                fill = color_progressbar,
        )
        width = int(width * progress)
        draw.rectangle(
                (x + (height / 2), y, x + width + (height / 2), y + height),
                fill = color_progressbar,
                width=10,
        )
        draw.ellipse(
                (x + width, y, x + height + width, y + height),
                fill = color_progressbar,
        )
        draw.ellipse(
                (x, y, x + height, y + height),
                fill = color_progressbar,
        )
        if os.path.isfile("avatar.png"):
            avatar = Image.open("avatar.png").convert("RGBA")
            avatar = avatar.resize((120, 120))
            background.paste(
                    avatar,
                    (450, 20),
                    avatar,
                    )
        elif os.path.isfile("avatar.gif"):
            avatar = Image.open("avatar.gif").convert("RGBA")
            avatar = avatar.resize((120, 120))
            background.paste(
                    avatar,
                    (450, 20),
                    avatar,
                    )
        try:
            font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 20)
            if level: 
                draw.text(
                        (30, 75),
                        f"Level {level}",
                        font = font,
                        align = "left",
                        )
            else:
                draw.text(
                        (30, 75),
                        "Level 0",
                        font = font,
                        align = "left",
                        )
        except: 
            font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 20)
            draw.text(
                    (30, 75),
                    "Level 0",
                    font = font,
                    align = "left",
                    )
            pass
        try:
            font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 20)
            if nextlevelxp and currentxp:
                draw.text(
                        (30, 100),
                        f"{currentxp}/{nextlevelxp} XP",
                        font = font,
                        align = "left"
                        )
        except:
            pass
        buffer = BytesIO()
        background.save(buffer, format="PNG")
        buffer.seek(0)

        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()

        self.wfile.write(buffer.read())
        try:
            os.remove("avatar.gif")
        except:
            pass
        try:
            os.remove("avatar.png")
        except:
            pass
    def handle_amongus(self, query_components):
        background = Image.open("backgrounds/Background-Amongus.png")
        draw = ImageDraw.Draw(background)
        for key, values in query_components.items():
            if key == "impostor":
                if values[0] == "true":
                    impostor = True
                else:
                    impostor = False
            elif key == "name":
                name = values[0]
            elif key == "crewmate":
                crewmate = values[0]
        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 30)
        x = 300
        y = background.height / 2
        try:
            if crewmate:
                crewmateimg = Image.open(f"impostors/{crewmate}.png").convert("RGBA")
                crewmateimg = crewmateimg.resize((100,100))
                crewmateimg = crewmateimg.rotate(
                        random.randint(1, 361)
                )
                random_x = random.randint(1, 500)
                random_y = random.randint(1, 300)
                background.paste(
                        crewmateimg,
                        (random_x, random_y),
                        crewmateimg,
                        )
        except Exception as e:
            pass
        try:
            if impostor:
                try:
                    draw.text(
                            (x, y),
                            f"{name} is the impostor.",
                            font = font,
                            )
                except:
                    pass
            else:
                draw.text(
                        (x, y),
                        f"{name} is not the impostor.",
                        font = font,
                        )
        except:
            try:
                draw.text(
                        (x, y),
                        f"{name} is not the impostor.",
                        font = font,
                        )
            except:
                draw.test(
                        (x, y),
                        f"User is not the impostor.",
                        font = font,
                        )
                pass
        buffer = BytesIO()
        background.save(buffer, format="PNG")
        buffer.seek(0)

        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()

        self.wfile.write(buffer.read())

def run(server_class=HTTPServer, handler_class=API, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Visit localhost:{port}, check the API documentation")
    httpd.serve_forever()
run()
