# album_music_quiz_maker
A small program to make an Album Music Quiz with your own mp3 files.

## How to use:

**At the moment only mp3 files can be used.**
**And all the information about the image and album needs to be meta information in the mp3 files already.**

Start the program with the `quiz_maker.py` file

You need a folder in the same directory as the python files you can change the name of it in the config.py (default "songs")

The Resulting File will be put into another folder as well (default folder "Output" default filename "Automated guess album")

```
# In the config.py file you can change the amount of songs, 
# how long the guessing and result time is and also change the file names and folders.
Configuration for quiz maker
quiz_configurations = {
    "amount_songs":50,
    "guessing_time":15,
    "result_time":5,
}

# File related configurations
file_configurations = {
    "output_folder":"Output",
    "output_file_name":"Automated guess album",
    "output_file_extension":"mp4",
    "input_folder":"songs",
    "default_image":"black_image.jpg",
    "image_size":(382*2,595*2),
}
```
