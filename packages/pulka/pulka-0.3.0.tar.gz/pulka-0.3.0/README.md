# Pulka

A small, vibe-engineered VisiData-like tabular viewer I built for myself. It loads CSV/TSV, Parquet, and Arrow/Feather/IPCs and presents a keyboard-driven table with sorting and filtering. I’m sharing it in case it sparks ideas, but it’s still very much a personal playground rather than a polished product.

## Project status

Pulka is intentionally personal and early-stage. I experiment freely and change APIs whenever it feels right for my own workflows. Please treat the codebase as reference material rather than a supported tool. I’m flattered by the interest, but I’m keeping the scope personal for now, so I’m not accepting contributions, feature requests, or support questions.

## Where to start (for readers)

- Repo rules: `AGENTS.md`
- Architecture map: `docs/architecture_overview.md`
- Debugging guide: `docs/how_to_debug.md`
- Glossary: `docs/glossary.md`
- Database sources: `docs/database_sources.md`

## Installation

Pulka is published as a standard Python package mostly so I can install it on my own machines. If you’d still like to poke around, the quickest way to install the CLI is:

```bash
pip install pulka
```

The installation provides the `pulka` console script (and the shorthand alias `pk`). Run `pulka --help` (or `pk --help`) to see all available options. Optional extras are available:

- `pulka[test]` – installs the pytest-based integration suite.
- `pulka[dev]` – installs the testing extras plus Ruff and the ancillary tooling used during development.

If you prefer [`uv`](https://github.com/astral-sh/uv) for local development, the project ships a `uv.lock` file. Run `uv sync --dev` to install Pulka along with its development dependencies inside an isolated virtual environment.

<img width="330" height="330" alt="IMG_7280" src="https://github.com/user-attachments/assets/a94d127f-b8f6-4e13-8444-c009802e554b" />


## Quick start

- Launch the viewer directly against any supported data source:

  ```bash
  pulka path/to/data.parquet
  ```

- Open a database table through DuckDB (include the table name after `#`):

  ```bash
  pulka "duckdb:///path/to/db.duckdb#my_table"
  pulka "sqlite:///path/to/db.sqlite#my_table"
  pulka "postgres://user:pass@host:5432/dbname#public.my_table"
  ```

- Open a local database file to browse its tables (press Enter to open a table):

  ```bash
  pulka /path/to/db.duckdb
  pulka /path/to/db.sqlite
  ```

- Start in file browser mode by pointing Pulka at a directory (press `Enter`/`o` to open
  datasets from the listing):

  ```bash
  pulka /path/to/datasets/
  ```

- Evaluate a Polars expression without writing an intermediate file (prints the
  result once; add `--tui` to browse interactively):

  ```bash
  pulka --expr "pl.scan_parquet('path/to/data.parquet').select(pl.all().head(5))"
  ```

  Headless output uses Polars' DataFrame formatting, so the preview matches what
  you'd see from `pl.DataFrame`. Add `--tui` to switch back to the interactive
  viewer. Within expressions you can call `df.glimpse()` for a per-column summary,
  reference columns via `c.<name>` (or `pl.col("name")`), use Polars selectors through
  the `cs` alias (fallback provided if selectors are missing), auto-scan files with
  `scan(path)`, adjust output sizing with `cfg_rows/cols/fmt_str_lengths`, and log
  quick debug info via `dbg(x, label="...")` without breaking the chain.

- Inspect a dataset quickly without launching the TUI:

  ```bash
  pulka data/sample.parquet --schema   # name + dtype table
  pulka data/sample.parquet --glimpse  # column-wise preview via df.glimpse()
  pulka data/sample.parquet --describe # descriptive stats via df.describe()
  ```

- Generate a comprehensive Parquet file that covers all core Polars dtypes:

  ```bash
  ./generate_all_polars_dtypes_parquet.py
  # writes data/all_polars_dtypes.parquet
  ```

- Run the viewer interactively with `uv` during development:

  ```bash
  uv run pulka data/all_polars_dtypes.parquet
  # or run the module entry point
  uv run python -m pulka data/all_polars_dtypes.parquet
  ```

## Supported formats

- Parquet (`.parquet`)
- CSV/TSV (`.csv`, `.tsv`)
- Arrow/Feather/IPC (`.arrow`, `.feather`, `.ipc`)
- NDJSON/JSONL (`.ndjson`, `.jsonl`, plus `.zst` variants)
- Excel via `polars[excel]` (`.xlsx`, `.xlsm`, `.xlsb`; `.xls` is not supported)
- DuckDB/SQLite database files (`.duckdb`, `.sqlite`)
- Database URIs via DuckDB (`duckdb://...#table`, `sqlite://...#table`, `postgres://...#table`)

## Controls

- q: back (or quit if at root)
- Q: quit immediately
- Esc: cancel modal (or dismiss sticky error status)
- Ctrl+C: clear modal input field
- arrows/hjkl: move cursor/viewport
- mouse wheel: vertical scroll; hold Ctrl to scroll horizontally
- PgUp/PgDn: page up/down
- J / K, zj / zk: half-page down/up
- zh / zl: half-page left/right
- gg / G: jump to top / bottom
- zt / zb: scroll current row to the top / bottom of the viewport
- zT / zM / zB: jump to the first / middle / last visible row
- zz: center current row in the viewport
- 0 / $: first / last visible column
- gh / gl: first / last column (horizontal gg/G)
- H / L: slide the current column left/right (reorder columns)
- gH / gL: slide the current column to the first/last position
- ma / mm: materialize active filters/sorts/projection into a new sheet
- ms: materialize the current selection into a new sheet
- _: maximize current column width (toggle)
- g_: maximize all columns' widths (toggle)
- r_: reset maximized widths
- d: drop the current column
- rd: restore all dropped columns
- ]: sort ascending by current column (toggle)
- [: sort descending by current column (toggle)
- } / {: stack ascending/descending sort on current column (toggle; last wins)
- <space>: select/unselect the focused row then move down (tracked by undo/redo)
- ,: select all rows that match the active cell's value in the current column
- +: append a filter matching the active cell's value on the current column
- ~: invert selection across all rows
- r<space>: clear all selected rows
- x (file browser): delete the focused file or selected files/directories (always asks for confirmation)
- enter / o (file browser): open focused directory/file
- enter in frequency views: applies a filter for all currently selected values (clears selection)
- yy: copy the active cell to the clipboard
- yp: copy the current dataset path to the clipboard
- yte: select a viewport region and copy it for Excel (includes headers)
- ytm: select a viewport region and copy it as a Markdown table (includes headers)
- yta: select a viewport region and copy it as an ASCII table (includes headers)
- ytu: select a viewport region and copy it as a Unicode table (includes headers)
- C: column summary sheet (per-column stats)
- i: toggle insight panel mode (column vs transforms)
- I: toggle insight sidecar (column stats or transforms)
- F: frequency table of the current column (value, count, percent)
- t: transpose the current row (single-row sample)
- T: transpose view (columns as rows with sample data; respects `PULKA_TRANSPOSE_SAMPLE_ROWS`)
- / or \\: search current column (substring, case-insensitive)
- ?: show available commands (opens the help sheet)
- |: select rows containing a substring in the active column (case-insensitive)
- * / #: jump to the next / previous row with the active cell value in the current column
- c: search columns by name (tab-complete + history; `n`/`N` cycle matches)
- n / N: next / previous match (row search or column search, depending on context)
- rr: reset filters, sorts, and selection
- re / rf / rs: clear expression filters / SQL filters / sorts
- rt<id>: remove the transform with the matching identifier from the transforms panel
- Ctrl+R: reload the current dataset from disk
- e: open expression filter prompt (Polars expression using `c.<column>`)
- E: open transform modal (apply a Polars LazyFrame transform into a derived view)
- f: open SQL filter prompt (provide a WHERE clause without the `WHERE` keyword)
- : open command prompt (`move_to_column <column>`, `record on`, ...)
- !: run a shell command (non-interactive; press Enter to return)
- @: toggle structured flight recorder (writes buffered session log)
- enter: in `F` mode, filter by selected value and return to DataFrame view

## Scripted/headless usage

Useful for debugging without a TTY, tests, CI, or capturing output sequences.

```bash
pulka data.parquet --cmd move_down --cmd move_right --cmd sort_asc --cmd quit
```

You can also skip the positional path entirely and provide a Polars
expression instead:

```bash
pulka --expr "pl.DataFrame({'a': [1, 2]}).lazy()"
# default: prints a single render to stdout
pulka --expr "df.describe()" data.parquet --tui  # reference the scanned dataset via `df`
```

- From a script file (one command per line):

  ```bash
  pulka data.parquet --script commands.txt
  ```

Supported commands:
- move_down [n], move_up [n], move_left [n], move_right [n]
- move_page_down, move_page_up, move_half_page_down, move_half_page_up
- move_half_page_left, move_half_page_right
- move_top, move_bottom, move_first_column, move_last_column
- move_column_first_overall (gh), move_column_last_overall (gl): navigate to first/last column overall (adjusts viewport)
- move_viewport_top (zT), move_viewport_middle (zM), move_viewport_bottom (zB): jump within the visible viewport
- move_row_to_top (zt), move_row_to_bottom (zb): align the current row to the top/bottom of the viewport
- slide_left (H), slide_right (L), gH, gL: slide the current column left/right or to the extremes
- materialize_all (ma, mm), materialize_selection (ms): persist current view or selection to a new sheet
- _, maximize_column: toggle maximize current column
- g_, maximize_all_columns: toggle maximize all columns
- r_, reset_max_columns: reset maximized column widths
- sort_asc, sort_desc, sort_asc_stack, sort_desc_stack, filter_expr <expr>, filter_value (+), filter_value_not (-)
- reset (rr), reset_expr_filter (re), reset_sql_filter (rf), reset_sort (rs), move_to_column <col>, render, quit
- select_row: toggle selection for the focused row
- filter_sql <where>: apply an SQL WHERE clause (omit the `WHERE` keyword)
- help_sheet: show available commands
- status: show status message history
- schema: show column schema information
- cd <dir>: change working directory (relative paths allowed)
- file_browser_sheet [dir]: open the file browser at DIR (defaults to current dataset directory)
- frequency_sheet [col]: frequency table of current or specified column
- summary_sheet (C): column summary sheet
- transpose_sheet [rows]: transpose view with optional row count
- transpose_row_sheet (t): transpose only the current row
- insight [on|off|column|transforms]: toggle the insight sidecar or switch modes (TUI only)
- move_center_row: center current row in viewport
- search <term>: search current column for substring
- select_contains (|) <term>: select rows where the active column contains substring; navigate with n/N
- search_value_next (*), search_value_prev (#): jump to next/previous row sharing the active cell value
- search_next_match, search_prev_match: repeat the last search or jump to next/previous selected row
- drop (d), reset_drop (rd): drop current column or restore all dropped columns
- select_same_value (,): select rows that match the active cell's value in the current column
- invert_selection, ~: invert selection across all rows
- clear_selection, r<space>: clear all selected rows
- undo, redo: undo/redo the last transformation
- move_next_different_value, move_prev_different_value: navigate to next/previous different value
- yank_cell (yy): copy the active cell to the clipboard
- yank_path (yp): copy the current dataset path to the clipboard
- yank_column (yc): copy the active column name to the clipboard
- yank_all_columns (yac): copy visible column names as a Python list
- yank_schema (ys): copy the current schema mapping
- yank_table_excel (yte): select a viewport region and copy it for Excel
- yank_table_markdown (ytm): select a viewport region and copy it as Markdown
- yank_table_ascii (yta): select a viewport region and copy it as an ASCII table
- yank_table_unicode (ytu): select a viewport region and copy it as a Unicode table
- copy <dest>, move <dest> or <src> <dest>, rename <name>, mkdir <path> (file browser only)

Filter expressions use the helper namespace `c` to refer to columns (`c.tripduration > 1200`, `c.name.str.contains('NY', literal=True)`). Any Polars Expr helpers are available via `pl`/`lit`.

## Debugging workflows

- Force a tiny viewport to study repaints/highlights clearly:

  ```bash
  pulka data.parquet --viewport-rows 4 --viewport-cols 4
  ```

- Scripted navigation with explicit renders between steps:

  ```bash
  pulka data.parquet --cmd render --cmd move_down --cmd render --cmd quit
  ```

- Use the included generator to cover edge cases across types:

  ```bash
  ./generate_all_polars_dtypes_parquet.py --rows 128 --seed 123
  pulka data/all_polars_dtypes.parquet
  # or run the module entry point
  python -m pulka data/all_polars_dtypes.parquet --viewport-rows 6 --viewport-cols 6
  ```

- Recording is disabled by default. Enable it from the CLI with `--record` or toggle inside the
  TUI. Logs are streamed to `~/.pulka/sessions/` (JSONL, compressed with zstd when available).
  Dataset paths are automatically redacted by default (replaced with basename + SHA1 digest)
  to make logs safe to share, with the original paths stored under `_raw_path` for internal use.

  - Enable recording with `pulka data.parquet --record` or press `@` during a session.
  - Change the destination with `--record-dir /path/to/sessions`.
  - While recording, Pulka emits `perf` events capturing render/status durations (TUI, headless, and API paths) so slow commands can be identified post-run.

  Headless runs respect the same options; add `--record` to persist logs for scripted sessions.
  
  **Cell redaction**: By default, cell values containing strings are hashed and replaced with `{hash, length}` dictionaries in the flight recorder logs to protect sensitive data. You can select other modes using the `--cell-redaction` flag or the `PULKA_RECORDER_CELL_REDACTION` environment variable:
  
  - `none`: No redaction applied to cell values (default when recording is disabled).
  - `hash_strings`: Hash string values and replace with `{hash, length}` (default when recording is enabled).
  - `mask_patterns`: Replace sensitive patterns (emails, IBANs, phones) with `***`.
  
  Example usage: `pulka data.parquet --cell-redaction mask_patterns` or `PULKA_RECORDER_CELL_REDACTION=hash_strings pulka data.parquet`.
  
  Note: `_raw_path` values remain for internal use and are not exported in shared logs.
  
  **Repro exports**: Export reproducible dataset slices for debugging with the `repro_export` command. The exported Parquet files contain the currently visible rows/columns plus a 10-row margin (configurable), and respect the active redaction policy. Files are saved in the session directory as `<session_id>-repro.parquet`. Trigger via:
  
  - Interactive mode: `:repro_export` or `:repro` command
  - Headless mode: `pulka data.parquet --repro-export` flag
  - Command: `pulka data.parquet --cmd repro_export --cmd quit`
  
  The export respects your current viewport and column visibility settings (use `all_columns=true` to export all columns).

## Flight Recorder & Debugging

Pulka’s structured flight recorder captures rich runtime telemetry—key events, perf timings,
viewer snapshots, and rendered frames—to make tricky bugs reproducible.

- **Toggle in the TUI**: Press `@` to enable or disable the recorder for the current session. When
  stopping, Pulka saves the buffered log to `~/.pulka/sessions/` and copies the full path to your
  clipboard when available.
- **Headless & API support**: Pass `--record` on the CLI or attach a `Recorder` in code to capture
  the same telemetry outside the TUI.
- **Artifacts**: Recorder files are UTF-8 JSONL (`*.pulka.jsonl`), optionally compressed with zstd.
  They include structured events (`command`, `key`, `state`, `frame`, `perf`, …) and respect cell
  redaction policies.

You can post-process these logs with your own tooling or scripts (see `PROFILING.md` for examples)
to analyse performance and reproduce user journeys.


## Benchmarks

- Run the microbenchmarks against the default fixture:

  ```bash
  uv run python benchmarks/bench_pulka.py --mode micro --iterations 5
  ```

  The pre-commit hooks call `benchmarks/check_microbench.py` to ensure the
  navigation microbenchmarks stay within budget. Update the baseline when
  intentional performance work lands:

  ```bash
  uv run python benchmarks/check_microbench.py --update-baseline
  ```

- Point the benchmark to another dataset or change the sample count via `--path` and `--iterations`.

- Measure fast vertical scrolling with the synthetic mini-nav fixture:

  ```bash
  uv run python benchmarks/bench_pulka.py --mode vscroll --iterations 10
  ```

  Use `--path` to benchmark a specific dataset or adjust `--vscroll-steps`,
  `--vscroll-rows`, and `--vscroll-cols` to mimic different scroll workloads.

- Point the benchmark to another dataset or change the sample count via `--path` and `--iterations`.

- Need a larger real-world dataset? Download one month of NYC Citi Bike trips (CSV) and convert to Parquet:

  ```bash
  mkdir -p data/fixtures/nyc_citibike
  curl -L 'https://s3.amazonaws.com/tripdata/202401-citibike-tripdata.zip' -o data/fixtures/nyc_citibike/202401-citibike-tripdata.zip
  unzip -d data/fixtures/nyc_citibike data/fixtures/nyc_citibike/202401-citibike-tripdata.zip
  uv run --with polars python - <<'PY'
  import polars as pl
  from pathlib import Path

  root = Path('data/fixtures/nyc_citibike')
  parts = sorted(root.glob('202401-citibike-tripdata_*.csv'))
  schema_overrides = {'start_station_id': pl.Utf8, 'end_station_id': pl.Utf8}
  lf = pl.concat([
      pl.scan_csv(p, infer_schema_length=10000, schema_overrides=schema_overrides) for p in parts
  ])
  lf.sink_parquet(root / '202401-citibike-tripdata.parquet')
  PY
  ```

  All generated files live under `data/fixtures/` (ignored by git) so you can keep large fixtures locally without polluting commits.

### Synthetic data presets

- Materialise any spec or capsule via the CLI:

  ```bash
  uv run pulka generate '549r/sol=sequence();value=normal(0,1)' --out data/mars.parquet
  ```

- Save frequently used specs under `~/.config/pulka/generate_presets.toml` (or override the path with `PULKA_GENERATE_PRESET_FILE`). Example:

  ```toml
  [presets]
  themartian = '549r/sol=sequence()!;earth_datetime=@(...);storm_alert=@(...)'
  mini_nav = '200r/id=sequence();value=normal(0,1)'
  ```

- Generate from a preset or inspect what is available:

  ```bash
  uv run pulka generate --preset themartian --out data/the-martian.parquet
  uv run pulka generate --preset hailmary --out data/hailmary.parquet
  uv run pulka generate --list-presets
  ```

  Pulka ships these presets out of the box. To customize or add new ones, edit
  `~/.config/pulka/generate_presets.toml` (create it if missing) or copy the sample from
  `docs/generate_presets.example.toml` as a starting point.

## Notes

- The viewer operates on the engine's physical plan (backed by Polars today), applying filter/sort lazily and fetching only the visible slice per render for performance.
- Filtering uses Polars expressions: refer to columns with `c.<name>` (or `c["name with spaces"]`) and combine with any `polars.Expr` helpers.
- Set `PULKA_POLARS_ENGINE=streaming` to force the new streaming engine on collect paths (default), or `PULKA_POLARS_ENGINE=in_memory` / `PULKA_POLARS_ENGINE=default` to fall back to Polars defaults.
- Use the `PULKA_TRANSPOSE_SAMPLE_ROWS` environment variable or the `transpose_sheet [rows]` command
  to control how many rows are sampled for transpose mode; press `t` to transpose just the current
  row.
- Rendering uses a prompt_toolkit-native table control by default for smoother scrolling and fewer ANSI redraw artifacts. Set `PULKA_PTK_TABLE=0` to fall back to the Rich-based renderer that still powers headless exports. If you see flicker on very small terminals, try `--viewport-rows 4 --viewport-cols 4` to debug.
- You can run both scripts directly thanks to the `uv` shebangs; no manual environment setup required.
- Colours are configurable via `pulka-theme.toml` (or `PULKA_THEME_PATH`) using two inputs:

  ```toml
  [theme]
  primary = "#f06595"
  secondary = "#63e6be"
  ```
- Background job concurrency defaults to `min(4, cpu_count)` threads. Set `PULKA_JOB_WORKERS=<n>` or add a `[jobs]` table with `max_workers = <n>` to your `pulka.toml` when you want shared runtimes to fan out over more worker threads.

### Configuration

Create `pulka.toml` in your project or under `~/.config/pulka/` to override defaults
(CLI flags and env vars still take precedence):

```toml
[recorder]
enabled = true
buffer_size = 1000
output_dir = "~/.pulka/sessions"
cell_redaction = "hash_strings"

[viewer]
min_col_width = 4
default_col_width_cap_compact = 25
default_col_width_cap_wide = 20
sep_overhead = 3
hscroll_fetch_overscan_cols = 4
status_large_number_threshold = 999999

[viewer.column_width]
sample_max_rows = 10000
sample_batch_rows = 1000
sample_budget_ms = 100
target_percentile = 0.99
padding = 2

[tui]
max_steps_per_frame = 3

[data]
csv_infer_rows = 20000
browser_strict_extensions = true

[jobs]
max_workers = 4
```

## Development

- Install the project (and optional test dependencies) locally:

  ```bash
  uv pip install -e ".[test]"
  ```

- Run the full test suite with uv:

  ```bash
  uv run pytest
  ```

  Add extra pytest arguments after `pytest` as needed.

### Essential Tools & Commands

```bash
# Run the application
pulka data/file.parquet

# Run tests
uv run python -m pytest

# Run specific test
uv run python -m pytest tests/test_specific.py::TestSpecific::test_name

# Install in development mode
uv pip install -e .

# Clear Python cache
rm -rf src/pulka/__pycache__ src/__pycache__
```

### Debugging Tips

1. **Terminal width issues**: Use `COLUMNS=80` environment variable to simulate different terminal widths
2. **Status bar debugging**: The status bar has responsive layouts - check both wide and narrow terminals
3. **Data type simplification**: Complex types (List, Array, Struct, etc.) are simplified to single words

### Writing Tests

1. **Test structure**: Follow existing patterns in `tests/` directory
2. **Status bar tests**: Use `capsys` fixture to capture output and verify status bar content
3. **Data type tests**: Test with `all_polars_dtypes.parquet` which contains all major data types

### Key Implementation Details

1. **Status bar format**: `filename • row n / col name[type] • status_message         total_rows • memory`
2. **Data type simplification**: Happens in `render_status_line()` function in `src/pulka/__init__.py`
3. **Responsive design**: Automatically switches between full and simplified layouts based on terminal width

### Common Development Tasks

1. **Add new data type simplification**: Modify the dtype simplification logic in `render_status_line()`
2. **Modify status bar layout**: Adjust the string formatting in `render_status_line()`
3. **Add new status messages**: Set `viewer.status_message` in relevant functions

### Useful Test Files

- `data/all_polars_dtypes.parquet`: Contains all major Polars data types for testing
- `tests/test_dtypes.py`: Tests for data type handling
- `tests/test_viewer.py`: Tests for status bar and viewer functionality

 - Tests guidelines: 

## Architecture

Pulka follows a modular architecture with clear separation of concerns:

- **Data Layer** (`src/pulka/data/`): Handles dataset scanning, filter compilation, and query building
  - `scan.py`: File format detection and Polars LazyFrame creation
  - `filter_lang.py`: AST validation and Polars expression compilation
  - `query.py`: Query plan construction utilities

- **Core Layer** (`src/pulka/core/`): Centralized state management and interfaces
  - `sheet.py`: Sheet protocol defining the interface for tabular data views
  - `viewer.py`: Viewport and cursor state management
  - `formatting.py`: Data type-aware formatting helpers
  - `jobs.py`: Background job management (for summary statistics)

- **Sheet Layer** (`src/pulka/sheets/`): First-class sheet implementations
  - `data_sheet.py`: Primary data view with filters/sorting
  - `freq_sheet.py`: Frequency tables showing value counts
  - `summary_sheet.py`: Column statistics summary
  - `transpose_sheet.py`: Transposed view with columns as rows

- **Command Layer** (`src/pulka/command/`): Unified command system
  - `registry.py`: Command registration and execution
  - `builtins.py`: Standard command handlers

- **Render Layer** (`src/pulka/render/`): Pure rendering functions
  - `table.py`: Table rendering with highlighting
  - `status_bar.py`: Status bar layout and truncation logic

- **TUI Layer** (`src/pulka/tui/`): Terminal UI implementation
  - `app.py`: Main application integration
  - `screen.py`: Screen state and modal management
  - `keymap.py`: Key binding definitions
  - `modals.py`: Dialog and modal implementations

- **Debug Layer** (`src/pulka/debug/`): Debugging and replay tools
  - `replay.py`: TUI replay tool for reproducing recorded sessions
  - `replay_cli.py`: Command line interface for replay functionality

- **API Layer** (`src/pulka/api/`): Public embeddable interface
  - `session.py`: Main `Session` class for programmatic access
  - `__init__.py`: Re-exported public API

## Embedding via pulka.api

Pulka provides a clean API for embedding in other applications:

```python
from pulka.api import Runtime, Session, open

# Construct a runtime once per process to load config + plugins
runtime = Runtime()

# Open a dataset with a runtime-managed session
session = runtime.open("data.parquet")

# Or fall back to the legacy helpers when you don't need to reuse the runtime
session = open("data.parquet")
session = Session("data.parquet", viewport_rows=10, viewport_cols=5)

# Runtime metadata is available without opening a session
print(runtime.loaded_plugins)

# Access the shared JobRunner to schedule background work in custom integrations
runner = runtime.job_runner

# Run script commands programmatically
outputs = session.run_script(["move_down", "move_right", "sort_asc", "render"])

# Or drive individual commands via the session runtime
runtime = session.command_runtime
result = runtime.invoke("move_down", source="docs")
if result.message:
    print(result.message)
if result.render.should_render:
    table_after_move_down = session.render()

# Render current view
table_output = session.render()

# Render without status bar
table_only = session.render(include_status=False)

# Open derived sheet views via the registry
freq_viewer = session.open_sheet_view(
    "frequency_sheet",
    base_viewer=session.viewer,
    column_name="category",
    viewer_options={"source_path": None},
)
transpose_viewer = session.open_sheet_view(
    "transpose",
    base_viewer=freq_viewer,
)
```

The API exposes:
- `Runtime` for shared configuration, registries, and plugin metadata
- `Session` class for managing a data view session
- `Session.open_sheet_view()` for constructing derived sheet viewers (frequency_sheet, histogram, transpose_sheet, plugins)
- Derived sheet constructors must accept the runtime-managed `JobRunner` via the `runner` keyword
- `open()` convenience function
- `run_script()` for executing command sequences
- `command_runtime` for fine-grained command dispatch and recorder integration
- `render()` for getting current view as text
- Sheet properties via `session.sheet`
- Viewer state via `session.viewer`

## Development

### Quick Start

1. **Install dependencies:**
   ```bash
   uv sync --dev
   ```

2. **Run all quality checks:**
   ```bash
   uv run python -m pulka.dev check
   ```

3. **Auto-fix common issues:**
   ```bash
   uv run python -m pulka.dev fix
   ```

### Development Commands

- **`uv run python -m pulka.dev lint`** - Run Ruff linter
- **`uv run python -m pulka.dev format`** - Format code with Ruff
- **`uv run python -m pulka.dev lint-imports`** - Check static import layering contracts
- **`uv run python -m pulka.dev test`** - Run all tests
- **`uv run python -m pulka.dev check`** - Run all quality checks (lint + format + import contracts + tests)
- **`uv run python -m pulka.dev fix`** - Auto-fix issues and run tests

See [docs/architecture_guardrails/README.md](docs/architecture_guardrails/README.md) for more background on the
import contracts and how to interpret failures.

### Pre-commit Hooks

Pre-commit hooks using `prek` automatically run:
- `uv run ruff check .`
- `uv run python -m pulka_fixtures check`
- `uv run python -m pulka.testing.runners smoke`
- `uv run python benchmarks/check_microbench.py`
- `uv run pytest tests/test_determinism_canary.py -v`

### Development Workflow

```bash
# Make changes
vim src/pulka/...

# Check for issues
uv run python -m pulka.dev check

# Auto-fix what you can
uv run python -m pulka.dev fix

# Commit (hooks run automatically)
git commit -m "Your changes"
```

Code is formatted with Ruff (100 character line length) and follows modern Python 3.12+ conventions.

This enables integration into other tools, automated analysis, and test scenarios without requiring TUI dependencies.

## License

Pulka is available under the [MIT License](LICENSE).
