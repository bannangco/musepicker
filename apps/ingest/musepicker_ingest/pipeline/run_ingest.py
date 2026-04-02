from __future__ import annotations

import argparse
import json
from pathlib import Path

from musepicker_ingest.adapters.registry import create_api_first_adapters
from musepicker_ingest.adapters.scraper_fallback import ScraperFallbackAdapter
from musepicker_ingest.config import IngestConfig
from musepicker_ingest.pipeline.runner import IngestRunner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MusePicker ingest workers")
    parser.add_argument("--source", help="One source only (klook|tripcom|ticketstodo|viator|scraper_fallback)")
    parser.add_argument("--fixture", help="Optional fixture path for the selected source")
    parser.add_argument("--root-dir", default=".ingest-data", help="Storage root for snapshots/state/runs/metrics")
    parser.add_argument("--dry-run", action="store_true", help="Validate and process without persisting state")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root_dir = Path(args.root_dir).resolve()
    config = IngestConfig(root_dir=root_dir)

    fixtures = {}
    if args.source and args.fixture:
        fixtures[args.source] = Path(args.fixture).resolve()

    adapters = create_api_first_adapters(fixtures=fixtures)

    if args.source == "scraper_fallback":
        if not args.fixture:
            raise SystemExit("--fixture is required for scraper_fallback source")
        adapters["scraper_fallback"] = ScraperFallbackAdapter(fixture_path=Path(args.fixture).resolve())

    runner = IngestRunner(config=config, adapters=adapters.values())
    summary = runner.run(source=args.source, dry_run=args.dry_run)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
