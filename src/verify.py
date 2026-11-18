"""Fase MONITOR de Ricardo Daniel: confirma que el estado real coincide con el deseado."""
import sys
import yaml
from payloads import build_items, is_subset
from restconf_client import RestconfClient


def main():
    with open("config/vars.yml", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    client = RestconfClient(cfg["host"], cfg.get("port", 443))
    failed = 0

    for path, payload in build_items(cfg):
        current = client.get(path)
        ok = current is not None and is_subset(payload, current)
        print(f"[{'PASS' if ok else 'FAIL'}] {path}")
        if not ok:
            failed += 1

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
