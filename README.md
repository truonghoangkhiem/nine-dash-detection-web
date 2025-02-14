# Nine-Dash Detection System

## Overview

This project aims to detect the "nine-dash" line in images or videos using YOLOv5. The backend is built with FastAPI, and the frontend is developed with HTML, CSS, and JavaScript. The system allows users to upload images or videos, process them for the nine-dash detection, and display the results with a confidence threshold set by the user. The project also includes testing the API endpoints using Postman.

## Features

- **Nine-Dash Detection**: Using YOLOv5, the system is capable of detecting the nine-dash line in images or videos.
- **Frontend**: The frontend is built with HTML, CSS, and JavaScript to provide an interactive user interface.
- **Backend**: The backend is built using FastAPI to handle file uploads, predictions, and serving the results.
- **Confidence Control**: Users can adjust the minimum confidence level to filter out less certain predictions.
- **Image and Video Support**: The system supports both image and video uploads for nine-dash detection.
- **API Testing**: The backend APIs are tested using Postman.

## Technology Stack

- **YOLOv5**: For object detection.
- **FastAPI**: A fast web framework for building the API backend.
- **Postman**: For testing the backend API endpoints.
- **HTML, CSS, JS**: For the frontend development.
- **OpenCV**: For handling video processing.

## Backend Setup

### Requirements

- Python 3.7+
- FastAPI
- PyTorch (for YOLOv5)
- OpenCV
- Uvicorn

### Installation

1. Install the necessary Python libraries:

```bash
pip install fastapi uvicorn torch opencv-python
