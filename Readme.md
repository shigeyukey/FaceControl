# Face Control for Anki

This addon allows you to control Anki using face movements, providing a hands-free interaction experience. The addon uses a webcam to track facial landmarks and maps specific face movements to Anki actions.

## Features
- **Show answer/Mark as "Good" (Space)**: Look Good.
- **Mark as "Again" (1)**: Look slightly left.
- **Undo (Ctrl+Z)**: Look far left.
- **Scroll**: Move your head up or down to scroll the content.

## Installation
1. Download the addon and extract it into your Anki addons folder:
   - Windows: `C:\Users\<YourUsername>\AppData\Roaming\Anki2\addons21`
   - macOS: `~/Library/Application Support/Anki2/addons21`
   - Linux: `~/.local/share/Anki2/addons21`
2. Ensure the `resources/shape_predictor.dat` file is in the `resources` folder within the addon directory.
3. Restart Anki.

## Usage
1. Open Anki.
2. Navigate to `Tools > Toggle Face Control` to enable or disable the addon.
3. Ensure your webcam is functioning properly.

## Requirements
- Anki 2.1.XX+
- Python 3.9+
- Dependencies:
  - `cv2` (OpenCV)
  - `dlib`
  - `pyautogui`

## Known Issues
- Ensure proper lighting for accurate facial detection.
- Webcam access might conflict with other applications.

## Troubleshooting
- If the addon doesn't work, check the Anki console (`Ctrl+Shift+;)` for error messages.
- Verify that the `shape_predictor.dat` file is correctly placed.

## License
This addon is released under the MIT License.
