# Gesture-Volume-Control
Hand Gesture Volume Control using OpenCV, Mediapipe &amp; Pycaw — control your system volume in real time with just your fingers!
# 🖐️ Hand Gesture Volume Control

Control your **system volume** with simple **hand gestures** using **OpenCV**, **MediaPipe**, and **Pycaw**.  
Move your **thumb and index finger** closer/farther to decrease/increase the volume — and when they touch, the system **mutes automatically**.

---

## ✨ Features
- 🎥 Real-time hand tracking with [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/hands).
- 🔊 Smooth system volume control via [Pycaw](https://github.com/AndreMiras/pycaw).
- 🖐️ Works with gestures:
  - **Pinch close → Mute**  
  - **Pinch open → Increase volume**  
  - **Max spread → 100% volume**  
- 📊 On-screen UI with FPS counter & volume bar.  
- ⚡ Optimized with smoothing for stable volume changes.  

---

## 🛠️ Tech Stack
- [Python 3](https://www.python.org/)  
- [OpenCV](https://opencv.org/)  
- [MediaPipe](https://developers.google.com/mediapipe)  
- [Pycaw](https://github.com/AndreMiras/pycaw) (Windows-only for system audio control)  

---

## 🚀 Setup & Usage

# Clone the repository
git clone https://github.com/your-username/HandVolumeControl.git
cd HandVolumeControl

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # On Linux / macOS
# venv\Scripts\activate    # On Windows

# Install requirements
pip install -r requirements.txt

# Run the program
python hand_volume_control.py


# 🎮 Controls
✋ No hands detected → Red warning text

👌 Thumb + Index pinch → Controls system volume

🔴 Touch (0%) → Mute

🟡 Wide (100%) → Max volume

📊 Volume percentage + bar visible on screen

# 📷 Demo
(Add a GIF or screenshot here once you capture your program running)

# ⚠️ Notes
Requires Windows (Pycaw doesn’t support Linux/macOS).

Works best with a well-lit environment and 720p webcam.

Default camera index is 1, change to 0 if needed:

capture = cv.VideoCapture(0)
# 📄 License
MIT License – feel free to use and modify.

# 👨‍💻 Author
Developed with ❤️ by Chetan Kochar
