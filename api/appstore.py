from models import Package, Device, DevicePackage


def notice_device_app(dev: Device, pkg, ver):
    matching_devs = (Device.select().where(Device.serial == dev.serial))
    # Device doesn't exist
    if len(matching_devs) == 0:
        dev.save()
    else:
        # Device exists
        match = matching_devs[0]
        match.imei = dev.imei
        match.wifi_mac = dev.wifi_mac
        match.ext_ip = dev.ext_ip
        match.update()
        dev = match
    pkgs = Package.select().where(Package.name == pkg)
    if len(pkgs) == 0:
        package = Package()
        package.name = pkg
        package.version = ver
    else:
        package = pkgs[0]
    DevicePackage.create(device=dev, package=package)
    return dev
