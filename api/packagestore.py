import os
import logging
import shutil
from werkzeug.utils import secure_filename
import models
from models import Package
from sqlite_orm.database import Database

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


def __store_package_info(pkgname, version, path):
    new_pkg = Package()
    new_pkg.version = version
    new_pkg.name = pkgname
    new_pkg.file = path
    matching_packages = (Package.select().where(Package.name == pkgname))
    if len(matching_packages) == 0:
        new_pkg.save()
    else:
        q = Package.delete().where(Package.name == pkgname)
        q.execute()
        new_pkg.save()


def put(file):
    import uuid
    unique_filename = str(uuid.uuid4())
    tmp_file_path = "/tmp/br_" + unique_filename
    file.save(tmp_file_path)
    apk = get_apkinfo(tmp_file_path)
    filename = secure_filename(apk.package)
    path = os.path.join(PACKAGE_DIR, filename + ".apk")
    shutil.move(tmp_file_path, path)
    __store_package_info(apk.package, apk.version_name, path)
    return {
        "package": apk.package, "version": apk.version_name
    }
