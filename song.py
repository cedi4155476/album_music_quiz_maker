import eyed3
import cv2
import numpy as np
import win32api

from random import randint
from io import BytesIO
from pydub import AudioSegment
from PIL import Image, ImageFont, ImageDraw

from config import quiz_configurations, file_configurations

class Song:
    def __init__(self, path):
        self.path = path
        self.get_info_from_file(path)
        self.prepare_image()
        self.prepare_audio()

    def get_info_from_file(self, path):
        mp3 = eyed3.load(path)
        tag = mp3.tag
        self.artist = tag.artist
        self.anime = tag.album
        self.title = tag.title
        self.cover = tag.images[0].image_data
        self.audio = mp3

    def write_text_with_border(self, draw, text, x, y, font):
        fillcolor = "white"
        shadowcolor = "black"

        draw.text((x-1, y), text, align="center", font=font, fill=shadowcolor)
        draw.text((x+1, y), text, align="center", font=font, fill=shadowcolor)
        draw.text((x, y-1), text, align="center", font=font, fill=shadowcolor)
        draw.text((x, y+1), text, align="center", font=font, fill=shadowcolor)

        draw.text((x, y), text, align="center", font=font, fill=fillcolor)
    

    def add_text_to_image(self, img):
        text = self.anime
        draw = ImageDraw.Draw(img)
        text_length = len(text)

        # Quite manual, but works for now
        if text_length <= 10:
            pointsize = 80
        elif text_length > 10 and text_length <= 15:
            pointsize = 76
        elif text_length > 15 and text_length <= 20:
            pointsize = 72
        elif text_length > 20 and text_length <= 25:
            pointsize = 68
        elif text_length > 25:
            pointsize = 60

        font = win32api.GetWindowsDirectory() + "\\Fonts\\ARIALBD.TTF"
        font = ImageFont.truetype(font, pointsize)

        base_width, base_height = img.size
        line = ""
        lines = []
        width_of_line = 0
        number_of_lines = 0
        # break string into multi-lines that fit base_width
        for token in text.split():
            token = token+' '
            token_width = font.getsize(token)[0]
            if width_of_line+token_width < base_width:
                line+=token
                width_of_line+=token_width
            else:
                lines.append(line)
                number_of_lines += 1
                width_of_line = 0
                line = ""
                line+=token
                width_of_line+=token_width
        if line:
            lines.append(line)
            number_of_lines += 1
        # create a background strip for the text
        # render each sentence

        full_height = 0
        for line in lines:
            width, height = font.getsize(line)
            full_height += height

        y_text = base_height - full_height - 10

        for line in lines:
            width, height = font.getsize(line)
            self.write_text_with_border(draw, line, ((base_width - width) / 2), y_text, font)
            y_text += height
        return img

    def prepare_image(self):
        img_data = BytesIO(self.cover)
        img = Image.open(img_data)
        img = img.resize(file_configurations["image_size"])

        img = self.add_text_to_image(img)
        buf = BytesIO()
        img.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        nparr = np.frombuffer(byte_im, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        self.cv_image = img

    def prepare_audio(self):
        sound = AudioSegment.from_file(self.path, "mp3")
        random_start = randint(0,len(sound)-(quiz_configurations["guessing_time"]+quiz_configurations["result_time"])*1000)
        sound = sound[random_start:random_start+((quiz_configurations["guessing_time"]+quiz_configurations["result_time"])*1000)]
        self.sound = sound

