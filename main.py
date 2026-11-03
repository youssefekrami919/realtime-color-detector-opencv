import cv2
import numpy as np

# Initialize camera capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    cx = int(width / 2)
    cy = int(height / 2)

    # 1. Sample a 15x15 pixel Region of Interest (ROI) at the center to minimize sensor noise
    roi_size = 15
    half_roi = roi_size // 2
    roi_bgr = frame[cy - half_roi : cy + half_roi + 1, cx - half_roi : cx + half_roi + 1]

    # Calculate average BGR values for the center region
    avg_b = int(np.mean(roi_bgr[:, :, 0]))
    avg_g = int(np.mean(roi_bgr[:, :, 1]))
    avg_r = int(np.mean(roi_bgr[:, :, 2]))

    # Convert frame to HSV and compute average values for the same ROI
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi_hsv = hsv_frame[cy - half_roi : cy + half_roi + 1, cx - half_roi : cx + half_roi + 1]

    h = int(np.mean(roi_hsv[:, :, 0]))  # Hue: color tone (0 - 179)
    s = int(np.mean(roi_hsv[:, :, 1]))  # Saturation: color intensity (0 - 255)
    v = int(np.mean(roi_hsv[:, :, 2]))  # Value: brightness (0 - 255)

    # 2. Determine color (evaluate brightness/saturation first for neutrals, then hue)
    if v < 40:
        color = "BLACK"
    elif s < 45 and v > 190:
        color = "WHITE"
    elif s < 45:
        color = "GRAY"
    else:
        # Determine chromatic colors by Hue range
        if h < 8 or h >= 170:
            color = "RED"
        elif h < 22:
            color = "ORANGE"
        elif h < 35:
            color = "YELLOW"
        elif h < 85:
            color = "GREEN"
        elif h < 105:
            color = "CYAN"
        elif h < 135:
            color = "BLUE"
        elif h < 155:
            color = "VIOLET"
        elif h < 170:
            color = "PINK"
        else:
            color = "UNDEFINED"

    # 3. Render HUD and results
    # Header panel background and border
    cv2.rectangle(frame, (cx - 240, 15), (cx + 240, 115), (255, 255, 255), -1)
    cv2.rectangle(frame, (cx - 240, 15), (cx + 240, 115), (0, 0, 0), 2)

    # Display detected color name using the sampled BGR color, alongside live HSV values
    cv2.putText(frame, color, (cx - 220, 75), cv2.FONT_HERSHEY_SIMPLEX, 2, (avg_b, avg_g, avg_r), 4)
    cv2.putText(frame, f"H:{h} S:{s} V:{v}", (cx - 220, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 50), 2)

    # Draw center sampling boundary box and center target point
    cv2.rectangle(frame, (cx - half_roi, cy - half_roi), (cx + half_roi, cy + half_roi), (0, 255, 0), 1)
    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)

    cv2.imshow("Accurate Color Detector", frame)

    # Exit on ESC key press
    if cv2.waitKey(1) == 27:
        break

# Release hardware and close all active windows
cap.release()
cv2.destroyAllWindows()