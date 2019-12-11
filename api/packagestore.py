import os
import logging
import shutil
from werkzeug.utils import secure_filename
from models import Package
from typing import Optional
import tempfile
PACKAGE_DIR = os.path.join(".", "packages")
TMPDIR = tempfile.gettempdir() # "/tmp"


def has(pkgname) -> Optional[Package]:
    """

    :param pkgname:
    :return: The matching package, None if not found.
    """
    matching_packages = (Package.select().where(Package.name == pkgname))
    return None if len(matching_packages)==0 else matching_packages[0]


def get(pkgname):
    """

    :param pkgname:
    :return: The filepath for the package.
    """
    matching_packages = (Package.select().where(Package.name == pkgname))
    return None if len(matching_packages) == 0 else matching_packages[0].path


def get_apkinfo(filepath):
    from pyaxmlparser import APK
    if filepath is not None:
        apk = APK(filepath)
        return apk


def __store_package_info(pkgname, version, path):
    """

    :param pkgname:
    :param version:
    :param path:
    :return: True or False if the package is new or not
    """
    new_pkg = Package()
    new_pkg.version = version
    new_pkg.name = pkgname
    new_pkg.file = path
    matching_packages = (Package.select().where(Package.name == pkgname))
    if len(matching_packages) == 0:
        new_pkg.save()
        return True
    else:
        q = Package.delete().where(Package.name == pkgname)
        q.execute()
        new_pkg.save()
        return False


def put(file):
    import uuid
    unique_filename = str(uuid.uuid4())
    tmp_file_path = os.path.join(TMPDIR , "br_" + unique_filename)
    file.save(tmp_file_path)
    apk = get_apkinfo(tmp_file_path)
    filename = secure_filename(apk.package)
    path = os.path.join(PACKAGE_DIR, filename + ".apk")
    shutil.move(tmp_file_path, path)
    is_new = __store_package_info(apk.package, apk.version_name, path)
    return {
        "package": apk.package, "version": apk.version_name, "is_new": is_new
    }
