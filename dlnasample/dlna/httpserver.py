from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import cgi

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
    def do_GET(self):
        if self.path == '/AVTransport_scpd.xml':
            self.send_response(200)
            self.send_header('Content-type', 'application/xml')
            self.end_headers()
            self.wfile.write(self.get_wsd_xml().encode())
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
        print '[UPNPHTTPServerHandler.do_POST] path : ',self.path
        print '[UPNPHTTPServerHandler.do_POST] headers : ',self.headers
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
            'CONTENT_TYPE':self.headers['Content-Type'],
            })
        print '[UPNPHTTPServerHandler.do_POST] form : ',form
        """while 1:
            line = form.file.readline(1<<16)
            if not line:
                break
            print 'line : ', line"""
        postdata = form.file.read()
        print 'data type : ',type(postdata)
        print '[UPNPHTTPServerHandler.form.file]', postdata

        tree = self.parse_xml(postdata)

        body = tree.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
        method = body.getchildren()[0]
        methodName = method.tag
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

    @staticmethod
    def get_wsd_xml():
        """
        Get the device WSD file.
        """
        return """<?xml version=\"1.0\"?>
            <scpd xmlns=\"urn:schemas-upnp-org:service-1-0\">
                <specVersion>
                <major>1</major>
                <minor>0</minor>
                </specVersion>
                <actionList>
                <action>
                <name>GetCurrentTransportActions</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>Actions</name>
                <direction>out</direction>
                <relatedStateVariable>CurrentTransportActions</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>GetDeviceCapabilities</name>           
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>PlayMedia</name>
                <direction>out</direction>
                <relatedStateVariable>PossiblePlaybackStorageMedia</relatedStateVariable>
                </argument>
                <argument>
                <name>RecMedia</name>
                <direction>out</direction>
                <relatedStateVariable>PossibleRecordStorageMedia</relatedStateVariable>
                </argument>
                <argument>
                <name>RecQualityModes</name>
                <direction>out</direction>
                <relatedStateVariable>PossibleRecordQualityModes</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>GetMediaInfo</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>NrTracks</name>
                <direction>out</direction>
                <relatedStateVariable>NumberOfTracks</relatedStateVariable>
                </argument>
                <argument>
                <name>MediaDuration</name>
                <direction>out</direction>
                <relatedStateVariable>CurrentMediaDuration</relatedStateVariable>
                </argument>
                <argument>
                <name>CurrentURI</name>
                <direction>out</direction>
                <relatedStateVariable>AVTransportURI</relatedStateVariable>
                </argument>
                <argument>
                <name>CurrentURIMetaData</name>
                <direction>out</direction>
                <relatedStateVariable>AVTransportURIMetaData</relatedStateVariable>
                </argument>
                <argument>
                <name>NextURI</name>
                <direction>out</direction>
                <relatedStateVariable>NextAVTransportURI</relatedStateVariable>
                </argument>
                <argument>
                <name>NextURIMetaData</name>
                <direction>out</direction>
                <relatedStateVariable>NextAVTransportURIMetaData</relatedStateVariable>
                </argument>
                <argument>
                <name>PlayMedium</name>
                <direction>out</direction>
                <relatedStateVariable>PlaybackStorageMedium</relatedStateVariable>
                </argument>
                <argument>
                <name>RecordMedium</name>
                <direction>out</direction>
                <relatedStateVariable>RecordStorageMedium</relatedStateVariable>
                </argument>
                <argument>
                <name>WriteStatus</name>
                <direction>out</direction>
                <relatedStateVariable>RecordMediumWriteStatus</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>GetPositionInfo</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>Track</name>
                <direction>out</direction>
                <relatedStateVariable>CurrentTrack</relatedStateVariable>
                </argument>
                <argument>
                <name>TrackDuration</name>
                <direction>out</direction>
                <relatedStateVariable>CurrentTrackDuration</relatedStateVariable>
                </argument>
                <argument>
                <name>TrackMetaData</name>
                <direction>out</direction>
                <relatedStateVariable>CurrentTrackMetaData</relatedStateVariable>
                </argument>
                <argument>
                <name>TrackURI</name>
                <direction>out</direction>
                <relatedStateVariable>CurrentTrackURI</relatedStateVariable>
                </argument>
                <argument>
                <name>RelTime</name>
                <direction>out</direction>
                <relatedStateVariable>RelativeTimePosition</relatedStateVariable>
                </argument>
                <argument>
                <name>AbsTime</name>
                <direction>out</direction>
                <relatedStateVariable>AbsoluteTimePosition</relatedStateVariable>
                </argument>
                <argument>
                <name>RelCount</name>
                <direction>out</direction>
                <relatedStateVariable>RelativeCounterPosition</relatedStateVariable>
                </argument>
                <argument>
                <name>AbsCount</name>
                <direction>out</direction>
                <relatedStateVariable>AbsoluteCounterPosition</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>GetTransportInfo</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>CurrentTransportState</name>
                <direction>out</direction>
                <relatedStateVariable>TransportState</relatedStateVariable>
                </argument>
                <argument>
                <name>CurrentTransportStatus</name>
                <direction>out</direction>
                <relatedStateVariable>TransportStatus</relatedStateVariable>
                </argument>
                <argument>
                <name>CurrentSpeed</name>
                <direction>out</direction>
                <relatedStateVariable>TransportPlaySpeed</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>GetTransportSettings</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>PlayMode</name>
                <direction>out</direction>
                <relatedStateVariable>CurrentPlayMode</relatedStateVariable>
                </argument>
                <argument>
                <name>RecQualityMode</name>
                <direction>out</direction>
                <relatedStateVariable>CurrentRecordQualityMode</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>Next</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>Pause</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>Play</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>Speed</name>
                <direction>in</direction>
                <relatedStateVariable>TransportPlaySpeed</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>Previous</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>Seek</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>Unit</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_SeekMode</relatedStateVariable>
                </argument>
                <argument>
                <name>Target</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_SeekTarget</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>SetAVTransportURI</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>CurrentURI</name>
                <direction>in</direction>
                <relatedStateVariable>AVTransportURI</relatedStateVariable>
                </argument>
                <argument>
                <name>CurrentURIMetaData</name>
                <direction>in</direction>
                <relatedStateVariable>AVTransportURIMetaData</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>SetPlayMode</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                <argument>
                <name>NewPlayMode</name>
                <direction>in</direction>
                <relatedStateVariable>CurrentPlayMode</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                <action>
                <name>Stop</name>
                <argumentList>
                <argument>
                <name>InstanceID</name>
                <direction>in</direction>
                <relatedStateVariable>A_ARG_TYPE_InstanceID</relatedStateVariable>
                </argument>
                </argumentList>
                </action>
                </actionList>
                <serviceStateTable>
                <stateVariable sendEvents=\"no\">
                    <name>TransportStatus</name>
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>OK</allowedValue>
                    <allowedValue>ERROR_OCCURRED</allowedValue>
                    <allowedValue> vendor-defined </allowedValue>
                    </allowedValueList>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>NextAVTransportURI</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>NextAVTransportURIMetaData</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>CurrentTrackMetaData</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>RelativeCounterPosition</name>
                    <dataType>i4</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>A_ARG_TYPE_InstanceID</name>
                    <dataType>ui4</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>A_ARG_TYPE_SeekTarget</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>PlaybackStorageMedium</name>
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>UNKNOWN</allowedValue>
                    <allowedValue>DV</allowedValue>
                    <allowedValue>MINI-DV</allowedValue>
                    <allowedValue>VHS</allowedValue>
                    <allowedValue>W-VHS</allowedValue>
                    <allowedValue>S-VHS</allowedValue>
                    <allowedValue>D-VHS</allowedValue>
                    <allowedValue>VHSC</allowedValue>
                    <allowedValue>VIDEO8</allowedValue>
                    <allowedValue>HI8</allowedValue>
                    <allowedValue>CD-ROM</allowedValue>
                    <allowedValue>CD-DA</allowedValue>
                    <allowedValue>CD-R</allowedValue>
                    <allowedValue>CD-RW</allowedValue>
                    <allowedValue>VIDEO-CD</allowedValue>
                    <allowedValue>SACD</allowedValue>
                    <allowedValue>MD-AUDIO</allowedValue>
                    <allowedValue>MD-PICTURE</allowedValue>
                    <allowedValue>DVD-ROM</allowedValue>
                    <allowedValue>DVD-VIDEO</allowedValue>
                    <allowedValue>DVD-R</allowedValue>
                    <allowedValue>DVD+RW</allowedValue>
                    <allowedValue>DVD-RW</allowedValue>
                    <allowedValue>DVD-RAM</allowedValue>
                    <allowedValue>DVD-AUDIO</allowedValue>
                    <allowedValue>DAT</allowedValue>
                    <allowedValue>LD</allowedValue>
                    <allowedValue>HDD</allowedValue>
                    <allowedValue>MICRO-MV</allowedValue>
                    <allowedValue>NETWORK</allowedValue>
                    <allowedValue>NONE</allowedValue>
                    <allowedValue>NOT_IMPLEMENTED</allowedValue>
                    <allowedValue> vendor-defined </allowedValue>
                    </allowedValueList>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>RelativeTimePosition</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>PossibleRecordStorageMedia</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>CurrentPlayMode</name>
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>NORMAL</allowedValue>
                    <allowedValue>REPEAT_ALL</allowedValue>
                    <allowedValue>INTRO</allowedValue>
                    </allowedValueList>
                    <defaultValue>NORMAL</defaultValue>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>TransportPlaySpeed</name>
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>1</allowedValue>
                    <allowedValue> vendor-defined </allowedValue>
                    </allowedValueList>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>PossiblePlaybackStorageMedia</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>AbsoluteTimePosition</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>CurrentTrack</name>
                    <dataType>ui4</dataType>
                    <allowedValueRange>
                    <minimum>0</minimum>
                    <maximum>4294967295</maximum>
                    <step>1</step>
                    </allowedValueRange>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>CurrentTrackURI</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>CurrentTransportActions</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>NumberOfTracks</name>
                    <dataType>ui4</dataType>
                    <allowedValueRange>
                    <minimum>0</minimum>
                    <maximum>4294967295</maximum>
                    </allowedValueRange>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>AVTransportURI</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>AbsoluteCounterPosition</name>
                    <dataType>i4</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>CurrentRecordQualityMode</name>
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>0:EP</allowedValue>
                    <allowedValue>1:LP</allowedValue>
                    <allowedValue>2:SP</allowedValue>
                    <allowedValue>0:BASIC</allowedValue>
                    <allowedValue>1:MEDIUM</allowedValue>
                    <allowedValue>2:HIGH</allowedValue>
                    <allowedValue>NOT_IMPLEMENTED</allowedValue>
                    <allowedValue> vendor-defined </allowedValue>
                    </allowedValueList>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>CurrentMediaDuration</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>A_ARG_TYPE_SeekMode</name>
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>ABS_TIME</allowedValue>
                    <allowedValue>REL_TIME</allowedValue>
                    <allowedValue>ABS_COUNT</allowedValue>
                    <allowedValue>REL_COUNT</allowedValue>
                    <allowedValue>TRACK_NR</allowedValue>
                    <allowedValue>CHANNEL_FREQ</allowedValue>
                    <allowedValue>TAPE-INDEX</allowedValue>
                    <allowedValue>FRAME</allowedValue>
                    </allowedValueList>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>AVTransportURIMetaData</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>RecordStorageMedium</name>\
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>UNKNOWN</allowedValue>
                    <allowedValue>DV</allowedValue>
                    <allowedValue>MINI-DV</allowedValue>
                    <allowedValue>VHS</allowedValue>
                    <allowedValue>W-VHS</allowedValue>
                    <allowedValue>S-VHS</allowedValue>
                    <allowedValue>D-VHS</allowedValue>
                    <allowedValue>VHSC</allowedValue>
                    <allowedValue>VIDEO8</allowedValue>
                    <allowedValue>HI8</allowedValue>
                    <allowedValue>CD-ROM</allowedValue>
                    <allowedValue>CD-DA</allowedValue>
                    <allowedValue>CD-R</allowedValue>
                    <allowedValue>CD-RW</allowedValue>
                    <allowedValue>VIDEO-CD</allowedValue>
                    <allowedValue>SACD</allowedValue>
                    <allowedValue>MD-AUDIO</allowedValue>
                    <allowedValue>MD-PICTURE</allowedValue>
                    <allowedValue>DVD-ROM</allowedValue>
                    <allowedValue>DVD-VIDEO</allowedValue>
                    <allowedValue>DVD-R</allowedValue>
                    <allowedValue>DVD+RW</allowedValue>
                    <allowedValue>DVD-RW</allowedValue>
                    <allowedValue>DVD-RAM</allowedValue>
                    <allowedValue>DVD-AUDIO</allowedValue>
                    <allowedValue>DAT</allowedValue>
                    <allowedValue>LD</allowedValue>
                    <allowedValue>HDD</allowedValue>
                    <allowedValue>MICRO-MV</allowedValue>
                    <allowedValue>NETWORK</allowedValue>
                    <allowedValue>NONE</allowedValue>
                    <allowedValue>NOT_IMPLEMENTED</allowedValue>
                    <allowedValue> vendor-defined </allowedValue>
                    </allowedValueList>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>RecordMediumWriteStatus</name>
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>WRITABLE</allowedValue>
                    <allowedValue>PROTECTED</allowedValue>
                    <allowedValue>NOT_WRITABLE</allowedValue>
                    <allowedValue>UNKNOWN</allowedValue>
                    <allowedValue>NOT_IMPLEMENTED</allowedValue>
                    </allowedValueList>
                </stateVariable>
                <stateVariable sendEvents=\"yes\">
                    <name>LastChange</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>CurrentTrackDuration</name>
                    <dataType>string</dataType>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>TransportState</name>
                    <dataType>string</dataType>
                    <allowedValueList>
                    <allowedValue>STOPPED</allowedValue>
                    <allowedValue>PAUSED_PLAYBACK</allowedValue>
                    <allowedValue>PAUSED_RECORDING</allowedValue>
                    <allowedValue>PLAYING</allowedValue>
                    <allowedValue>RECORDING</allowedValue>
                    <allowedValue>TRANSITIONING</allowedValue>
                    <allowedValue>NO_MEDIA_PRESENT</allowedValue>
                    </allowedValueList>
                </stateVariable>
                <stateVariable sendEvents=\"no\">
                    <name>PossibleRecordQualityModes</name>
                    <dataType>string</dataType>
                </stateVariable>
            </serviceStateTable>
            </scpd>"""


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

    def run(self):
        self.server.serve_forever()
