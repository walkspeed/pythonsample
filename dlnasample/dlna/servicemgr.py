
class ServiceMgr:
    def __new__(cls, *args, **kwargs):
        obj = getattr(cls, '_instance_', None)
        if obj is not None:
            return obj
        else:
            obj = super(ServiceMgr, cls).__new__(cls, *args, **kwargs)
            cls._instance_ = obj
            return obj

    def __init__(self):
        self.services = {}
    
    def registService(self, serviceName, service):
        self.services[serviceName] = service
    
    def unregistService(self, serviceName):
        self.services.remove(serviceName)

class AVTransportService:
    def __init__(self, servicemgr):
        servicemgr.registService('urn:schemas-upnp-org:service:AVTransport:1',self)
    
    def SetAVTransportURI(self, **kwargs):
        print '[AVTransportService.SetAVTransportURI] kwargs : ', kwargs
        return """<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <SOAP-ENV:Body>
            <m:SetAVTransportURIResponse xmlns:m="urn:schemas-upnp-org:service:AVTransport:1">
            </m:SetAVTransportURIResponse>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""

    def Play(self, **kwargs):
        print '[AVTransportService.Play] kwargs : ', kwargs
        return """<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <SOAP-ENV:Body>
            <m:PlayResponse xmlns:m="urn:schemas-upnp-org:service:AVTransport:1">
            </m:PlayResponse>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""

    def Stop(self, **kwargs):
        print '[AVTransportService.Stop] kwargs : ', kwargs
        return """<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <SOAP-ENV:Body>
            <m:StopResponse xmlns:m="urn:schemas-upnp-org:service:AVTransport:1">
            </m:StopResponse>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""

    def Pause(self, **kwargs):
        print '[AVTransportService.Pause] kwargs : ', kwargs
        return """<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <SOAP-ENV:Body>
            <m:PauseResponse xmlns:m="urn:schemas-upnp-org:service:AVTransport:1">
            </m:PauseResponse>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""

    def GetCurrentTransportActions(self, **kwargs):
        print '[AVTransportService.GetCurrentTransportActions] kwargs : ', kwargs
        return """<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <SOAP-ENV:Body>
            <m:GetCurrentTransportActionsResponse xmlns:m="urn:schemas-upnp-org:service:AVTransport:1">
                <Actions>Play</Actions>
            </m:GetCurrentTransportActionsResponse>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""

serviceManager = ServiceMgr()