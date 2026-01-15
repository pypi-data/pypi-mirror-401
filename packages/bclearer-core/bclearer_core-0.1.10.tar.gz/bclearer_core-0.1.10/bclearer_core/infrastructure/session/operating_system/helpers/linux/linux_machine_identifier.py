"""Linux specific machine identifier helpers."""

import uuid
from pathlib import Path
from typing import Optional

from bclearer_core.infrastructure.session.common.session_config import (
    LINUX_MACHINE_ID_FALLBACK_PREFIX,
    LINUX_MACHINE_ID_PATHS,
)


def _read_machine_id_file(
    path: str | Path,
) -> Optional[str]:
    try:
        value = (
            Path(path)
            .read_text(encoding="utf-8")
            .strip()
        )
    except FileNotFoundError:
        return None

    return value or None


def get_linux_machine_identifier() -> (
    str
):
    for (
        candidate
    ) in LINUX_MACHINE_ID_PATHS:
        machine_id = (
            _read_machine_id_file(
                candidate
            )
        )
        if machine_id:
            return machine_id

    return f"{LINUX_MACHINE_ID_FALLBACK_PREFIX}{uuid.getnode():012x}"
