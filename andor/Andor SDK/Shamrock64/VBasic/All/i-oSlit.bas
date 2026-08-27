Attribute VB_Name = "mod8"
Sub ShowControlsInputSlit(bEnable As Long)
  If IsInputSlit = 0 Then bEnable = False
  ini.ebCurrentInputSlit.Enabled = bEnable
  ini.pbSetInputSlit.Enabled = bEnable
  ini.ebSetInputSlit.Enabled = bEnable
  ini.pbResetInputSlit.Enabled = bEnable
End Sub

Sub startinputslit()
  ReturnValue = ShamrockGetSlit(device, InputSlit)
  Evaluate ("Input Slit")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebCurrentInputSlit.text = InputSlit
  End If
End Sub

Sub ShowControlsOutputSlit(bEnable As Long)
  If IsOutputSlit = 0 Then bEnable = False
  ini.ebCurrentOutputSlit.Enabled = bEnable
  ini.pbSetOutputSlit.Enabled = bEnable
  ini.ebSetOutputSlit.Enabled = bEnable
  ini.pbResetOutputSlit.Enabled = bEnable
End Sub

Sub startoutputslit()
  ReturnValue = ShamrockGetOutputSlit(device, OutputSlit)
  Evaluate ("Output Slit")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebCurrentOutputSlit.text = OutputSlit
  End If
End Sub
