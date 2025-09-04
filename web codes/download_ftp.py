# download_ftp.py
# Recursively download all files/folders from FTP directory.

import os
import posixpath
from ftplib import FTP, error_perm

# ===== CONFIG =====
FTP_HOST = "ftpupload.net"
FTP_USER = "if0_38887836"
FTP_PASS = "uZnrqJ55D3nN"
FTP_REMOTE_DIR = "/htdocs"
LOCAL_DIR = "./web codes/htdocs"
# ==================

def _ensure_local_dir(path):
    os.makedirs(path, exist_ok=True)

def download_file(ftp, remote_path, local_path):
    _ensure_local_dir(os.path.dirname(local_path))
    with open(local_path, "wb") as f:
        ftp.retrbinary(f"RETR " + remote_path, f.write)
    print(f"↓ Downloaded: {remote_path} -> {local_path}")

def _is_dir(ftp, name):
    curr = ftp.pwd()
    try:
        ftp.cwd(name)
        ftp.cwd(curr)
        return True
    except error_perm:
        return False

def download_dir(ftp, remote_dir, local_dir):
    _ensure_local_dir(local_dir)
    ftp.cwd(remote_dir)

    try:
        entries = list(ftp.mlsd())
    except Exception:
        # fallback if MLSD unsupported
        entries = [(n, {}) for n in ftp.nlst()]

    for name, facts in entries:
        if name in (".", ".."):
            continue
        remote_path = posixpath.join(ftp.pwd(), name)
        local_path = os.path.join(local_dir, name)

        kind = facts.get("type") if isinstance(facts, dict) else None
        if kind == "dir" or _is_dir(ftp, name):
            download_dir(ftp, name, local_path)
            ftp.cwd("..")  # go back up after folder
        else:
            download_file(ftp, name, local_path)

def main():
    with FTP() as ftp:
        ftp.connect(FTP_HOST, 21, timeout=60)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.set_pasv(True)

        print(f"Downloading {FTP_REMOTE_DIR} -> {LOCAL_DIR}")
        download_dir(ftp, FTP_REMOTE_DIR, LOCAL_DIR)

if __name__ == "__main__":
    main()