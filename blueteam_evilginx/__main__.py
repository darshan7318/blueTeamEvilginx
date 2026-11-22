"""Command line interface for local AiTM event correlation."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .engine import correlate


def main() -> None:
    parser = argparse.ArgumentParser(description="Correlate defensive identity telemetry for AiTM indicators")
    parser.add_argument("--input", required=True, help="JSONL event file")
    parser.add_argument("--output", help="Output JSON file (defaults to stdout)")
    args = parser.parse_args()
    events = []
    with Path(args.input).open(encoding="utf-8-sig") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                parser.error(f"invalid JSON on line {line_no}: {exc}")
    result = json.dumps(correlate(events), indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(result + "\n", encoding="utf-8")
    else:
        print(result)

if __name__ == "__main__":
    main()
