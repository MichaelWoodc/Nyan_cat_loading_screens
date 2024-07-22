from pydub import AudioSegment
from pydub.playback import play

input_filename = "rickRolled.mp4"
output_filename = "rickRolled_no_left_audio.mp4"

# Load the audio from the video
audio = AudioSegment.from_file(input_filename, format="mp4")

# Split stereo audio into left and right channels
left_channel = audio.split_to_mono()[0]

# Create a new stereo audio with the left channel only
new_audio = AudioSegment.from_mono_audiosegments(left_channel)

# Save the modified audio
new_audio.export(output_filename, format="mp4")

print("Left channel audio removed and saved to", output_filename)
