from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Dict, Any, List, Tuple

import numpy as np
from PIL import Image

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}


@dataclass(frozen=True)
class ImageError:
    path: str
    error: str


def iter_image_paths(root: Path, exts: set[str] = IMAGE_EXTS) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            yield p


def dhash(img: Image.Image, hash_size: int = 8) -> int:
    g = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    arr = np.asarray(g, dtype=np.int16)
    diff = arr[:, 1:] > arr[:, :-1]
    # Pack bits row-major into an int
    bits = diff.flatten()
    out = 0
    for b in bits:
        out = (out << 1) | int(b)
    return out


def _percentiles(values: List[int], ps=(0, 5, 50, 95, 100)) -> Dict[str, float]:
    if not values:
        return {}
    a = np.array(values, dtype=np.float64)
    qs = np.percentile(a, ps).tolist()
    return {f"p{int(p)}": float(q) for p, q in zip(ps, qs)}


def _streaming_mean_std_rgb(sample_paths: List[Path]) -> Tuple[List[float], List[float], int]:
    # Streaming Welford over all pixels of sampled images (converted to RGB)
    n = 0
    mean = np.zeros(3, dtype=np.float64)
    m2 = np.zeros(3, dtype=np.float64)

    used = 0
    for p in sample_paths:
        try:
            with Image.open(p) as im:
                im = im.convert("RGB")
                arr = np.asarray(im, dtype=np.float32) / 255.0
        except Exception:
            continue

        x = arr.reshape(-1, 3).astype(np.float64, copy=False)
        if x.size == 0:
            continue

        used += 1
        for row in x:
            n += 1
            delta = row - mean
            mean += delta / n
            delta2 = row - mean
            m2 += delta * delta2

    if n < 2:
        return [float(x) for x in mean], [0.0, 0.0, 0.0], used

    var = m2 / (n - 1)
    std = np.sqrt(var)
    return [float(x) for x in mean], [float(x) for x in std], used


def audit_folder(
    root: str | Path,
    *,
    sample_images: int = 200,
    hash_size: int = 8,
    compute_dupes: bool = True,
    max_error_examples: int = 50,
) -> Dict[str, Any]:
    root = Path(root).expanduser().resolve()
    paths = list(iter_image_paths(root))

    formats: Dict[str, int] = {}
    modes: Dict[str, int] = {}
    widths: List[int] = []
    heights: List[int] = []
    errors: List[ImageError] = []
    dhash_map: Dict[int, List[str]] = {}

    for p in paths:
        try:
            with Image.open(p) as im:
                fmt = (im.format or "UNKNOWN").upper()
                formats[fmt] = formats.get(fmt, 0) + 1

                mode = im.mode
                modes[mode] = modes.get(mode, 0) + 1

                w, h = im.size
                widths.append(int(w))
                heights.append(int(h))

                if compute_dupes:
                    try:
                        hval = dhash(im, hash_size=hash_size)
                        dhash_map.setdefault(hval, []).append(str(p))
                    except Exception:
                        # hashing failure shouldn't kill the audit
                        pass

        except Exception as e:
            if len(errors) < max_error_examples:
                errors.append(ImageError(path=str(p), error=str(e)))

    # sample for mean/std
    sample_paths = paths[:]
    if len(sample_paths) > sample_images:
        rng = np.random.default_rng(0)
        idx = rng.choice(len(sample_paths), size=sample_images, replace=False)
        sample_paths = [sample_paths[i] for i in idx]

    mean, std, used = _streaming_mean_std_rgb(sample_paths)

    dupes = []
    if compute_dupes:
        for hval, plist in dhash_map.items():
            if len(plist) >= 2:
                dupes.append(
                    {
                        "hash": hex(hval),
                        "count": len(plist),
                        "paths": plist[:50],  # cap for readability
                    }
                )
        dupes.sort(key=lambda x: x["count"], reverse=True)

    report: Dict[str, Any] = {
        "root": str(root),
        "n_files_total": len(paths),
        "formats": dict(sorted(formats.items(), key=lambda kv: kv[1], reverse=True)),
        "modes": dict(sorted(modes.items(), key=lambda kv: kv[1], reverse=True)),
        "width": _percentiles(widths),
        "height": _percentiles(heights),
        "mean_std_rgb_approx": {
            "n_images_used": used,
            "mean": mean,
            "std": std,
            "sample_images_target": sample_images,
        },
        "errors": [e.__dict__ for e in errors],
    }
    if compute_dupes:
        report["duplicates_dhash"] = dupes

    return report