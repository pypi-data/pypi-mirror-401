from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import audit_folder


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="vision-data-audit",
        description="Quick audit of an image folder: formats, sizes, mean/std, duplicates.",
    )
    p.add_argument("path", help="Folder containing images")
    p.add_argument("--out", help="Write full JSON report to this file")
    p.add_argument("--sample", type=int, default=200, help="Max images to sample for mean/std (default: 200)")
    p.add_argument("--hash-size", type=int, default=8, help="dHash size (default: 8)")
    p.add_argument("--no-dupes", action="store_true", help="Skip duplicate detection")
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    return p


def main() -> None:
    args = build_parser().parse_args()
    report = audit_folder(
        args.path,
        sample_images=args.sample,
        hash_size=args.hash_size,
        compute_dupes=not args.no_dupes,
    )

    # human summary
    print(f"Root: {report['root']}")
    print(f"Images found: {report['n_files_total']}")
    if report.get("errors"):
        print(f"Errors (showing up to {len(report['errors'])}): {len(report['errors'])}")

    fmts = report.get("formats", {})
    if fmts:
        top = ", ".join([f"{k}:{v}" for k, v in list(fmts.items())[:5]])
        print(f"Top formats: {top}")

    if "duplicates_dhash" in report:
        dupes = report["duplicates_dhash"]
        print(f"Duplicate groups (dHash): {len(dupes)}")
        if dupes:
            print("Top duplicate group:")
            print(f"  hash={dupes[0]['hash']} count={dupes[0]['count']}")

    if args.out:
        out_path = Path(args.out).expanduser()
        payload = json.dumps(report, indent=2 if args.pretty else None)
        out_path.write_text(payload, encoding="utf-8")
        print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()