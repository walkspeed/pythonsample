
#from dlna.ssdp import SSDPServer
from dlna.ssdpserver import ssdpServer
from dlna.httpserver import UPNPHTTPServer

import uuid
import netifaces as ni
from time import sleep
import logging

#logging.basicConfig()

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

device_uuid = uuid.uuid4()
localportal = '{BAFC7980-2EF6-48F1-99B7-5E0FE672F4BC}'
wlanportal = '{4F692136-26AE-4B71-A0C0-71312D269F62}'
local_ip_address = get_network_interface_ip_address(wlanportal)
print 'local_ip_address : ', local_ip_address

if __name__ == '__main__':
    http_server = UPNPHTTPServer(8088,friendly_name="dinobot 4k",
                                manufacturer="Boucherie numerique SAS",
                                manufacturer_url='http://www.boucherie.example.com/',
                                model_description='dinobot Appliance 4k',
                                model_name="dinobot",
                                model_number="4k",
                                model_url="http://www.boucherie.example.com/en/prducts/jambon-3000/",
                                serial_number="JBN425133",
                                uuid=device_uuid,
                                presentation_url="http://{}:5000/".format(local_ip_address))

    http_server.start()

    ssdp = ssdpServer()
    ssdp.register('local','uuid:{}::upnp:rootdevice'.format(device_uuid),'upnp:rootdevice','http://{}:8088/TxMediaRenderer_desc.xml'.format(local_ip_address))
    ssdp.start()#run()

    while True:
        cmd = raw_input()
        print 'cmd : ',cmd
        if cmd is None:
            continue
        if cmd == 'quit':
            break
    
    #ssdp.stop()
    #ssdp.join()
    #ssdp.destroy()
    ssdp.shutdown()
    ssdp.server_close()
    http_server.stop()
    http_server.join()
