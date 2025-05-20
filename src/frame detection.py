import cv2
from ultralytics import YOLO
import os

# === CONFIG ===
model_path = r'E:\1_Work_Files\Internship - Garuda Aerospace\MSARS\Models\yolov8l.pt'  # Replace with your actual .pt file path
video_path = r'E:\1_Work_Files\Internship - Garuda Aerospace\MSARS\src\swimming aerial view.mp4'  # Make sure this file exists in the current directory

# Check if paths exist
if not os.path.exists(model_path):
    print(f"❌ Model not found at: {model_path}")
    exit()

if not os.path.exists(video_path):
    print(f"❌ Video not found at: {video_path}")
    exit()

# Load model
model = YOLO(model_path)

# Load video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    for box in results.boxes:
        cls_id = int(box.cls[0])
        if cls_id == 0:  # Class 0 = person
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'Person {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("People Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
