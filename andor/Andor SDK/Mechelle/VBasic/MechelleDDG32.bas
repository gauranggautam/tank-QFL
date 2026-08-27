Attribute VB_Name = "Module1"
Global Const LOCALERROR = 0
Global Const XON = 1
Global Const XOFF = 0
Global nXPixels As Long
Global nYPixels As Long
Global test As Long
Global aData() As Long
Global aRowData() As Long
Global buf As String
Global buffer As String
Global newLine
Global StartTimer As Long
Global ErrorString As Long
Global bMechelleInitialized As Boolean
Global iMechelleSpect() As Long
Global spectralDataArray() As SpectralData
Global iMaxArraySize As Long
Global dCoefs() As Double
Global iSpectrumSize As Long
Global szSpectrumSaveFileName As String
Global calibrationResults(20) As CalibrationData
Global bImageAcquired As Boolean
Global szMechInitDir As String
Global szLastCalibrationFile As String
Global prevTemp As Single
Global curTemp As Single
Global bTemperatureAdjust As Boolean

Public Const OFN_NOCHANGEDIR = &H8

Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)








