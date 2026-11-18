"""Cliente RESTCONF para Cisco IOS-XE - Creado por Ricardo Daniel."""
import os
import requests
import urllib3

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}


class RestconfClient:

    def __init__(self, host, port=443):
        self.base = f"https://{host}:{port}/restconf/data"
        self.auth = (os.environ["SANDBOX_USER"], os.environ["SANDBOX_PASS"])
        self.verify = os.getenv("VERIFY_SSL", "false").lower() == "true"
        if not self.verify:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

    def _url(self, path):
        return f"{self.base}/{path}"

    def get(self, path):
        r = requests.get(
            self._url(path), headers=HEADERS, auth=self.auth,
            verify=self.verify, timeout=30
        )
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def put(self, path, payload):
        r = requests.put(
            self._url(path), headers=HEADERS, auth=self.auth,
            json=payload, verify=self.verify, timeout=30
        )
        r.raise_for_status()
        return r.status_code
