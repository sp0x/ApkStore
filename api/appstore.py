import datetime

from models.device import  Device
from models.package import  Package
from models.devpackage import DevicePackage

import logging
from geolite2 import geolite2


def notice_device_app(dev: Device, pkg, ver):
    matching_devs = (Device.select().where(Device.serial == dev.serial))
    # Device doesn't exist
    if len(matching_devs) == 0:
        dev.save()
    else:
        print("Updating device with info: ")
        print(dev)
        # Device exists
        match = matching_devs[0]
        match.imei = dev.imei
        match.wifi_mac = dev.wifi_mac
        match.ext_ip = dev.ext_ip
        match.lan_ip = dev.lan_ip
        match.last_noticed = datetime.datetime.now()
        match.update()
        dev = match
    pkgs = Package.select().where(Package.name == pkg)
    if len(pkgs) == 0:
        package = Package()
        package.name = pkg
        package.version = ver
        package.save()
    else:
        package = pkgs[0]
    existing_devpacks = DevicePackage.select().where((DevicePackage.device == dev) & (DevicePackage.package == package))
    if len(existing_devpacks) == 0:
        DevicePackage.create(device=dev, package=package, version=ver)

    return dev


def get_dev_packages(dev: Device):
    out = DevicePackage.select().where(DevicePackage.device == dev)
    return out


def __format_package(package: Package):

    return {
        'name': package.name,
        'version': package.version
    }


def get_all_dev_packages():
    ret = []
    devs = (Device
            .select())
    ipreader = geolite2.reader()
    for dev in devs:
        devpacks = get_dev_packages(dev)
        devpacks = list(devpacks)
        if len(devpacks) == 0:
            continue
        match = None
        try:
            match = ipreader.get(str(dev.ext_ip).strip())
        except Exception as ex:
            logging.warning(ex)
            pass
        country = ''
        city = ''
        if match is not None:
            country = match['country']['iso_code'] if 'country' in match else ''
            city = match['city']['names']['en'] if 'city' in match else ''

        ret.append({
            'device': {
                'id': dev.id,
                'serial': dev.serial,
                'ip': dev.ext_ip,
                "lan_ip": dev.lan_ip,
                'country': country,
                'city': city,
                'mac': dev.wifi_mac
            },
            'packages': [__format_package(x.package) for x in devpacks]
        })
    #ipreader.close()
    return ret
