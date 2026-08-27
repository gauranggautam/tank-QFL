Attribute VB_Name = "mod1"
Global Const SHAMROCK_COMMUNICATION_ERROR = 20201
Global Const SHAMROCK_SUCCESS = 20202
Global Const SHAMROCK_P1INVALID = 20266
Global Const SHAMROCK_P2INVALID = 20267
Global Const SHAMROCK_P3INVALID = 20268
Global Const SHAMROCK_NOT_INITIALIZED = 20275

Global Const SHAMROCK_ACCESSORYMIN = 1
Global Const SHAMROCK_ACCESSORYMAX = 3
Global Const SHAMROCK_FILTERMIN = 1
Global Const SHAMROCK_FILTERMAX = 6
Global Const SHAMROCK_PORTMIN = 1
Global Const SHAMROCK_PORTMAX = 6
Global Const SHAMROCK_TURRETMIN = 1
Global Const SHAMROCK_TURRETMAX = 3
Global Const SHAMROCK_GRATINGMIN = 1
Global Const SHAMROCK_SLITWIDTHMIN = 10
Global Const SHAMROCK_SLITWIDTHMAX = 2500
Global Const SHAMROCK_SHUTTERMODEMIN = 0
Global Const SHAMROCK_SHUTTERMODEMAX = 1


Declare Function ShamrockInitialize Lib "shamrockcif.dll" (ByVal dirName As String) As Long
Declare Function ShamrockClose Lib "shamrockcif.dll" () As Long
Declare Function ShamrockGetNumberDevices Lib "shamrockcif.dll" (noDevices As Long) As Long
Declare Function ShamrockGetSerialNumber Lib "shamrockcif.dll" (ByVal device As Long, ByVal serial As String) As Long
Declare Function ShamrockGetFunctionReturnDescription Lib "shamrockcif.dll" (ByVal error As Long, ByVal description As String, ByVal maxstrlen As Long) As Long

Declare Function ShamrockSetWavelength Lib "shamrockcif.dll" (ByVal device As Long, ByVal wavelength As Single) As Long
Declare Function ShamrockGetWavelength Lib "shamrockcif.dll" (ByVal device As Long, wavelength As Single) As Long
Declare Function ShamrockGotoZeroOrder Lib "shamrockcif.dll" (ByVal device As Long) As Long
Declare Function ShamrockAtZeroOrder Lib "shamrockcif.dll" (ByVal device As Long, atZeroOrder As Long) As Long
Declare Function ShamrockGetWavelengthLimits Lib "shamrockcif.dll" (ByVal device As Long, ByVal Grating As Long, Min As Single, Max As Single) As Long
Declare Function ShamrockWavelengthIsPresent Lib "shamrockcif.dll" (ByVal device As Long, present As Long) As Long

Declare Function ShamrockSetAccessory Lib "shamrockcif.dll" (ByVal device As Long, ByVal Accessory As Long, ByVal state As Long) As Long
Declare Function ShamrockGetAccessoryState Lib "shamrockcif.dll" (ByVal device As Long, ByVal Accessory As Long, state As Long) As Long
Declare Function ShamrockAccessoryIsPresent Lib "shamrockcif.dll" (ByVal device As Long, present As Long) As Long

Declare Function ShamrockSetFilter Lib "shamrockcif.dll" (ByVal device As Long, ByVal Filter As Long) As Long
Declare Function ShamrockGetFilter Lib "shamrockcif.dll" (ByVal device As Long, Filter As Long) As Long
Declare Function ShamrockGetFilterInfo Lib "shamrockcif.dll" (ByVal device As Long, ByVal Filter As Long, ByVal Info As String) As Long
Declare Function ShamrockSetFilterInfo Lib "shamrockcif.dll" (ByVal device As Long, ByVal Filter As Long, ByVal Info As String) As Long
Declare Function ShamrockFilterIsPresent Lib "shamrockcif.dll" (ByVal device As Long, present As Long) As Long

Declare Function ShamrockSetPort Lib "shamrockcif.dll" (ByVal device As Long, ByVal port As Long) As Long
Declare Function ShamrockGetPort Lib "shamrockcif.dll" (ByVal device As Long, port As Long) As Long
Declare Function ShamrockFlipperReset Lib "shamrockcif.dll" (ByVal device As Long) As Long
Declare Function ShamrockGetCCDLimits Lib "shamrockcif.dll" (ByVal device As Long, ByVal port As Long, Low As Single, High As Single) As Long
Declare Function ShamrockFlipperIsPresent Lib "shamrockcif.dll" (ByVal device As Long, present As Long) As Long

Declare Function ShamrockSetGrating Lib "shamrockcif.dll" (ByVal device As Long, ByVal Grating As Long) As Long
Declare Function ShamrockGetGrating Lib "shamrockcif.dll" (ByVal device As Long, Grating As Long) As Long
Declare Function ShamrockWavelengthReset Lib "shamrockcif.dll" (ByVal device As Long) As Long
Declare Function ShamrockGetNumberGratings Lib "shamrockcif.dll" (ByVal device As Long, noGratings As Long) As Long
Declare Function ShamrockGetGratingInfo Lib "shamrockcif.dll" (ByVal device As Long, ByVal Grating As Long, Lines As Single, ByVal blaze As String, Home As Long, offset As Long) As Long
Declare Function ShamrockSetDetectorOffset Lib "shamrockcif.dll" (ByVal device As Long, ByVal offset As Long) As Long
Declare Function ShamrockGetDetectorOffset Lib "shamrockcif.dll" (ByVal device As Long, offset As Long) As Long
Declare Function ShamrockSetGratingOffset Lib "shamrockcif.dll" (ByVal device As Long, ByVal Grating As Long, ByVal offset As Long) As Long
Declare Function ShamrockGetGratingOffset Lib "shamrockcif.dll" (ByVal device As Long, ByVal Grating As Long, offset As Long) As Long
Declare Function ShamrockGratingIsPresent Lib "shamrockcif.dll" (ByVal device As Long, present As Long) As Long
Declare Function ShamrockSetTurret Lib "shamrockcif.dll" (ByVal device As Long, ByVal Turret As Long) As Long
Declare Function ShamrockGetTurret Lib "shamrockcif.dll" (ByVal device As Long, Turret As Long) As Long

Declare Function ShamrockSetOutputSlit Lib "shamrockcif.dll" (ByVal device As Long, ByVal width As Single) As Long
Declare Function ShamrockGetOutputSlit Lib "shamrockcif.dll" (ByVal device As Long, width As Single) As Long
Declare Function ShamrockOutputSlitReset Lib "shamrockcif.dll" (ByVal device As Long) As Long
Declare Function ShamrockOutputSlitIsPresent Lib "shamrockcif.dll" (ByVal device As Long, present As Long) As Long

Declare Function ShamrockSetShutter Lib "shamrockcif.dll" (ByVal device As Long, ByVal mode As Long) As Long
Declare Function ShamrockGetShutter Lib "shamrockcif.dll" (ByVal device As Long, mode As Long) As Long
Declare Function ShamrockIsModePossible Lib "shamrockcif.dll" (ByVal device As Long, ByVal mode As Long, possible As Long) As Long
Declare Function ShamrockShutterIsPresent Lib "shamrockcif.dll" (ByVal device As Long, present As Long) As Long

Declare Function ShamrockSetSlit Lib "shamrockcif.dll" (ByVal device As Long, ByVal width As Single) As Long
Declare Function ShamrockGetSlit Lib "shamrockcif.dll" (ByVal device As Long, width As Single) As Long
Declare Function ShamrockSlitReset Lib "shamrockcif.dll" (ByVal device As Long) As Long
Declare Function ShamrockSlitIsPresent Lib "shamrockcif.dll" (ByVal device As Long, present As Long) As Long

Declare Function ShamrockEepromGetOpticalParams Lib "shamrockcif.dll" (ByVal device As Long, FocalLength As Single, AngularDeviation As Single, FocalTilt As Single) As Long

Declare Function ShamrockSetPixelWidth Lib "shamrockcif.dll" (ByVal device As Long, ByVal width As Single) As Long
Declare Function ShamrockSetNumberPixels Lib "shamrockcif.dll" (ByVal device As Long, ByVal NumberPixels As Long) As Long
Declare Function ShamrockGetPixelWidth Lib "shamrockcif.dll" (ByVal device As Long, Width As Single) As Long
Declare Function ShamrockGetNumberPixels Lib "shamrockcif.dll" (ByVal device As Long, NumberPixels As Long) As Long
Declare Function ShamrockGetCalibration Lib "shamrockcif.dll" (ByVal device As Long, DArray As Single, ByVal NumberPixels As Long) As Long


