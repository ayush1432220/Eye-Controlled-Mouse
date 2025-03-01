Eye-Controlled Mouse 🎯
A hands-free mouse control system that enables users to navigate and interact with a computer using eye blinks and facial expressions. This project is designed for accessibility, hands-free computing, and an enhanced user experience.

📌 Features
✅ Single Left-Eye Blink → Click
✅ Double Left-Eye Blink → Double Click
✅ Both Eyes Blink → Exit Program
✅ Smile Detection → Opens a New Tab
✅ Real-time Eye & Face Tracking
✅ Works on Windows/Linux/macOS

🛠️ Technology Stack
Languages: Python
Libraries: OpenCV, Mediapipe, PyAutoGUI, NumPy
🚀 Installation & Setup
1️⃣ Prerequisites
Ensure you have Python installed. Then, install the required dependencies:

bash
Copy
Edit
pip install opencv-python numpy mediapipe pyautogui
2️⃣ Run the Project
bash
Copy
Edit
python eye_controlled_mouse.py
🖥️ How It Works
Face & Eye Detection: Uses OpenCV & Mediapipe to detect the user's face and eyes.
Gesture Recognition:
Detects left-eye blinks for click actions.
Detects double left-eye blinks for double-click.
Detects both eyes blinking to exit the program.
Detects smiling to open a new browser tab.
Cursor & Click Control: Uses PyAutoGUI to simulate mouse interactions.


🛠️ Customization & Settings
Adjust blink sensitivity & detection thresholds in config.py.
Modify gesture actions to customize functionality.
📌 Known Issues & Future Enhancements
❌ Issues
May require good lighting conditions for accurate detection.
Webcam-based tracking may have slight delays compared to infrared tracking.
✅ Future Enhancements
Add gesture-based scrolling and zooming.
Improve blink detection accuracy with machine learning.
Optimize multi-screen support.
