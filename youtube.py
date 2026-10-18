import os
import threading
import time
import static_ffmpeg
import streamlit as st
import yt_dlp

try:
  static_ffmpeg.add_paths()
except Exception:
  pass

st.set_page_config(
    page_title="YouTube Video Downloader",
    page_icon="▶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Session States Initialization
if "downloaded_file" not in st.session_state:
  st.session_state.downloaded_file = None
if "downloaded_mime" not in st.session_state:
  st.session_state.downloaded_mime = "video/mp4"
if "is_audio" not in st.session_state:
  st.session_state.is_audio = False
if "is_downloading" not in st.session_state:
  st.session_state.is_downloading = False
if "progress_val" not in st.session_state:
  st.session_state.progress_val = 0
if "show_ad" not in st.session_state:
  st.session_state.show_ad = False
if "ad_timer" not in st.session_state:
  st.session_state.ad_timer = 25

st.markdown(
    """
<style>
#MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #04060d !important;
    color: #ffffff !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
}

.main .block-container, [data-testid="stMainBlockContainer"] {
    max-width: 480px !important; width: 100% !important; margin: 0 auto !important; padding: 12px 10px 130px 10px !important;
}

.header-box { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; margin-top: 2px; }
.brand-row { display: flex; align-items: center; gap: 8px; }
.yt-icon { background: #ff0000; color: #ffffff; padding: 4px 10px; border-radius: 8px; font-size: 16px; font-weight: 700; box-shadow: 0 0 12px rgba(255, 0, 0, 0.75); display: flex; align-items: center; justify-content: center; }
.title-white { font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; line-height: 1; }
.title-row { display: flex; gap: 6px; margin-top: 4px; align-items: flex-start; }
.title-dark { font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; line-height: 1; }
.title-red { font-size: 20px; font-weight: 800; color: #ff2236; letter-spacing: -0.5px; line-height: 1; }
.subtitle-text { font-size: 11px; color: #838d9d; margin-top: 4px; font-weight: 500; }

.stTextInput input {
    background-color: #0d1224 !important;
    color: #ffffff !important;
    border: 1px solid #1f293d !important;
    border-radius: 10px !important;
}
.stButton button {
    width: 100%;
    background: linear-gradient(135deg, #ff0000, #cc0000);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 10px;
    box-shadow: 0 4px 14px rgba(255, 0, 0, 0.4);
}
</style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
<div class="header-box">
    <div>
        <div class="brand-row">
            <div class="yt-icon">▶</div>
            <div class="title-white">YouTube</div>
        </div>
        <div class="title-row">
            <div class="title-dark">Video</div>
            <div class="title-red">Downloader</div>
        </div>
        <div class="subtitle-text">Save your favorite videos anywhere, anytime!</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

url = st.text_input("Youtube Link", placeholder="Paste YouTube link here...")

format_choice = st.radio(
    "Choose Format :", ["MP4 (video)", "Mp3 (audio)", "MKV (video)", "WebM (video)"]
)

quality_choice = st.selectbox(
    "Select Quality :", ["1080P", "720P", "480P", "360P", "240P", "144P"]
)


def get_ydl_opts(download_path, is_audio, quality, fmt):
  res_map = {
      "1080P": "1080",
      "720P": "720",
      "480P": "480",
      "360P": "360",
      "240P": "240",
      "144P": "144",
  }
  height = res_map.get(quality, "720")

  opts = {
      "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
      "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
  }

  if is_audio:
    opts["format"] = "bestaudio/best"
    opts["postprocessors"] = [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }]
  else:
    if fmt == "MKV (video)":
      opts["format"] = (
          f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"
      )
      opts["merge_output_format"] = "mkv"
    elif fmt == "WebM (video)":
      opts["format"] = (
          f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"
      )
      opts["merge_output_format"] = "webm"
    else:
      opts["format"] = (
          f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"
      )
      opts["merge_output_format"] = "mp4"

  return opts


if st.button("Download Now"):
  if not url:
    st.error("Please enter a valid YouTube link.")
  else:
    with st.spinner("Downloading... Please do not close the app"):
      try:
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        is_aud = "Mp3" in format_choice
        ydl_opts = get_ydl_opts(
            download_dir, is_aud, quality_choice, format_choice
        )

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(url, download=True)
          filename = ydl.prepare_filename(info)
          if is_aud:
            filename = os.path.splitext(filename)[0] + ".mp3"
            mime = "audio/mpeg"
          else:
            if "MKV" in format_choice:
              filename = os.path.splitext(filename)[0] + ".mkv"
              mime = "video/mkv"
            elif "WebM" in format_choice:
              filename = os.path.splitext(filename)[0] + ".webm"
              mime = "video/webm"
            else:
              filename = os.path.splitext(filename)[0] + ".mp4"
              mime = "video/mp4"

          st.session_state.downloaded_file = filename
          st.session_state.downloaded_mime = mime
          st.success("Download completed successfully!")

      except Exception as e:
        st.error(f"Error: {e}")

if st.session_state.downloaded_file and os.path.exists(
    st.session_state.downloaded_file
):
  with open(st.session_state.downloaded_file, "rb") as f:
    st.download_link(
        label="📥 Click here to save file",
        data=f,
        file_name=os.path.basename(st.session_state.downloaded_file),
        mime=st.session_state.downloaded_mime,
    )

if st.button("⬅ Back to Home"):
  st.query_params["page"] = "home"
  st.rerun()
