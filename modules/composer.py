from moviepy import VideoFileClip, concatenate_videoclips
import os
import shutil

OUTPUT_DIR = "assets/outputs"
UPLOAD_DIR = "assets/uploads"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

def normalize_video(input_path, output_path):
    """
    Re-encode video to constant frame rate and valid keyframe.
    This fixes WhatsApp/mobile video issues on Windows.
    """
    clip = VideoFileClip(input_path)
    clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        preset="medium",
        ffmpeg_params=["-movflags", "+faststart"]
    )
    clip.close()

def compose_videos(video_files):
    clips = []
    normalized_paths = []

    for file in video_files:
        filename = os.path.basename(file)
        stable_path = os.path.join(UPLOAD_DIR, filename)
        shutil.copy(file, stable_path)

        normalized_path = os.path.join(
            UPLOAD_DIR, f"normalized_{filename}"
        )

        normalize_video(stable_path, normalized_path)
        normalized_paths.append(normalized_path)

    for path in normalized_paths:
        clips.append(VideoFileClip(path))

    final_clip = concatenate_videoclips(clips)
    output_path = os.path.join(OUTPUT_DIR, "final_video.mp4")

    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    for clip in clips:
        clip.close()

    return output_path
