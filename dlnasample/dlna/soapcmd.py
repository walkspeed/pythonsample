soapcmd = {}

mediarenderer_scpd = """<?xml version=\"1.0\"?>
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

soapcmd['/AVTransport_scpd.xml'] = mediarenderer_scpd