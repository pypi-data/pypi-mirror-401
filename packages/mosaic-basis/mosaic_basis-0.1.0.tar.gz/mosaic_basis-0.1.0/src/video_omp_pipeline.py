
import argparse
import os
import sys
import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional

import numpy as np

try:
    import cv2
except Exception as _e:
    cv2 = None

try:
    from sklearn.linear_model import OrthogonalMatchingPursuit
except Exception as _e:
    OrthogonalMatchingPursuit = None

try:
    from temporal_omp_aug import augment_dictionary_framewise
except Exception as _e:
    augment_dictionary_framewise = None

try:
    from yt_dlp import YoutubeDL
except Exception as _e:
    YoutubeDL = None


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _is_tool_available(cmd: str) -> bool:
    try:
        subprocess.run([cmd, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return True
    except Exception:
        return False


def _bgr_to_ycbcr_mean(img_bgr: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    x, y, w, h = bbox
    H, W = img_bgr.shape[:2]
    x0 = max(0, x); y0 = max(0, y)
    x1 = min(W, x + w); y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        roi = img_bgr
    else:
        roi = img_bgr[y0:y1, x0:x1]

    ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
    mean_ycrcb = ycrcb.reshape(-1, 3).mean(axis=0)
    Y, Cr, Cb = mean_ycrcb.tolist()
    return np.array([Y, Cb, Cr], dtype=float)


def _ffprobe_timestamps(video_path: str) -> Optional[List[float]]:
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "frame=best_effort_timestamp_time",
            "-of", "csv=p=0",
            video_path
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True)
        if proc.returncode != 0:
            return None
        lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
        ts = []
        for ln in lines:
            try:
                ts.append(float(ln))
            except:
                pass
        return ts if ts else None
    except Exception:
        return None


def _opencv_timestamps(video_path: str, stride: int = 1) -> Optional[List[float]]:
    if cv2 is None:
        return None
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    idx = 0
    ts = []
    while True:
        ok = cap.grab()
        if not ok:
            break
        if idx % stride == 0:
            msec = cap.get(cv2.CAP_PROP_POS_MSEC)
            ts.append(float(msec) / 1000.0)
        idx += 1
    cap.release()
    return ts if ts else None


def _timestamps_for_extracted_frames(video_path: str, out_count: int, fps: Optional[float], stride: int) -> List[float]:
    ts = None
    if _is_tool_available("ffprobe"):
        ts = _ffprobe_timestamps(video_path)
    if ts is None:
        ts = _opencv_timestamps(video_path, stride=stride)
    if ts is None:
        if fps and fps > 0:
            ts = [i / fps for i in range(out_count)]
        else:
            ts = [i / 30.0 for i in range(out_count)]
    if len(ts) >= out_count:
        return ts[:out_count]
    if ts:
        last = ts[-1]
    else:
        last = 0.0
    while len(ts) < out_count:
        ts.append(last)
    return ts


def download_video_with_ytdlp(
    url: str,
    out_path: str,
    *,
    max_height: int = 360,
    overwrite: bool = True,
) -> str:
    """Download a remote clip via yt-dlp and return the resulting path."""
    if YoutubeDL is None:
        raise ImportError("yt-dlp is not installed. Install with 'pip install mosaic-basis[yt]'.")

    if not url:
        raise ValueError("URL must be provided to download_video_with_ytdlp.")

    final_path = out_path
    root, ext = os.path.splitext(final_path)
    if not ext:
        final_path = f"{final_path}.mp4"
    out_dir = os.path.dirname(final_path) or "."
    _ensure_dir(out_dir)

    if os.path.exists(final_path):
        if not overwrite:
            return final_path
        os.remove(final_path)

    format_selector = f"mp4[height<={max_height}]/mp4/best"
    ydl_opts = {
        "format": format_selector,
        "quiet": True,
        "noprogress": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "outtmpl": final_path,
        "merge_output_format": "mp4",
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if not os.path.isfile(final_path):
        raise RuntimeError(f"yt-dlp did not produce the expected file at {final_path}")

    return final_path


def save_to_dir(
    video_path: str,
    out_dir: str,
    fps: Optional[float] = None,
    stride: int = 1,
    method: str = "auto",
    overwrite: bool = True,
) -> Tuple[List[str], List[float]]:
    if overwrite and os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    _ensure_dir(out_dir)

    use_ffmpeg = False
    if method == "ffmpeg" or (method == "auto" and _is_tool_available("ffmpeg")):
        use_ffmpeg = True

    frames = []
    if use_ffmpeg:
        vf = []
        if fps is not None:
            vf.append(f"fps={fps}")
        filter_arg = ",".join(vf) if vf else "fps=fps=30"
        out_pattern = os.path.join(out_dir, "frame_%06d.png")
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", filter_arg, out_pattern]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {proc.stderr.decode('utf-8', errors='ignore')}")
        frames = sorted([os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.lower().endswith(".png")])
        timestamps = _timestamps_for_extracted_frames(video_path, len(frames), fps=fps, stride=stride)
    else:
        if cv2 is None:
            raise ImportError("OpenCV not available; cannot use 'opencv' extraction. Install ffmpeg or opencv-python.")
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video: {video_path}")
        idx = 0
        frame_idx = 0
        timestamps = []
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if idx % stride == 0:
                out_path = os.path.join(out_dir, f"frame_{frame_idx:06d}.png")
                cv2.imwrite(out_path, frame)
                frames.append(out_path)
                msec = cap.get(cv2.CAP_PROP_POS_MSEC)
                timestamps.append(float(msec) / 1000.0)
                frame_idx += 1
            idx += 1
        cap.release()

        if not timestamps:
            timestamps = _timestamps_for_extracted_frames(video_path, len(frames), fps=fps, stride=stride)

    return frames, timestamps


from dataclasses import dataclass

@dataclass
class Tracklet:
    track_id: int
    frames: List[int]
    bboxes: List[Tuple[int,int,int,int]]
    ycbcr_series: List[List[float]]

def _create_tracker(tracker_type: str = "CSRT"):
    if cv2 is None:
        raise ImportError("OpenCV not available; trackers require OpenCV.")
    t = tracker_type.upper()
    if t == "KCF":
        return cv2.TrackerKCF_create()
    if t == "CSRT":
        return cv2.TrackerCSRT_create()
    if t == "MOSSE":
        return cv2.TrackerMOSSE_create()
    if t == "MIL":
        return cv2.TrackerMIL_create()
    return cv2.TrackerCSRT_create()

def _bbox_iou(a: Tuple[int,int,int,int], b: Tuple[int,int,int,int]) -> float:
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    ax2, ay2 = ax+aw, ay+ah
    bx2, by2 = bx+bw, by+bh
    inter_x1, inter_y1 = max(ax, bx), max(ay, by)
    inter_x2, inter_y2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0, inter_x2 - inter_x1), max(0, inter_y2 - inter_y1)
    inter = iw * ih
    if inter == 0:
        return 0.0
    union = aw*ah + bw*bh - inter
    return inter / union if union > 0 else 0.0

def detect_and_track(
    video_path: str,
    min_track_len: int = 10,
    tracker_type: str = "CSRT",
    init_every_n: int = 30,
    bg_history: int = 300,
    var_threshold: float = 16.0,
    detect_area_thresh: int = 400,
) -> Dict[int, Tracklet]:
    if cv2 is None:
        raise ImportError("OpenCV not available; cannot track. Install opencv-python.")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fgbg = cv2.createBackgroundSubtractorMOG2(history=bg_history, varThreshold=var_threshold, detectShadows=False)

    trackers = {}
    next_id = 1
    tracklets: Dict[int, Tracklet] = {}

    frame_idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if frame_idx % init_every_n == 0:
            mask = fgbg.apply(frame)
            mask = cv2.medianBlur(mask, 5)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            dets = []
            for c in contours:
                x, y, w, h = cv2.boundingRect(c)
                if w * h >= detect_area_thresh:
                    dets.append((x, y, w, h))

            for (x, y, w, h) in dets:
                new_box = (x, y, w, h)
                too_close = False
                for tid, (_tr, last_bbox) in trackers.items():
                    iou = _bbox_iou(new_box, last_bbox)
                    if iou > 0.3:
                        too_close = True
                        break
                if not too_close:
                    tr = _create_tracker(tracker_type)
                    tr.init(frame, new_box)
                    trackers[next_id] = (tr, new_box)
                    tracklets[next_id] = Tracklet(track_id=next_id, frames=[], bboxes=[], ycbcr_series=[])
                    next_id += 1

        to_remove = []
        for tid, (tr, last_bbox) in list(trackers.items()):
            ok_tr, bbox = tr.update(frame)
            if not ok_tr:
                to_remove.append(tid)
                continue
            trackers[tid] = (tr, bbox)
            ycbcr = _bgr_to_ycbcr_mean(frame, tuple(map(int, bbox)))
            tl = tracklets[tid]
            tl.frames.append(frame_idx)
            tl.bboxes.append(tuple(map(int, bbox)))
            tl.ycbcr_series.append(ycbcr.tolist())

        for tid in to_remove:
            trackers.pop(tid, None)

        frame_idx += 1

    cap.release()

    tracklets = {tid: tl for tid, tl in tracklets.items() if len(tl.frames) >= min_track_len}
    return tracklets


@dataclass
class OMPParams:
    rho: float = 0.02
    tau: float = 0.05
    safety: float = 1.25
    gamma: Optional[float] = None
    mode: str = "empirical"
    k_sparsity: int = 4

@dataclass
class OMPResult:
    track_id: int
    support: List[int]
    coef: List[float]
    gamma_used: float
    meta: dict

def run_omp_for_track(series_ycbcr: np.ndarray, params: OMPParams) -> Tuple[np.ndarray, List[int], np.ndarray, float, dict]:
    if augment_dictionary_framewise is None:
        raise ImportError("temporal_omp_aug not found on PYTHONPATH.")
    if OrthogonalMatchingPursuit is None:
        raise ImportError("scikit-learn not available. Install scikit-learn.")

    target = series_ycbcr[0]

    X_aug, y_aug, gamma, meta = augment_dictionary_framewise(
        series_ycbcr, target,
        rho=params.rho, tau=params.tau, safety=params.safety, gamma=params.gamma, mode=params.mode
    )

    omp = OrthogonalMatchingPursuit(n_nonzero_coefs=params.k_sparsity)
    omp.fit(X_aug, y_aug)
    coef = omp.coef_
    support = np.flatnonzero(coef).tolist()
    return coef, support, coef, float(gamma), meta


def run_omp_on_tracklets(tracklets: Dict[int, Tracklet], params: OMPParams) -> List[OMPResult]:
    results: List[OMPResult] = []
    for tid, tl in tracklets.items():
        series = np.asarray(tl.ycbcr_series, dtype=float)
        coef, support, weights, gamma, meta = run_omp_for_track(series, params)
        results.append(OMPResult(
            track_id=tid,
            support=support,
            coef=coef.tolist(),
            gamma_used=gamma,
            meta=meta
        ))
    return results


@dataclass
class PipelineConfig:
    fps: Optional[float] = None
    stride: int = 1
    method: str = "auto"
    overwrite: bool = True

    min_track_len: int = 10
    tracker_type: str = "CSRT"
    init_every_n: int = 30
    bg_history: int = 300
    var_threshold: float = 16.0
    detect_area_thresh: int = 400

    rho: float = 0.02
    tau: float = 0.05
    safety: float = 1.25
    gamma: Optional[float] = None
    mode: str = "empirical"
    k_sparsity: int = 4


def process_video_to_omp(
    video_path: str,
    work_dir: str,
    config: PipelineConfig
) -> Dict:
    frames_dir = os.path.join(work_dir, "frames")
    _ensure_dir(work_dir)

    frames, timestamps = save_to_dir(
        video_path, frames_dir,
        fps=config.fps, stride=config.stride,
        method=config.method, overwrite=config.overwrite
    )

    # Persist timestamps
    ts_json = os.path.join(work_dir, "frames_timestamps.json")
    with open(ts_json, "w") as f:
        json.dump({"timestamps_sec": timestamps}, f, indent=2)

    tracklets = detect_and_track(
        video_path,
        min_track_len=config.min_track_len,
        tracker_type=config.tracker_type,
        init_every_n=config.init_every_n,
        bg_history=config.bg_history,
        var_threshold=config.var_threshold,
        detect_area_thresh=config.detect_area_thresh,
    )

    tracklets_json = os.path.join(work_dir, "tracklets.json")
    serial = {
        tid: dict(
            track_id=tl.track_id,
            frames=tl.frames,
            bboxes=tl.bboxes,
            ycbcr_series=tl.ycbcr_series
        )
        for tid, tl in tracklets.items()
    }
    with open(tracklets_json, "w") as f:
        json.dump(serial, f, indent=2)

    omp_params = OMPParams(
        rho=config.rho, tau=config.tau, safety=config.safety,
        gamma=config.gamma, mode=config.mode, k_sparsity=config.k_sparsity
    )
    omp_results = run_omp_on_tracklets(tracklets, omp_params)

    out_json = os.path.join(work_dir, "omp_results.json")
    summary = {
        "video": video_path,
        "frames_dir": frames_dir,
        "num_frames": len(frames),
        "num_tracklets": len(tracklets),
        "omp_results": [asdict(r) for r in omp_results],
        "config": asdict(config),
        "tracklets_json": tracklets_json,
        "frames_timestamps_json": ts_json
    }
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2)

    return summary


def _parse_cli(argv: List[str]) -> Tuple[argparse.Namespace, PipelineConfig]:
    p = argparse.ArgumentParser("video_omp_pipeline")
    p.add_argument("--video", required=True, help="Input video path")
    p.add_argument("--work", required=True, help="Working directory for frames and outputs")
    p.add_argument("--method", default="auto", choices=["auto","ffmpeg","opencv"])
    p.add_argument("--fps", type=float, default=None)
    p.add_argument("--stride", type=int, default=1)
    p.add_argument("--overwrite", action="store_true", default=True)

    p.add_argument("--min-track-len", type=int, default=10)
    p.add_argument("--tracker", default="CSRT", choices=["CSRT","KCF","MOSSE","MIL"])
    p.add_argument("--init-every-n", type=int, default=30)
    p.add_argument("--bg-history", type=int, default=300)
    p.add_argument("--var-threshold", type=float, default=16.0)
    p.add_argument("--detect-area-thresh", type=int, default=400)

    p.add_argument("--rho", type=float, default=0.02)
    p.add_argument("--tau", type=float, default=0.05)
    p.add_argument("--safety", type=float, default=1.25)
    p.add_argument("--gamma", type=float, default=None)
    p.add_argument("--mode", default="empirical", choices=["empirical","global"])
    p.add_argument("--k", type=int, default=4)

    p.add_argument("--download-url", default=None, help="Optional URL to download via yt-dlp into --video before processing.")
    p.add_argument("--download-overwrite", action="store_true", help="Re-download even if the file already exists.")
    p.add_argument("--download-max-height", type=int, default=360, help="Maximum video height to request when downloading.")

    args = p.parse_args(argv)

    cfg = PipelineConfig(
        fps=args.fps, stride=args.stride, method=args.method, overwrite=args.overwrite,
        min_track_len=args.min_track_len, tracker_type=args.tracker,
        init_every_n=args.init_every_n, bg_history=args.bg_history, var_threshold=args.var_threshold,
        detect_area_thresh=args.detect_area_thresh,
        rho=args.rho, tau=args.tau, safety=args.safety, gamma=args.gamma, mode=args.mode, k_sparsity=args.k
    )
    return args, cfg


def main(argv: Optional[List[str]] = None):
    if argv is None:
        argv = sys.argv[1:]
    args, cfg = _parse_cli(argv)
    work = args.work
    video_path = args.video
    if args.download_url:
        video_path = download_video_with_ytdlp(
            args.download_url,
            video_path,
            max_height=args.download_max_height,
            overwrite=args.download_overwrite or args.overwrite,
        )
    summary = process_video_to_omp(video_path, work, cfg)
    out_json = os.path.join(work, "omp_results.json")
    print(f"Wrote: {out_json}")
    print(json.dumps({k: v for k, v in summary.items() if k != "omp_results"}, indent=2))


if __name__ == "__main__":
    main()
