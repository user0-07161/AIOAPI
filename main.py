from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import urllib.request
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os.path
from fractions import Fraction
import random


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
            self.send_error(404, "Page not found")

    def handle_rankcard(self, query_components):
        img = Image.open("backgrounds/Background-Rankcard.png")
        draw = ImageDraw.Draw(img)
        for key, values in query_components.items():
            if key == "username":
                print(f"{key} is {values[0]}")
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
            # Creating fraction
            xpfrac = Fraction(currentxp, nextlevelxp)

        font = ImageFont.truetype("fonts/Roboto-BoldItalic.ttf", 40)
        x = 10
        y = 150
        progress = 50
        bg = (129, 66, 97)
        fg = (211, 211, 211)
        fg2 = (15, 15, 15)
        height = 30
        width = 5.5
        if username:
            draw.text((10, 10), username, font=font)
        if xpfrac:
            progress = xpfrac * 100
            draw.rectangle(
                (x + (height / 2), y, x + width + (height / 2), y + height),
                fill=fg2,
                width=10,
            )
            draw.ellipse((x + width, y, x + height + width, y + height), fill=fg2)
            draw.ellipse((x, y, x + height, y + height), fill=fg2)
            width = int(width * progress)
            draw.rectangle(
                (x + (height / 2), y, x + width + (height / 2), y + height),
                fill=fg,
                width=10,
            )
            draw.ellipse((x + width, y, x + height + width, y + height), fill=fg)
            draw.ellipse((x, y, x + height, y + height), fill=fg)
        if os.path.isfile("avatar.png"):
            avatar = Image.open("avatar.png").convert("RGBA")
            avt2 = avatar.resize((120, 120))
            img_w, img_h = avt2.size
            bg_w, bg_h = img.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            img.paste(avt2, (450, 20), avt2)
        elif os.path.isfile("avatar.gif"):
            avatar = Image.open("avatar.gif").convert("RGBA")
            avt2 = avatar.resize((120, 120))
            img_w, img_h = avt2.size
            bg_w, bg_h = img.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            img.paste(avt2, (450, 20), avt2)
        else:
            pass
        try:
            if level:
                font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 20)
                draw.text((30, 75), f"Level {level}", font=font, align="left")
            else:
                font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 20)
                draw.text((30, 75), f"Level 0", font=font, align="left")
        except:
            font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 20)
            draw.text((30, 75), f"Level 0", font=font, align="left")
            pass
        try:
            if nextlevelxp and currentxp:
                draw.text(
                    (30, 100), f"{currentxp}/{nextlevelxp} XP", font=font, align="left"
                )
        except:
            pass
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()

        self.wfile.write(buffer.read())
        try:
            os.remove("avatar.gif")
        except OSError:
            pass
        try:
            os.remove("avatar.png")
        except OSError:
            pass

    def handle_amongus(self, query_components):
        img = Image.open("backgrounds/Background-Amongus.png")
        draw = ImageDraw.Draw(img)
        for key, values in query_components.items():
            if key == "impostor":
                if values[0] == "true":
                    impostor = True
                elif values[0] == "false":
                    impostor = False
                else:
                    impostor = False
            elif key == "name":
                name = values[0]
            elif key == "crewmate":
                crewmate = values[0]
                print("blah")

        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 30)
        x = 300
        y = img.height / 2
        try:
            if crewmate:

                crewmateimg = Image.open(f"impostors/{crewmate}.png")
                print(f"Crewmate: impostors/{crewmate}.png")
                crewmateimg.thumbnail((100, 100))
                rotatedcrewmateimg = crewmateimg.rotate(random.randint(1, 361)).convert(
                    "RGBA"
                )
                randomx = random.randint(1, 1000)
                randomy = random.randint(1, 768)
                img.paste(rotatedcrewmateimg, (randomx, randomy), rotatedcrewmateimg)
        except Exception as e:
            print(e)
            pass
        try:
            if impostor:
                try:
                    if name:
                        draw.text((x, y), f"{name} is the impostor.", font=font)
                except:
                    pass
            else:
                draw.text((x, y), f"{name} is not the impostor.", font=font)
        except:
            draw.text((x, y), f"{name} is not the impostor.", font=font)
            pass
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()

        self.wfile.write(buffer.read())


def run(server_class=HTTPServer, handler_class=API, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Visit localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
