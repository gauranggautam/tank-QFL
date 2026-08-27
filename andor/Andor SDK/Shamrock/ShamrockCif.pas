unit shamrockcif;

interface

  function ShamrockInitialize(dirName : PChar): Integer; stdcall;
  function ShamrockClose(): Integer; stdcall;
  function ShamrockGetNumberDevices(var noDevices : Integer): Integer; stdcall;
  function ShamrockGetSerialNumber(device : Integer; var serial : PChar): Integer; stdcall;

  function ShamrockSetWavelength(device : Integer; wavelength : Single): Integer; stdcall;
  function ShamrockGetWavelength(device : Integer; var wavelength : Single): Integer; stdcall;
  function ShamrockGotoZeroOrder(device : Integer): Integer; stdcall;
  function ShamrockAtZeroOrder(device : Integer; var atZeroOrder : Integer): Integer; stdcall;
  function ShamrockGetWavelengthLimits(device : Integer; Grating : Integer; var Min : Single; var Max : Single): Integer; stdcall;
  function ShamrockWavelengthIsPresent(device : Integer; var present : Integer): Integer; stdcall;

  function ShamrockSetAccessory(device : Integer; Accessory : Integer; state : Integer): Integer; stdcall;
  function ShamrockGetAccessoryState(device : Integer; Accessory : Integer; var state : Integer): Integer; stdcall;
  function ShamrockAccessoryIsPresent(device : Integer; var present : Integer): Integer; stdcall;

  function ShamrockSetFilter(device : Integer; Filter : Integer): Integer; stdcall;
  function ShamrockGetFilter(device : Integer; Filter : Integer): Integer; stdcall;
  function ShamrockGetFilterInfo(device : Integer; Filter : Integer; Info : PChar): Integer; stdcall;
  function ShamrockSetFilterInfo(device : Integer; Filter : Integer; Info : PChar): Integer; stdcall;
  function ShamrockFilterIsPresent(device : Integer; var present : Integer): Integer; stdcall;

  function ShamrockSetPort(device : Integer; port : Integer): Integer; stdcall;
  function ShamrockGetPort(device : Integer; var port : Integer): Integer; stdcall;
  function ShamrockFlipperReset(device : Integer): Integer; stdcall;
  function ShamrockGetCCDLimits(device : Integer; port : Integer; var Low : Single; var High : Single): Integer; stdcall;
  function ShamrockFlipperIsPresent(device : Integer; var present : Integer): Integer; stdcall;

  function ShamrockSetGrating(device : Integer; Grating : Integer): Integer; stdcall;
  function ShamrockGetGrating(device : Integer; var Grating : Integer): Integer; stdcall;
  function ShamrockWavelengthReset(device : Integer): Integer; stdcall;
  function ShamrockGetNumberGratings(device : Integer; var noGratings : Integer): Integer; stdcall;
  function ShamrockGetGratingInfo(device : Integer; Grating : Integer; var Lines : Single; var Blaze : PChar; var Home : Single; var offset : PChar): Integer; stdcall;
  function ShamrockSetDetectorOffset(device : Integer; offset : Integer): Integer; stdcall;
  function ShamrockGetDetectorOffset(device : Integer; var offset : Integer): Integer; stdcall;
  function ShamrockSetGratingOffset(device : Integer; Grating : Integer; offset : Integer): Integer; stdcall;
  function ShamrockGetGratingOffset(device : Integer; Grating : Integer; var offset : Integer): Integer; stdcall;
  function ShamrockGratingIsPresent(device : Integer; var present : Integer): Integer; stdcall;
  function ShamrockSetTurret(device : Integer; Turret : Integer): Integer; stdcall;
  function ShamrockGetTurret(device : Integer; var Turret : Integer): Integer; stdcall;

  function ShamrockSetOutputSlit(device : Integer; width : Single): Integer; stdcall;
  function ShamrockGetOutputSlit(device : Integer; var width : Single): Integer; stdcall;
  function ShamrockOutputSlitReset(device : Integer): Integer; stdcall;
  function ShamrockOutputSlitIsPresent(device : Integer; var present : Integer): Integer; stdcall;

  function ShamrockSetShutter(device : Integer; mode : Integer): Integer; stdcall;
  function ShamrockGetShutter(device : Integer; var mode : Integer): Integer; stdcall;
  function ShamrockIsModePossible(device : Integer; mode : Integer; var possible : Integer): Integer; stdcall;
  function ShamrockShutterIsPresent(device : Integer; var present : Integer): Integer; stdcall;

  function ShamrockSetSlit(device : Integer; width : Single): Integer; stdcall;
  function ShamrockGetSlit(device : Integer; var width : Single): Integer; stdcall;
  function ShamrockSlitReset(device : Integer): Integer; stdcall;
  function ShamrockSlitIsPresent(device : Integer; var present : Integer): Integer; stdcall;

  function ShamrockEepromGetOpticalParams(device : Integer; FocalLength : Single; AngularDeviation : Single; FocalTilt : Single): Integer; stdcall;

  function ShamrockSetPixelWidth(device : Integer; width : Single): Integer; stdcall;  
  function ShamrockGetPixelWidth(device : Integer; var width : Single): Integer; stdcall;
  function ShamrockSetNumberPixels(device : Integer; number : Integer): Integer; stdcall;
  function ShamrockGetNumberPixels(device : Integer; var number : Integer): Integer; stdcall;
  function ShamrockGetCalibration(device : Integer; CalibrationValues : PSingle; number : Integer): Integer; stdcall;

implementation

  function ShamrockInitialize; external 'shamrockcif.dll' name 'ShamrockInitialize';
  function ShamrockClose; external 'shamrockcif.dll' name 'ShamrockClose';
  function ShamrockGetNumberDevices; external 'shamrockcif.dll' name 'ShamrockGetNumberDevices';
  function ShamrockGetSerialNumber; external 'shamrockcif.dll' name 'ShamrockGetSerialNumber';

  function ShamrockSetWavelength; external 'shamrockcif.dll' name 'ShamrockSetWavelength';
  function ShamrockGetWavelength; external 'shamrockcif.dll' name 'ShamrockGetWavelength';
  function ShamrockGotoZeroOrder; external 'shamrockcif.dll' name 'ShamrockGotoZeroOrder';
  function ShamrockAtZeroOrder; external 'shamrockcif.dll' name 'ShamrockAtZeroOrder';
  function ShamrockGetWavelengthLimits; external 'shamrockcif.dll' name 'ShamrockGetWavelengthLimits';
  function ShamrockWavelengthIsPresent; external 'shamrockcif.dll' name 'ShamrockWavelengthIsPresent';

  function ShamrockSetAccessory; external 'shamrockcif.dll' name 'ShamrockSetAccessory';
  function ShamrockGetAccessoryState; external 'shamrockcif.dll' name 'ShamrockGetAccessoryState';
  function ShamrockAccessoryIsPresent; external 'shamrockcif.dll' name 'ShamrockAccessoryIsPresent';

  function ShamrockSetFilter; external 'shamrockcif.dll' name 'ShamrockSetFilter';
  function ShamrockGetFilter; external 'shamrockcif.dll' name 'ShamrockGetFilter';
  function ShamrockGetFilterInfo; external 'shamrockcif.dll' name 'ShamrockGetFilterInfo';
  function ShamrockSetFilterInfo; external 'shamrockcif.dll' name 'ShamrockSetFilterInfo';
  function ShamrockFilterIsPresent; external 'shamrockcif.dll' name 'ShamrockFilterIsPresent';

  function ShamrockSetPort; external 'shamrockcif.dll' name 'ShamrockSetPort';
  function ShamrockGetPort; external 'shamrockcif.dll' name 'ShamrockGetPort';
  function ShamrockFlipperReset; external 'shamrockcif.dll' name 'ShamrockFlipperReset';
  function ShamrockGetCCDLimits; external 'shamrockcif.dll' name 'ShamrockGetCCDLimits';
  function ShamrockFlipperIsPresent; external 'shamrockcif.dll' name 'ShamrockFlipperIsPresent';

  function ShamrockSetGrating; external 'shamrockcif.dll' name 'ShamrockSetGrating';
  function ShamrockGetGrating; external 'shamrockcif.dll' name 'ShamrockGetGrating';
  function ShamrockWavelengthReset; external 'shamrockcif.dll' name 'ShamrockWavelengthReset';
  function ShamrockGetNumberGratings; external 'shamrockcif.dll' name 'ShamrockGetNumberGratings';
  function ShamrockGetGratingInfo; external 'shamrockcif.dll' name 'ShamrockGetGratingInfo';
  function ShamrockSetDetectorOffset; external 'shamrockcif.dll' name 'ShamrockSetDetectorOffset';
  function ShamrockGetDetectorOffset; external 'shamrockcif.dll' name 'ShamrockGetDetectorOffset';
  function ShamrockSetGratingOffset; external 'shamrockcif.dll' name 'ShamrockSetGratingOffset';
  function ShamrockGetGratingOffset; external 'shamrockcif.dll' name 'ShamrockGetGratingOffset';
  function ShamrockGratingIsPresent; external 'shamrockcif.dll' name 'ShamrockGratingIsPresent';
  function ShamrockSetTurret; external 'shamrockcif.dll' name 'ShamrockSetTurret';
  function ShamrockGetTurret; external 'shamrockcif.dll' name 'ShamrockGetTurret';

  function ShamrockSetOutputSlit; external 'shamrockcif.dll' name 'ShamrockSetOutputSlit';
  function ShamrockGetOutputSlit; external 'shamrockcif.dll' name 'ShamrockGetOutputSlit';
  function ShamrockOutputSlitReset; external 'shamrockcif.dll' name 'ShamrockOutputSlitReset';
  function ShamrockOutputSlitIsPresent; external 'shamrockcif.dll' name 'ShamrockOutputSlitIsPresent';

  function ShamrockSetShutter; external 'shamrockcif.dll' name 'ShamrockSetShutter';
  function ShamrockGetShutter; external 'shamrockcif.dll' name 'ShamrockGetShutter';
  function ShamrockIsModePossible; external 'shamrockcif.dll' name 'ShamrockIsModePossible';
  function ShamrockShutterIsPresent; external 'shamrockcif.dll' name 'ShamrockShutterIsPresent';

  function ShamrockSetSlit; external 'shamrockcif.dll' name 'ShamrockSetSlit';
  function ShamrockGetSlit; external 'shamrockcif.dll' name 'ShamrockGetSlit';
  function ShamrockSlitReset; external 'shamrockcif.dll' name 'ShamrockSlitReset';
  function ShamrockSlitIsPresent; external 'shamrockcif.dll' name 'ShamrockSlitIsPresent';

  function ShamrockEepromGetOpticalParams; external 'shamrockcif.dll' name 'ShamrockEepromGetOpticalParams';

  function ShamrockSetPixelWidth; external 'shamrockcif.dll' name 'ShamrockSetPixelWidth';     
  function ShamrockGetPixelWidth; external 'shamrockcif.dll' name 'ShamrockGetPixelWidth';
  function ShamrockSetNumberPixels; external 'shamrockcif.dll' name 'ShamrockSetNumberPixels';
  function ShamrockGetNumberPixels; external 'shamrockcif.dll' name 'ShamrockGetNumberPixels';
  function ShamrockGetCalibration; external 'shamrockcif.dll' name 'ShamrockGetCalibration';

end.
