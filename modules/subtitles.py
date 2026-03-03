from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_subtitles(video_path, text):
    video = VideoFileClip(video_path)
    subtitle = TextClip(text, fontsize=40, color='white').set_position('bottom').set_duration(video.duration)

    final = CompositeVideoClip([video, subtitle])
    output = "assets/outputs/subtitled.mp4"
    final.write_videofile(output)

    return output
