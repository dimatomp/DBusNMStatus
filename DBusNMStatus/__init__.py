import dbus
import gi.repository.GObject
import sys
from dbus.mainloop.glib import DBusGMainLoop

_NM_BUS = 'org.freedesktop.NetworkManager'
_NM_DEVICE = _NM_BUS + ".Device"
_NM_WIRELESS_DEVICE = _NM_DEVICE + ".Wireless"
_NM_ACCESS_POINT = _NM_BUS + ".AccessPoint"
_NM_PATH = '/org/freedesktop/NetworkManager'

class DBusNMStatus:
    def __init__(self, prefix=''):
        self.prefix = prefix
        self.cSsid = None
        self.cStrength = None
        self.handler = lambda m: self.updateRate(m)

    def updateRate(self, message):
        if 'Ssid' in message:
            self.cSsid = str(bytes(map(int, message['Ssid'])), encoding='utf8') if message['Ssid'] else None
        if 'Strength' in message:
            self.cStrength = int(message['Strength'])
        if self.cSsid:
            sticks = min(4, self.cStrength // 20)
            print(self.prefix + self.cSsid, '[' + '|' * sticks + '-' * (4 - sticks) + ']')
        else:
            print(self.prefix + 'No WiFi connection')
        sys.stdout.flush()

    def refreshAccessPoint(self, newAP):
        self.bus.remove_signal_receiver(self.handler)
        if not newAP or newAP == '/':
            self.updateRate({'Ssid': None})
        else:
            apObject = self.bus.get_object(_NM_BUS, newAP)
            apProps = dbus.Interface(apObject, dbus.PROPERTIES_IFACE)
            self.updateRate(apProps.GetAll(_NM_ACCESS_POINT))
            apObject.connect_to_signal('PropertiesChanged', self.handler, _NM_ACCESS_POINT)

    def dispatchAPMessage(self, message):
        if 'ActiveAccessPoint' in message:
            self.refreshAccessPoint(message['ActiveAccessPoint'])

    def run(self):
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()

        try:
            manager = dbus.Interface(self.bus.get_object(_NM_BUS, _NM_PATH), _NM_BUS)
            for obj in manager.GetAllDevices():
                iface = dbus.Interface(self.bus.get_object(_NM_BUS, obj), dbus.PROPERTIES_IFACE)
                if iface.Get(_NM_DEVICE, "DeviceType") == 2:
                    break
            self.refreshAccessPoint(iface.Get(_NM_WIRELESS_DEVICE, 'ActiveAccessPoint'))
        except dbus.DBusException as e:
            print(e)
            self.updateRate({})
        self.bus.add_signal_receiver(lambda m: self.dispatchAPMessage(m), 'PropertiesChanged', _NM_WIRELESS_DEVICE, _NM_BUS)

        gi.repository.GObject.MainLoop().run()

def main():
    DBusNMStatus().run()

if __name__ == '__main__':
    main()
