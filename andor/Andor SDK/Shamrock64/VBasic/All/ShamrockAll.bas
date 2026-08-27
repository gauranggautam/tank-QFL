Attribute VB_Name = "mod2"
Global TextLineCounter As Integer
Global IsIni As Integer
Global buf As String
Global newLine As String
Global ReturnValue As Long
Global noDevices As Long
Global device As Long

Global IsWavelength As Long
Global Turret As Long

Global IsGrating As Long
Global Grating As Long

Global IsFilter As Long
Global Filter As Long

Global IsFlipper As Long
Global Flipper As Long

Global IsShutter As Long
Global Shutter As Long

Global IsInputSlit As Long
Global InputSlit As Single

Global IsOutputSlit As Long
Global OutputSlit As Single

Global IsAccessory As Long
Global Accessory1 As Long
Global Accessory2 As Long

Sub InitializeAccessoriesPresence()
'**************************************************************
' No elements/accessories are a priori functional in the Shamrock
'**************************************************************
  IsWavelength = 0
  IsGrating = 0
  IsFilter = 0
  IsFlipper = 0
  IsShutter = 0
  IsInputSlit = 0
  IsOutputSlit = 0
  IsAccessory = 0
End Sub

Sub AreAccessoriesPresent()
'**************************************************************
' Finds what elements/accessories are functional in the Shamrock
'**************************************************************
  ReturnValue = ShamrockWavelengthIsPresent(device, IsWavelength)
  ReturnValue = ShamrockGratingIsPresent(device, IsGrating)
  ReturnValue = ShamrockFilterIsPresent(device, IsFilter)
  ReturnValue = ShamrockFlipperIsPresent(device, IsFlipper)
  ReturnValue = ShamrockShutterIsPresent(device, IsShutter)
  ReturnValue = ShamrockSlitIsPresent(device, IsInputSlit)
  ReturnValue = ShamrockOutputSlitIsPresent(device, IsOutputSlit)
  ReturnValue = ShamrockAccessoryIsPresent(device, IsAccessory)
End Sub

Sub ShowControls(bEnable As Long)
'**************************************************************
' Activates/deactivates controls.
'**************************************************************
  If bEnable = False Then
    ini.Height = 4575
    ini.width = 4350
  Else
    ini.Height = 8490
    ini.width = 12660
  End If
  
  ini.pbOpenControls.Enabled = Not bEnable
  ini.pbCloseControls.Enabled = bEnable
  ini.cbDevice.Enabled = bEnable
  ini.ebSerialNumber.Enabled = bEnable
  ini.ebFocalLength.Enabled = bEnable
  ini.ebAngularDev.Enabled = bEnable
  ini.ebFocalTilt.Enabled = bEnable
    
  ShowControlsGratings (bEnable)
  ShowControlsWavelength (bEnable)
  ShowControlsFilter (bEnable)
  ShowControlsFlipper (bEnable)
  ShowControlsShutter (bEnable)
  ShowControlsInputSlit (bEnable)
  ShowControlsOutputSlit (bEnable)
  ShowControlsAccessory (bEnable)
End Sub

Sub GetShamrockInfo()
  Dim SerialNo As String
  
  device = ini.cbDevice.ListIndex
  AreAccessoriesPresent
  ShowControls (True)
  SerialNo = "not available"
  ReturnValue = ShamrockGetSerialNumber(device, SerialNo)
  Evaluate ("Serial Number")
  ini.ebSerialNumber.text = SerialNo
  
  ReturnValue = ShamrockEepromGetOpticalParams(device, FocalLength, AngularDev, FocalTilt)
  Evaluate ("Optical Parameters")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebFocalLength.text = Str(FocalLength)
    ini.ebAngularDev.text = Str(AngularDev)
    ini.ebFocalTilt.text = Str(FocalTilt)
  End If
  
  If IsGrating = 1 Then startgratings
  If IsWavelength = 1 Then startwavelength
  If IsFilter = 1 Then startfilter
  If IsFlipper = 1 Then startflipper
  If IsShutter = 1 Then startshutter
  If IsInputSlit = 1 Then startinputslit
  If IsOutputSlit = 1 Then startoutputslit
  If IsAccessory = 1 Then startaccessory
End Sub

Sub Evaluate(text As String)
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.PrintStatusMsg ("Got " & text)
  Else
    ini.PrintStatusMsg ("Can't get " & text)
  End If
End Sub

Sub EvaluateAction(text As String)
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.PrintStatusMsg (text & " successful")
  Else
    ini.PrintStatusMsg ("Can't " & text)
  End If
End Sub
