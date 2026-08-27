Attribute VB_Name = "mod5"
Sub ShowControlsFilter(bEnable As Long)
  If IsFilter = 0 Then bEnable = False
  ini.ebCurrentFilter.Enabled = bEnable
  ini.ebCurrentFilterInfo.Enabled = bEnable
  ini.pbGotoFilter.Enabled = bEnable
  ini.ebGotoFilter.Enabled = bEnable
  ini.pbSetFilterInfo.Enabled = bEnable
  ini.ebSetFilterInfo.Enabled = bEnable
End Sub

Sub startfilter()
  ReturnValue = ShamrockGetFilter(device, Filter)
  Evaluate ("Filter")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebCurrentFilter.text = Filter
  End If
  
  Dim Info As String
  Info = "not available"
  ReturnValue = ShamrockGetFilterInfo(device, Filter, Info)
  Evaluate ("Filter information")
  If ReturnValue = SHAMROCK_SUCCESS Then
    ini.ebCurrentFilterInfo.text = Info
  End If
End Sub
