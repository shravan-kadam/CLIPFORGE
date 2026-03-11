from faster_whisper import WhisperModel
import os

OUTPUT_DIR = "assets/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Force CPU usage
model = WhisperModel("base", device="cpu", compute_type="int8")

def generate_subtitles(video_path):

    segments, info = model.transcribe(video_path)

    srt_path = os.path.join(OUTPUT_DIR, "subtitles.srt")

    with open(srt_path, "w", encoding="utf-8") as srt:

        for i, segment in enumerate(segments, start=1):

            start = format_time(segment.start)
            end = format_time(segment.end)
            text = segment.text.strip()

            srt.write(f"{i}\n")
            srt.write(f"{start} --> {end}\n")
            srt.write(f"{text}\n\n")

    return srt_path


def format_time(seconds):

    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"