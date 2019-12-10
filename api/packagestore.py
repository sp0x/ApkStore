import os
import logging
import shutil
from werkzeug.utils import secure_filename

PACKAGE_DIR = "/app/packages"


def has(package):
    return None


def get(package):
    return None


def get_apkinfo(filepath):
    from pyaxmlparser import APK
    if filepath is not None:
        apk = APK(filepath)
        return apk


def put(file):
    import uuid
    unique_filename = str(uuid.uuid4())
    tmp_file_path = "/tmp/br_" + unique_filename
    file.save(tmp_file_path)
    apk = get_apkinfo(tmp_file_path)
    filename = secure_filename(apk.package)
    path = os.path.join(PACKAGE_DIR, filename + ".apk")
    shutil.move(tmp_file_path, path)
    return {
        "package": apk.package, "version": apk.version_name
    }
