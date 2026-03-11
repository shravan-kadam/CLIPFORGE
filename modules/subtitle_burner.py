from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import pysrt
import os

OUTPUT_DIR = "assets/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def burn_subtitles(video_path, subtitle_path):

    video = VideoFileClip(video_path)
    subs = pysrt.open(subtitle_path)

    subtitle_clips = []

    for sub in subs:

        start = sub.start.ordinal / 1000
        end = sub.end.ordinal / 1000

        txt_clip = TextClip(
            text=sub.text,
            font_size=40,
            color="white",
            stroke_color="black",
            stroke_width=2,
            size=(int(video.w * 0.9), None),
            method="caption"
        )

        txt_clip = txt_clip.with_start(start).with_end(end).with_position(("center","bottom"))

        subtitle_clips.append(txt_clip)

    final = CompositeVideoClip([video] + subtitle_clips)

    output_path = os.path.join(OUTPUT_DIR, "captioned_video.mp4")

    final.write_videofile(output_path, codec="libx264")

    return output_path