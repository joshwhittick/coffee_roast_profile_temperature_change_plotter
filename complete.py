import os
import cv2
import pytesseract
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt

def extract_frames_from_video(video_path, output_folder="snapshots", snapshot_interval=2):
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_seconds = int(total_frames / fps)

    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        os.remove(file_path)

    for t in range(0, duration_seconds + 1, snapshot_interval):
        frame_number = int(t * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = cap.read()

        #rotate frame 90 degrees clockwise
        if success:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if not success:
            print(f"Failed to read frame at {t} seconds")
            continue

        filename = os.path.join(output_folder, f"{t}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")

    cap.release()
    print("\nAll snapshots saved.\n")


def preprocess_image(image_path):
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    image = image.filter(ImageFilter.MedianFilter())  # Reduce noise
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast
    return image

def perform_ocr_on_folder(image_folder="snapshots", output_excel="ocr_output.xlsx"):
    data = []

    for filename in sorted(os.listdir(image_folder)):
        if filename.lower().endswith(".jpg"):
            timestamp = int(os.path.splitext(filename)[0])

            image_path = os.path.join(image_folder, filename)
            preprocessed = preprocess_image(image_path)
            
            text = pytesseract.image_to_string(preprocessed, config='--psm 7 digits')
            #text = pytesseract.image_to_string(image)
            
            text = text.strip().replace('\n', ' ').replace("'","").replace(")","")

            print(f"Processing {filename}: extracted text: '{text}'")

            if not text:
                print(f"Skipping {filename}: no text found")
                continue

            data.append({"Timestamp (s)": timestamp, "Temperature": int(text)})

    df = pd.DataFrame(data)
    df = df.sort_values(by="Timestamp (s)").reset_index(drop=True)
    plt.plot(df["Timestamp (s)"], df["Temperature"], marker='o')
    plt.xlabel("Timestamp (s)")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Over Time")
    plt.grid()
    plt.savefig("temperature_plot.png")
    df.to_excel(output_excel, index=False)
    print(f"\nOCR results saved to {output_excel}")
    plt.show()

extract_frames_from_video("vid2.mov")
perform_ocr_on_folder()