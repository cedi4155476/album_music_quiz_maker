import os
import cv2
import numpy as np
import moviepy.editor as mpe
import win32api

from pathlib import Path
from random import shuffle
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

from Exceptions import NoSongsAvailableException
from config import quiz_configurations, file_configurations, temp_files
from song import Song

class QuizMaker:
    def __init__(self):
        self.songs = []
        self.countdown = self.make_countdown()

    def make_countdown(self):
        image_list = []
        for i in range(quiz_configurations["guessing_time"]):
            image_list.append(self.add_text_to_image(file_configurations["default_image"],i+1))
        image_list.reverse()
        return image_list

    def add_text_to_image(self, origin_image, nr):
        msg = str(nr)
        im = Image.open(origin_image)
        im = im.resize(file_configurations["image_size"])
        W, H = im.size
        font = win32api.GetWindowsDirectory() + "\\Fonts\\ARIALBD.TTF"
        font = ImageFont.truetype(font, 80)

        draw = ImageDraw.Draw(im)
        w, h = draw.textsize(msg)

        draw.text(((W-w)/2,(H-h)/2), msg, font=font, fill="white")
        
        buf = BytesIO()
        im.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        nparr = np.frombuffer(byte_im, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return img

    def run(self):
        input_folder = Path(file_configurations["input_folder"])
        if not input_folder.exists():
            input_folder.mkdir()
            raise NoSongsAvailableException(f"There are no mp3 files in the {file_configurations['input_folder']} folder.")
        random_songs = self.get_random_songs(input_folder)
        out = cv2.VideoWriter(temp_files["video"],cv2.VideoWriter_fourcc(*'DIVX'), 1, file_configurations["image_size"])
        sound_chain = None
        for filename in random_songs:
            song = Song(filename)
            for i in range(quiz_configurations["guessing_time"]):
                out.write(self.countdown[i])
            for _ in range(quiz_configurations["result_time"]):
                out.write(song.cv_image)
            if sound_chain:
                sound_chain += song.sound
            else:
                sound_chain = song.sound
        sound_chain.export(temp_files["audio"], format="mp3")
        out.release()
        self.combine_audio_video()

    def combine_audio_video(self, fps=25):
        my_clip = mpe.VideoFileClip(temp_files["video"])
        audio_background = mpe.AudioFileClip(temp_files["audio"])
        final_clip = my_clip.set_audio(audio_background)

        output_folder = Path(file_configurations["output_folder"])
        if not output_folder.exists():
            output_folder.mkdir()

        output_path = output_folder / f"{file_configurations['output_file_name']}.{file_configurations['output_file_extension']}")
        if output_path.is_file():
            output_path = self.add_number_to_file(file_configurations)
        final_clip.write_videofile(output_path.as_posix(), codec="libx264", fps=fps)
        os.remove(temp_files["video"])
        os.remove(temp_files["audio"])

    def add_number_to_file(self, file_configurations):
        file_counter = 1
        folder_path = Path(file_configurations["output_folder"])
        while True :
            output_path = folder_path / f"{file_configurations['output_file_name']} ({file_counter}).{file_configurations['output_file_extension']}"
            if not output_path.is_file():
                return output_path
            file_counter += 1

    def get_random_songs(self, input_folder):
        all_songs = list(input_folder.glob('*.mp3'))
        if not all_songs:
            raise NoSongsAvailableException(f"There are no mp3 files in the {file_configurations['input_folder']} folder.")

        shuffle(all_songs)
        return all_songs[:quiz_configurations["amount_songs"]]

if __name__ == "__main__":
    try:
        g = QuizMaker()
        g.run()
    except NoSongsAvailableException as e:
        input(f"{e.args[0]} Press any Key to close...")