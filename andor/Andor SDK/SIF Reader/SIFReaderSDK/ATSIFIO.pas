
{ Pascal Interface }
unit ATSIFIO;

interface
		
const
				ATSIF_SIF_FORMAT_ERROR = 22003;
				ATSIF_NO_SIF_LOADED = 22004;
				ATSIF_FILE_NOT_FOUND = 22005;
				ATSIF_FILE_ACCESS_ERROR = 22006;
				ATSIF_DATA_NOT_PRESENT = 22007;

				ATSIF_P1INVALID = 22101;
				ATSIF_P2INVALID = 22102;
				ATSIF_P3INVALID = 22103;
				ATSIF_P4INVALID = 22104;
				ATSIF_P5INVALID = 22105;
				ATSIF_P6INVALID = 22106;
				ATSIF_P7INVALID = 22107;
				ATSIF_P8INVALID = 22108;		

	  {ATSIF_PropertyType Definitions}
		ATSIF_AT_8   = $40000000;
		ATSIF_AT_U8  = $00000001;
		ATSIF_AT_32  = $40000002;
		ATSIF_AT_U32 = $40000003;
		ATSIF_AT_64  = $40000004;
		ATSIF_AT_U64 = $40000005;
		ATSIF_Float  = $40000006;
		ATSIF_Double = $40000007;
		ATSIF_String = $40000008;		
		ATSIF_NoOfPropertyTypes = 9;
		
	  {ATSIF_DataSource Definitions}
		ATSIF_Signal     = $40000000;
		ATSIF_Reference  = $40000001;
		ATSIF_Background = $40000002;
		ATSIF_Live       = $40000003;
		ATSIF_Source     = $40000004;
		ATSIF_NoOfDataSources = 5;
		
	  {ATSIF_StructureElement Definitions}
		ATSIF_File  = $40000000;
		ATSIF_Insta = $40000001;
		ATSIF_Calib = $40000002;
		ATSIF_Andor = $40000003;
		ATSIF_NoOfStructureElements = 4;		

	  {ATSIF_CalibrationAxis Definitions}
		ATSIF_CalibX = $40000000;
		ATSIF_CalibY = $40000001;
		ATSIF_CalibZ = $40000002;
		ATSIF_NoOfCalibrationAxis = 3;	
		
	  {ATSIF_ReadMode Definitions}
		ATSIF_ReadAll        = $40000000;
		ATSIF_ReadHeaderOnly = $40000001;
		ATSIF_NoOfReadModes = 2;			
		
				ATSIF_PROP_TYPE =                      'Type';
				ATSIF_PROP_ACTIVE =                    'Active';				
				ATSIF_PROP_VERSION =                   'Version';				
				ATSIF_PROP_TIME =                      'Time';				
				ATSIF_PROP_FORMATTED_TIME =            'FormattedTime';				
				ATSIF_PROP_FILENAME =                  'FileName';				
				ATSIF_PROP_TEMPERATURE =               'Temperature';				
				ATSIF_PROP_UNSTABILIZEDTEMPERATURE =   'UnstabalizedTemperature';
				ATSIF_PROP_HEAD =                      'Head';
				ATSIF_PROP_HEADMODEL =                 'HeadModel';				
				ATSIF_PROP_STORETYPE =                 'StoreType';				
				ATSIF_PROP_DATATYPE =                  'DataType';				
				ATSIF_PROP_SIDISPLACEMENT =            'SIDisplacement';				
				ATSIF_PROP_SINUMBERSUBFRAMES =         'SINumberSubFrames';				
				ATSIF_PROP_PIXELREADOUTTIME =          'PixelReadOutTime';				
				ATSIF_PROP_TRACKHEIGHT =               'TrackHeight';				
				ATSIF_PROP_READPATTERN =               'ReadPattern';				
				ATSIF_PROP_READPATTERN_FULLNAME =      'ReadPatternFullName';				
				ATSIF_PROP_SHUTTERDELAY =              'ShutterDelay';				
				ATSIF_PROP_CENTREROW =                 'CentreRow';				
				ATSIF_PROP_ROWOFFSET =                 'RowOffset';				
				ATSIF_PROP_OPERATION =                 'Operation';				
				ATSIF_PROP_MODE =                      'Mode';				
				ATSIF_PROP_MODE_FULLNAME =             'ModeFullName';				
				ATSIF_PROP_TRIGGERSOURCE =             'TriggerSource';
				ATSIF_PROP_TRIGGERSOURCE_FULLNAME =    'TriggerSourceFullName';				
				ATSIF_PROP_TRIGGERLEVEL =              'TriggerLevel';				
				ATSIF_PROP_EXPOSURETIME =              'ExposureTime';				
				ATSIF_PROP_DELAY =                     'Delay';				
				ATSIF_PROP_INTEGRATIONCYCLETIME =      'IntegrationCycleTime';				
				ATSIF_PROP_NUMBERINTEGRATIONS =        'NumberIntegrations';				
				ATSIF_PROP_KINETICCYCLETIME =          'KineticCycleTime';				
				ATSIF_PROP_FLIPX =                     'FlipX';				
				ATSIF_PROP_FLIPY =                     'FlipY';				
				ATSIF_PROP_CLOCK =                     'Clock';				
				ATSIF_PROP_ACLOCK =                    'AClock';				
				ATSIF_PROP_IOC =                       'IOC';				
				ATSIF_PROP_FREQUENCY =                 'Frequency';				
				ATSIF_PROP_NUMBERPULSES =              'NumberPulses';				
				ATSIF_PROP_FRAMETRANSFERACQMODE =      'FrameTransferAcquisitionMode';				
				ATSIF_PROP_BASELINECLAMP =             'BaselineClamp';				
				ATSIF_PROP_PRESCAN =                   'PreScan';				
				ATSIF_PROP_EMREALGAIN =                'EMRealGain';				
				ATSIF_PROP_BASELINEOFFSET =            'BaselineOffset';				
				ATSIF_PROP_SWVERSION =                 'SWVersion';				
				ATSIF_PROP_SWVERSIONEX =               'SWVersionEx';				
				ATSIF_PROP_MCP =                       'MCP';				
				ATSIF_PROP_GAIN =                      'Gain';				
				ATSIF_PROP_VERTICALCLOCKAMP =          'VerticalClockAmp';				
				ATSIF_PROP_VERTICALSHIFTSPEED =        'VerticalShiftSpeed';				
				ATSIF_PROP_OUTPUTAMPLIFIER =           'OutputAmplifier';				
				ATSIF_PROP_PREAMPLIFIERGAIN =          'PreAmplifierGain';				
				ATSIF_PROP_SERIAL =                    'Serial';				
				ATSIF_PROP_DETECTORFORMATX =           'DetectorFormatX';				
				ATSIF_PROP_DETECTORFORMATZ =           'DetectorFormatZ';				
				ATSIF_PROP_NUMBERIMAGES =              'NumberImages';				
				ATSIF_PROP_NUMBERSUBIMAGES =           'NumberSubImages';				
				ATSIF_PROP_SUBIMAGE_HBIN =             'SubImageHBin';				
				ATSIF_PROP_SUBIMAGE_VBIN =             'SubImageVBin';				
				ATSIF_PROP_SUBIMAGE_LEFT =             'SubImageLeft';				
				ATSIF_PROP_SUBIMAGE_RIGHT =            'SubImageRight';				
				ATSIF_PROP_SUBIMAGE_TOP =              'SubImageTop';				
				ATSIF_PROP_SUBIMAGE_BOTTOM =           'SubImageBottom';				
				ATSIF_PROP_BASELINE =                  'Baseline';				
				ATSIF_PROP_CCD_LEFT =                  'CCDLeft';				
				ATSIF_PROP_CCD_RIGHT =                 'CCDRight';				
				ATSIF_PROP_CCD_TOP =                   'CCDTop';				
				ATSIF_PROP_CCD_BOTTOM =                'CCDBottom';				
				ATSIF_PROP_SENSITIVITY =               'Sensitivity';				
				ATSIF_PROP_DETECTIONWAVELENGTH =       'DetectionWavelength';				
				ATSIF_PROP_COUNTCONVERTMODE =          'CountConvertMode';				
				ATSIF_PROP_ISCOUNTCONVERT =            'IsCountConvert';				
				ATSIF_PROP_X_AXIS_TYPE =               'XAxisType';				
				ATSIF_PROP_X_AXIS_UNIT =               'XAxisUnit';				
				ATSIF_PROP_Y_AXIS_TYPE =               'YAxisType';				
				ATSIF_PROP_Y_AXIS_UNIT =               'YAxisUnit';				
				ATSIF_PROP_Z_AXIS_TYPE =               'ZAxisType';				
				ATSIF_PROP_Z_AXIS_UNIT =               'ZAxisUnit';				
				ATSIF_PROP_USERTEXT =                  'UserText';				


				ATSIF_PROP_ISPHOTONCOUNTINGENABLED =   'IsPhotonCountingEnabled';				
				ATSIF_PROP_NUMBERTHRESHOLDS =          'NumberThresholds';				
				ATSIF_PROP_THRESHOLD1 =                'Threshold1';				
				ATSIF_PROP_THRESHOLD2 =                'Threshold2';				
				ATSIF_PROP_THRESHOLD3 =                'Threshold3';				
				ATSIF_PROP_THRESHOLD4 =                'Threshold4';				

				ATSIF_PROP_AVERAGINGFILTERMODE =       'AveragingFilterMode';				
				ATSIF_PROP_AVERAGINGFACTOR =           'AveragingFactor';				
				ATSIF_PROP_FRAMECOUNT =                'FrameCount';				

				ATSIF_PROP_NOISEFILTER =               'NoiseFilter';				
				ATSIF_PROP_THRESHOLD =                 'Threshold';				

				ATSIF_PROP_TIME_STAMP =                'TimeStamp';				

				ATSIF_PROP_OUTPUTA_ENABLED =           'OutputAEnabled';				
				ATSIF_PROP_OUTPUTA_WIDTH =             'OutputAWidth';				
				ATSIF_PROP_OUTPUTA_DELAY =             'OutputADelay';				
				ATSIF_PROP_OUTPUTA_POLARITY =          'OutputAPolarity';				
				ATSIF_PROP_OUTPUTB_ENABLED =           'OutputBEnabled';				
				ATSIF_PROP_OUTPUTB_WIDTH =             'OutputBWidth';				
				ATSIF_PROP_OUTPUTB_DELAY =             'OutputBDelay';				
				ATSIF_PROP_OUTPUTB_POLARITY =          'OutputBPolarity';				
				ATSIF_PROP_OUTPUTC_ENABLED =           'OutputCEnabled';				
				ATSIF_PROP_OUTPUTC_WIDTH =             'OutputCWidth';				
				ATSIF_PROP_OUTPUTC_DELAY =             'OutputCDelay';				
				ATSIF_PROP_OUTPUTC_POLARITY =          'OutputCPolarity';				
				ATSIF_PROP_GATE_MODE =                 'GateMode';				
				ATSIF_PROP_GATE_WIDTH =                'GateWidth';				
				ATSIF_PROP_GATE_DELAY =                'GateDelay';				
				ATSIF_PROP_GATE_DELAY_STEP =           'GateDelayStep';				
				ATSIF_PROP_GATE_WIDTH_STEP =           'GateWidthStep';				         					

	  function ATSIF_SetFileAccessMode(_mode: Integer): integer; stdcall;
	  function ATSIF_ReadFromFile(dir: PChar): integer; stdcall;
	  function ATSIF_CloseFile(): integer; stdcall;
	  function ATSIF_ReadFromByteArray(_buffer: PByte; _ui_bufferSize: Integer): integer; stdcall;
	  function ATSIF_IsLoaded(var _i_loaded: Integer): integer; stdcall;
	  function ATSIF_IsDataSourcePresent(_source: Integer; var _i_present: Integer): integer; stdcall;
	  function ATSIF_GetStructureVersion(_element: Integer; var _ui_versionHigh: Integer; var _ui_versionLow: Integer): integer; stdcall;
	  function ATSIF_GetFrameSize(_source: Integer; var _ui_size: Integer): integer; stdcall;
	  function ATSIF_GetNumberFrames(_source: Integer; var _ui_images: Integer): integer; stdcall;
	  function ATSIF_GetNumberSubImages(_source: Integer; var _ui_subimages: Integer): integer; stdcall;
	  function ATSIF_GetSubImageInfo(_source: Integer; _ui_index: Integer;
                                                     var _ui_left: Integer; var _ui_bottom: Integer;
                                                     var _ui_right: Integer; var _ui_top: Integer;
                                                     var _ui_hBin: Integer; var _ui_vBin: Integer): integer; stdcall;
	  function ATSIF_GetAllFrames(_source: Integer; _pf_data: PSingle; _ui_bufferSize: Integer): integer; stdcall;
	  function ATSIF_GetFrame(_source: Integer; _ui_index: Integer; _pf_data: PSingle; _ui_bufferSize: Integer): integer; stdcall;
	  function ATSIF_GetPropertyValue(_source: Integer;
                                                     _sz_propertyName: PChar;
																										 _sz_propertyValue: PChar;
                                                     _ui_bufferSize: Integer): integer; stdcall;
	  function ATSIF_GetPropertyType(_source: Integer;
                                                    _sz_propertyName: PChar;
                                                    _propertyType: PInteger): integer; stdcall;
	  function ATSIF_GetDataStartBytePosition(_source: Integer; var _i_startPosition: Int64): integer; stdcall;
	  function ATSIF_GetPixelCalibration(_source: Integer; _axis: Integer;
                                                        _i_pixel: Integer; var _d_calibValue: Double): integer; stdcall;																																																													

implementation
		
	  function ATSIF_SetFileAccessMode(_mode: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_SetFileAccessMode';
	  function ATSIF_ReadFromFile(dir: PChar): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_ReadFromFile';
	  function ATSIF_CloseFile(): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_CloseFile';
	  function ATSIF_ReadFromByteArray(_buffer: PByte; _ui_bufferSize: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_ReadFromByteArray';
	  function ATSIF_IsLoaded(var _i_loaded: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_IsLoaded';
	  function ATSIF_IsDataSourcePresent(_source: Integer; var _i_present: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_IsDataSourcePresent';
	  function ATSIF_GetStructureVersion(_element: Integer; var _ui_versionHigh: Integer; var _ui_versionLow: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetStructureVersion';
	  function ATSIF_GetFrameSize(_source: Integer; var _ui_size: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetFrameSize';
	  function ATSIF_GetNumberFrames(_source: Integer; var _ui_images: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetNumberFrames';
	  function ATSIF_GetNumberSubImages(_source: Integer; var _ui_subimages: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetNumberSubImages';
	  function ATSIF_GetSubImageInfo(_source: Integer; _ui_index: Integer;
                                                     var _ui_left: Integer; var _ui_bottom: Integer;
                                                     var _ui_right: Integer; var _ui_top: Integer;
                                                     var _ui_hBin: Integer; var _ui_vBin: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetSubImageInfo';
	  function ATSIF_GetAllFrames(_source: Integer; _pf_data: PSingle; _ui_bufferSize: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetAllFrames';
	  function ATSIF_GetFrame(_source: Integer; _ui_index: Integer; _pf_data: PSingle; _ui_bufferSize: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetFrame';
	  function ATSIF_GetPropertyValue(_source: Integer;
                                                     _sz_propertyName: PChar;
																										 _sz_propertyValue: PChar;
                                                     _ui_bufferSize: Integer): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetPropertyValue';
	  function ATSIF_GetPropertyType(_source: Integer;
                                                    _sz_propertyName: PChar;
                                                    _propertyType: PInteger): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetPropertyType';
	  function ATSIF_GetDataStartBytePosition(_source: Integer; var _i_startPosition: Int64): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetDataStartBytePosition';
	  function ATSIF_GetPixelCalibration(_source: Integer; _axis: Integer;
                                                        _i_pixel: Integer; var _d_calibValue: Double): integer; stdcall; external 'ATSIFIO.dll' name 'ATSIF_GetPixelCalibration';
end.
