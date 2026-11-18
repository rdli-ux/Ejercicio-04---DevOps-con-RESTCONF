"""Construye los payloads YANG para Ricardo Daniel a partir de config/vars.yml."""
NATIVE = "Cisco-IOS-XE-native:native"


def build_items(cfg):
    lb, snmp = cfg["loopback"], cfg["snmp"]
    return [
        (
            f"{NATIVE}/interface/Loopback={lb['id']}",
            {
                "Cisco-IOS-XE-native:Loopback": {
                    "name": lb["id"],
                    "description": lb["description"],
                    "ip": {"address": {"primary": {
                        "address": lb["ip"], "mask": lb["mask"]}}},
                }
            },
        ),
        (
            f"{NATIVE}/snmp-server/Cisco-IOS-XE-snmp:community={snmp['community']}",
            {"Cisco-IOS-XE-snmp:community": {
                "name": snmp["community"], "RO": [None]}},
        ),
        (
            f"{NATIVE}/snmp-server/Cisco-IOS-XE-snmp:location",
            {"Cisco-IOS-XE-snmp:location": snmp["location"]},
        ),
        (
            f"{NATIVE}/snmp-server/Cisco-IOS-XE-snmp:contact",
            {"Cisco-IOS-XE-snmp:contact": snmp["contact"]},
        ),
    ]


def is_subset(desired, current):
    """True si todo lo deseado ya existe en la configuración actual."""
    if isinstance(desired, dict):
        return isinstance(current, dict) and all(
            k in current and is_subset(v, current[k]) for k, v in desired.items()
        )
    if isinstance(desired, list):
        return isinstance(current, list) and len(desired) == len(current) and all(
            isinstance(d, dict) and any(is_subset(d, c) for c in current) for d in desired
        )
    return str(desired) == str(current)
