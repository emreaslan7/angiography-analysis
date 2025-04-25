# Angiography Analysis Tool

This project is a **PyQt5-based application** designed for analyzing angiography images and videos. It provides tools for object detection, segmentation, and media playback, making it a comprehensive solution for medical imaging analysis.

## Features

- **Image and Video Support**: Load and display images (`.png`, `.jpg`, `.bmp`) and videos (`.mp4`, `.avi`).
- **Object Detection**: Toggle visibility of object detection components.
- **Segmentation**: Toggle visibility of segmentation components.
- **Video Playback**: Play, pause, stop, and seek through video files.
- **Interactive Toolbar**: Easy access to file operations and analysis tools.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/emreaslan7/angiography-analysis.git
   cd angiography-analysis
   ```

2. Install dependencies

   ```python
   pip install -r requirements.txt
   ```

3. Run the application:
   ```python
   python src/main.py
   ```

## Project Structure

```txt
angiography-analysis/
├── src/
│   ├── models/
│   │   ├── object-detection-v1.pt
│   ├── functions/
│   │   ├── detection_utils.py
│   │   ├── image_utils.py
│   │   ├── video_utils.py
│   ├── ui/
│   │   ├── components/
│   │   ├── tool_bar.py
│   │   ├── video_player.py
│   │   ├── menu_bar.py.py
│   │   ├── main_window.py
│   ├── main.py
│   ├── state_manager.py
├── output/
│   ├── annotated_result_video.mp4
│   ├── annotated_result.jpg
├── README.md
├── requirements.txt
└── .gitignore
```

## Usage

1. Launch the application.
2. Use the toolbar to open an image or video file.
3. Toggle object detection or segmentation tools as needed.
4. For videos, use playback controls to navigate through frames.

## Requirements

- Python 3.10+
- PyQt5
- OpenCV
- NumPy

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
