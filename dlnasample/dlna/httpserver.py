try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import threading
import cgi
import soapcmd

from servicemgr import serviceManager, AVTransportService

try:
    import cElementTree as ET
    import elementtree
except ImportError:
    try:
        from elementtree import ElementTree as ET
        import elementtree
    except ImportError:
        # this seems to be necessary with the python2.5 on the Maemo platform
        try:
            from xml.etree import cElementTree as ET
            from xml import etree as elementtree
        except ImportError:
            try:
                from xml.etree import ElementTree as ET
                from xml import etree as elementtree
            except ImportError:
                raise ImportError("ElementTree: no ElementTree module found, "
                                  "critical error")

PORT_NUMBER = 8080


class UPNPHTTPServerHandler(BaseHTTPRequestHandler):
    """
    A HTTP handler that serves the UPnP XML files.
    """

    # Handler for the GET requests
    def log_message(self, format, *args):
        pass
    def do_GET(self):
        if self.path == '/AVTransport_scpd.xml':
            if self.path in soapcmd.soapcmd.keys():
                self.send_response(200)
                self.send_header('Content-type', 'application/xml')
                self.end_headers()
                self.wfile.write(soapcmd.soapcmd[self.path].encode())#(self.get_wsd_xml().encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Not found.")
            return
        if self.path == '/TxMediaRenderer_desc.xml':
            self.send_response(200)
            self.send_header('Content-type', 'application/xml')
            self.end_headers()
            self.wfile.write(self.get_device_xml().encode())
            return
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not found.")
            return

    def do_POST(self):
        if self.path == '/AVTransport_control':
            #print '[UPNPHTTPServerHandler.do_POST] path : ',self.path
            print '[UPNPHTTPServerHandler.do_POST] headers : ',self.headers
            soapaction = self.headers['SOAPAction'][1:-1]
            if soapaction is not None:
                service = soapaction.split('#')[0]
                action = soapaction.split('#')[1]
            print '[UPNPHTTPServerHandler.do_POST] service : ',service,' action : ',action
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type'],
                })

            postdata = form.file.read()
            print '[UPNPHTTPServerHandler.form.file]', postdata

            tree = self.parse_xml(postdata)

            body = tree.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
            print '[UPNPHTTPServerHandler] body : ',ET.tostring(body)
            method = body.getchildren()[0]
            print '[UPNPHTTPServerHandler] method : ',ET.tostring(method)
            methodName = method.tag
            print '[UPNPHTTPServerHandler] methodName : ', methodName
            ns = None

            if methodName.startswith('{') and methodName.rfind('}') > 1:
                ns, methodName = methodName[1:].split('}')

            args = []
            kwargs = {}
            for child in method.getchildren():
                kwargs[child.tag] = self.decode_result(child)
                args.append(kwargs[child.tag])
            
            print '[UPNPHTTPServerHandler] methodName : ', methodName
            print '[UPNPHTTPServerHandler] args : ', args
            print '[UPNPHTTPServerHandler] kwargs : ', kwargs

            resultxml = ''
            if service in serviceManager.services.keys():
                if hasattr( serviceManager.services[service], methodName ):
                    method = getattr( serviceManager.services[service], methodName)
                    resultxml = method( **kwargs )

            self.send_response(200)
            self.send_header('Content-type', 'application/xml')
            self.end_headers()
            self.wfile.write(resultxml.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not found.")
        return

    def decode_result(self, element):
        type = element.get('{http://www.w3.org/1999/XMLSchema-instance}type')
        if type is not None:
            try:
                prefix, local = type.split(":")
                if prefix == 'xsd':
                    type = local
            except ValueError:
                pass

        if type in ("integer", "int"):
            return int(element.text)
        elif type in ("float", "double"):
            return float(element.text)
        elif type == "boolean":
            return element.text == "true"
        else:
            return element.text or ""

    def parse_xml(self, data, encoding="utf-8", dump_invalid_data=False):
        try:
            parser = ET.XMLParser(encoding=encoding)
        except exceptions.TypeError:
            parser = ET.XMLParser()

        # my version of twisted.web returns page_infos as a dictionary in
        # the second item of the data list
        # :fixme: This must be handled where twisted.web is fetching the data
        if isinstance(data, (list, tuple)):
            data = data[0]

        try:
            data = data.encode(encoding)
        except UnicodeDecodeError:
            pass

        # Guess from who we're getting this?
        data = data.replace('\x00', '')
        try:
            parser.feed(data)
        except Exception, error:
            if dump_invalid_data:
                print error, repr(data)
            parser.close()
            raise
        else:
            return ET.ElementTree(parser.close())


    def get_device_xml(self):
        """
        Get the main device descriptor xml file.
        """
        xml = """<root>
    <specVersion>
        <major>1</major>
        <minor>0</minor>
    </specVersion>
    <device>
        <deviceType>urn:schemas-upnp-org:device:MediaRenderer:1</deviceType>
        <friendlyName>{friendly_name}</friendlyName>
        <manufacturer>{manufacturer}</manufacturer>
        <manufacturerURL>{manufacturer_url}</manufacturerURL>
        <modelDescription>{model_description}</modelDescription>
        <modelName>{model_name}</modelName>
        <modelNumber>{model_number}</modelNumber>
        <modelURL>{model_url}</modelURL>
        <serialNumber>{serial_number}</serialNumber>
        <UDN>uuid:{uuid}</UDN>
        <serviceList>
            <service>
                <serviceType>urn:schemas-upnp-org:service:AVTransport:1</serviceType>
                <serviceId>urn:upnp-org:serviceId:AVTransport</serviceId>
                <controlURL>AVTransport_control</controlURL>
                <SCPDURL>/AVTransport_scpd.xml</SCPDURL>
                <eventSubURL>AVTransport_event</eventSubURL>
            </service>
        </serviceList>
        <presentationURL>{presentation_url}</presentationURL>
    </device>
</root>"""
        return xml.format(friendly_name=self.server.friendly_name,
                          manufacturer=self.server.manufacturer,
                          manufacturer_url=self.server.manufacturer_url,
                          model_description=self.server.model_description,
                          model_name=self.server.model_name,
                          model_number=self.server.model_number,
                          model_url=self.server.model_url,
                          serial_number=self.server.serial_number,
                          uuid=self.server.uuid,
                          presentation_url=self.server.presentation_url)


class UPNPHTTPServerBase(HTTPServer):
    """
    A simple HTTP server that knows the information about a UPnP device.
    """
    def __init__(self, server_address, request_handler_class):
        HTTPServer.__init__(self, server_address, request_handler_class)
        self.port = None
        self.friendly_name = None
        self.manufacturer = None
        self.manufacturer_url = None
        self.model_description = None
        self.model_name = None
        self.model_url = None
        self.serial_number = None
        self.uuid = None
        self.presentation_url = None


class UPNPHTTPServer(threading.Thread):
    """
    A thread that runs UPNPHTTPServerBase.
    """

    def __init__(self, port, friendly_name, manufacturer, manufacturer_url, model_description, model_name,
                 model_number, model_url, serial_number, uuid, presentation_url):
        threading.Thread.__init__(self)
        self.server = UPNPHTTPServerBase(('', port), UPNPHTTPServerHandler)
        self.server.port = port
        self.server.friendly_name = friendly_name
        self.server.manufacturer = manufacturer
        self.server.manufacturer_url = manufacturer_url
        self.server.model_description = model_description
        self.server.model_name = model_name
        self.server.model_number = model_number
        self.server.model_url = model_url
        self.server.serial_number = serial_number
        self.server.uuid = uuid
        self.server.presentation_url = presentation_url
        self.services = []
        self.services.append(AVTransportService(serviceManager))

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
