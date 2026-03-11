import gradio as gr
import shutil
import os

from dotenv import load_dotenv
load_dotenv()

from modules.summarizer import summarize_text
from modules.frame_extractor import extract_frame
from modules.thumbnail import generate_thumbnail
from modules.composer import compose_videos
from modules.subtitles import generate_subtitles
from modules.subtitle_burner import burn_subtitles

# --------------------------------------------------
# Configuration
# --------------------------------------------------
UPLOAD_DIR = "assets/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------------------------
# Functions
# --------------------------------------------------
def save_uploaded_video(video_file):
    if video_file is None:
        return "No video uploaded."

    filename = os.path.basename(video_file)
    destination = os.path.join(UPLOAD_DIR, filename)
    shutil.copy(video_file, destination)

    return f"Video uploaded successfully: {filename}"


def summarize_ui(text):
    if not text.strip():
        return "Please enter some text to summarize."
    return summarize_text(text)


def create_thumbnail(video_file, title_text):
    if video_file is None:
        return None

    frame_path = extract_frame(video_file)
    thumbnail_path = generate_thumbnail(frame_path, title_text)
    return thumbnail_path


def compose_ui(video_files):
    if not video_files or len(video_files) < 1:
        return None

    return compose_videos(video_files)


def subtitle_ui(video):
    if video is None:
        return None
    return generate_subtitles(video)

def burn_subtitles_ui(video, subtitle_file):
    if video is None or subtitle_file is None:
        return None

    return burn_subtitles(video, subtitle_file)


# --------------------------------------------------
# Gradio App
# --------------------------------------------------
with gr.Blocks(theme=gr.themes.Soft()) as app:

    gr.Markdown("## 🎬 ClipForge AI")
    gr.Markdown("Transform raw footage into short viral content")

    # Top navigation
    with gr.Row():
        gr.Button("Upload Clips")
        gr.Button("Describe Vision")
        gr.Button("AI Processing")
        gr.Button("Export & Share")

    # --------------------------------------------------
    # Upload Section
    # --------------------------------------------------
    gr.Markdown("### 📥 Upload Video")

    video_input = gr.Video(label="Upload Video")
    upload_status = gr.Textbox(label="Status", interactive=False)

    gr.Button("Save Video").click(
        save_uploaded_video,
        inputs=video_input,
        outputs=upload_status
    )

    # --------------------------------------------------
    # Video Summarizer Tab
    # --------------------------------------------------
    with gr.Tab("📝 Video Summarizer"):

        gr.Markdown("### AI Video Summary")
        gr.Markdown("Paste your video transcript or description below.")

        input_text = gr.Textbox(
            label="Video Text",
            placeholder="Paste video transcript or description here...",
            lines=6
        )

        output_text = gr.Textbox(label="AI Summary", lines=4)

        gr.Button("Generate Summary").click(
            summarize_ui,
            inputs=input_text,
            outputs=output_text
        )

    # --------------------------------------------------
    # Thumbnail Generator Tab
    # --------------------------------------------------
    with gr.Tab("🖼 Thumbnail Generator"):

        gr.Markdown("### Generate Video Thumbnail")

        video_for_thumb = gr.Video(label="Select Video")

        title_text = gr.Textbox(
            label="Thumbnail Text",
            placeholder="Enter title text"
        )

        thumbnail_output = gr.Image(label="Generated Thumbnail")

        gr.Button("Create Thumbnail").click(
            create_thumbnail,
            inputs=[video_for_thumb, title_text],
            outputs=thumbnail_output
        )

    # --------------------------------------------------
    # Subtitle Generator Tab
    # --------------------------------------------------
    with gr.Tab("📝 Subtitle Generator"):

        gr.Markdown("### Generate Subtitles from Video")

        video_input_sub = gr.Video(label="Upload Video")

        subtitle_file = gr.File(label="Generated Subtitle (.srt)")

        gr.Button("Generate Subtitles").click(
            subtitle_ui,
            inputs=video_input_sub,
            outputs=subtitle_file
        )

    # --------------------------------------------------
    # Video Composer Tab
    # --------------------------------------------------
    with gr.Tab("🎞 Video Composer"):

        gr.Markdown("### Combine Video Clips")
        gr.Markdown("⚠️ Use normal MP4 videos (not WhatsApp videos)")

        video_inputs = gr.File(
            label="Upload Video Clips",
            file_types=[".mp4"],
            file_count="multiple"
        )

        final_video = gr.Video(label="Final Composed Video")

        gr.Button("Compose Video").click(
            compose_ui,
            inputs=video_inputs,
            outputs=final_video
        )

    with gr.Tab("🎬 Burn Subtitles Into Video"):

        gr.Markdown("### Overlay Subtitles On Video")

        video_input_burn = gr.Video(label="Upload Video")

        subtitle_input = gr.File(label="Upload Subtitle File (.srt)")

        output_video = gr.Video(label="Captioned Video")

        gr.Button("Burn Subtitles").click(
            burn_subtitles_ui,
            inputs=[video_input_burn, subtitle_input],
            outputs=output_video
    )


# --------------------------------------------------
# Launch App
# --------------------------------------------------
app.launch()