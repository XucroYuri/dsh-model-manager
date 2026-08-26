#!/usr/bin/env python3
"""dsh-model-manager: manage enabled model allowlists in DeepSeek Harness settings."""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("dsh-model-manager requires PyYAML (pip install pyyaml)") from exc


def load_settings(dsh_home: pathlib.Path) -> dict:
    path = dsh_home / "settings.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_settings(dsh_home: pathlib.Path, settings: dict) -> None:
    dsh_home.mkdir(parents=True, exist_ok=True)
    path = dsh_home / "settings.yaml"
    path.write_text(yaml.safe_dump(settings, sort_keys=False, allow_unicode=True), encoding="utf-8")


def get_providers(settings: dict) -> dict:
    llm = settings.get("llm-pi-ai", {})
    if not isinstance(llm, dict):
        return {}
    providers = llm.get("providers", {})
    return providers if isinstance(providers, dict) else {}


def list_models(settings: dict, provider_filter: str | None = None) -> list[tuple[str, str, str]]:
    result = []
    for provider, profile in get_providers(settings).items():
        if provider_filter and provider_filter != provider:
            continue
        if not isinstance(profile, dict):
            continue
        models = profile.get("models", [])
        if not isinstance(models, list):
            continue
        for model in models:
            if isinstance(model, dict) and "id" in model:
                result.append((provider, model["id"], model.get("name", "")))
    return result


def enable_model(settings: dict, provider: str, model_id: str) -> bool:
    providers = get_providers(settings)
    profile = providers.get(provider)
    if not isinstance(profile, dict):
        profile = {}
        providers[provider] = profile
    models = profile.get("models", [])
    if not isinstance(models, list):
        models = []
    if any(isinstance(m, dict) and m.get("id") == model_id for m in models):
        return False
    models.append({"id": model_id})
    profile["models"] = models
    llm = settings.setdefault("llm-pi-ai", {})
    if not isinstance(llm, dict):
        llm = {}
        settings["llm-pi-ai"] = llm
    llm["providers"] = providers
    return True


def disable_model(settings: dict, provider: str, model_id: str) -> bool:
    providers = get_providers(settings)
    profile = providers.get(provider)
    if not isinstance(profile, dict):
        return False
    models = profile.get("models", [])
    if not isinstance(models, list):
        return False
    new_models = [m for m in models if not (isinstance(m, dict) and m.get("id") == model_id)]
    if len(new_models) == len(models):
        return False
    profile["models"] = new_models
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dsh-home", default=os.environ.get("DSH_HOME") or str(pathlib.Path.home() / ".dsh"))
    sub = ap.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list enabled models")
    p_list.add_argument("--provider", default=None)

    p_enable = sub.add_parser("enable", help="enable a model")
    p_enable.add_argument("model", help="provider/model")

    p_disable = sub.add_parser("disable", help="disable a model")
    p_disable.add_argument("model", help="provider/model")

    p_search = sub.add_parser("search", help="search enabled models")
    p_search.add_argument("query")

    args = ap.parse_args(argv)
    dsh_home = pathlib.Path(args.dsh_home)
    settings = load_settings(dsh_home)

    if args.command == "list":
        for provider, model_id, name in list_models(settings, args.provider):
            suffix = f" ({name})" if name else ""
            print(f"{provider}/{model_id}{suffix}")
        return 0

    if args.command == "search":
        q = args.query.lower()
        for provider, model_id, name in list_models(settings):
            haystack = f"{provider}/{model_id} {name}".lower()
            if q in haystack:
                suffix = f" ({name})" if name else ""
                print(f"{provider}/{model_id}{suffix}")
        return 0

    if "/" not in args.model:
        print(f"error: expected provider/model, got {args.model!r}", file=sys.stderr)
        return 2
    provider, _, model_id = args.model.partition("/")

    if args.command == "enable":
        changed = enable_model(settings, provider, model_id)
        if changed:
            save_settings(dsh_home, settings)
            print(f"enabled {provider}/{model_id}")
        else:
            print(f"{provider}/{model_id} already enabled")
        return 0

    if args.command == "disable":
        changed = disable_model(settings, provider, model_id)
        if changed:
            save_settings(dsh_home, settings)
            print(f"disabled {provider}/{model_id}")
        else:
            print(f"{provider}/{model_id} not enabled")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
