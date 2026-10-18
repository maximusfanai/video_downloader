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
</style>
""",
    unsafe_allow_html=True,
)
