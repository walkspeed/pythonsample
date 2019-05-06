import re
import requests
#import xml.etree.cElementTree
from lxml import etree
from functools import partial

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet import task

SSDP_PORT = 1900
SSDP_ADDR = '239.255.255.250'

HTTP_TIMEOUT = 10

RESPONSE_REGEX = re.compile(r'\n(.*?)\: *(.*)\r')

class MSearch(DatagramProtocol):
	def __init__(self):
		self._port = reactor.listenUDP(0, self)
		self._double_discover_loop = task.LoopingCall(self.double_discover)
		self._double_discover_loop.start(120.0)

	def double_discover(self):
		" Because it's worth it (with UDP's reliability) "
		print 'send out discovery for ssdp:all'
		self.discover()
		self.discover()

	def discover(self):
		req = ['M-SEARCH * HTTP/1.1','HOST: %s:%d' % (SSDP_ADDR, SSDP_PORT),'MAN: "ssdp:discover"','MX: 5','ST: ssdp:all','', '']
		req = '\r\n'.join(req)

		try:
			self.transport.write(req, (SSDP_ADDR, SSDP_PORT))
		except socket.error, msg:
			print "failure sending out the discovery message: %r" % (msg,)

	def datagramReceived(self, data, (host, port)):
		response = self.parse_http_response(data)
		#print '[MSearch.datagramReceived] response : ',response
		#del content # we do not need the content
		#print 'datagramReceived data : ',data
		#print 'datagramReceived from %s:%d, protocol %s code %s' % (host, port, cmd[0], cmd[1])
		#if cmd[0].startswith('HTTP/1.') and cmd[1] == '200':
			#print 'for %r' % (headers['usn'],)

		resp = requests.get(response['location'],timeout=HTTP_TIMEOUT,auth=None,headers=None)
		resp.raise_for_status()

		#print '[MSearch.datagramReceived] resp.content : ',str(resp.content)
		root = etree.fromstring(resp.content)
		#root = xml.etree.cElementTree.fromstring(str(resp.content)).getroot()
		print '[MSearch.datagramReceived] root : ',etree.tostring(root)
		findtext = partial(root.findtext, namespaces=root.nsmap)
		self.device_type = findtext('device/deviceType')
		#if self.device_type is not None:
		print '[MSearch.datagramReceived] device_type : ', self.device_type

	def parse_http_response(self,data):
		responsedict = {key.lower(): item for key, item in RESPONSE_REGEX.findall(data)}
		return responsedict
		"""
		try:
			header, content = data.split('\r\n\r\n')[0]
		except ValueError:
			header = data.strip()
		content = ''
		lines = header.splitlines()
		cmd = lines.pop(0).split(None, 2)
		lines = (l.split(':', 1) for l in lines if l)
		headers = dict((h.strip().lower(), d.strip())for (h, d) in lines)
		return cmd, headers, content
		"""


if __name__ == '__main__':
	search = MSearch()
	reactor.run()

