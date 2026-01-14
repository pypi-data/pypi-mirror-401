import requests
from packaging import version
from m2h_ai import __version__

PYPI_URL = "https://pypi.org/pypi/m2h-ai/json"


def check_for_update():
    try:
        r = requests.get(PYPI_URL, timeout=3)
        if r.status_code != 200:
            return

        latest = r.json()["info"]["version"]

        if version.parse(latest) > version.parse(__version__):
            print(
                f"\n⬆ Update available: {__version__} → {latest}\n"
                f"Run: pip install --upgrade m2h-ai\n"
            )
    except Exception:
        pass
