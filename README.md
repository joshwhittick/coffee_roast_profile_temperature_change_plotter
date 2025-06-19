# ☕ Coffee Roast Profile Temperature Change Plotter

### From roast room curiosity to data visualization - a tool for tracking and analyzing small-batch coffee roasting temperatures.

## 🛠️ Project Overview

This project was inspired by a visit to my friend Alex’s coffee roastery, where I saw first-hand the skill and intuition involved in roasting small batches of award-winning, ethically sourced artisan coffee.

At the heart of his process is a **Diedrich gas-powered roaster**, an old-school machine that handles 20kg batches at a time. The only input Alex controls is the **gas level**, and while the machine does offer a digital readout of the current temperature, its instrumentation is minimal. This means the roast profile - the curve of temperature over time — is largely shaped by experience and feel. A roast typically lasts about 14 minutes, and different beans or flavor profiles require different temperature trends.

While watching him work, I thought: *What if we could chart the actual temperature changes and compare them to the target profile?*

Alex already kept a rough roast profile written in a text document — a list of target temperatures and gas settings at 30-second intervals. That was the seed of this project.

## 🔁 The Workflow

This tool follows a simple 5-step process:

**Video → Image → Text → Table → Graph**

1. **Video**: A close-up video records the digital temperature display during the roast.
2. **Image**: The video is broken down into frame snapshots at regular intervals.
3. **Text**: Optical Character Recognition (OCR) is used to extract temperature values from each image.
4. **Table**: Extracted values and timestamps are compiled into a structured CSV or Excel table.
5. **Graph**: A temperature vs. time line plot is generated to visualize the roast profile.

> ✅ The project is currently tested using a video of a radiator display (which changes color with temperature). Real coffee roasting data is expected next week — fingers crossed!

## 📂 Folder Structure

```
.
├── complete.py               # Full version of code combining vid_to_imgs.py + imgs_to_csv.py
├── folder_structure.md       # Documentation of file structure
├── imgs_to_csv.py            # Extracts OCR text from images and outputs XLSX
├── local_app.py              # Local version of Streamlit app - uses Tesseract
├── ocr_output.xlsx           # Example OCR output file
├── requirements.txt          # Required Python packages
├── snapshots/                # Folder of extracted images from video
│   ├── 0.jpg
│   ├── ...
│   └── 38.jpg
├── streamlit_app.py          # Streamlit app for web deployment (https://coffee-roast-profile-plotting.streamlit.app/) - uses Python based OCR since cant have Tesseract in Streamlit
├── temperature_plot.png      # Sample output plot
├── vid_to_imgs.py            # Converts video to image snapshots
└── vid2.mov                  # Demo input video (radiator display)
```

## 🧪 Current Status

### [Try the web-app here!](https://coffee-roast-profile-plotting.streamlit.app/)

* ✅ End-to-end pipeline working with demo footage
* 🕵️ Tested OCR accuracy with my radiator temperature readout
* 📊 Streamlit app prototype is functional

## 📌 Next Steps

* Collect and test with real coffee roasting data
* Fine-tune OCR to handle screen glare, font types, and resolution
* Add support for comparing live roast data against stored "ideal" profiles
* Optional: Add ability to annotate plots with gas settings or notable events

## 👋 Get in Touch

If you're a roaster, coffee geek, or just curious about combining analog artistry with digital tools, feel free to reach out via [my profile](https://github.com/joshwhittick).
