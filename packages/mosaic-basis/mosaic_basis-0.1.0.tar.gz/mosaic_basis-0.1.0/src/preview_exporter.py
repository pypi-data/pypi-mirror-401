
import os
import json
from typing import Dict, List, Tuple, Optional

import numpy as np

try:
    import cv2
except Exception as _e:
    cv2 = None

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def _load_image(path: str):
    if cv2 is None:
        raise ImportError("OpenCV (cv2) is required for previews.")
    return cv2.imread(path, cv2.IMREAD_COLOR)

def _put_label(img, text: str, org=(5,20), color=(255,255,255)):
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

def _draw_timeline_seconds(img: np.ndarray, total_sec: float, current_sec: float,
                           active_min_sec: float, active_max_sec: float,
                           key_secs: Optional[List[float]] = None, height: int = 10):
    h, w = img.shape[:2]
    bar_h = max(6, height)
    pad = 2
    y0 = h - bar_h - pad
    x0 = pad
    x1 = w - pad
    cv2.rectangle(img, (x0, y0), (x1, y0 + bar_h), (30, 30, 30), -1)
    length = max(1e-6, total_sec)
    ax0 = x0 + int((max(0.0, active_min_sec) / length) * (x1 - x0))
    ax1 = x0 + int((min(total_sec, active_max_sec) / length) * (x1 - x0))
    cv2.rectangle(img, (ax0, y0), (ax1, y0 + bar_h), (90, 90, 90), -1)
    xp = x0 + int((min(total_sec, max(0.0, current_sec)) / length) * (x1 - x0))
    cv2.line(img, (xp, y0), (xp, y0 + bar_h), (0, 255, 255), 2)
    if key_secs:
        for s in key_secs:
            xk = x0 + int(((min(total_sec, max(0.0, s))) / length) * (x1 - x0))
            cv2.line(img, (xk, y0), (xk, y0 + bar_h), (0, 200, 0), 1)

def export_track_previews(
    frames_dir: str,
    tracklets_json: str,
    omp_results_json: str,
    out_dir: str,
    timestamps_json: Optional[str] = None,
    crop_size: Tuple[int,int]=(256,256),
    fps: int = 15,
    make_keyframe_video: bool = True,
    make_contact_sheet: bool = True,
    contact_sheet_cols: int = 8,
    timeline: bool = True
):
    if cv2 is None:
        raise ImportError("OpenCV (cv2) is required for previews.")

    _ensure_dir(out_dir)

    with open(tracklets_json, "r") as f:
        tracklets = json.load(f)
    with open(omp_results_json, "r") as f:
        summary = json.load(f)
    omp_results = summary.get("omp_results", [])

    ts = None
    frame_files = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.lower().endswith(".png")])
    if not frame_files:
        raise RuntimeError(f"No frames found in {frames_dir}")
    if timestamps_json and os.path.isfile(timestamps_json):
        with open(timestamps_json, "r") as f:
            tsj = json.load(f)
            ts = tsj.get("timestamps_sec", None)

    total_frames = len(frame_files)
    if ts and len(ts) == total_frames:
        total_sec = float(ts[-1]) if ts[-1] > 0 else (total_frames / fps)
    else:
        ts = [i / fps for i in range(total_frames)]
        total_sec = ts[-1]

    support_map: Dict[int, List[int]] = {}
    for r in omp_results:
        s = sorted(r.get("support", []))
        support_map[r["track_id"]] = s

    width, height = crop_size
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    for tid_str, t in tracklets.items():
        tid = int(tid_str)
        frames = t["frames"]
        bboxes = t["bboxes"]
        support_local = support_map.get(tid, [])
        key_secs = [ts[frames[i]] for i in support_local if 0 <= i < len(frames) and 0 <= frames[i] < len(ts)]

        out_path = os.path.join(out_dir, f"track_{tid:04d}.mp4")
        vw = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        keyframe_crops = []

        for local_idx, gfi in enumerate(frames):
            frame_path = frame_files[gfi] if 0 <= gfi < len(frame_files) else None
            if frame_path is None or not os.path.isfile(frame_path):
                continue
            frame_img = _load_image(frame_path)
            H, W = frame_img.shape[:2]
            x, y, w, h = map(int, bboxes[local_idx])
            x0 = max(0, x); y0 = max(0, y)
            x1 = min(W, x + w); y1 = min(H, y + h)
            if x1 <= x0 or y1 <= y0:
                crop = np.zeros((height, width, 3), dtype=np.uint8)
            else:
                crop = frame_img[y0:y1, x0:x1]
                crop = cv2.resize(crop, (width, height), interpolation=cv2.INTER_AREA)

            if local_idx in support_local:
                cv2.rectangle(crop, (0,0), (width-1,height-1), (0,255,0), 3)
                keyframe_crops.append(crop.copy())

            current_sec = ts[gfi]
            _put_label(crop, f"id={tid} t={current_sec:.2f}s")

            if timeline:
                if frames:
                    amin = ts[frames[0]]
                    amax = ts[frames[-1]]
                else:
                    amin = 0.0; amax = 0.0
                _draw_timeline_seconds(crop, total_sec, current_sec, amin, amax, key_secs, height=10)

            vw.write(crop)

        vw.release()

        if make_keyframe_video and keyframe_crops:
            out_kv = os.path.join(out_dir, f"track_{tid:04d}_keyframes.mp4")
            vw2 = cv2.VideoWriter(out_kv, fourcc, fps, (width, height))
            for kcrop in keyframe_crops:
                vw2.write(kcrop)
            vw2.release()

        if make_contact_sheet and keyframe_crops:
            cols = max(1, int(contact_sheet_cols))
            rows = (len(keyframe_crops) + cols - 1) // cols
            sheet = np.zeros((rows*height, cols*width, 3), dtype=np.uint8)
            for i, kcrop in enumerate(keyframe_crops):
                r = i // cols
                c = i % cols
                y0 = r*height; x0 = c*width
                sheet[y0:y0+height, x0:x0+width] = kcrop
            out_png = os.path.join(out_dir, f"track_{tid:04d}_keyframes.png")
            cv2.imwrite(out_png, sheet)

    return {"out_dir": out_dir}

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser("preview_exporter")
    p.add_argument("--frames-dir", required=True)
    p.add_argument("--tracklets-json", required=True)
    p.add_argument("--omp-results-json", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--timestamps-json", default=None, help="frames_timestamps.json with timestamps_sec")
    p.add_argument("--w", type=int, default=256)
    p.add_argument("--h", type=int, default=256)
    p.add_argument("--fps", type=int, default=15)
    p.add_argument("--no-keyframe-video", action="store_true")
    p.add_argument("--no-contact-sheet", action="store_true")
    p.add_argument("--cols", type=int, default=8)
    p.add_argument("--no-timeline", action="store_true")
    args = p.parse_args()

    res = export_track_previews(
        frames_dir=args.frames_dir,
        tracklets_json=args.tracklets_json,
        omp_results_json=args.omp_results_json,
        out_dir=args.out_dir,
        timestamps_json=args.timestamps_json,
        crop_size=(args.w, args.h),
        fps=args.fps,
        make_keyframe_video=(not args.no_keyframe_video),
        make_contact_sheet=(not args.no_contact_sheet),
        contact_sheet_cols=args.cols,
        timeline=(not args.no_timeline)
    )
    print(json.dumps(res, indent=2))
