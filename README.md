# PyQt Desktop Application for Angiography Analysis

This project is a desktop application developed using PyQt that automates the analysis of angiography data through pathological region detection. The application utilizes a tracking algorithm and a segmentation model to compute the radial wall strain parameters.

## Project Structure

```
pyqt-desktop-app
├── src
│   ├── main.py                  # Entry point of the application
│   ├── ui
│   │   └── main_window.ui       # UI layout designed with Qt Designer
│   ├── controllers
│   │   └── main_controller.py    # Logic for handling user interactions
│   ├── models
│   │   └── segmentation_model.py  # Segmentation model for pathological detection
│   ├── views
│   │   └── main_view.py          # UI rendering and display updates
│   └── utils
│       └── tracking_algorithm.py   # Functions for the tracking algorithm
├── requirements.txt              # Project dependencies
├── README.md                     # Project documentation
└── .gitignore                    # Files to ignore in version control
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pyqt-desktop-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage

- Launch the application to access the main window.
- Load angiography data for analysis.
- The application will automatically detect pathological regions and compute the radial wall strain parameters.

## Overview

This application aims to streamline the analysis of angiography data, providing a user-friendly interface for medical professionals to efficiently detect and analyze pathological regions. The integration of machine learning models enhances the accuracy and reliability of the analysis.