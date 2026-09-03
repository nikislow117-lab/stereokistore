"""
Storage for watched crypto wallet addresses, keyed by guild.

Persisted to a local JSON file so watched addresses and which
transactions have already been posted/edited survive bot restarts.
"""

import json
from pathlib import Path
from threading import Lock

DATA_FILE = Path(__file__).parent / "data" / "wallets.json"
_lock = Lock()


def _load() -> dict:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        _save({})
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_wallet(guild_id: int, address: str, chain: str, added_by: int) -> bool:
    """Returns False if this address+chain is already watched in this guild."""
    with _lock:
        data = _load()
        guild = data.setdefault(str(guild_id), {})
        key = f"{chain}:{address}"
        if key in guild:
            return False
        guild[key] = {
            "address": address,
            "chain": chain,
            "added_by": added_by,
            "known_txs": {},  # "{tx_hash}:{tx_output_n}" -> {message_id, channel_id, confirmations}
        }
        _save(data)
        return True


def remove_wallet(guild_id: int, address: str, chain: str) -> bool:
    with _lock:
        data = _load()
        guild = data.get(str(guild_id), {})
        key = f"{chain}:{address}"
        if key not in guild:
            return False
        del guild[key]
        _save(data)
        return True


def list_wallets(guild_id: int) -> list:
    data = _load()
    return list(data.get(str(guild_id), {}).values())


def all_wallets() -> dict:
    """Returns {guild_id: [wallet_dict, ...]} for every guild — used by the poller."""
    data = _load()
    return {int(gid): list(wallets.values()) for gid, wallets in data.items()}


def record_tx_posted(guild_id: int, address: str, chain: str, tx_key: str,
                      message_id: int, channel_id: int, confirmations: int) -> None:
    with _lock:
        data = _load()
        wallet = data[str(guild_id)][f"{chain}:{address}"]
        wallet["known_txs"][tx_key] = {
            "message_id": message_id,
            "channel_id": channel_id,
            "confirmations": confirmations,
        }
        _save(data)


def update_tx_confirmations(guild_id: int, address: str, chain: str, tx_key: str,
                             confirmations: int) -> None:
    with _lock:
        data = _load()
        wallet = data[str(guild_id)][f"{chain}:{address}"]
        if tx_key in wallet["known_txs"]:
            wallet["known_txs"][tx_key]["confirmations"] = confirmations
            _save(data)