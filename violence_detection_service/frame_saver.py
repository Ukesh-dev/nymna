import cv2
import os

from violence_detection_service.settings import get_video_path

cap = cv2.VideoCapture(get_video_path())

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

train_path = os.path.join(os.getcwd(), "train_data/images/train")
val_path = os.path.join(os.getcwd(), "train_data/images/val")
os.makedirs(train_path, exist_ok=True)
os.makedirs(val_path, exist_ok=True)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_rate = 15
frame_count = 0
saved_frames = 0
target_frame_interval = int(fps / frame_rate)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if frame_count % target_frame_interval == 0:
        if saved_frames < 0.8 * total_frames:
            save_path = os.path.join(train_path, f'frame_{frame_count:04d}.jpg')
        else:
            save_path = os.path.join(val_path, f'frame_{frame_count:04d}.jpg')

        cv2.imwrite(save_path, frame)
        saved_frames += 1

    frame_count += 1

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
