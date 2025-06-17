import pytesseract
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter

image_folder = "snapshots"
output_excel = "ocr_output.xlsx"           

data = []

def preprocess_image(image_path):
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    image = image.filter(ImageFilter.MedianFilter())  # Reduce noise
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast
    return image

for filename in sorted(os.listdir(image_folder)):
    if filename.endswith(".jpg"):
        timestamp = int(os.path.splitext(filename)[0])

        image_path = os.path.join(image_folder, filename)
        #image = cv2.imread(image_path)

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
print(f"OCR results saved to {output_excel}")
plt.show()