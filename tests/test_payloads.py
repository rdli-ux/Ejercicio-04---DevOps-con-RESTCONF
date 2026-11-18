"""Pruebas unitarias desarrolladas por Ricardo Daniel."""
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from payloads import build_items, is_subset  # noqa: E402

with open(ROOT / "config" / "vars.yml", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)


def test_cuatro_recursos():
    assert len(build_items(CFG)) == 4


def test_loopback_ip_en_payload():
    path, body = build_items(CFG)[0]
    assert "Loopback=201" in path
    prim = body["Cisco-IOS-XE-native:Loopback"]["ip"]["address"]["primary"]
    assert prim["address"] == CFG["loopback"]["ip"]


def test_is_subset():
    assert is_subset({"a": 1}, {"a": 1, "b": 2})
    assert not is_subset({"a": 1}, {"a": 2})