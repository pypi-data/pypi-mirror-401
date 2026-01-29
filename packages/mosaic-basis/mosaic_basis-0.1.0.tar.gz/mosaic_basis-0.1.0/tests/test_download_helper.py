"""Unit tests for the yt-dlp download helper without hitting the network."""

from __future__ import annotations

from pathlib import Path

import pytest

import video_omp_pipeline


def test_download_helper_requires_ytdlp(monkeypatch, tmp_path):
    """Ensure we raise a helpful error when yt-dlp is missing."""
    monkeypatch.setattr(video_omp_pipeline, "YoutubeDL", None)
    with pytest.raises(ImportError):
        video_omp_pipeline.download_video_with_ytdlp("https://example.com/video", str(tmp_path / "clip.mp4"))


def test_download_helper_creates_file_and_respects_overwrite(monkeypatch, tmp_path):
    """Simulate a download via a dummy YoutubeDL implementation."""

    created_paths = []

    class DummyYoutubeDL:
        def __init__(self, opts):
            self.opts = opts

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def download(self, urls):
            target = Path(self.opts["outtmpl"])
            target.write_text("dummy video data")
            created_paths.append(target)

    monkeypatch.setattr(video_omp_pipeline, "YoutubeDL", DummyYoutubeDL)

    out_path = tmp_path / "clip.mp4"
    result_path = video_omp_pipeline.download_video_with_ytdlp("https://example.com/video", str(out_path))
    assert Path(result_path).exists()
    assert Path(result_path).read_text() == "dummy video data"
    assert created_paths[-1] == out_path

    class FailingYoutubeDL:
        def __init__(self, *args, **kwargs):
            raise AssertionError("Should not instantiate YoutubeDL when overwrite=False and file exists.")

    monkeypatch.setattr(video_omp_pipeline, "YoutubeDL", FailingYoutubeDL)
    out_path.write_text("existing data")
    result_path_2 = video_omp_pipeline.download_video_with_ytdlp(
        "https://example.com/video",
        str(out_path),
        overwrite=False,
    )
    assert Path(result_path_2).read_text() == "existing data"
