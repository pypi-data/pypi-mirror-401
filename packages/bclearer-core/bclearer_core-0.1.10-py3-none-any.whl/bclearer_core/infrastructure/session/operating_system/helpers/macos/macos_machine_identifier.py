"""macOS specific machine identifier helpers."""

import re
import subprocess
import uuid

from bclearer_core.infrastructure.session.common.session_config import (
    MACOS_IOREG_COMMAND,
    MACOS_IOREG_UUID_PATTERN,
    MACOS_MACHINE_FALLBACK_PREFIX,
)


def get_macos_machine_identifier() -> (
    str
):
    try:
        output = (
            subprocess.check_output(
                MACOS_IOREG_COMMAND,
                text=True,
            )
        )
    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
    ):
        return f"{MACOS_MACHINE_FALLBACK_PREFIX}{uuid.getnode():012x}"

    match = re.search(
        MACOS_IOREG_UUID_PATTERN, output
    )
    if match:
        return match.group(1)

    return f"{MACOS_MACHINE_FALLBACK_PREFIX}{uuid.getnode():012x}"
