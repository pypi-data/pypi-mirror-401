import os

from mtcli.conf import config

SYMBOL = os.getenv("SYMBOL", config["DEFAULT"].get("symbol", fallback="WIN$N"))
DIGITOS = int(os.getenv("DIGITOS", config["DEFAULT"].getint("digitos", fallback=0)))
