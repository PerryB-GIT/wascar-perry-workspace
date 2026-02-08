#!/usr/bin/env python3
"""
Evie Vision - Camera & Screen Capture
Captures images from webcam or screen for context

Usage:
    python evie-vision.py                    # Capture from webcam
    python evie-vision.py --screen           # Capture screen
    python evie-vision.py --save photo.jpg   # Save to file
    python evie-vision.py --preview          # Show preview window
"""

import subprocess
import sys
import argparse
import os
from pathlib import Path
from datetime import datetime

# Install dependencies if needed
def ensure_deps():
    deps = [
        ("cv2", "opencv-python"),
        ("PIL", "Pillow"),
        ("mss", "mss"),
    ]
    for module, package in deps:
        try:
            __import__(module)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

ensure_deps()

import cv2
import mss
import numpy as np
from PIL import Image

def list_cameras():
    """List available camera devices."""
    print("\nSearching for cameras...")
    print("-" * 40)

    available = []
    for i in range(5):  # Check first 5 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                print(f"  [{i}] Camera {i} ({w}x{h})")
                available.append(i)
            cap.release()

    if not available:
        print("  No cameras found.")
    print()
    return available

def capture_webcam(camera_index=0, save_path=None, preview=False):
    """
    Capture image from webcam.

    Args:
        camera_index: Camera device index
        save_path: Path to save image (optional)
        preview: Show preview window before capturing

    Returns:
        numpy array of the image, or None if failed
    """
    print(f"[Evie] Accessing camera {camera_index}...")

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("[Evie] Couldn't open camera.")
        return None

    # Let camera warm up
    for _ in range(10):
        cap.read()

    if preview:
        print("[Evie] Preview mode - press SPACE to capture, Q to cancel")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Mirror the preview
            display = cv2.flip(frame, 1)
            cv2.imshow("Evie Vision - Press SPACE to capture", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space to capture
                break
            elif key == ord('q'):  # Q to cancel
                cap.release()
                cv2.destroyAllWindows()
                print("[Evie] Cancelled.")
                return None

        cv2.destroyAllWindows()

    # Capture frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("[Evie] Couldn't capture image.")
        return None

    print("[Evie] Got it!")

    if save_path:
        cv2.imwrite(save_path, frame)
        print(f"[Evie] Saved to: {save_path}")

    return frame

def capture_screen(monitor=0, save_path=None, region=None):
    """
    Capture screen or region.

    Args:
        monitor: Monitor number (0 = all, 1+ = specific)
        save_path: Path to save image (optional)
        region: Tuple of (left, top, width, height) for partial capture

    Returns:
        numpy array of the image
    """
    print("[Evie] Capturing screen...")

    with mss.mss() as sct:
        if region:
            monitor_area = {
                "left": region[0],
                "top": region[1],
                "width": region[2],
                "height": region[3]
            }
        else:
            monitor_area = sct.monitors[monitor]

        screenshot = sct.grab(monitor_area)

        # Convert to numpy array (BGR format for OpenCV)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    print(f"[Evie] Captured {img.shape[1]}x{img.shape[0]} pixels")

    if save_path:
        cv2.imwrite(save_path, img)
        print(f"[Evie] Saved to: {save_path}")

    return img

def encode_for_api(image, format="jpeg", quality=85):
    """
    Encode image for sending to vision APIs.

    Args:
        image: numpy array or PIL Image
        format: Output format (jpeg, png)
        quality: JPEG quality (1-100)

    Returns:
        Base64-encoded string
    """
    import base64
    import io

    if isinstance(image, np.ndarray):
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

    buffer = io.BytesIO()
    image.save(buffer, format=format.upper(), quality=quality)
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode('utf-8')

def get_timestamp_filename(prefix="evie", ext="jpg"):
    """Generate timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{ext}"

class EvieVision:
    """
    Evie's vision system for capturing and analyzing images.
    """

    def __init__(self, camera_index=0, save_dir=None):
        self.camera_index = camera_index
        self.save_dir = Path(save_dir) if save_dir else Path.home()
        self.last_capture = None

    def look(self, save=False, preview=False):
        """Capture from webcam."""
        save_path = None
        if save:
            save_path = str(self.save_dir / get_timestamp_filename("evie_photo"))

        self.last_capture = capture_webcam(
            camera_index=self.camera_index,
            save_path=save_path,
            preview=preview
        )
        return self.last_capture

    def see_screen(self, save=False, monitor=0):
        """Capture screen."""
        save_path = None
        if save:
            save_path = str(self.save_dir / get_timestamp_filename("evie_screen"))

        self.last_capture = capture_screen(
            monitor=monitor,
            save_path=save_path
        )
        return self.last_capture

    def get_base64(self):
        """Get last capture as base64 for API calls."""
        if self.last_capture is None:
            return None
        return encode_for_api(self.last_capture)

def main():
    parser = argparse.ArgumentParser(description="Evie Vision - Camera & Screen Capture")
    parser.add_argument("--screen", "-s", action="store_true",
                       help="Capture screen instead of webcam")
    parser.add_argument("--save", "-o", type=str, default=None,
                       help="Save image to file")
    parser.add_argument("--preview", "-p", action="store_true",
                       help="Show preview before capturing (webcam only)")
    parser.add_argument("--camera", "-c", type=int, default=0,
                       help="Camera index (default: 0)")
    parser.add_argument("--monitor", "-m", type=int, default=0,
                       help="Monitor number for screen capture (0=all)")
    parser.add_argument("--list-cameras", action="store_true",
                       help="List available cameras")

    args = parser.parse_args()

    if args.list_cameras:
        list_cameras()
        return

    # Generate default save path if not specified but saving
    save_path = args.save
    if save_path is None and not args.preview:
        # Default to saving in home directory
        save_path = str(Path.home() / get_timestamp_filename(
            "evie_screen" if args.screen else "evie_photo"
        ))

    if args.screen:
        capture_screen(monitor=args.monitor, save_path=save_path)
    else:
        capture_webcam(
            camera_index=args.camera,
            save_path=save_path,
            preview=args.preview
        )

if __name__ == "__main__":
    main()
