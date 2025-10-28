import os
import sys
import glob
import cv2
import torch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_PATH = os.path.join(BASE_DIR, 'bin', 'best.pt')
INPUT_DIR = os.path.join(BASE_DIR, 'test_images')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_images')

ALLOWED_CLASS_NAMES = {
    'car', 'bus', 'truck', 'motorcycle', 'motorbike', 'bike', 'bicycle', 'rickshaw'
}

CONF_THRESHOLD = float(os.environ.get('YOLO_CONF', 0.3))


def load_model(weights: str):
    try:
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights, force_reload=False)
        model.conf = CONF_THRESHOLD 
        return model
    except Exception as e:
        print('ERROR: torch.hub failed to load YOLOv5 model:', e, file=sys.stderr)
        sys.exit(1)


def main():
    if not os.path.exists(WEIGHTS_PATH):
        print(f'ERROR: Weights not found at {WEIGHTS_PATH}', file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(INPUT_DIR):
        print(f'ERROR: Input directory not found: {INPUT_DIR}', file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    model = load_model(WEIGHTS_PATH)

    exts = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
    image_paths = []
    for ext in exts:
        image_paths.extend(glob.glob(os.path.join(INPUT_DIR, ext)))

    if not image_paths:
        print(f'No images found in {INPUT_DIR}. Supported: {", ".join(exts)}')
        return

    print(f'Found {len(image_paths)} image(s). Running YOLOv5 detection (conf>={CONF_THRESHOLD}) ...')

    processed = 0
    for img_path in sorted(image_paths):
        img = cv2.imread(img_path)
        if img is None:
            print(f'WARN: Failed to read image: {img_path}', file=sys.stderr)
            continue

        try:
            results = model(img)  
        except Exception as e:
            print(f'ERROR: Inference failed for {img_path}: {e}', file=sys.stderr)
            continue

        try:
            df = results.pandas().xyxy[0]
        except Exception:
            out_path = os.path.join(OUTPUT_DIR, 'output_' + os.path.basename(img_path))
            cv2.imwrite(out_path, img)
            print('Saved (no detections):', out_path)
            processed += 1
            continue

        if df is None or df.empty:
            out_path = os.path.join(OUTPUT_DIR, 'output_' + os.path.basename(img_path))
            cv2.imwrite(out_path, img)
            print('Saved (no detections):', out_path)
            processed += 1
            continue

        for _, row in df.iterrows():
            name = str(row.get('name', '')).lower()
            if name == 'motorbike':
                name = 'motorcycle'
            if name not in ALLOWED_CLASS_NAMES:
                continue
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            conf = float(row['confidence']) if 'confidence' in row else None
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = name
            if conf is not None:
                label += f' {conf:.2f}'
            cv2.putText(img, label, (x1, max(0, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        out_path = os.path.join(OUTPUT_DIR, 'output_' + os.path.basename(img_path))
        cv2.imwrite(out_path, img)
        print('Saved:', out_path)
        processed += 1

    print(f'Done! Processed {processed} image(s). Outputs in: {OUTPUT_DIR}')


if __name__ == '__main__':
    main()
