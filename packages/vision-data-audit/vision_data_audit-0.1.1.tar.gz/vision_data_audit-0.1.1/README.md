# vision-data-audit

Audit an image dataset folder in seconds. Get counts, stats, and duplicates.

## What you get

- Image formats (JPEG, PNG, etc.)
- Color modes (RGB, grayscale, etc.)
- Size distribution (width/height percentiles)
- RGB mean/std (quick estimate for normalization)
- Duplicate detection (perceptual hash)

## Install
```bash
pip install vision-data-audit
```

## Usage

**Basic audit:**
```bash
vision-data-audit /path/to/images
```

**Save to JSON:**
```bash
vision-data-audit /path/to/images --out report.json
```

**Skip duplicates (faster):**
```bash
vision-data-audit /path/to/images --no-dupes
```

## Options

- `--out FILE` - save report as JSON
- `--no-dupes` - skip duplicate detection
- `--sample N` - max images for mean/std (default: 200)

## Python
```python
from vision_data_audit.core import audit_folder

report = audit_folder(
    "/path/to/images",
    sample_images=200,
    hash_size=8,
    compute_dupes=True,
)

print(report["formats"])
print(report["width"], report["height"])
print(report["mean_std_rgb_approx"])

# Duplicate groups (if enabled)
print(report.get("duplicates_dhash", []))
```

## Notes

- Mean/std uses a random sample for speed
- Duplicates found using perceptual hashing (dHash)


## Help improve this

If you use this tool, please open a GitHub issue with:
- the command you ran
- the printed summary (or report.json with paths removed)
- what you wish it reported (corrupt files? split leakage? near-duplicates?)

Ideas on the roadmap:
- near-duplicate grouping by Hamming distance threshold
- train/val/test leakage detection across subfolders
- faster mean/std computation (vectorized)

## Development
```bash
uv sync
uv run vision-data-audit --help
uv run pytest
uv build
```

## License
Apache-2.0