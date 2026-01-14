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

    # Download unidic-lite dictionary directly from PyPI
    print("Downloading UniDic dictionary to /tmp...")
    url = "https://files.pythonhosted.org/packages/source/u/unidic-lite/unidic-lite-1.0.8.tar.gz"

    tar_path = os.path.join(tmp_dir, "unidic-lite.tar.gz")

    try:
        urllib.request.urlretrieve(url, tar_path)
    except Exception as e:
        print(f"Failed to download UniDic: {e}")
        raise

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

    # Cleanup
    if os.path.exists(tar_path):
        os.remove(tar_path)

    # Remove extracted source directory
    extracted_source = os.path.join(tmp_dir, "unidic-lite-1.0.8")
    if os.path.exists(extracted_source):
        import shutil
        shutil.rmtree(extracted_source)
    print(f"UniDic dictionary ready at: {unidic_dir}")

    return unidic_dir
