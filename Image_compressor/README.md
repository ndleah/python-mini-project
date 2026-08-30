<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Image Compressor

## 🛠️ Description
The image compressor takes JPEG or PNG images and reduces their file size by applying quality and palette optimizations.

## 🚀 Features
- **Path Bug Fixes**: Correctly resolves file paths returned by picker without `FileNotFoundError`.
- **PNG Palette Optimization**: Uses adaptive 256-color palette and `compress_level=9` for effective PNG compression.
- **CLI & GUI Modes**: Run via command-line arguments or GUI file picker.

## ⚙️ Requirements
```bash
pip install pillow easygui
```

## 🌟 How to run

### Command Line
```bash
python image_compressor.py input_image.jpg [quality_10_to_100]
```

### GUI Mode
```bash
python image_compressor.py
```

## 🤖 Author
Discord: dumb_potato#1734


