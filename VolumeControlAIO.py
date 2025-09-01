import cv2 as cv
import math as mt
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from PalmDetection import HandTracker

##################################
max_num_hands = 2
detection_confidence = 0.7
tracking_confidence = 0.7
frame_w = 640
frame_h = 480
fps = 30
markers = [4, 8]  # thumb tip, index tip
##################################

tracker = HandTracker(max_num_hands, detection_confidence, tracking_confidence)

# Initialize camera
capture = cv.VideoCapture(1)
capture.set(cv.CAP_PROP_FPS, fps)
capture.set(cv.CAP_PROP_FRAME_WIDTH, frame_w)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, frame_h)

# Initialize volume control once (not every frame)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# FPS calculation
prevT = 0
fps_smooth = []

# Smooth volume calculation
vol_list = []

while True:
    flag, frame = capture.read()
    if not flag:
        print("Error fetching live footage")
        break

    # Mirror + convert to RGB
    frame = cv.flip(frame, 1)
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Get landmarks
    result = tracker.get_landmarks(frameRGB)

    # FPS calculation with smoothing
    currT = time.time()
    fps_val = 1 / (currT - prevT) if prevT != 0 else 0
    prevT = currT
    fps_smooth.append(fps_val)
    if len(fps_smooth) > 10:
        fps_smooth.pop(0)
    actual_fps = int(sum(fps_smooth) / len(fps_smooth))

    # Draw FPS
    cv.rectangle(frame, (480, 430), (610, 470), (0, 0, 0), -1)
    cv.putText(frame, f"{actual_fps} FPS", (490, 460), cv.FONT_HERSHEY_SIMPLEX,
               0.8, (0, 255, 255), 2, cv.LINE_AA)

    # Process only if valid hand data
    if result and result[0] is not None and hasattr(result[0], "landmark"):
        tracker.draw_landmarks(frame, result, markers)

        # Landmark coordinates
        landmarks = result[0].landmark
        x1, y1 = int(landmarks[4].x * frame_w), int(landmarks[4].y * frame_h)
        x2, y2 = int(landmarks[8].x * frame_w), int(landmarks[8].y * frame_h)

        # Draw control line + midpoint
        cv.line(frame, (x1, y1), (x2, y2), (32, 65, 30), 3)
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        cv.circle(frame, (mid_x, mid_y), 10, (0, 255, 0), -1)

        # Distance between points
        length = round(mt.hypot(x2 - x1, y2 - y1), 1)

        # Clamp length to avoid extreme values
        length = max(15, min(145, length))

        # Volume percentage mapping
        vol = (length - 15) / 1.3
        vol = max(0, min(100, vol))  # clamp 0–100
        # Append the new volume first
        vol_list.append(vol)

        # Keep only the last 10 readings
        if len(vol_list) > 10:
            vol_list.pop(0)

        # Only calculate if we have data
        if vol_list:
            weights = range(1, len(vol_list) + 1)
            avgVol = int(sum(v * w for v, w in zip(vol_list, weights)) / sum(weights))
        else:
            avgVol = 0


        # Set system volume safely
        try:
            if avgVol <= 0:  
                volume.SetMute(1, None)  # mute if zero
            else:
                volume.SetMute(0, None)  # unmute
                volume.SetMasterVolumeLevelScalar(avgVol / 100.0, None) 
        except Exception as e:
            print("[WARN] Volume set failed:", e)
            
        # Status text
        if avgVol <= 0:
            cv.putText(frame, "Muted", (40, 30), cv.FONT_HERSHEY_SIMPLEX,
                       1.2, (0, 0, 255), 3, cv.LINE_AA)
            cv.circle(frame, (mid_x, mid_y), 10, (0, 0 , 255), -1)
            
        elif avgVol >= 100:
            cv.putText(frame, "Max", (40, 30), cv.FONT_HERSHEY_SIMPLEX,
                       1.2, (0, 255, 0), 3, cv.LINE_AA)
            cv.circle(frame, (mid_x, mid_y), 10, (0, 255 , 255), -1)

        # Volume bar
        cv.rectangle(frame, (30, 60), (50, 160), (0, 255, 0), 2)
        cv.rectangle(frame, (21, 28), (75, 52), (0, 0, 0), -1)
        cv.putText(frame, f"{int(avgVol)}%", (28, 50), cv.FONT_HERSHEY_SIMPLEX,
                   0.6, (255, 255, 255), 2, cv.LINE_AA)
        cv.rectangle(frame, (31, 160 - int(avgVol)), (49, 159),
                     (255, 0, 0), -1, cv.LINE_AA)

    else:
        cv.putText(frame, "No Hands Detected", (200, 400),
            cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)


    cv.imshow("Live Cam", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Exiting program")
        break

capture.release()
cv.destroyAllWindows()