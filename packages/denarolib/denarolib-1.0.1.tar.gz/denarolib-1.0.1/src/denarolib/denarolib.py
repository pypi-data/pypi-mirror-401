import requests
import time
import json
import hashlib
from ecdsa import SigningKey, SECP256k1

DECIMALS = 10**6
NODE = "http://denaro.mine.bz:3006/"
DEBUG = False

def get_node_info():
    response = requests.get(NODE)
    if DEBUG: print(response); print(response.json())
    return response

def get_status():
    response = requests.get(NODE+"get_status")
    if DEBUG: print(response); print(response.json())
    return response

def get_peers():
    response = requests.get(NODE+"get_peers")
    if DEBUG: print(response); print(response.json())
    return response

def get_block():
    response = requests.get(NODE+"get_block")
    if DEBUG: print(response); print(response.json())
    return response

def get_blocks():
    response = requests.get(NODE+"get_blocks")
    if DEBUG: print(response); print(response.json())
    return response

def get_transaction(txhash):
    response = requests.get(NODE+"get_transaction?"+txhash)
    if DEBUG: print(response); print(response.json())
    return response

def get_pending_transactions():
    response = requests.get(NODE+"get_transactions")
    if DEBUG: print(response); print(response.json())
    return response

def get_address_info(addr):
    response = requests.get(NODE+"get_address_info?address="+addr)
    if DEBUG: print(response); print(response.json())
    return response

def submit_tx(tx_hex):
    response = requests.post(NODE+"submit_tx", json={"tx_hex":tx_hex})
    if DEBUG: print(response); print(response.json())
    return response

def sync_blockchain():
    response = requests.get(NODE+"sync_blockchain")
    if DEBUG: print(response); print(response.json())
    return response

def get_mining_info():
    response = requests.get(NODE+"get_mining_info")
    if DEBUG: print(response); print(response.json())
    return response

def submit_block(id,content,txs):
    response = requests.post(NODE+"submit_block", json={"id":id, "block_content":content, "txs":txs})
    if DEBUG: print(response); print(response.json())
    return response

def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def double_sha256(b: bytes) -> bytes:
    return sha256(sha256(b))


def amount_to_int(amount: float) -> int:
    return int(round(amount * DECIMALS))


def build_tx_object(from_addr: str, to_addr: str, amount_int: int) -> dict:
    return {
        "inputs": [
            {
                "address": from_addr,
                "amount": amount_int
            }
        ],
        "outputs": [
            {
                "address": to_addr,
                "amount": amount_int
            }
        ],
        "timestamp": int(time.time())
    }


def serialize_tx(tx: dict) -> bytes:
    return json.dumps(
        tx,
        sort_keys=True,
        separators=(",", ":")
    ).encode()


def sign_tx(tx_bytes: bytes, privkey_hex: str) -> dict:
    sk = SigningKey.from_string(bytes.fromhex(privkey_hex), curve=SECP256k1)
    digest = double_sha256(tx_bytes)

    signature = sk.sign_digest(digest)
    pubkey = sk.get_verifying_key().to_string()

    return {
        "signature": signature.hex(),
        "public_key": pubkey.hex()
    }

def make_tx_hex(from_addr: str, to_addr: str, amount: float, privkey_hex: str) -> str:
    amount_int = amount_to_int(amount)
    tx = build_tx_object(from_addr, to_addr, amount_int)
    tx_bytes = serialize_tx(tx)
    sig_block = sign_tx(tx_bytes, privkey_hex)
    tx["signature"] = sig_block["signature"]
    tx["public_key"] = sig_block["public_key"]
    final_bytes = serialize_tx(tx)
    return final_bytes.hex()

def send(from_addr: str, to_addr: str, amount: float, privkey_hex: str):
    return submit_tx(make_tx_hex(from_addr, to_addr, amount, privkey_hex))

