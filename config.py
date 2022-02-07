# Configuration for quiz maker
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

# Its easier to combine video and audio files together, thats why temporary files are necessary, will automatically be deleted after combining
temp_files = {
    "audio":"audio.mp3",
    "video":"video.avi"
}
