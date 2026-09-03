"""
Order numbering and ID generation, persisted to a local JSON file so
counts survive bot restarts.
"""

import json
import os
import random
import string
from pathlib import Path
from threading import Lock

from dotenv import load_dotenv

load_dotenv()

DATA_FILE = Path(__file__).parent / "data" / "orders.json"
_lock = Lock()

START_ORDER_NUMBER = int(os.getenv("START_ORDER_NUMBER", "1000"))


def _load() -> dict:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        _save({"last_order_number": START_ORDER_NUMBER - 1})
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def next_order_number() -> int:
    """Returns the next sequential order number, shown as e.g. 'Order #1001'."""
    with _lock:
        data = _load()
        data["last_order_number"] += 1
        _save(data)
        return data["last_order_number"]


def generate_order_id() -> str:
    """Generates a long random numeric Order ID. Purely cosmetic — not
    sequential and not tied to any real payment system."""
    first_digit = random.choice("123456789")
    rest = "".join(random.choices(string.digits, k=27))
    return first_digit + rest
