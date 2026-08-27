Attribute VB_Name = "mod4"
Sub ShowControlsWavelength(bEnable As Long)
If IsWavelength = 0 Then bEnable = False
  ini.ebCurrentWl.Enabled = bEnable
  ini.ebMinWl.Enabled = bEnable
  ini.ebMaxWl.Enabled = bEnable
  ini.pbGotoWl.Enabled = bEnable
  ini.ebGotoWl.Enabled = bEnable
  ini.pbGotoZeroOrder.Enabled = bEnable
End Sub

Sub startwavelength()
  ReturnValue = ShamrockGetWavelength(device, wavelength)
  Evaluate ("Wavelength")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebCurrentWl.text = wavelength
  End If
  
  ReturnValue = ShamrockGetWavelengthLimits(device, Grating, MinWl, MaxWl)
  Evaluate ("WavelengthLimits")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebMinWl.text = Str(MinWl)
    ini.ebMaxWl.text = Str(MaxWl)
  End If
End Sub


