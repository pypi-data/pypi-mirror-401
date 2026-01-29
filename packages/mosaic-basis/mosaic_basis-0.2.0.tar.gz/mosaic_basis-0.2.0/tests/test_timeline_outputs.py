"""Integration-style tests that exercise timestamp propagation for mosaics and previews."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

import mosaic_compositor
import preview_exporter
import video_omp_pipeline

cv2 = pytest.importorskip("cv2")

YT_TEST_VIDEO = "https://www.youtube.com/watch?v=V3-HL7MgzzA&t=14s"


def _download_with_yt_dlp(target_dir: Path) -> Path:
    existing = sorted(target_dir.glob("sample.*"))
    if existing:
        return existing[0]

    outtmpl = str(target_dir / "sample.%(ext)s")
    ydl_opts = {
        "format": "mp4[height<=360]/mp4/best",
        "quiet": True,
        "noprogress": True,
        "nocheckcertificate": True,
        "noplaylist": True,
        "outtmpl": outtmpl,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([YT_TEST_VIDEO])
    except DownloadError as exc:
        pytest.skip(f"yt-dlp download failed: {exc}")

    files = sorted(target_dir.glob("sample.*"))
    if not files:
        pytest.skip("yt-dlp did not produce a sample video")
    return files[0]


@pytest.fixture(scope="session")
def downloaded_video(tmp_path_factory: pytest.TempPathFactory) -> Path:
    cache_dir = tmp_path_factory.mktemp("yt_video_cache")
    return _download_with_yt_dlp(cache_dir)


@pytest.fixture(scope="session")
def extracted_sample(
    tmp_path_factory: pytest.TempPathFactory, downloaded_video: Path
) -> dict:
    frames_root = tmp_path_factory.mktemp("frames")
    frames_dir = frames_root / "frames"
    frames, timestamps = video_omp_pipeline.save_to_dir(
        str(downloaded_video),
        str(frames_dir),
        stride=12,
        method="opencv",
        overwrite=True,
    )
    if len(frames) < 3:
        pytest.skip("Sample video did not yield enough frames for validation")
    sample_img = cv2.imread(frames[0])
    if sample_img is None:
        pytest.skip("Unable to read extracted frames for validation")
    height, width = sample_img.shape[:2]
    return {
        "frames": frames,
        "timestamps": timestamps,
        "frames_dir": frames_dir,
        "frame_shape": (height, width),
    }


@pytest.fixture
def tracklet_bundle(tmp_path: Path, extracted_sample: dict) -> dict:
    timestamps: list[float] = extracted_sample["timestamps"]
    frame_shape = extracted_sample["frame_shape"]
    track_frames = list(range(min(4, len(extracted_sample["frames"]))))
    if len(track_frames) < 2:
        pytest.skip("Need at least two frames for timeline tests")

    bbox = [0, 0, frame_shape[1], frame_shape[0]]
    tracklets = {
        "1": {
            "track_id": 1,
            "frames": track_frames,
            "bboxes": [bbox for _ in track_frames],
            "ycbcr_series": [[0.0, 0.0, 0.0] for _ in track_frames],
        }
    }
    tracklets_json = tmp_path / "tracklets.json"
    tracklets_json.write_text(json.dumps(tracklets))

    omp_summary = {
        "omp_results": [
            {
                "track_id": 1,
                "support": [0, len(track_frames) - 1],
                "coef": [1.0 for _ in track_frames],
                "gamma_used": 1.0,
                "meta": {"source": "test"},
            }
        ]
    }
    omp_json = tmp_path / "omp_results.json"
    omp_json.write_text(json.dumps(omp_summary))

    ts_json = tmp_path / "frames_timestamps.json"
    ts_json.write_text(json.dumps({"timestamps_sec": timestamps}))

    expected_idx = track_frames[1]
    expected_label = f"id=1 t={timestamps[expected_idx]:.2f}s"
    return {
        "tracklets_path": tracklets_json,
        "omp_path": omp_json,
        "timestamps_path": ts_json,
        "expected_label": expected_label,
    }


def test_save_to_dir_generates_monotonic_timestamps(extracted_sample: dict):
    timestamps = extracted_sample["timestamps"]
    frames = extracted_sample["frames"]
    assert len(frames) == len(timestamps)
    assert all(b >= a for a, b in zip(timestamps, timestamps[1:]))
    assert timestamps[-1] > timestamps[0]


def test_compose_mosaic_uses_real_timestamps(
    extracted_sample: dict,
    tracklet_bundle: dict,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    captured_labels: list[str] = []
    original_put_label = mosaic_compositor._put_label

    def capture_label(img, text: str, *args, **kwargs):
        captured_labels.append(text)
        return original_put_label(img, text, *args, **kwargs)

    monkeypatch.setattr(mosaic_compositor, "_put_label", capture_label)

    out_path = tmp_path / "mosaic.mp4"
    result = mosaic_compositor.compose_mosaic(
        frames_dir=str(extracted_sample["frames_dir"]),
        tracklets_json=str(tracklet_bundle["tracklets_path"]),
        omp_results_json=str(tracklet_bundle["omp_path"]),
        out_video_path=str(out_path),
        frames_timestamps_json=str(tracklet_bundle["timestamps_path"]),
        grid_rows=1,
        grid_cols=1,
        tile_w=96,
        tile_h=96,
        fps=30,
        highlight_keyframes=True,
        timeline=True,
    )

    assert out_path.exists()
    assert out_path.stat().st_size > 0
    assert result["out_video"] == str(out_path)
    expected_label = tracklet_bundle["expected_label"]
    assert any(expected_label in label for label in captured_labels)


def test_preview_exporter_produces_artifacts_with_timestamps(
    extracted_sample: dict,
    tracklet_bundle: dict,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    captured_labels: list[str] = []
    original_put_label = preview_exporter._put_label

    def capture_label(img, text: str, *args, **kwargs):
        captured_labels.append(text)
        return original_put_label(img, text, *args, **kwargs)

    monkeypatch.setattr(preview_exporter, "_put_label", capture_label)

    out_dir = tmp_path / "previews"
    result = preview_exporter.export_track_previews(
        frames_dir=str(extracted_sample["frames_dir"]),
        tracklets_json=str(tracklet_bundle["tracklets_path"]),
        omp_results_json=str(tracklet_bundle["omp_path"]),
        out_dir=str(out_dir),
        timestamps_json=str(tracklet_bundle["timestamps_path"]),
        crop_size=(96, 96),
        fps=30,
        make_keyframe_video=True,
        make_contact_sheet=True,
        contact_sheet_cols=2,
        timeline=True,
    )

    assert Path(result["out_dir"]).exists()
    track_mp4 = out_dir / "track_0001.mp4"
    assert track_mp4.exists() and track_mp4.stat().st_size > 0
    keyframes_mp4 = out_dir / "track_0001_keyframes.mp4"
    assert keyframes_mp4.exists() and keyframes_mp4.stat().st_size > 0
    keyframes_png = out_dir / "track_0001_keyframes.png"
    assert keyframes_png.exists() and keyframes_png.stat().st_size > 0

    expected_label = tracklet_bundle["expected_label"]
    assert any(expected_label in label for label in captured_labels)
