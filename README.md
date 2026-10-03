# Image Converter

A lightweight desktop image converter built with **Python + Tkinter**.

Designed for fast and convenient image conversion on macOS, with support for drag & drop, multiple image formats, resizing, conversion progress, and detailed logs.

---

## Features

- 🖼️ Convert images between multiple formats
- 📂 Drag & Drop files and folders
- 📁 Add individual files or entire folders
- 🔄 Recursive folder scanning
- 📐 Resize images
- 🔒 Keep aspect ratio
- 📊 Real-time conversion progress
- 📝 Conversion log
- 🧮 Conversion statistics
- 🧵 Background processing to keep the GUI responsive
- 🧭 Automatically correct EXIF image orientation
- 🚫 Never overwrites existing output files
- 🍎 Designed for macOS
- 📦 Can be packaged as a standalone `.app`

---

## Supported Input Formats

The application currently supports:

- JPG
- JPEG
- PNG
- WebP
- AVIF
- BMP
- TIF
- TIFF
- GIF
- ICO

---

## Supported Output Formats

The application can export to:

- WebP
- AVIF
- JPEG
- PNG
- BMP
- TIFF
- GIF
- ICO

---

## Requirements

- macOS
- Python 3.10+
- Tkinter
- Pillow
- pillow-avif-plugin
- tkinterdnd2

Python 3.14 has been tested during development.

---

## Installation

### 1. Clone or download the project

```bash
git clone https://github.com/ghuninew1/ImageConverter.git
cd ImageConverter
```

Or simply place the project files in your preferred directory.

---

### 2. Create a virtual environment

It is recommended to use a virtual environment for the project.

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, your terminal should show something similar to:

```text
(.venv)
```

---

### 3. Install dependencies

```bash
python3 -m pip install --upgrade pip
```

Then install the required packages:

```bash
pip3 install Pillow pillow-avif-plugin tkinterdnd2
```

For building the macOS application, also install PyInstaller:

```bash
pip3 install pyinstaller
```

---

## Run the Application

Start the GUI with:

```bash
python3 image_converter_gui.py
```

The application window should open.

---

# Usage

## 1. Add Images

There are several ways to add images.

### Drag & Drop

Drag image files or folders directly into:

```text
DROP FILES OR FOLDERS HERE
```

The application will automatically detect supported image files.

Folders are scanned recursively.

---

### Add Files

Click:

```text
Add Files
```

and select one or more image files.

---

### Add Folder

Click:

```text
Add Folder
```

and select an image folder.

All supported images inside the folder and its subfolders will be added.

---

## 2. Select Output Format

Choose the desired output format from:

```text
Output
```

Available formats:

```text
WebP
AVIF
JPEG
PNG
BMP
TIFF
GIF
ICO
```

---

## 3. Set Quality

The quality setting ranges from:

```text
1 - 100
```

Higher values generally produce better image quality but may result in larger files.

The quality setting is used for formats that support quality-based encoding such as:

- JPEG
- WebP
- AVIF

---

## 4. Resize Images

The Resize section allows you to specify:

```text
Width
Height
```

Example:

```text
Width: 1920
Height: 1080
```

### Keep Aspect Ratio

When:

```text
Keep Aspect Ratio
```

is enabled, the image is resized while maintaining its original proportions.

When disabled, the image can be resized to the specified dimensions.

---

## 5. Start Conversion

Click:

```text
START CONVERSION
```

The application will begin processing the selected files.

The original files are not deleted.

---

# Progress Tab

During conversion, the application automatically switches to the **Progress** tab.

The Progress tab displays:

### Progress Percentage

Example:

```text
65%
```

### File Counter

Example:

```text
65 / 100 files
```

### Current File

Shows the image currently being processed.

### Statistics

The application tracks:

```text
Converted
Skipped
Failed
```

### Log

The log displays conversion activity in real time.

Example:

```text
✓ image01.png → image01.webp
✓ image02.jpg → image02.webp
Skipping: image03.webp
✗ image04.png: error message
```

---

# Output Files

Converted files are saved in the same directory as the source image.

For example:

```text
images/
├── photo.jpg
├── photo.webp
├── image.png
└── image.webp
```

The original image is preserved.

---

## Duplicate File Protection

The application does not overwrite an existing output file.

If:

```text
photo.webp
```

already exists, the application automatically creates:

```text
photo-1.webp
```

If that also exists:

```text
photo-2.webp
```

and so on.

---

# Image Orientation

Images containing EXIF orientation information are automatically corrected before conversion.

This is especially useful for photographs taken with cameras and mobile devices.

The application uses:

```python
ImageOps.exif_transpose()
```

to handle image orientation.

---

# Transparency

When converting transparent images to formats that do not support transparency, such as JPEG and BMP, transparent areas are placed on a white background.

For example:

```text
PNG with transparency
        ↓
      JPEG
        ↓
White background
```

---

# Project Structure

A typical project structure is:

```text
ImageConverter/
│
├── image_converter_gui.py
├── README.md
├── build.sh
├── icon.png
├── ImageConverter.icns
│
├── .venv/
│
├── build/
│
└── dist/
    └── Image Converter.app
```

The `.venv`, `build`, and `dist` directories are generated locally and normally should not be committed to Git.

---

# Build macOS Application

The project can be packaged as a standalone macOS application using **PyInstaller**.

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

Then run:

```bash
pyinstaller \
    --clean \
    --windowed \
    --name "Image Converter" \
    image_converter_gui.py
```

The application will be generated at:

```text
dist/Image Converter.app
```

Run it with:

```bash
open "dist/Image Converter.app"
```

---

# Build Script

For convenience, a `build.sh` script can be used.

```bash
#!/bin/bash

set -e

echo "================================"
echo " Building Image Converter"
echo "================================"

rm -rf build
rm -rf dist

pyinstaller \
    --clean \
    --windowed \
    --name "Image Converter" \
    image_converter_gui.py

echo ""
echo "================================"
echo " Build completed!"
echo "================================"
echo ""
echo "Application:"
echo "dist/Image Converter.app"
```

Make the script executable:

```bash
chmod +x build.sh
```

Then build:

```bash
./build.sh
```

---

# Custom Application Icon

A custom macOS icon can be created from a PNG file.

Recommended source:

```text
icon.png
```

Ideally:

- 1024 × 1024 pixels
- PNG
- Transparent background
- High-resolution artwork

Create the macOS icon set:

```bash
mkdir ImageConverter.iconset

sips -z 16 16 \
    icon.png \
    --out ImageConverter.iconset/icon_16x16.png

sips -z 32 32 \
    icon.png \
    --out ImageConverter.iconset/icon_16x16@2x.png

sips -z 32 32 \
    icon.png \
    --out ImageConverter.iconset/icon_32x32.png

sips -z 64 64 \
    icon.png \
    --out ImageConverter.iconset/icon_32x32@2x.png

sips -z 128 128 \
    icon.png \
    --out ImageConverter.iconset/icon_128x128.png

sips -z 256 256 \
    icon.png \
    --out ImageConverter.iconset/icon_128x128@2x.png

sips -z 256 256 \
    icon.png \
    --out ImageConverter.iconset/icon_256x256.png

sips -z 512 512 \
    icon.png \
    --out ImageConverter.iconset/icon_256x256@2x.png

sips -z 512 512 \
    icon.png \
    --out ImageConverter.iconset/icon_512x512.png

cp icon.png \
    ImageConverter.iconset/icon_512x512@2x.png

iconutil \
    -c icns \
    ImageConverter.iconset
```

This creates:

```text
ImageConverter.icns
```

Build the application with the icon:

```bash
pyinstaller \
    --clean \
    --windowed \
    --name "Image Converter" \
    --icon ImageConverter.icns \
    image_converter_gui.py
```

---

# Create a DMG

If desired, the `.app` can be distributed as a macOS DMG.

Install `create-dmg`:

```bash
brew install create-dmg
```

Then:

```bash
create-dmg \
    --volname "Image Converter" \
    --window-pos 200 120 \
    --window-size 800 500 \
    --icon-size 100 \
    --app-drop-link 600 300 \
    "Image Converter.dmg" \
    "dist/Image Converter.app"
```

The result will be:

```text
Image Converter.dmg
```

---

# macOS Security

Applications built locally with PyInstaller are normally not signed or notarized by Apple.

Depending on the macOS security settings, the first launch may display a warning.

If macOS blocks the application:

1. Open **System Settings**
2. Go to **Privacy & Security**
3. Find the message indicating that the application was blocked
4. Select **Open Anyway**

Alternatively, right-click the application and select:

```text
Open
```

This is expected behavior for locally built unsigned applications.

---

# Development

Activate the virtual environment before working on the project:

```bash
source .venv/bin/activate
```

Run the application directly:

```bash
python image_converter_gui.py
```

Install or update dependencies when necessary:

```bash
pip install --upgrade Pillow pillow-avif-plugin tkinterdnd2
```

Build the application:

```bash
./build.sh
```

---

# Dependencies

This project uses:

### Pillow

Image processing and conversion library.

```text
Pillow
```

### pillow-avif-plugin

AVIF support for Pillow.

```text
pillow-avif-plugin
```

### tkinterdnd2

Drag & Drop support for Tkinter.

```text
tkinterdnd2
```

### PyInstaller

Used to package the Python application into a macOS `.app`.

```text
pyinstaller
```

---

# Notes and Limitations

- Original images are never automatically deleted.
- Existing output files are not overwritten.
- Duplicate output names receive an automatic numeric suffix.
- Folder scanning is recursive.
- Animated GIF files are currently processed as a normal image and animation is not preserved.
- JPEG and BMP cannot preserve transparency.
- When transparency is converted to JPEG/BMP, transparent areas are rendered with a white background.
- Resize with **Keep Aspect Ratio** fits the image within the specified dimensions rather than forcing an exact crop.
- The application is currently optimized for local desktop use on macOS.

---

# License

This project is currently intended for personal/internal use.

Add an appropriate license here if the project is later published for public distribution.

---

# Author

**GHUNINEW**

Built with:

- Python
- Tkinter
- Pillow
- tkinterdnd2
- PyInstaller

---
## 👤 ผู้พัฒนา (Author)

- **GhuniNew** - [@ghuninew1](https://github.com/ghuninew1)

## Version

Current development version:

```text
1.0.0
```

Status:

```text
Stable / Ready for packaging
```