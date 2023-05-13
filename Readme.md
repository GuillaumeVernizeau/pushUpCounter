# Pushup Counter

This Python script uses the Mediapipe library and OpenCV to detect pushup exercises in real-time using a webcam. It counts the number of completed pushups and displays the count on the video feed.

## Requirements

To run this script, you need to have the following dependencies installed:

- Python 3
- OpenCV (`pip install opencv-python`)
- Mediapipe (`pip install mediapipe`)

## Usage

1. Make sure you have a webcam connected to your computer.
2. Install the required dependencies using pip.
3. Save the script to a file, e.g., `pushup_counter.py`.
4. Open a terminal or command prompt and navigate to the directory where the script is saved.
5. Run the script by executing the following command:
```bash
    python pushup_counter.py
```
or
```bash
    ./pushup_counter.py
```
6. A window will open showing the webcam feed with pushup detection and counting.
7. To quit the script, press 'q' on your keyboard.
8. To reset the pushup count, press 'r' on your keyboard.

Note: The script requires a clear view of the user's elbows and mouth to accurately detect pushup movements. Make sure the lighting conditions are suitable for proper detection.

Feel free to modify and improve the code according to your needs. Happy pushup!
