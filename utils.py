import os
import time

GROUPS_DIR = "group_data"
TOKEN_POOL_PATH = "token_pool.txt"

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def write_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

def append_file(path, data):
    with open(path, "a", encoding="utf-8") as f:
        f.write(data + "\n")

def load_placeholders(path):
    values = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    values[key.strip()] = val.strip()
    return values

def apply_placeholders(msg: str, placeholders: dict) -> str:
    for key, value in placeholders.items():
        msg = msg.replace(key, value)
    return msg

def log_bad_token(group_name, token, error_info=""):
    path = os.path.join(GROUPS_DIR, group_name, "bad_tokens.txt")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    append_file(path, f"{timestamp} | {token} | {error_info}")

def replace_token_from_pool(group_name, bad_token):
    group_path = os.path.join(GROUPS_DIR, group_name)
    token_path = os.path.join(group_path, "tokens.txt")

    if not os.path.exists(TOKEN_POOL_PATH):
        return False

    pool_tokens = [t.strip() for t in read_file(TOKEN_POOL_PATH).splitlines() if t.strip()]
    if not pool_tokens:
        return False

    new_token = pool_tokens.pop(0)

    # Update group tokens
    group_tokens = [t.strip() for t in read_file(token_path).splitlines() if t.strip()]
    group_tokens = [new_token if t == bad_token else t for t in group_tokens]
    write_file(token_path, "\n".join(group_tokens))

    # Update pool
    write_file(TOKEN_POOL_PATH, "\n".join(pool_tokens))

    return True
