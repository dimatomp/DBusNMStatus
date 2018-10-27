from setuptools import setup, find_packages
setup(
    name="DBusNMStatus",
    version="0.2",
    packages=find_packages(),
    description="A script that prints current Wi-Fi connection info in readable format",
    long_description="A script that subscribes to NetworkManager via DBus and prints SSID and signal strength of current Wi-Fi connection in readable format",
    install_requires="PyGObject>=3.18.2",
    url="http://github.com/dimatomp/DBusNMStatus",
    author="Dmitry Tomp",
    author_email="dmitrytomp@gmail.com",
    entry_points={
        'console_scripts': [
            'dbus_nm_status = DBusNMStatus:main',
        ]
    }
)
