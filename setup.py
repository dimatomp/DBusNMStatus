from setuptools import setup, find_packages
setup(
    name="DBusNMStatus",
    version="0.1",
    packages=find_packages(),
    summary="A script that prints SSID and signal strength of current Wi-Fi connection in readable format",
    install_requires=["dbus-python>=1.2.4", "PyGObject>=3.24.1"],
    url="http://github.com/dimatomp/DBusNMStatus",
    author="Dmitry Tomp",
    author_email="dmitrytomp@gmail.com",
    entry_points={
        'console_scripts': [
            'dbus_nm_status = DBusNMStatus:main',
        ]
    }
)