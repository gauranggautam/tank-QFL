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

Sub InitializeAccessoriesPresence()
'**************************************************************
' No elements/accessories are a priori functional in the Shamrock
'**************************************************************
  IsWavelength = 0
  IsGrating = 0
End Sub

Sub AreAccessoriesPresent()
'**************************************************************
' Finds what elements/accessories are functional in the Shamrock
'**************************************************************
  ReturnValue = ShamrockWavelengthIsPresent(device, IsWavelength)
  ReturnValue = ShamrockGratingIsPresent(device, IsGrating)
End Sub

Sub ShowControls(bEnable As Long)
'**************************************************************
' Activates/deactivates controls.
'**************************************************************
  If bEnable = False Then
    ini.Height = 4575
    ini.width = 4350
  Else
    ini.Height = 5580
    ini.width = 6495
  End If
  
  ini.pbOpenControls.Enabled = Not bEnable
  ini.pbCloseControls.Enabled = bEnable
  ini.cbDevice.Enabled = bEnable
  ini.ebSerialNumber.Enabled = bEnable
  ini.ebFocalLength.Enabled = bEnable
  ini.ebAngularDev.Enabled = bEnable
  ini.ebFocalTilt.Enabled = bEnable
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
