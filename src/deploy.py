"""Aplica la configuración por RESTCONF por Ricardo Daniel. --check = prueba en seco."""
import argparse
import sys
import yaml
from payloads import build_items, is_subset
from restconf_client import RestconfClient


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/vars.yml")
    ap.add_argument("--check", action="store_true", help="no modifica el equipo")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    client = RestconfClient(cfg["host"], cfg.get("port", 443))
    changes = 0

    for path, payload in build_items(cfg):
        current = client.get(path)
        if current is not None and is_subset(payload, current):
            print(f"[OK] sin cambios -> {path}")
            continue
        changes += 1
        if args.check:
            print(f"[CAMBIO] se aplicaría -> {path}")
        else:
            code = client.put(path, payload)
            print(f"[APLICADO] HTTP {code} -> {path}")

    estado = "pendiente(s)" if args.check else "aplicado(s)"
    print(f"\nResumen: {changes} cambio(s) {estado}")
    return 0


if __name__ == "__main__":
    sys.exit(main())