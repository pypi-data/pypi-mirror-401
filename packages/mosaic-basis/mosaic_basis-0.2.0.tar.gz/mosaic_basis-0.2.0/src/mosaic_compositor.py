import json
import os
from typing import Optional

import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None  # type: ignore[assignment]


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _load_image(path: str) -> Optional[np.ndarray]:
    if cv2 is None:
        raise ImportError("OpenCV (cv2) is required for mosaic composition.")
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img


def _draw_border(
    img: np.ndarray, color: tuple[int, int, int] = (0, 255, 255), thickness: int = 3
) -> None:
    h, w = img.shape[:2]
    cv2.rectangle(img, (0, 0), (w - 1, h - 1), color, thickness)


def _put_label(
    img: np.ndarray,
    text: str,
    org: tuple[int, int] = (5, 20),
    color: tuple[int, int, int] = (255, 255, 255),
) -> None:
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)


def _draw_timeline_seconds(
    img: np.ndarray,
    total_sec: float,
    current_sec: float,
    active_min_sec: float,
    active_max_sec: float,
    key_secs: Optional[list[float]] = None,
    height: int = 10,
) -> None:
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


def compose_mosaic(
    frames_dir: str,
    tracklets_json: str,
    omp_results_json: str,
    out_video_path: str,
    frames_timestamps_json: Optional[str] = None,
    grid_rows: int = 2,
    grid_cols: int = 2,
    tile_w: int = 256,
    tile_h: int = 256,
    fps: int = 15,
    highlight_keyframes: bool = True,
    timeline: bool = True,
) -> dict[str, object]:
    if cv2 is None:
        raise ImportError("OpenCV (cv2) is required for mosaic composition.")

    with open(tracklets_json) as f:
        tracklets = json.load(f)
    with open(omp_results_json) as f:
        summary = json.load(f)
    omp_results = summary.get("omp_results", [])

    # timestamps (seconds)
    ts = None
    if frames_timestamps_json and os.path.isfile(frames_timestamps_json):
        with open(frames_timestamps_json) as f:
            tsj = json.load(f)
            ts = tsj.get("timestamps_sec", None)

    frame_files = sorted(
        [
            os.path.join(frames_dir, f)
            for f in os.listdir(frames_dir)
            if f.lower().endswith(".png")
        ]
    )
    if not frame_files:
        raise RuntimeError(f"No frames found in {frames_dir}")
    total_frames = len(frame_files)
    if ts and len(ts) == total_frames:
        total_sec = float(ts[-1]) if ts[-1] > 0 else (total_frames / fps)
    else:
        ts = [i / fps for i in range(total_frames)]
        total_sec = ts[-1]

    support_map_local: dict[int, set] = {}
    for r in omp_results:
        support_map_local[r["track_id"]] = set(r.get("support", []))

    track_ids = sorted([int(k) for k in tracklets.keys()])
    max_tiles = grid_rows * grid_cols
    selected_ids = track_ids[:max_tiles]

    per_track_maps: dict[int, dict[int, tuple[tuple[int, int, int, int], int]]] = {}
    active_span_sec: dict[int, tuple[float, float]] = {}
    key_secs_map: dict[int, list[float]] = {}

    for tid in selected_ids:
        t = tracklets[str(tid)]
        mapping = {}
        gfis = t["frames"]
        bbs = t["bboxes"]
        for local_idx, gfi in enumerate(gfis):
            mapping[gfi] = (tuple(bbs[local_idx]), local_idx)
        per_track_maps[tid] = mapping
        if gfis:
            amin = ts[gfis[0]]
            amax = ts[gfis[-1]]
        else:
            amin = 0.0
            amax = 0.0
        active_span_sec[tid] = (amin, amax)
        k_local = support_map_local.get(tid, set())
        key_secs = []
        for local_idx, gfi in enumerate(gfis):
            if local_idx in k_local:
                key_secs.append(ts[gfi])
        key_secs_map[tid] = key_secs

    mosaic_w = grid_cols * tile_w
    mosaic_h = grid_rows * tile_h
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # type: ignore[attr-defined]
    out = cv2.VideoWriter(out_video_path, fourcc, fps, (mosaic_w, mosaic_h))

    black_tile = np.zeros((tile_h, tile_w, 3), dtype=np.uint8)
    border_color = (0, 255, 255)

    for global_idx, frame_path in enumerate(frame_files):
        frame_img = _load_image(frame_path)
        if frame_img is None:
            continue
        H, W = frame_img.shape[:2]
        current_sec = ts[global_idx]

        mosaic = np.zeros((mosaic_h, mosaic_w, 3), dtype=np.uint8)
        tile_i = 0
        for r in range(grid_rows):
            for c in range(grid_cols):
                if tile_i >= len(selected_ids):
                    tile = black_tile.copy()
                else:
                    tid = selected_ids[tile_i]
                    mapping = per_track_maps[tid]
                    if global_idx in mapping:
                        bbox, local_idx = mapping[global_idx]
                        x, y, w, h = bbox
                        x0 = max(0, x)
                        y0 = max(0, y)
                        x1 = min(W, x + w)
                        y1 = min(H, y + h)
                        if x1 > x0 and y1 > y0:
                            crop = frame_img[y0:y1, x0:x1]
                            tile = cv2.resize(
                                crop, (tile_w, tile_h), interpolation=cv2.INTER_AREA
                            )
                        else:
                            tile = black_tile.copy()
                        if highlight_keyframes and (
                            local_idx in support_map_local.get(tid, set())
                        ):
                            _draw_border(tile, color=border_color, thickness=3)
                        _put_label(tile, f"id={tid} t={current_sec:.2f}s")
                    else:
                        tile = black_tile.copy()

                    if timeline:
                        amin, amax = active_span_sec.get(tid, (0.0, 0.0))
                        _draw_timeline_seconds(
                            tile,
                            total_sec,
                            current_sec,
                            amin,
                            amax,
                            key_secs_map.get(tid, []),
                            height=10,
                        )

                y_start = r * tile_h
                x_start = c * tile_w
                mosaic[y_start : y_start + tile_h, x_start : x_start + tile_w] = tile
                tile_i += 1

        out.write(mosaic)

    out.release()
    return {
        "out_video": out_video_path,
        "grid_rows": grid_rows,
        "grid_cols": grid_cols,
        "tile_w": tile_w,
        "tile_h": tile_h,
        "fps": fps,
    }


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser("mosaic_compositor")
    p.add_argument("--frames-dir", required=True)
    p.add_argument("--tracklets-json", required=True)
    p.add_argument("--omp-results-json", required=True)
    p.add_argument("--out", required=True)
    p.add_argument(
        "--timestamps-json",
        default=None,
        help="frames_timestamps.json with timestamps_sec",
    )
    p.add_argument("--rows", type=int, default=2)
    p.add_argument("--cols", type=int, default=2)
    p.add_argument("--tile-w", type=int, default=256)
    p.add_argument("--tile-h", type=int, default=256)
    p.add_argument("--fps", type=int, default=15)
    p.add_argument("--no-highlight", action="store_true")
    p.add_argument("--no-timeline", action="store_true")
    args = p.parse_args()

    res = compose_mosaic(
        args.frames_dir,
        args.tracklets_json,
        args.omp_results_json,
        args.out,
        frames_timestamps_json=args.timestamps_json,
        grid_rows=args.rows,
        grid_cols=args.cols,
        tile_w=args.tile_w,
        tile_h=args.tile_h,
        fps=args.fps,
        highlight_keyframes=(not args.no_highlight),
        timeline=(not args.no_timeline),
    )
    print(json.dumps(res, indent=2))
