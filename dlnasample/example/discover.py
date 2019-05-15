#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Demonstrate a simple UPnP device discovery.
#

import upnpclient

ssdp = upnpclient.SSDP()
servers = ssdp.discover()
"""
print "%s: %s" % (servers[0].friendly_name, servers[0].model_description)
for service in servers[0].services:
	print "   %s" % (service.service_type)
	for action in service.actions:
		print "      %s" % (action.name)
		for arg_name, arg_def in action.argsdef_in:
			valid = ', '.join(arg_def['allowed_values']) or '*'
			print "          in: %s (%s): %s" % (arg_name, arg_def['datatype'], valid)
		for arg_name, arg_def in action.argsdef_out:
			valid = ', '.join(arg_def['allowed_values']) or '*'
			print "         out: %s (%s): %s" % (arg_name, arg_def['datatype'], valid)
"""	
deviceMDS = None
		
for server in servers:
    print "%s: %s" % (server.friendly_name, server.model_description)
    if server.friendly_name == 'dinobot 4k':
		deviceMDS = server
		break
		
if deviceMDS is not None:
	print '************************************************************************************'
	print ' '
	#param = {'ObjectID': 'ttx3', 'BrowserFlag': 'BrowseDirectChildren'}
	#print 'deviceMDS.ContentDirectory.Browse : ',deviceMDS.ContentDirectory.Browse(ObjectID='ttx3',BrowseFlag='BrowseDirectChildren',
	#Filter='',StartingIndex=0,RequestedCount=50,SortCriteria='')
	deviceMDS.AVTransport.SetAVTransportURI(InstanceID=1,CurrentURI='test.mp4',CurrentURIMetaData='')
	deviceMDS.AVTransport.Play(InstanceID=1,Speed='1')
	deviceMDS.AVTransport.Pause(InstanceID=1)
	deviceMDS.AVTransport.Stop(InstanceID=1)
	deviceMDS.AVTransport.GetCurrentTransportActions(InstanceID=1)
#通过设备上的服务，使用服务的功能
#servers[0]:获取发现的设备的第一个设备
#servers[0].QPlay:使用第一个设备上的QPlay服务。服务通过service.service_type获得
"""
print '************************************************************************************'
print ' '
print 'server type ',servers[0].device_type
print ' '
print 'server.services ', servers[0].services
print ' '
print 'server.services QPlay actions', servers[0].QPlay.actions
print ' '
print 'service QPlay.GetTracksCount %s'%(servers[0].QPlay.GetTracksCount())
print ' '
print 'service QPlay.GetMaxTracks %s'%(servers[0].QPlay.GetMaxTracks())
"""