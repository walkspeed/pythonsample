
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

class ServiceBase:
    def __init__(self,servicename):
        self.servicename = servicename
    
    def resultXml(self, action, **kwargs):
        resultstr = ''
        for key, value in kwargs.items():
            itemstr = '<{0}>{1}</{0}>\n'.format(key, value)
            resultstr += itemstr
        
        resultxmlformat = """<?xml version="1.0"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <SOAP-ENV:Body>
            <m:{cmd}Response xmlns:m="{service}">
            {result}
            </m:{cmd}Response>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>"""
        return resultxmlformat.format(cmd=action,result=resultstr,service=self.servicename)

class AVTransportService(ServiceBase):
    def __init__(self, servicemgr):
        ServiceBase.__init__(self,'urn:schemas-upnp-org:service:AVTransport:1')
        servicemgr.registService('urn:schemas-upnp-org:service:AVTransport:1',self)
    
    def SetAVTransportURI(self, **kwargs):
        print '[AVTransportService.SetAVTransportURI] kwargs : ', kwargs
        return self.resultXml('SetAVTransportURI',**{})

    def Play(self, **kwargs):
        print '[AVTransportService.Play] kwargs : ', kwargs
        return self.resultXml('Play',**{})

    def Stop(self, **kwargs):
        print '[AVTransportService.Stop] kwargs : ', kwargs
        return self.resultXml('Stop',**{})

    def Pause(self, **kwargs):
        print '[AVTransportService.Pause] kwargs : ', kwargs
        return self.resultXml('Pause',**{})

    def GetCurrentTransportActions(self, **kwargs):
        print '[AVTransportService.GetCurrentTransportActions] kwargs : ', kwargs
        return self.resultXml('GetCurrentTransportActions',**{"Actions":"Play"})

serviceManager = ServiceMgr()