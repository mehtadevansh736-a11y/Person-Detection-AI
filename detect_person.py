"""Person detection using pretrained Ultralytics YOLO26.

Detects people in an image/video/webcam and saves annotated results.
Runs on CUDA GPU automatically if available.

Usage:
    python detect_person.py <image_or_video_path> [model]
      model: n (nano), s (small - default), m (medium)
    python detect_person.py 0 s        # live webcam with small model
"""
import sys
from pathlib import Path

import torch
from ultralytics import YOLO

PERSON_CLASS_ID = 0  # COCO class 0 = person
MODEL_FILES = {"n": "yolo26n.pt", "s": "yolo26s.pt", "m": "yolo26m.pt"}


def detect(source, model_key="s"):
    model_path = Path(__file__).parent / MODEL_FILES[model_key]
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Model: {model_path.name} | Device: {device}"
          + (f" ({torch.cuda.get_device_name(0)})" if device.startswith("cuda") else ""))

    is_live = isinstance(source, int) or str(source).endswith(
        (".mp4", ".avi", ".mkv", ".mov", ".webm"))
    if is_live:
        print("Live mode: press Q in the video window to quit.")

    model = YOLO(str(model_path))
    results = model.predict(source, save=True, show=is_live, conf=0.35,
                            classes=[PERSON_CLASS_ID], device=device)

    for r in results:
        boxes = r.boxes
        persons = [(float(conf)) for conf in boxes.conf]
        print(f"\rPersons in frame: {len(persons)}   ", end="", flush=is_live)
        if not is_live:
            print()
            for i, conf in enumerate(persons, 1):
                print(f"  Person {i}: confidence {conf:.2f}")
    annotated = results[0].save_dir
    print(f"\nAnnotated output saved to: {annotated}")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "https://ultralytics.com/images/bus.jpg"
    if str(src).isdigit():
        src = int(src)  # webcam index
    key = sys.argv[2].lower() if len(sys.argv) > 2 else "s"
    if key not in MODEL_FILES:
        sys.exit(f"Unknown model '{key}'. Use n, s, or m.")
    detect(src, key)
