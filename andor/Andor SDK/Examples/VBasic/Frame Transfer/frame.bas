Attribute VB_Name = "Module1"
Option Explicit

Type PALETTEENTRY
  peRed As String * 1
  peGreen As String * 1
  peBlue As String * 1
  peFlags As String * 1
End Type

Type LOGPALETTE
  palVersion As Integer
  palNumEntries As Integer
  palPalEntry(255) As PALETTEENTRY ' Enough for 256 colors
End Type

Global Const LOCALERROR = 0
Global Const XON = 1
Global Const XOFF = 0
Global Const NUMCOLORS = 24
Global naXPixels As Long
Global naYPixels As Long
Global test As Long
Global aData() As Long
Global bData() As Long
Global buf As String
Global buffer As String
Global newLine
Global StartTimer As Long

Declare Function GetWindowDC Lib "USER32" (ByVal hWnd As Integer) As Integer
Declare Function GetDeviceCaps Lib "GDI32" (ByVal hDC As Integer, ByVal nIndex As Integer) As Integer
Declare Function GetSystemPaletteEntries Lib "GDI32" (ByVal hDC As Integer, ByVal wStartIndex As Integer, ByVal wNumEntries As Integer, lpPaletteEntries As PALETTEENTRY) As Integer
Declare Function CreatePalette Lib "GDI32" (lpLogPalette As LOGPALETTE) As Integer
Declare Function SelectPalette Lib "GDI32" (ByVal hDC As Integer, ByVal hPalette As Integer, ByVal bForceBackground As Integer) As Integer
Declare Function RealizePalette Lib "GDI32" (ByVal hDC As Integer) As Integer








