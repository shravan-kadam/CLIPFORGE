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


UPLOAD_DIR = "assets/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------- FUNCTIONS ----------------

def save_uploaded_video(video_file):
    if video_file is None:
        return "❌ No video uploaded."

    filename = os.path.basename(video_file)
    destination = os.path.join(UPLOAD_DIR, filename)
    shutil.copy(video_file, destination)

    return f"✅ Video uploaded: {filename}"


def summarize_ui(text):
    if not text.strip():
        return "Please enter text."
    return summarize_text(text)


def create_thumbnail(video_file, title_text):
    if video_file is None:
        return None
    frame = extract_frame(video_file)
    return generate_thumbnail(frame, title_text)


def compose_ui(video_files):
    if not video_files:
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


# ---------------- CSS ----------------

custom_css = """
body{
background:linear-gradient(135deg,#020617,#0f172a);
font-family:Inter;
}

.hero{
text-align:center;
padding:50px;
}

.hero-title{
font-size:44px;
font-weight:800;
background:linear-gradient(90deg,#60a5fa,#a78bfa,#c084fc);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.navbar{
display:flex;
gap:20px;
justify-content:center;
margin-bottom:25px;
}

.card{
background:#0f172a;
padding:25px;
border-radius:14px;
box-shadow:0 8px 20px rgba(0,0,0,0.4);
}
"""


# ---------------- UI ----------------

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as app:

    with gr.Column(elem_classes="hero"):
        gr.Markdown("""
<div class="hero-title">🎬 ClipForge AI</div>
Create viral short-form content using AI
""")

    # NAVIGATION BAR
    with gr.Row():
        btn_upload = gr.Button("📥 Upload")
        btn_summary = gr.Button("📝 Summary")
        btn_thumbnail = gr.Button("🖼 Thumbnail")
        btn_subtitle = gr.Button("🎤 Subtitles")
        btn_composer = gr.Button("🎞 Composer")
        btn_burn = gr.Button("🔥 Burn")

    # SECTIONS

    with gr.Column(visible=True) as upload_section:
        with gr.Column(elem_classes="card"):
            video_input = gr.Video()
            upload_btn = gr.Button("Upload Video")
            upload_status = gr.Textbox(label="Status")

            upload_btn.click(
                save_uploaded_video,
                inputs=video_input,
                outputs=upload_status
            )


    with gr.Column(visible=False) as summary_section:
        with gr.Column(elem_classes="card"):
            input_text = gr.Textbox(lines=5)
            summarize_btn = gr.Button("Generate Summary")
            output_text = gr.Textbox()

            summarize_btn.click(
                summarize_ui,
                inputs=input_text,
                outputs=output_text
            )


    with gr.Column(visible=False) as thumb_section:
        with gr.Column(elem_classes="card"):
            video_for_thumb = gr.Video()
            title_text = gr.Textbox()
            thumb_btn = gr.Button("Generate Thumbnail")
            thumbnail_output = gr.Image()

            thumb_btn.click(
                create_thumbnail,
                inputs=[video_for_thumb, title_text],
                outputs=thumbnail_output
            )


    with gr.Column(visible=False) as subtitle_section:
        with gr.Column(elem_classes="card"):
            video_input_sub = gr.Video()
            subtitle_btn = gr.Button("Generate Subtitles")
            subtitle_file = gr.File()

            subtitle_btn.click(
                subtitle_ui,
                inputs=video_input_sub,
                outputs=subtitle_file
            )


    with gr.Column(visible=False) as composer_section:
        with gr.Column(elem_classes="card"):
            video_inputs = gr.File(file_types=[".mp4"], file_count="multiple")
            compose_btn = gr.Button("Compose Video")
            final_video = gr.Video()

            compose_btn.click(
                compose_ui,
                inputs=video_inputs,
                outputs=final_video
            )


    with gr.Column(visible=False) as burn_section:
        with gr.Column(elem_classes="card"):
            video_input_burn = gr.Video()
            subtitle_input = gr.File()
            burn_btn = gr.Button("Burn Subtitles")
            output_video = gr.Video()

            burn_btn.click(
                burn_subtitles_ui,
                inputs=[video_input_burn, subtitle_input],
                outputs=output_video
            )


    # ---------- NAVIGATION FUNCTIONS (FIXED) ----------

    def show_upload():
        return (
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
        )


    def show_summary():
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
        )


    def show_thumb():
        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
        )


    def show_subtitle():
        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
        )


    def show_composer():
        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
        )


    def show_burn():
        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
        )


    btn_upload.click(show_upload,
        outputs=[upload_section, summary_section, thumb_section, subtitle_section, composer_section, burn_section])

    btn_summary.click(show_summary,
        outputs=[upload_section, summary_section, thumb_section, subtitle_section, composer_section, burn_section])

    btn_thumbnail.click(show_thumb,
        outputs=[upload_section, summary_section, thumb_section, subtitle_section, composer_section, burn_section])

    btn_subtitle.click(show_subtitle,
        outputs=[upload_section, summary_section, thumb_section, subtitle_section, composer_section, burn_section])

    btn_composer.click(show_composer,
        outputs=[upload_section, summary_section, thumb_section, subtitle_section, composer_section, burn_section])

    btn_burn.click(show_burn,
        outputs=[upload_section, summary_section, thumb_section, subtitle_section, composer_section, burn_section])


app.launch(server_name="0.0.0.0", server_port=7860)