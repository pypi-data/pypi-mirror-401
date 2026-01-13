# schema-classifier

**PySchemaClassifier** — a Python library and CLI to detect file/table/dataframe formats, infer/extract schemas, and emit schemas (Spark StructType-like dict, YAML, JSON, TXT).MVP focuses on single-level compression, core formats (CSV/JSON/XML/Parquet/Avro/ORC + Delta/Iceberg/Hudi metadata), sampling policies, and robust exceptions.

## Status
This is a **design-locked skeleton** for MVP implementation. Modules are scaffolded with docstrings and TODO markers.

## Quick Start
```bash
# create and activate venvpip install -e .
 
python -m venv .venv
source .venv/bin/activate 
##or 
.\.venv\Scripts\activate

# editable install
pip install -e .
pip install -e .[orc]
pip install -e .[dataframe]

# run CLI (prints skeleton info)
schema-detect --help

# Try running below commands to test this framework

## schema-detect defaults
# --fmt: yaml
# --output-dir .
# --output-file schema.yml

schema-detect tests/data/csv/sales_header.csv
schema-detect tests/data/csv/sales_no_header.csv --fmt yaml --output-file schema_no_header.yml
schema-detect tests/data/csv/very_wide.csv --fmt yaml --output-file schema_wide.yml
schema-detect tests/data/csv/sales_utf8_sig.csv --fmt yaml --output-file schema_utf8.yml
schema-detect tests/data/orc/TestOrcFile.testDate1900.orc --fmt yaml --output-file schema_orc.yml
schema-detect tests/data/avro/weather.avro --fmt yaml --output-file schema_avro.yml
schema-detect tests/data/parquet/v0.7.1.all-named-index.parquet --fmt yaml --output-file schema_pqt.yml
schema-detect tests/data/delta/people_countries_delta_dask/ --fmt yaml --output-file schema_delta.yml
schema-detect tests/data/json/events.ndjson --fmt yaml --output-file schema_json.yml
schema-detect tests/data/xml/books.xml --fmt yaml --output-file schema_xml.yml
schema-detect tests/data/csv/ --multi-file-fmt txt
schema-detect tests/data/csv/sales_20250101.csv --fmt json --output-file schema_date.json

## To print the schema on CLI
schema-detect tests/data/json/events.ndjson --fmt dict

## To verify the schemas
schema-verify ./tests/data/csv/sales_20250101.csv ./tests/data/csv/sales_20260101.csv --fmt txt --output verify_sales_2025_vs_2026.txt
schema-verify ./tests/data/csv/sales_20250101.csv ./tests/data/csv/sales_20260101.csv --fmt json --output verify_sales_2025_vs_2026.json
schema-verify ./tests/data/csv/sales_20250101.csv ./tests/data/csv/sales_20260101.csv --fmt yaml --output verify_sales_2025_vs_2026.yml
schema-verify ./tests/data/csv/sales_20250101.csv ./tests/data/csv/sales_header.csv --fmt json --output verify_sales_2025_vs_header.json
schema-verify ./tests/data/csv/sales_20250101.csv ./tests/data/csv/sales_header.csv --fmt yaml --output verify_sales_2025_vs_header.yml
schema-verify ./tests/data/csv/sales_20250101.csv ./tests/data/csv/sales_header.csv --fmt txt --output verify_sales_2025_vs_header.txt
schema-verify ./cli/schema_2025.yml ./cli/schema_2026.yml --fmt txt
schema-verify ./api/schema_orc.yml ./api/schema_avro.yml --fmt json

```

```bash
## To test Python APIs
python .\tests\unit\combined_api_detect_write.py
python .\tests\unit\combined_api_verify.py
python .\tests\unit\detect_df_schemas.py
python .\tests\unit\verify_df_schemas.py
```

```bash
## To build the image
.\build.ps1 -Target [test|prod]
##or 


```



## Key Features

Supports single file or directory mode (multi-file detection).
Configurable via:

- YAML config (--config)
- Environment variables (PYSCH_*)
- CLI flags (highest precedence)
- Outputs schema in multiple formats: yaml, json, txt, or raw dict.


## Key flags :

--config CONFIG
Path to YAML config file for defaults.

--detection-mode {trust_hint,verify_hint,auto_detect}
Detection strategy (default: trust_hint).

--coverage-mode {any,max,full}
Sampling coverage (default: max).

--sample-records SAMPLE_RECORDS
Number of records to sample (default: 500).

--sample-bytes SAMPLE_BYTES
Byte-based sampling limit (default: 5MB).

--output-dir OUTPUT_DIR
Directory for schema outputs.

--output-file OUTPUT_FILE
File name for single-file mode (default: schema.yml).

--fmt {yaml,json,txt,dict}
Output format (default: yaml).

--multi-file-fmt MULTI_FILE_FMT
Optional suffix for multi-file outputs (e.g., schema → filename.schema.yaml).


## Performance & Limits

--zip-max-size ZIP_MAX_SIZE (default: 500MB)

--zip-max-members ZIP_MAX_MEMBERS (default: 100)

--sample-total-bytes-cap SAMPLE_TOTAL_BYTES_CAP (default: 1GB)

--max-file-size MAX_FILE_SIZE (default: 50GB)

--max-workers MAX_WORKERS (default: os.cpu_count())

--retries RETRIES (default: 3)

--timeout-seconds TIMEOUT_SECONDS (default: 180)


## Logging

--log-json → Structured JSON logs.

-v, --verbose → Increase verbosity.


## CSV-Specific Knobs

--csv.header {auto,true,false}
Header detection (auto flips to true if confidence ≥ 0.80).

--csv.delimiter CSV.DELIMITER
Custom delimiter.

--csv.quote CSV.QUOTE
Quote character.

--csv.escape CSV.ESCAPE
Escape character.

--encoding {utf-8,utf-8-sig,utf-16le,utf-16be}
File encoding.


## Test cases
```bash
## Check this repository for examples for CLI & API and the schema files in respective folders
git checkout https://github.com/aashish72it/schema-classifier-test-cases

```

<pre>

schema-classifier/
├─ README.md                        # Project overview, installation, usage
├─ LICENSE                          # License details
├─ build.ps1                        # build in windows
├─ build.sh                         # build in mac/linux
├─ pyproject.toml                   # Packaging metadata, dependencies, console script entrypoint
├─ .gitignore                       # Ignore build artifacts, venv, etc.
├─ src/
│  └─ pyschemaclassifier/           # Core library code
│     ├─ __init__.py
│     ├─ cli.py                     # CLI entrypoint: parses args, merges config, calls infer
│     ├─ infer.py                   # Orchestrator: classify → detect → normalize → emit
│     ├─ cli_verify.py              # CLI entrypoint for schema verify: parses args, merges config, calls infer
│     ├─ verify.py                  # Orchestrator: verify the schemas for 2 inputs(files/dir/pandas df/spark df)
│     ├─ config.py                  # Config model + load/merge logic (YAML/env/CLI precedence)
│     ├─ logging_utils.py           # Logging helpers (colored, JSON, verbosity)
│     ├─ exceptions.py              # Custom exceptions (ArgumentError, DetectionError, etc.)
│     ├─ models/
│     │  ├─ __init__.py
│     │  └─ schema.py               # Normalized schema model + Spark StructType JSON conversion
│     ├─ detection/                 # Format-specific schema detection
│     │  ├─ __init__.py
│     │  ├─ classifier.py           # Detect file type by extension/magic bytes/table markers
│     │  ├─ compression.py          # Handle gzip/bz2/xz/zstd/zip; size/member caps; corruption checks
│     │  ├─ sampling.py             # Sampling logic (records/bytes, coverage_mode, error budget)
│     │  ├─ csv.py                  # CSV detection: delimiter, header inference, BOM handling
│     │  ├─ json.py                 # NDJSON vs JSON array/object; recursive inference
│     │  ├─ xml.py                  # XML detection: element→object mapping, arrays via repeated tags
│     │  ├─ parquet.py              # Extract schema via PyArrow footer; logical type mapping
│     │  ├─ avro.py                 # Schema extraction via fastavro
│     │  ├─ orc.py                  # Schema extraction via pyorc
│     │  ├─ delta.py                # Delta Lake: parse _delta_log JSON for latest snapshot
│     │  ├─ iceberg.py              # Iceberg: parse metadata.json; partition transforms
│     │  └─ hudi.py                 # Hudi: COW support; raise TableFormatError for MOR
│     ├─ writers/                   # Output schema in different formats
│     │  ├─ __init__.py
│     │  ├─ yaml.py                 # Default writer: schema.yml
│     │  ├─ json.py                 # Pretty JSON output (schema + meta)
│     │  ├─ txt.py                  # Human-readable text summary
│     │  └─ struct.py               # Dict matching Spark StructType.jsonValue()
│     ├─ dataframe/                 # Detect schema from in-memory data
│     │  ├─ __init__.py
│     │  ├─ pandas.py               # detect_schema_from_df(pd.DataFrame)
│     │  └─ spark.py                # detect_schema_from_df(Spark DataFrame)
│     └─ utils/                     # Generic helpers
│        ├─ __init__.py
│        ├─ io.py                   # Safe file I/O, retries, timeouts, size checks
│        ├─ path.py                 # Path utilities, directory traversal, sampling selection
│        └─ metrics.py              # Confidence scoring, delimiter stability, provenance/meta helpers
├─ tests/
│  ├─ conftest.py                   # Pytest setup
│  ├─ unit/                         # Unit tests for individual modules
│  │  ├─ combined_cli_verify.py
│  │  ├─ combined_api_verify.py
│  │  ├─ combined_cli_detect.py
│  │  ├─ detect_df_schemas.py
│  │  ├─ verify_df_schemas.py
│  │  └─ combined_api_detect_write.py
│  ├─ integration/                  # End-to-end scenarios
│  │  ├─ test_directory_mode.py
│  │  ├─ test_zip_container.py
│  │  └─ test_parallel_sampling.py
│  ├─ data/                         # Test fixtures for all formats
│  │  ├─ csv/                       # CSV samples (header/no-header, BOM, wide)
│  │  ├─ json/                      # NDJSON samples
│  │  ├─ xml/                       # XML samples
│  │  ├─ parquet/                   # Parquet samples
│  │  ├─ avro/                      # Avro samples
│  │  ├─ orc/                       # ORC samples
│  │  ├─ delta/                     # Delta Lake minimal _delta_log
│  │  ├─ iceberg/                   # Iceberg metadata.json
│  │  ├─ hudi/                      # Hudi .hoodie markers
│  │  └─ containers/                # Compressed multi-entry zip
│  └─ golden/                       # Expected schema outputs for regression tests
├─ examples/
│  ├─ configs/
│  │  └─ mvp_defaults.yml           # Centralized defaults for detection/writing
│  ├─ cli/
│  │  ├─ detect_csv.sh              # Sample CLI commands for CSV
│  │  ├─ detect_json.sh             # Sample CLI commands for JSON
│  │  └─ detect_parquet.sh          # Sample CLI commands for Parquet
│  └─ api/
│     ├─ detect_from_path.md        # Programmatic usage: detect from file path
│     └─ detect_from_df.md          # Programmatic usage: detect from Spark/Pandas DataFrame
└─ docs/
   ├─ mvp_overview.md               # MVP architecture and goals
   └─ config_reference.md           # YAML keys, CLI flags, precedence



</pre>

