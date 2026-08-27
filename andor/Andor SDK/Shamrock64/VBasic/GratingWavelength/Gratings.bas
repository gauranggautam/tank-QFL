Attribute VB_Name = "mod3"

Sub ShowControlsGratings(bEnable As Long)
  If IsGrating = 0 Then bEnable = False
  ini.ebTurretSettings.Enabled = bEnable
  ini.ebNoGratings.Enabled = bEnable
  ini.ebCurrentGrating.Enabled = bEnable
  ini.ebLines.Enabled = bEnable
  ini.ebBlaze.Enabled = bEnable
  ini.ebHome.Enabled = bEnable
  ini.ebGratingOffset.Enabled = bEnable
  ini.ebDetectorOffset.Enabled = bEnable
  ini.pbSetTurret.Enabled = bEnable
  ini.ebSetTurret.Enabled = bEnable
  ini.pbSetGrating.Enabled = bEnable
  ini.ebSetGrating.Enabled = bEnable
  ini.pbSetGratingOffset.Enabled = bEnable
  ini.ebSetGratingOffset.Enabled = bEnable
  ini.pbSetDetectorOffset.Enabled = bEnable
  ini.ebSetDetectorOffset.Enabled = bEnable
  ini.pbResetWl.Enabled = bEnable
End Sub

Sub startgratings()
  ReturnValue = ShamrockGetTurret(device, Turret)
  Evaluate ("Turret")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebTurretSettings.text = Str(Turret)
  End If
  
  ReturnValue = ShamrockGetNumberGratings(device, noGratings)
  Evaluate ("Number of Gratings")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebNoGratings.text = Str(noGratings)
  End If
  
  ReturnValue = ShamrockGetGrating(device, Grating)
  Evaluate ("Grating")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebCurrentGrating.text = Str(Grating)
    GetGratingInfo
  End If
  
  ReturnValue = ShamrockGetDetectorOffset(device, detOffset)
  Evaluate ("Detector Offset")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebDetectorOffset.text = Str(detOffset)
  End If
  
  startwavelength
End Sub


Sub GetGratingInfo()
  Dim blaze As String
  blaze = "not available"
  ReturnValue = ShamrockGetGratingInfo(device, Grating, Lines, blaze, Home, offset)
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebLines.text = Str(Lines)
    ini.ebBlaze.text = blaze
    ini.ebHome.text = Str(Home)
    ini.ebGratingOffset.text = Str(offset)
  End If
End Sub
