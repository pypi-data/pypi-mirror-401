"""Configuration parsing for twshtd."""

import logging
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

_log = logging.getLogger(__name__)


@dataclass
class RepoConfig:
    """Configuration for a single repository."""

    path: Path
    pull_mode: Literal["pull", "fetch"] = "pull"
    pre_command: str | None = None
    post_command: str | None = None
    enabled: bool = True


@dataclass
class Settings:
    """Global settings for twshtd."""

    workers: int = 1  # 1 = sequential, >1 = parallel


@dataclass
class DirtyConfig:
    """Configuration for a directory to scan for dirty repos."""

    path: Path
    enabled: bool = True


@dataclass
class Config:
    """Full configuration for twshtd."""

    settings: Settings = field(default_factory=Settings)
    repos: list[RepoConfig] = field(default_factory=list)
    dirty: list[DirtyConfig] = field(default_factory=list)


def resolve_env_vars(path_str: str) -> str:
    """
    Resolve environment variables and user home directory in path strings.
    Supports both $VAR and ${VAR} syntax, plus ~ expansion.
    """
    # First expand user home directory (~)
    expanded = os.path.expanduser(path_str)
    # Then expand environment variables ($VAR and ${VAR})
    resolved = os.path.expandvars(expanded)
    return resolved


def get_default_config_path() -> Path:
    """Return the default config file path."""
    if env_path := os.environ.get("TWSHTD_CONFIG"):
        return Path(env_path)
    return Path.home() / ".config" / "twshtd" / "repos.toml"


def parse_config(config_file: Path) -> Config:
    """
    Parse TOML config file and return Config object.

    Args:
        config_file: Path to the TOML configuration file

    Returns:
        Config object with settings and repos

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config is invalid
    """
    _log.debug("Parsing config file: %s", config_file)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with config_file.open("rb") as f:
        data = tomllib.load(f)

    # Parse settings
    settings_data = data.get("settings", {})
    settings = Settings(
        workers=settings_data.get("workers", 1),
    )
    _log.debug("Settings: workers=%s", settings.workers)

    # Parse repos
    repos: list[RepoConfig] = []
    for repo_data in data.get("repos", []):
        path_str = repo_data.get("path")
        if not path_str:
            raise ValueError("Each repo must have a 'path' field")

        resolved_path = resolve_env_vars(path_str)
        repo = RepoConfig(
            path=Path(resolved_path),
            pull_mode=repo_data.get("pull_mode", "pull"),
            pre_command=repo_data.get("pre_command"),
            post_command=repo_data.get("post_command"),
            enabled=repo_data.get("enabled", True),
        )
        repos.append(repo)
        _log.debug(
            "Repo: %s (mode=%s, enabled=%s)", repo.path, repo.pull_mode, repo.enabled
        )

    # Parse dirty directories
    dirty: list[DirtyConfig] = []
    for dirty_data in data.get("dirty", []):
        path_str = dirty_data.get("path")
        if not path_str:
            raise ValueError("Each dirty entry must have a 'path' field")

        resolved_path = resolve_env_vars(path_str)
        dirty_config = DirtyConfig(
            path=Path(resolved_path),
            enabled=dirty_data.get("enabled", True),
        )
        dirty.append(dirty_config)
        _log.debug("Dirty: %s (enabled=%s)", dirty_config.path, dirty_config.enabled)

    _log.debug(
        "Config loaded: %d repos, %d dirty directories", len(repos), len(dirty)
    )
    return Config(settings=settings, repos=repos, dirty=dirty)
