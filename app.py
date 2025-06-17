import os, io, shutil, tempfile, cv2, pytesseract, pandas as pd
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError
import matplotlib.pyplot as plt
import streamlit as st
import atexit

# ---------- low-level helpers ----------
def extract_frames(video_bytes: bytes, interval_s: int = 2, rotate: bool = True) -> tuple:
    """Save snapshots every <interval_s> seconds and return (folder path, duration in seconds)."""
    tmpdir = tempfile.mkdtemp()
    vid_path = os.path.join(tmpdir, "video")
    with open(vid_path, "wb") as f: f.write(video_bytes)

    cap = cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(total_frames / fps)

    for t in range(0, duration + 1, interval_s):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        ok, frame = cap.read()
        if not ok: continue
        if rotate:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite(os.path.join(tmpdir, f"{t}.jpg"), frame)
    cap.release()
    return tmpdir, duration

def preprocess(image_path: str) -> Image.Image:
    img = Image.open(image_path).convert("L")
    img = img.filter(ImageFilter.MedianFilter())
    img = ImageEnhance.Contrast(img).enhance(2)
    return img

def run_ocr(folder: str, debug: bool = False) -> pd.DataFrame:
    frames = [
        f for f in os.listdir(folder)
        if f.lower().endswith(".jpg") and os.path.splitext(f)[0].isdigit()
    ]
    rows = []
    for fname in sorted(frames, key=lambda x: int(os.path.splitext(x)[0])):
        ts = int(os.path.splitext(fname)[0])
        img_path = os.path.join(folder, fname)
        txt = pytesseract.image_to_string(
            preprocess(img_path),
            config="--psm 7 digits"
        ).strip().replace("\n", " ")

        if debug:
            st.text(f"[{ts}s] Raw OCR: '{txt}'")

        if txt.isdigit():
            rows.append({"Timestamp (s)": ts, "Temperature (°C)": int(txt)})
    return pd.DataFrame(rows).sort_values("Timestamp (s)")

def line_plot(df: pd.DataFrame):
    fig, ax = plt.subplots()
    ax.plot(df["Timestamp (s)"], df["Temperature (°C)"], marker="o")
    ax.set_xlabel("Timestamp (s)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature over time")
    ax.grid()
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.download_button("⬇️ Download Plot", buf, file_name="temperature_plot.png", mime="image/png")

# ---------- Streamlit UI ----------
st.set_page_config("Video Thermometer OCR", layout="wide")
st.title("Video Thermometer OCR")
st.markdown(
    "Upload a short video of your **thermometer display**, and this app will:\n"
    "1. grab snapshots every *N* seconds,\n"
    "2. run OCR on each frame, and\n"
    "3. plot and export the temperature data."
)

video_file = st.file_uploader("📼 Select a video file", type=["mp4", "mov", "avi", "mkv"])

if video_file:
    interval = st.number_input("Snapshot interval (seconds)", 1, 30, 2, 1)
    rotate = st.checkbox("Rotate frames 90° clockwise", value=True)
    debug_ocr = st.checkbox("Enable OCR debug mode")

    st.video(video_file)

    if st.button("✨ Process"):
        with st.spinner("Extracting frames…"):
            snapshot_dir, duration = extract_frames(video_file.read(), interval, rotate)
        st.success(f"Snapshots saved from 0s to {duration}s")

        cols = st.columns(5)
        for i, imgname in enumerate(sorted(os.listdir(snapshot_dir))[:10]):
            img_path = os.path.join(snapshot_dir, imgname)
            try:
                cols[i % 5].image(img_path, use_container_width=True)
            except UnidentifiedImageError:
                st.warning(f"⚠️ Skipped invalid image file: {imgname}")

        with st.spinner("Running OCR…"):
            df = run_ocr(snapshot_dir, debug_ocr)

        if df.empty:
            st.warning("No digits recognised 🤔")
        else:
            st.subheader("Results")
            st.dataframe(df, hide_index=True, use_container_width=True)
            line_plot(df)

            # --- download buttons ---
            excel_bytes = io.BytesIO()
            df.to_excel(excel_bytes, index=False)
            xl_name = f"ocr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            st.download_button("⬇️ Download Excel", excel_bytes.getvalue(), file_name=xl_name)

        # Cleanup
        st.session_state.setdefault("tmpdirs", []).append(snapshot_dir)

# ----- Cleanup on shutdown -----
def _cleanup():
    for d in st.session_state.get("tmpdirs", []):
        shutil.rmtree(d, ignore_errors=True)
atexit.register(_cleanup)