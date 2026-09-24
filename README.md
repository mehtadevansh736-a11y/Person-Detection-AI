# Person-Detection-AI

Real-time person detection in images, videos and live webcam feed using pretrained Ultralytics YOLO26.

![Python 3.11](https://img.shields.io/badge/python-3.11-blue)
![Ultralytics 8.4.126](https://img.shields.io/badge/ultralytics-8.4.126-orange)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

## Features

- Person detection using YOLO26 nano / small / medium weights pretrained on COCO
- Person-only filtering (COCO class 0), other classes ignored
- Supports image files, video files and webcam input in a single script
- Automatic device selection (CUDA if available, otherwise CPU)
- Annotated results saved to `runs/detect/predict*/`
- Per-person confidence scores printed to terminal
- Windows batch launcher included
- VS Code launch configurations included

## Model Details

- Model family: Ultralytics YOLO26
- Type: Single-stage object detector
- Pretrained on: COCO dataset (80 classes)
- Task: Detection with bounding boxes and confidence scores
- Class used: 0 (person), filtered with `classes=[0]`
- Confidence threshold: 0.35
- Device: `cuda:0` if `torch.cuda.is_available()` else `cpu`
- Inference: `ultralytics.YOLO.predict(save=True, show=is_live)`

### Included Weights

| Model | File | Size | Notes |
|-------|------|------|-------|
| Nano | `yolo26n.pt` | 5.5 MB | Fastest, suitable for CPU and webcam |
| Small (default) | `yolo26s.pt` | 20.4 MB | Balanced speed and accuracy |
| Medium | `yolo26m.pt` | 44.2 MB | Higher accuracy, slower inference |

All three weight files are included in the repository so the project runs offline.

### How It Works

1. Load selected `yolo26*.pt` weight with `ultralytics.YOLO`
2. Select device based on CUDA availability
3. Run `model.predict(source, classes=[0], conf=0.35)`
4. Draw bounding boxes and save annotated output to `runs/detect/predict*/`
5. For video/webcam input, display live window (press Q to quit)
6. Print person count and confidence per detection

## Project Structure

```
Person-Detection-AI/
├── detect_person.py            # Main detection script
├── run_person_detection.bat    # Windows launcher
├── yolo26n.pt                  # Nano weights
├── yolo26s.pt                  # Small weights (default)
├── yolo26m.pt                  # Medium weights
├── bus.jpg                     # Sample test image
├── requirements.txt
├── .gitignore
├── README.md
├── LICENSE
├── .vscode/
│   ├── launch.json
│   └── settings.json
└── runs/detect/predict*/       # Generated output (not tracked)
```

`detect_person.py` contains `detect(source, model_key)` and CLI handling. Use `0` as source for webcam.

## Installation

### Prerequisites

- Python 3.10 or 3.11 ([download](https://www.python.org/downloads/))
- Git ([download](https://git-scm.com/downloads))
- Windows, macOS or Linux
- Optional: NVIDIA GPU with CUDA for faster inference, webcam for live mode

### Windows

```powershell
git clone https://github.com/mehtadevansh736-a11y/Person-Detection-AI.git
cd Person-Detection-AI

python -m venv venv
.\venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python detect_person.py bus.jpg s
```

### macOS / Linux

```bash
git clone https://github.com/mehtadevansh736-a11y/Person-Detection-AI.git
cd Person-Detection-AI

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python detect_person.py bus.jpg s
```

### GPU Support (NVIDIA)

The default install works on CPU. For CUDA:

```powershell
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
python -c "import torch; print(torch.cuda.is_available())"
```

Tested with `torch 2.13.0+cu130`, CUDA 13.0, `ultralytics 8.4.126`.

## Usage

Detect in an image:

```powershell
python detect_person.py bus.jpg s
python detect_person.py C:\Photos\crowd.jpg m
python detect_person.py https://ultralytics.com/images/bus.jpg
```

Detect in a video:

```powershell
python detect_person.py myvideo.mp4 s
```

Output is saved under `runs/detect/predict*/`.

Live webcam detection:

```powershell
python detect_person.py 0 s
python detect_person.py 0 n
```

Press Q in the video window to quit.

Switch models with the second argument:

| Command | Description |
|---------|-------------|
| `python detect_person.py bus.jpg n` | Nano, fastest |
| `python detect_person.py bus.jpg s` | Small, default |
| `python detect_person.py bus.jpg m` | Medium, most accurate |

Windows launcher:

```bat
run_person_detection.bat bus.jpg s
run_person_detection.bat 0 s
run_person_detection.bat myvideo.mp4 m
```

VS Code: open the folder and press F5. Available configs are demo image, webcam, and active file.

## Sample Output

```text
Model: yolo26s.pt | Device: cuda:0 (NVIDIA GeForce RTX 4060)
Persons in frame: 3
  Person 1: confidence 0.92
  Person 2: confidence 0.88
  Person 3: confidence 0.71

Annotated output saved to: runs/detect/predict3
```

Output directories are auto-incremented (`predict`, `predict2`, ...) and excluded from git.

## Dependencies

| Package | Tested Version | Purpose |
|---------|----------------|---------|
| python | 3.11.15 | Runtime |
| ultralytics | 8.4.126 | YOLO26 model and inference |
| torch | 2.13.0+cu130 | Deep learning backend |
| torchvision | 0.28.0+cu130 | Vision utilities |
| opencv-python | 5.0.0.93 | Video and webcam handling |
| numpy | 2.4.6 | Array operations |
| pillow | 12.3.0 | Image I/O |
| matplotlib | 3.11.1 | Plotting dependency |
| pyyaml | 6.0.3 | Config parsing |

See `requirements.txt` for the full list. Install with `pip install -r requirements.txt`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `torch.cuda.is_available()` returns False | Expected on CPU-only machines, the script falls back to CPU. Install the CUDA build of torch for GPU use |
| Webcam does not open | Close other apps using the camera, try index `1` instead of `0`, check OS camera privacy settings |
| Slow inference | Use the nano model (`n`), or reduce input resolution |
| `yolo26s.pt not found` | Run from the project root directory, keep the script next to the `.pt` files |
| `ModuleNotFoundError: ultralytics` | Activate the virtual environment and run `pip install -r requirements.txt` |
| Video window does not close | Press Q while the OpenCV window is focused |
| `cv2.imshow` error on macOS | Install OpenCV via brew, or use image mode which does not require display |

## Acknowledgements

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLO and pretrained weights
- [PyTorch](https://pytorch.org/) for the deep learning backend
- [OpenCV](https://opencv.org/) for video handling
- Sample image `bus.jpg` from Ultralytics

## License

MIT License. See `LICENSE`.

## Author

Devansh Mehta — [@mehtadevansh736-a11y](https://github.com/mehtadevansh736-a11y)
