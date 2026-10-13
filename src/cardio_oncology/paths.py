from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    source: Path
    processed: Path
    run: Path


def project_paths(root: Path) -> ProjectPaths:
    root = Path(root).resolve()
    return ProjectPaths(root=root,
                        source=root / "data/private/source",
                        processed=root / "data/private/processed",
                        run=root / "results/private/runs/current")
