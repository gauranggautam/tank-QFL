VERSION 5.00
Begin VB.Form CalibrationForm 
   Caption         =   "Calibration"
   ClientHeight    =   6405
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   8160
   LinkTopic       =   "Form2"
   ScaleHeight     =   6405
   ScaleWidth      =   8160
   StartUpPosition =   3  'Windows Default
   WhatsThisButton =   -1  'True
   WhatsThisHelp   =   -1  'True
   Begin VB.CommandButton pbDefault 
      Caption         =   "Make Current Calibration Default"
      Height          =   735
      Left            =   5880
      TabIndex        =   16
      Top             =   5400
      Width           =   1215
   End
   Begin VB.CommandButton pbRestore 
      Caption         =   "Restore Default Calibration"
      Height          =   735
      Left            =   4440
      TabIndex        =   15
      Top             =   5400
      Width           =   1215
   End
   Begin VB.CheckBox optTempAdjust 
      Caption         =   "Temperature Adjust"
      Height          =   375
      Left            =   3000
      TabIndex        =   14
      Top             =   2400
      Width           =   1215
   End
   Begin VB.TextBox txtCurrentTemp 
      Height          =   285
      Left            =   5160
      TabIndex        =   12
      Text            =   "Text1"
      Top             =   1800
      Width           =   1095
   End
   Begin VB.TextBox txtPreviousTemp 
      Height          =   285
      Left            =   1920
      TabIndex        =   10
      Text            =   "Text1"
      Top             =   1800
      Width           =   1095
   End
   Begin VB.CommandButton cmdGoCalibrate 
      Caption         =   "Calibrate"
      Height          =   375
      Left            =   3120
      TabIndex        =   9
      Top             =   1080
      Width           =   1215
   End
   Begin VB.TextBox txtCalibrationFile 
      Height          =   285
      Left            =   240
      TabIndex        =   8
      Top             =   720
      Width           =   7455
   End
   Begin VB.CommandButton pbCancel 
      Caption         =   "Close"
      Height          =   495
      Left            =   1680
      TabIndex        =   7
      Top             =   5760
      Width           =   1215
   End
   Begin VB.CommandButton pbSaveCalibration 
      Caption         =   "Save Calibration"
      Height          =   495
      Left            =   240
      TabIndex        =   6
      Top             =   5760
      Width           =   1215
   End
   Begin VB.ListBox CalibrationResultsList 
      Height          =   1035
      Left            =   240
      TabIndex        =   4
      Top             =   4200
      Width           =   7335
   End
   Begin VB.TextBox SearchAreaText 
      Height          =   285
      Left            =   5880
      TabIndex        =   1
      Text            =   "Text1"
      Top             =   240
      Width           =   1095
   End
   Begin VB.Label Label6 
      Caption         =   "Current Mechelle Temperature"
      Height          =   495
      Left            =   3360
      TabIndex        =   13
      Top             =   1800
      Width           =   1575
   End
   Begin VB.Label Label5 
      Caption         =   "Previous Calibration Temperature"
      Height          =   495
      Left            =   240
      TabIndex        =   11
      Top             =   1800
      Width           =   1575
   End
   Begin VB.Label Label4 
      Caption         =   "Cal X        CalY        InitialX          InitialY           MeasX          MeasY              ResidX         ResidY"
      Height          =   495
      Left            =   240
      TabIndex        =   5
      Top             =   3720
      Width           =   7335
   End
   Begin VB.Label Label3 
      Caption         =   "Calibration results"
      Height          =   375
      Left            =   1200
      TabIndex        =   3
      Top             =   3240
      Width           =   1695
   End
   Begin VB.Label Label2 
      Caption         =   "Search Area"
      Height          =   255
      Left            =   4560
      TabIndex        =   2
      Top             =   240
      Width           =   1095
   End
   Begin VB.Label Label1 
      BackColor       =   &H00808000&
      Caption         =   "calibration File"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   255
      Left            =   240
      TabIndex        =   0
      Top             =   360
      Width           =   1575
   End
End
Attribute VB_Name = "CalibrationForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Dim szCalFile As String
Dim iLinesFound As Long


Private Sub Calibrationdir_Change()
Calibrationfile.path = Calibrationdir.path
End Sub


Private Sub cmdGoCalibrate_Click()
  CalibrationResultsList.Clear
  If Not bMechelleInitialized Then
    szfoundlinetxt = "Mechelle Not Inititlized"
    CalibrationResultsList.AddItem (szfoundlinetxt)
    Exit Sub
  End If
  If Not bImageAcquired Then
    szfoundlinetxt = "Image not acquired"
    CalibrationResultsList.AddItem (szfoundlinetxt)
    Exit Sub
  End If
  
  ErrorString = MechelleCalibrate(txtCalibrationFile.text, Val(SearchAreaText.text), aData(1), calibrationResults(0), iLinesFound)
  If ErrorString = DRV_SUCCESS Then
    If iLinesFound > 0 Then
      For i = 0 To iLinesFound - 1
        szfoundlinetxt = calibrationResults(i).calculatedX & "  " & calibrationResults(i).calculatedY & "  " & calibrationResults(i).initialX & "  " & calibrationResults(i).initialY & "  " & calibrationResults(i).measuredX & "  " & calibrationResults(i).measuredY & "  " & calibrationResults(i).residualX & "  " & calibrationResults(i).residualY
        CalibrationResultsList.AddItem (szfoundlinetxt)
      Next i
    Else
      szfoundlinetxt = "*****No Lines Found*****"
      CalibrationResultsList.AddItem (szfoundlinetxt)
    End If
  End If
  
End Sub

Private Sub Form_Load()
SearchAreaText.text = "20"
txtCalibrationFile = szLastCalibrationFile

ErrorString = MechelleGetSavedCalibrationTemperature(prevTemp)
ErrorString = MechelleGetInternalTemperature(curTemp)
txtPreviousTemp.text = prevTemp
txtCurrentTemp.text = curTemp
If (bTemperatureAdjust = True) Then
  optTempAdjust.Value = 1
Else
  optTempAdjust.Value = 0
End If
  
End Sub

Private Sub optTempAdjust_Click()
  If bTemperatureAdjust = True Then
    bTemperatureAdjust = False
  Else
    bTemperatureAdjust = True
  End If
End Sub

Private Sub pbCancel_Click()
Unload Me
End Sub

Private Sub pbDefault_Click()
  If Not bMechelleInitialized Then
    szfoundlinetxt = "Mechelle Not Inititlized"
    CalibrationResultsList.AddItem (szfoundlinetxt)
    Exit Sub
  End If
  MechelleBackupCalibration
End Sub

Private Sub pbRestore_Click()
  CalibrationResultsList.Clear

  If Not bMechelleInitialized Then
    szfoundlinetxt = "Mechelle Not Inititlized"
    CalibrationResultsList.AddItem (szfoundlinetxt)
    Exit Sub
  End If
  
  MechelleRestoreCalibration
End Sub

Private Sub pbSaveCalibration_Click()
  CalibrationResultsList.Clear
  
  Dim temperature As Single
  ErrorString = MechelleGetInternalTemperature(temperature)
  ErrorString = MechelleSaveCalibration(temperature)
  If ErrorString = DRV_SUCCESS Then
    szfoundlinetxt = "Calibration Saved OK"
    CalibrationResultsList.AddItem (szfoundlinetxt)
  End If
End Sub

Private Sub Text1_Change()

End Sub
