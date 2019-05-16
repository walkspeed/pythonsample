from dlna.ssdpserver import ssdpServer

import netifaces as ni

def get_network_interface_ip_address(interface='eth0'):
    """
    Get the first IP address of a network interface.
    :param interface: The name of the interface.
    :return: The IP address.
    """
    while True:
        print 'ni.interfaces : ',ni.interfaces(), ' interface : ', interface
        if interface not in ni.interfaces():
            logger.error('Could not find interface %s.' % (interface,))
            exit(1)
        interface = ni.ifaddresses(interface)
        if (2 not in interface) or (len(interface[2]) == 0):
            logger.warning('Could not find IP of interface %s. Sleeping.' % (interface,))
            sleep(60)
            continue
        return interface[2][0]['addr']

import uuid
device_uuid = uuid.uuid4()
localportal = '{BAFC7980-2EF6-48F1-99B7-5E0FE672F4BC}'
wlanportal = '{4F692136-26AE-4B71-A0C0-71312D269F62}'
local_ip_address = get_network_interface_ip_address(localportal)

if __name__ == '__main__':
    s = ssdpServer()
    s.register('local','uuid:{}::upnp:rootdevice'.format(device_uuid),'upnp:rootdevice','http://{}:8088/TxMediaRenderer_desc.xml'.format(local_ip_address))
    s.start()

    cmd = ''
    while True:
        cmd = raw_input()
        if cmd == 'quit':
            break
    
    s.shutdown()
    s.server_close()
