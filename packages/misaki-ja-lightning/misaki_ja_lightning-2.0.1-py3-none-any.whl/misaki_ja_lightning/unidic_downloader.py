"""Download and setup UniDic dictionary at runtime for serverless environments"""
import os
import tempfile
import urllib.request
import tarfile
from pathlib import Path


def get_unidic_path():
    """Get path to UniDic dictionary, downloading if necessary"""
    # Check if unidic-lite is installed
    try:
        import unidic_lite
        return unidic_lite.DICDIR
    except ImportError:
        pass

    # For serverless: download to /tmp
    tmp_dir = tempfile.gettempdir()
    unidic_dir = os.path.join(tmp_dir, "unidic-lite")

    # Check if already downloaded
    if os.path.exists(unidic_dir) and os.path.exists(os.path.join(unidic_dir, "sys.dic")):
        return unidic_dir

    # Download unidic-lite
    print("Downloading UniDic dictionary to /tmp...")
    url = "https://github.com/polm/unidic-lite/releases/download/v1.0.8/unidic-lite-1.0.8.tar.gz"

    tar_path = os.path.join(tmp_dir, "unidic-lite.tar.gz")
    urllib.request.urlretrieve(url, tar_path)

    # Extract
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(tmp_dir)

    # Find the dictionary directory
    extracted = os.path.join(tmp_dir, "unidic-lite-1.0.8", "unidic_lite", "dicdir")
    if os.path.exists(extracted):
        # Move to expected location
        import shutil
        if os.path.exists(unidic_dir):
            shutil.rmtree(unidic_dir)
        shutil.move(extracted, unidic_dir)

    os.remove(tar_path)
    print(f"UniDic dictionary ready at: {unidic_dir}")

    return unidic_dir
