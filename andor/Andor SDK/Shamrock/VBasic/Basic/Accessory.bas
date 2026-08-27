Attribute VB_Name = "mod9"
Sub ShowControlsAccessory(bEnable As Long)
  If IsAccessory = 0 Then bEnable = False
  ini.ebLine1.Enabled = bEnable
  ini.ebLine2.Enabled = bEnable
  ini.pbSetLine1.Enabled = bEnable
  ini.ebSetLine1.Enabled = bEnable
  ini.ebSetLine1.Enabled = bEnable
  ini.pbSetLine2.Enabled = bEnable
  ini.ebSetLine2.Enabled = bEnable
End Sub

Sub startaccessory()
  ReturnValue = ShamrockGetAccessoryState(device, 1, Accessory1)
  temp = ReturnValue
  Evaluate ("Accessory Line 1")
  ReturnValue = ShamrockGetAccessoryState(device, 2, Accessory2)
  Evaluate ("Accessory Line 2")
  If ReturnValue = SHAMROCK_SUCCESS And temp = SHAMROCK_SUCCESS Then
    ini.ebLine1.text = Accessory1
    ini.ebLine1.text = Accessory2
  End If
End Sub
