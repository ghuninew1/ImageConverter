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
    --icon ImageConverter.icns \
    image_converter_gui.py

echo ""
echo "================================"
echo " Build completed!"
echo "================================"

echo ""
echo "Application:"
echo "dist/Image Converter.app"
create-dmg \
    --volname "Image Converter" \
    --window-pos 200 120 \
    --window-size 800 500 \
    --icon-size 100 \
    --app-drop-link 600 300 \
    "Image Converter.dmg" \
    "dist/Image Converter.app"

echo ""
echo "DMG:"
echo "Image Converter.dmg"

echo ""
echo "================================"
echo " Done!"
echo "================================"