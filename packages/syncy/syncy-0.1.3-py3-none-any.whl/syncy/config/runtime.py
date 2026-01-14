from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import click

from .rules import RULE_PACK

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - handled at runtime
    yaml = None


def load_yaml_config(path: Optional[str]) -> Dict[str, Any]:
    """Load YAML config file if provided and available. Supports env expansion.

    Precedence (CLI resolution) is applied outside this helper; here we just read.
    """
    if path is None:
        default = Path("validator.yaml")
        if not default.exists():
            return {}
        path = str(default)

    if yaml is None:
        click.echo("PyYAML not installed; skipping YAML config.", err=True)
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # environment variable expansion: ${VAR}
        expanded = os.path.expandvars(content)
        data = yaml.safe_load(expanded) or {}
        if not isinstance(data, dict):
            return {}
        return data
    except FileNotFoundError:
        return {}
    except Exception as exc:  # pragma: no cover - runtime safeguard
        click.echo(f"Failed to parse config at {path}: {exc}", err=True)
        return {}


def read_rules_yaml_file(path: str) -> List[dict]:
    """Read rule pack from a YAML file, falling back to built-in on errors."""
    if yaml is None:
        click.echo("PyYAML not installed; using built-in rules.", err=True)
        return RULE_PACK
    try:
        p = Path(os.path.expandvars(os.path.expanduser(path)))
        with open(p, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("rules"), list):
            return data["rules"]
        click.echo("Rules YAML did not contain a list; using built-in rules.", err=True)
        return RULE_PACK
    except FileNotFoundError:
        click.echo(f"Rules file not found: {path}. Using built-in rules.", err=True)
        return RULE_PACK
    except Exception as exc:  # pragma: no cover
        click.echo(f"Failed to load rules from {path}: {exc}. Using built-in rules.", err=True)
        return RULE_PACK


def resolve_rule_pack(rules_path: Optional[str], cfg: Dict[str, Any]) -> List[dict]:
    """Resolve rule pack with precedence: CLI path > YAML inline/path > built-in."""
    if rules_path:
        return read_rules_yaml_file(rules_path)
    candidate = cfg.get("rules") or cfg.get("rule_pack")
    if isinstance(candidate, list):
        return candidate
    if isinstance(candidate, str):
        return read_rules_yaml_file(candidate)
    return RULE_PACK


def resolve_connection_urls(
    source: Optional[str], target: Optional[str], config_path: Optional[str]
) -> Tuple[str, str]:
    """Resolve connection URLs with precedence: flags > YAML > env vars.

    Env vars: SYNCY_SOURCE_URL, SYNCY_TARGET_URL
    YAML keys: source.url, target.url
    """
    cfg = load_yaml_config(config_path)
    cfg_source = (
        (cfg.get("source") or {}).get("url") if isinstance(cfg.get("source"), dict) else None
    )
    cfg_target = (
        (cfg.get("target") or {}).get("url") if isinstance(cfg.get("target"), dict) else None
    )

    src = source or cfg_source or os.getenv("SYNCY_SOURCE_URL")
    tgt = target or cfg_target or os.getenv("SYNCY_TARGET_URL")

    if not src or not tgt:
        raise click.ClickException(
            "Missing connection URLs. Provide via CLI flags, validator.yaml, or env vars.\n"
            "- CLI: --source <url> --target <url>\n"
            "- YAML: validator.yaml with source.url and target.url\n"
            "- ENV: SYNCY_SOURCE_URL, SYNCY_TARGET_URL"
        )

    return src, tgt

