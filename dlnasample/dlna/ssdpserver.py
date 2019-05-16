from SocketServer import UDPServer,DatagramRequestHandler
import socket
import logging
import random
import time
import threading
from email.utils import formatdate

SSDP_PORT = 1900
SSDP_ADDR = '239.255.255.250'
SERVER_ID = 'Dinobot SSDP Server'

logger = logging.getLogger()
#logging.basicConfig()

class ssdpRequestHandler( DatagramRequestHandler ):
    def handle(self):
        rdata = self.rfile.read(1024)
        #print '[ssdpRequestHandler.handle] rdata : ',rdata
        self.datagramparse(rdata)

    def datagramparse(self, data):
        try:
            header, payload = data.decode().split('\r\n\r\n')[:2]
        except ValueError as err:
            print '[ssdpRequestHandler.datagramparse] err : ',err
            return
        
        (host, port) = self.client_address

        lines = header.split('\r\n')
        cmd = lines[0].split(' ')
        lines = map(lambda x: x.replace(': ', ':', 1), lines[1:])
        lines = filter(lambda x: len(x) > 0, lines)

        headers = [x.split(':', 1) for x in lines]
        headers = dict(map(lambda x: (x[0].lower(), x[1]), headers))

        logger.info('SSDP command %s %s - from %s:%d' % (cmd[0], cmd[1], host, port))
        logger.debug('with headers: {}.'.format(headers))
        if cmd[0] == 'M-SEARCH' and cmd[1] == '*':
            # SSDP discovery
            self.discovery_request(headers)
        elif cmd[0] == 'NOTIFY' and cmd[1] == '*':
            # SSDP presence
            logger.debug('NOTIFY *')
        else:
            logger.warning('Unknown SSDP command %s %s' % (cmd[0], cmd[1]))

    def discovery_request(self, headers):
        """Process a discovery request.  The response must be sent to
        the address specified by (host, port)."""

        (host, port) = self.client_address

        logger.info('Discovery request from (%s,%d) for %s' % (host, port, headers['st']))
        logger.info('Discovery request for %s' % headers['st'])

        # Do we know about this service?
        for i in self.server.known.values():
            if i['MANIFESTATION'] == 'remote':
                continue
            if headers['st'] == 'ssdp:all' and i['SILENT']:
                continue
            if i['ST'] == headers['st'] or headers['st'] == 'ssdp:all':
                response = ['HTTP/1.1 200 OK']

                usn = None
                for k, v in i.items():
                    if k == 'USN':
                        usn = v
                    if k not in ('MANIFESTATION', 'SILENT', 'HOST'):
                        response.append('%s: %s' % (k, v))

                if usn:
                    response.append('DATE: %s' % formatdate(timeval=None, localtime=False, usegmt=True))

                    response.extend(('', ''))
                    delay = random.randint(0, int(headers['mx']))
                    #print '[ssdpRequestHandler.discovery_request] send data : ','\r\n'.join(response)
                    self.send_it('\r\n'.join(response), (host, port), delay, usn)

    def send_it(self, response, destination, delay, usn):
        logger.debug('send discovery response delayed by %ds for %s to %r' % (delay, usn, destination))
        try:
            self.socket.sendto(response.encode(), destination)
        except (AttributeError, socket.error) as msg:
            logger.warning("failure sending out byebye notification: %r" % msg)

class ssdpServer(UDPServer,threading.Thread):
    known = {}

    def __init__(self):
        threading.Thread.__init__(self)
        UDPServer.__init__(self,('0.0.0.0',1900),ssdpRequestHandler,False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        addr = socket.inet_aton(SSDP_ADDR)
        interface = socket.inet_aton('0.0.0.0')
        cmd = socket.IP_ADD_MEMBERSHIP
        self.socket.setsockopt(socket.IPPROTO_IP, cmd, addr + interface)
        self.socket.bind(('0.0.0.0', SSDP_PORT))
        self.socket.settimeout(1)

    def register(self, manifestation, usn, st, location, server=SERVER_ID, cache_control='max-age=1800', silent=False,
                 host=None):
        """Register a service or device that this SSDP server will
        respond to."""

        logging.info('Registering %s (%s)' % (st, location))

        self.known[usn] = {}
        self.known[usn]['USN'] = usn
        self.known[usn]['LOCATION'] = location
        self.known[usn]['ST'] = st
        self.known[usn]['EXT'] = ''
        self.known[usn]['SERVER'] = server
        self.known[usn]['CACHE-CONTROL'] = cache_control

        self.known[usn]['MANIFESTATION'] = manifestation
        self.known[usn]['SILENT'] = silent
        self.known[usn]['HOST'] = host
        self.known[usn]['last-seen'] = time.time()

        if manifestation == 'local' and self.socket:
            self.do_notify(usn)

    def unregister(self, usn):
        logger.info("Un-registering %s" % usn)
        del self.known[usn]

    def is_known(self, usn):
        return usn in self.known

    def do_notify(self, usn):
        """Do notification"""

        if self.known[usn]['SILENT']:
            return
        logger.info('Sending alive notification for %s' % usn)

        resp = [
            'NOTIFY * HTTP/1.1',
            'HOST: %s:%d' % (SSDP_ADDR, SSDP_PORT),
            'NTS: ssdp:alive',
        ]
        stcpy = dict(self.known[usn].items())
        stcpy['NT'] = stcpy['ST']
        del stcpy['ST']
        del stcpy['MANIFESTATION']
        del stcpy['SILENT']
        del stcpy['HOST']
        del stcpy['last-seen']

        resp.extend(map(lambda x: ': '.join(x), stcpy.items()))
        resp.extend(('', ''))
        logger.debug('do_notify content', resp)
        try:
            self.socket.sendto('\r\n'.join(resp).encode(), (SSDP_ADDR, SSDP_PORT))
            self.socket.sendto('\r\n'.join(resp).encode(), (SSDP_ADDR, SSDP_PORT))
        except (AttributeError, socket.error) as msg:
            logger.warning("failure sending out alive notification: %r" % msg)
    
    def run(self):
        self.serve_forever()
