import cv2 as cv
import mediapipe as mp
import time

class HandTracker:
    def __init__(self, max_num_hands=2, detection_confidence=0.7, tracking_confidence=0.7):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils

    def get_landmarks(self, frameRGB):
        """Returns list of hand landmarks from RGB frame."""
        return (self.hands.process(frameRGB).multi_hand_landmarks) if (self.hands.process(frameRGB).multi_hand_landmarks) else []

    def draw_landmarks(self, frame, hand_landmarks ,markers=list(range(21))):
        """Draws landmarks and connections on the frame."""
        h, w, _ = frame.shape
        if hand_landmarks :
            for hand_id, handLms in enumerate(hand_landmarks):
                # print(f"Hand {hand_id + 1}: {handLms}")
                for ld_idx, ldm in enumerate(handLms.landmark):
                    if ld_idx in markers:
                        cx, cy = int(ldm.x * w), int(ldm.y * h)
                        cv.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)

# Testing CODE
# def main():
#     prev_frame_time , new_frame_time=0,0
#     capture = cv.VideoCapture(1)
#     tracker = HandTracker()
#     # Set desired width 
#     capture.set(cv.CAP_PROP_FRAME_WIDTH, 640) 

#     # Set desired height
#     capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480) 

#     #Set desired fps
#     desired_fps = 30  
#     capture.set(cv.CAP_PROP_FPS, desired_fps)
#     while True:
#         success, frame = capture.read()
#         if not success:
#             break
#         frame = cv.flip(frame, 1)
        
#      # Calculate FPS
#         new_frame_time = time.time()
#         fps = round(1 / (new_frame_time - prev_frame_time))
#         prev_frame_time = new_frame_time

#         cv.putText(frame,f"FPS :{fps}",(500,420),1,1.2,(255,0,0),3)
        
#         frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

#         hand_landmarks = tracker.get_landmarks(frameRGB)
#         tracker.draw_landmarks(frame, hand_landmarks)
        
#         cv.imshow("Live cam", frame)
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

#     capture.release()
#     cv.destroyAllWindows()

# if __name__ == "__main__":
#     main()