import cv2
import os

video_path = "vid2.mov"
output_folder = "snapshots"
snapshot_interval = 2

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
print("All snapshots saved.")
