"""
Configurações globais do plugin
"""
import os

from mtcli.conf import config


SYMBOL = os.getenv("SYMBOL", config["DEFAULT"].get("symbol", fallback="WIN$N"))
DIGITOS = int(os.getenv("DIGITOS", config["DEFAULT"].getint("digitos", fallback=0)))
PERCENT_STEP = float(os.getenv("PERCENT_STEP", config["DEFAULT"].getfloat("percent_step", fallback=0.5)))
PERCENT_TOTAL = float(os.getenv("PERCENT_TOTAL", config["DEFAULT"].getfloat("percent_total", fallback=3)))
PERCENT_REF = os.getenv("PERCENT_REF", config["DEFAULT"].get("percent_ref", fallback="close"))
