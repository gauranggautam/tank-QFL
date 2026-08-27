Attribute VB_Name = "mod7"
Sub ShowControlsShutter(bEnable As Long)
  If IsShutter = 0 Then bEnable = False
  ini.ebCurrentShutter.Enabled = bEnable
  ini.pbSetShutter.Enabled = bEnable
  ini.ebSetShutter.Enabled = bEnable
End Sub

Sub startshutter()
  ReturnValue = ShamrockGetShutter(device, Shutter)
  Evaluate ("Shutter")
  If ReturnValue = SHAMROCK_SUCCESS Then
    If Shutter = 0 Then
      shutterbuffer = "closed (0)"
    ElseIf Shutter = 1 Then
      shutterbuffer = "open (1)"
    Else
      shutterbuffer = "unknown"
    End If
    ini.ebCurrentShutter.text = shutterbuffer
  End If
End Sub

