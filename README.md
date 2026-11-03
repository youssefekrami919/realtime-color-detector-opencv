# Real-Time Color Detector using OpenCV & NumPy

A robust, real-time color detection and identification application built with Python, OpenCV, and NumPy. Utilizing HSV color space analysis and Region-of-Interest (ROI) spatial averaging, this tool delivers stable, noise-resistant color classification directly from a live webcam feed.

---

## Key Features

- **Noise-Resistant ROI Averaging:** Samples a central $15 \times 15$ pixel region to compute mean color values, preventing high-frequency camera sensor noise and pixel flickering from causing misclassifications.
- **HSV Color Classification:** Evaluates colors in the Hue-Saturation-Value (HSV) color space for illumination-invariant detection compared to standard RGB/BGR.
- **Achromatic & Chromatic Hierarchy:** Prioritizes brightness and saturation checks to reliably separate Black, White, and Gray before evaluating Hue ranges.
- **Dynamic Head-Up Display (HUD):**
  - Displays the identified color name rendered in the actual sampled BGR color.
  - Live readout of real-time $H$, $S$, and $V$ coordinates.
  - Central bounding box and reticle target indicating the exact sampling area.
- **High Resolution:** Configured for 720p HD ($1280 \times 720$) video stream.

---

## How It Works

1. **Capture & Preprocessing:**
   - Frame is captured from the primary webcam (`cv2.VideoCapture(0)`) at 1280x720.
   - The central coordinate $(c_x, c_y)$ is computed based on frame dimensions.

2. **Region-of-Interest (ROI) Extraction:**
   - A $15 \times 15$ pixel bounding box centered at $(c_x, c_y)$ is sliced from both the BGR frame and the converted HSV frame.
   - Mean BGR and HSV values are calculated across this patch.

3. **Color Decision Tree:**
   - **Neutrals / Achromatic Colors (Value & Saturation checks):**
     - **BLACK:** $V < 40$
     - **WHITE:** $S < 45 \text{ and } V > 190$
     - **GRAY:** $S < 45$
   - **Chromatic Colors (Hue thresholding, range 0–179):**
     - **RED:** $H < 8 \text{ or } H \ge 170$ (wraps around 0/180)
     - **ORANGE:** $8 \le H < 22$
     - **YELLOW:** $22 \le H < 35$
     - **GREEN:** $35 \le H < 85$
     - **CYAN:** $85 \le H < 105$
     - **BLUE:** $105 \le H < 135$
     - **VIOLET:** $135 \le H < 155$
     - **PINK:** $155 \le H < 170$

---

## 🎨 Color Classification Range Reference

| Color | Hue ($H$) Range | Saturation ($S$) | Value ($V$) |
| :--- | :--- | :--- | :--- |
| **Black** | Any | Any | $V < 40$ |
| **White** | Any | $S < 45$ | $V > 190$ |
| **Gray** | Any | $S < 45$ | $40 \le V \le 190$ |
| **Red** | $0 \le H < 8$ or $170 \le H \le 179$ | $S \ge 45$ | $V \ge 40$ |
| **Orange**| $8 \le H < 22$ | $S \ge 45$ | $V \ge 40$ |
| **Yellow**| $22 \le H < 35$ | $S \ge 45$ | $V \ge 40$ |
| **Green** | $35 \le H < 85$ | $S \ge 45$ | $V \ge 40$ |
| **Cyan**  | $85 \le H < 105$ | $S \ge 45$ | $V \ge 40$ |
| **Blue**  | $105 \le H < 135$ | $S \ge 45$ | $V \ge 40$ |
| **Violet**| $135 \le H < 155$ | $S \ge 45$ | $V \ge 40$ |
| **Pink**  | $155 \le H < 170$ | $S \ge 45$ | $V \ge 40$ |

---

## Prerequisites & Installation

### Requirements
- Python 3.8+
- Webcam / Camera device

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/realtime-color-detector-opencv.git
cd realtime-color-detector-opencv
```

### 2. (Optional) Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install opencv-python numpy
```

---

## Running the Detector

Run the main script:
```bash
python main.py
```

### Controls
- **Targeting:** Aim the center green crosshair box at the object or surface you want to detect.
- **Exit:** Press the <kbd>ESC</kbd> key to close the window and release the webcam.

---

## 📁 Project Structure

```plaintext
realtime-color-detector-opencv/
├── main.py          # Real-time webcam capture, ROI sampling, and HUD overlay
└── README.md        # Project documentation
```

---

## 💡 Troubleshooting & Tips

- **Camera Not Opening:** If you have multiple cameras (or an external USB webcam), change `cv2.VideoCapture(0)` in [`main.py`](file:///c:/Users/Youssef%20Ekrami/Desktop/Computer%20Vision/realtime-color-detector-opencv/main.py#L5) to index `1` or `2`.
- **Lighting Conditions:** Extreme shadows or harsh glares can shift Hue and Saturation values. For best results, use diffuse lighting.
- **ROI Adjustment:** You can adjust the sampling patch size by modifying `roi_size = 15` in `main.py`.

---


