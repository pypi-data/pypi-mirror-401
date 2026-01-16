from __future__ import annotations

import polars as pl

from pulka.api import Runtime


def test_runtime_respects_env_job_workers(monkeypatch):
    monkeypatch.setenv("PULKA_JOB_WORKERS", "6")
    runtime = Runtime(load_entry_points=False)
    try:
        runner = runtime.job_runner
        assert getattr(runner, "_max_workers", None) == 6
    finally:
        runtime.close()
        monkeypatch.delenv("PULKA_JOB_WORKERS", raising=False)


def test_runtime_uses_config_job_workers(monkeypatch, tmp_path):
    config_path = tmp_path / "pulka.toml"
    config_path.write_text("[jobs]\nmax_workers = 7\n", encoding="utf-8")
    monkeypatch.delenv("PULKA_JOB_WORKERS", raising=False)
    monkeypatch.setenv("PULKA_CONFIG", str(config_path))
    runtime = Runtime(load_entry_points=False)
    try:
        runner = runtime.job_runner
        assert getattr(runner, "_max_workers", None) == 7
    finally:
        runtime.close()
        monkeypatch.delenv("PULKA_CONFIG", raising=False)


def test_runtime_applies_data_scan_config(monkeypatch, tmp_path):
    config_path = tmp_path / "pulka.toml"
    config_path.write_text(
        "[data]\ncsv_infer_rows = 123\nbrowser_strict_extensions = false\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("PULKA_CONFIG", str(config_path))

    from pulka.data import scan as scan_module

    original_infer_rows = scan_module.CSV_INFER_ROWS
    original_browser_strict = scan_module._BROWSER_STRICT_EXTENSIONS
    runtime = Runtime(load_entry_points=False)
    try:
        assert scan_module.CSV_INFER_ROWS == 123
        assert scan_module._BROWSER_STRICT_EXTENSIONS is False
    finally:
        runtime.close()
        scan_module.CSV_INFER_ROWS = original_infer_rows
        scan_module._BROWSER_STRICT_EXTENSIONS = original_browser_strict
        monkeypatch.delenv("PULKA_CONFIG", raising=False)


def test_session_applies_viewer_and_recorder_config(monkeypatch, tmp_path):
    config_path = tmp_path / "pulka.toml"
    config_path.write_text(
        "\n".join(
            [
                "[recorder]",
                "buffer_size = 10",
                'cell_redaction = "mask_patterns"',
                f'output_dir = "{tmp_path}/sessions"',
                "",
                "[viewer]",
                "min_col_width = 7",
                "hscroll_fetch_overscan_cols = 8",
                "status_large_number_threshold = 555",
                "",
                "[viewer.column_width]",
                "sample_max_rows = 99",
                "sample_batch_rows = 9",
                "sample_budget_ms = 1",
                "target_percentile = 0.5",
                "padding = 3",
                "",
                "[tui]",
                "max_steps_per_frame = 2",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("PULKA_CONFIG", str(config_path))

    dataset_path = tmp_path / "tiny.parquet"
    df = pl.DataFrame({"id": [1, 2], "name": ["a", "b"]})
    df.write_parquet(dataset_path)

    runtime = Runtime(load_entry_points=False)
    try:
        session = runtime.open(str(dataset_path))
        viewer = session.viewer
        assert viewer is not None
        assert viewer._min_col_width == 7
        assert viewer._hscroll_fetch_overscan_cols == 8
        assert viewer._status_large_number_threshold == 555
        assert viewer._max_steps_per_frame_override == 2
        assert viewer._widths._sample_max_rows == 99
        assert viewer._widths._sample_batch_rows == 9
        assert viewer._widths._sample_budget_ns == 1_000_000
        assert viewer._widths._target_percentile == 0.5
        assert viewer._widths._padding == 3
        assert session.recorder.config.buffer_size == 10
        assert session.recorder.config.cell_redaction == "mask_patterns"
        assert session.recorder.config.output_dir == (tmp_path / "sessions")
        session.close()
    finally:
        runtime.close()
        monkeypatch.delenv("PULKA_CONFIG", raising=False)
