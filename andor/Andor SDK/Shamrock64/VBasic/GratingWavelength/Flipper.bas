Attribute VB_Name = "mod6"
Sub ShowControlsFlipper(bEnable As Long)
  If IsFlipper = 0 Then bEnable = False
  ini.ebCurrentFlipper.Enabled = bEnable
  ini.ebCCDLow.Enabled = bEnable
  ini.ebCCDHigh.Enabled = bEnable
  ini.pbSetFlipper.Enabled = bEnable
  ini.ebSetFlipper.Enabled = bEnable
  ini.pbResetFlipper.Enabled = bEnable
End Sub

Sub startflipper()
  ReturnValue = ShamrockGetPort(device, Flipper)
  Evaluate ("Flipper")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebCurrentFlipper.text = Flipper
  End If
  
  ReturnValue = ShamrockGetCCDLimits(device, Flipper, Low, High)
  Evaluate ("CCD Limits")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebCCDLow.text = Low
    ini.ebCCDHigh.text = High
  End If
End Sub

