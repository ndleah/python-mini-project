import os
from moviepy.editor import *

# Create array for clips
videos = []
# Assign directory
directory = 'clips'

# Iterate over files in
# that directory and add them
# to the array
for filename in sorted(os.listdir(directory)):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        videos.append(f)

# Print list of clips for debugging purposes
print(videos)

# Setup first clip and initialize array
# for updated clips to be put in
start = os.path.getmtime(videos[0])
concated = []

# For each clip, update its start and end time so that
# they play relative to the time they were recoreded
for path in videos:
    print(path)
    print(os.path.getmtime(path) - start)
    concated.append(VideoFileClip(path, audio=True).set_start(
        os.path.getmtime(path) - start))

# Combine clips into one video
output = CompositeVideoClip(concated)

# Output
output.write_videofile("output.mp4", codec='libx264',
                       audio_codec='aac',
                       temp_audiofile='temp-audio.m4a',
                       remove_temp=True)
