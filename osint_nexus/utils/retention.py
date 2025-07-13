from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import List


def cleanup_files(directory: Path | str, pattern: str, max_age_hours: int = 24) -> List[Path]:
    """Elimina archivos que coincidan con un patrón si superan la antigüedad dada."""
    now = datetime.utcnow()
    removed: List[Path] = []
    directory = Path(directory)
    for file_path in directory.glob(pattern):
        mtime = datetime.utcfromtimestamp(file_path.stat().st_mtime)
        if now - mtime > timedelta(hours=max_age_hours):
            try:
                file_path.unlink()
                removed.append(file_path)
            except Exception:  # pylint: disable=broad-except
                pass
    return removed