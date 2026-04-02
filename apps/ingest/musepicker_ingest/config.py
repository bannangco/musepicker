from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class IngestConfig:
    root_dir: Path
    retries: int = 3
    initial_backoff_seconds: float = 0.5

    @property
    def state_dir(self) -> Path:
        return self.root_dir / "state"

    @property
    def snapshots_dir(self) -> Path:
        return self.root_dir / "snapshots"

    @property
    def runs_dir(self) -> Path:
        return self.root_dir / "runs"

    @property
    def metrics_dir(self) -> Path:
        return self.root_dir / "metrics"
