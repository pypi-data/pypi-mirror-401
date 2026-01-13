"""Process checking utilities for twshtd."""

import subprocess


def is_process_running(process_name: str) -> bool:
    """
    Check if a process is running by name.

    Uses pgrep -x for exact process name matching.

    Args:
        process_name: Name of the process to check

    Returns:
        True if the process is running, False otherwise
    """
    result = subprocess.run(
        ["pgrep", "-x", process_name],
        capture_output=True,
    )
    return result.returncode == 0


def check_anki_running() -> bool:
    """
    Check if Anki is currently running.

    Returns:
        True if Anki is running, False otherwise
    """
    return is_process_running("anki")
