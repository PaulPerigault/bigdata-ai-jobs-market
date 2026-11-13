"""Check that a locally downloaded copy of the real dataset is the one the project was built on.

    python data/verify_raw.py [path]    default: data/raw/ai_jobs_market_2025_2026.csv

The file is not in the repository (data/README.md says why). The expected SHA-256, size and row
count were measured on the file used by the original project.
"""

import hashlib
import sys
from pathlib import Path

DEFAULT = Path(__file__).parent / "raw" / "ai_jobs_market_2025_2026.csv"
SHA256 = "6ae7bc7bf724250cd8c977f86b620128318070a23cb0b17340e58d2321f7864e"
BYTES = 383_900
LINES = 1_501  # header + 1500 offers


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT
    if not path.is_file():
        print(f"{path}: not found. See data/README.md to download it.", file=sys.stderr)
        return 1
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    lines = data.count(b"\n")
    problems = []
    if digest != SHA256:
        problems.append(f"SHA-256 is {digest}, expected {SHA256}")
    if len(data) != BYTES or lines != LINES:
        problems.append(f"{len(data)} bytes and {lines} lines, expected {BYTES} and {LINES}")
    for problem in problems:
        print(f"{path}: {problem}", file=sys.stderr)
    if not problems:
        print(f"{path}: OK ({len(data)} bytes, {lines} lines, SHA-256 matches)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
