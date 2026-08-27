VERSION 5.00
Begin VB.Form Form1 
   BackColor       =   &H00808000&
   Caption         =   "AndorMCD Visual Basic Example Drivers:- Frame Transfer"
   ClientHeight    =   5400
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   8385
   FillColor       =   &H00808000&
   BeginProperty Font 
      Name            =   "MS Sans Serif"
      Size            =   13.5
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   ForeColor       =   &H00808000&
   LinkTopic       =   "Form1"
   ScaleHeight     =   5400
   ScaleWidth      =   8385
   StartUpPosition =   3  'Windows Default
   Begin VB.Frame Frame1 
      BackColor       =   &H00808000&
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   800
      Left            =   4250
      TabIndex        =   16
      Top             =   4455
      Width           =   4000
      Begin VB.CommandButton pbUpdate 
         Caption         =   "Update"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   2880
         TabIndex        =   19
         Top             =   240
         Width           =   975
      End
      Begin VB.TextBox ebCCDScan 
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   324
         Left            =   1800
         TabIndex        =   17
         Text            =   "1"
         Top             =   240
         Width           =   732
      End
      Begin VB.Label lblDisplayScan 
         BackColor       =   &H00808000&
         Caption         =   "Scan of the series to display on the screen"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   612
         Left            =   120
         TabIndex        =   18
         Top             =   160
         Width           =   1692
      End
   End
   Begin VB.TextBox ebNumber 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   288
      Left            =   3480
      TabIndex        =   15
      Text            =   "2"
      Top             =   1550
      Width           =   612
   End
   Begin VB.PictureBox Picture2 
      Height          =   4000
      Left            =   4250
      Picture         =   "frame.frx":0000
      ScaleHeight     =   263
      ScaleMode       =   0  'User
      ScaleWidth      =   263
      TabIndex        =   13
      Top             =   120
      Width           =   4000
   End
   Begin VB.PictureBox Picture1 
      BackColor       =   &H80000005&
      Height          =   975
      Left            =   120
      Picture         =   "frame.frx":518A
      ScaleHeight     =   915
      ScaleWidth      =   3915
      TabIndex        =   12
      Top             =   120
      Width           =   3975
   End
   Begin VB.TextBox ebShutterTime 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   288
      Left            =   3480
      TabIndex        =   2
      Text            =   "100"
      Top             =   2600
      Width           =   612
   End
   Begin VB.ComboBox cbShutterTTL 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   315
      Left            =   2400
      TabIndex        =   3
      Top             =   2950
      Width           =   1692
   End
   Begin VB.Timer Timer1 
      Interval        =   100
      Left            =   2520
      Top             =   1320
   End
   Begin VB.CommandButton pbClose 
      Caption         =   "&Close"
      Default         =   -1  'True
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   492
      Index           =   2
      Left            =   3120
      TabIndex        =   6
      Top             =   3450
      Width           =   972
   End
   Begin VB.CommandButton pbAbortAcq 
      Caption         =   "&Abort Acq"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   492
      Index           =   1
      Left            =   1600
      TabIndex        =   5
      Top             =   3450
      Width           =   972
   End
   Begin VB.CommandButton pbStartAcq 
      Caption         =   "&Start Acq"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   492
      Index           =   0
      Left            =   120
      TabIndex        =   4
      Top             =   3450
      Width           =   972
   End
   Begin VB.ComboBox cbTrigger 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   315
      Left            =   2400
      TabIndex        =   1
      Top             =   2250
      Width           =   1692
   End
   Begin VB.TextBox ebExposureTime 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   288
      Left            =   3480
      TabIndex        =   0
      Text            =   "3.5"
      Top             =   1200
      Width           =   612
   End
   Begin VB.TextBox ebStatusBox 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   1200
      Left            =   120
      MultiLine       =   -1  'True
      TabIndex        =   11
      Top             =   4065
      Width           =   3945
   End
   Begin VB.Label lblNumber 
      BackColor       =   &H00808000&
      Caption         =   "Number in series"
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
      Left            =   120
      TabIndex        =   14
      Top             =   1550
      Width           =   1575
   End
   Begin VB.Label lblShutterTime 
      BackColor       =   &H00808000&
      Caption         =   "Ti&me to open or close shutter (ms)"
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
      Left            =   120
      TabIndex        =   9
      Top             =   2600
      Width           =   3375
   End
   Begin VB.Label lblShutterTTL 
      BackColor       =   &H00808000&
      Caption         =   "Shutter &opens on:"
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
      Left            =   120
      TabIndex        =   10
      Top             =   2950
      Width           =   1455
   End
   Begin VB.Label lblTrigger 
      BackColor       =   &H00808000&
      Caption         =   "&Trigger Mode"
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
      Left            =   120
      TabIndex        =   8
      Top             =   2250
      Width           =   1455
   End
   Begin VB.Label lblExposureTime 
      BackColor       =   &H00808000&
      Caption         =   "&Exposure Time (secs)"
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
      Left            =   120
      TabIndex        =   7
      Top             =   1200
      Width           =   1935
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'***********************************************************************
'This application demonstrates how to program AndorMCD to
'acquire a Frame Transfer, Full Resolution Image.
'
'All AndorMCD driver calls are in functions preceded by the
'letters vb to simplify error catching, eg the driver call
'SetExposureTime(exposureTime) is located in the Visual Basic
'function vbSetExposureTime().
'
'NB The dimensions of the Windows interface were devised for
'a Windows monitor with 1024x768 pixels.  The
'application will work with other configurations (eg SVGA
'640x480) but may appear large.
'**************************************************************************

Sub Form_Load()
'**************************************************************
' Initializing routine called before the Window interface
' is displayed
'**************************************************************
  cbTrigger.AddItem "Internal"
  cbTrigger.AddItem "External"
  cbTrigger.text = cbTrigger.List(0) 'Choose Internal as default
  cbTrigger.ListIndex = 0

  cbShutterTTL.AddItem "TTL Low"
  cbShutterTTL.AddItem "TTL High"
  cbShutterTTL.text = cbShutterTTL.List(1) 'Choose TTL Low as default
  cbShutterTTL.ListIndex = 1

  newLine = Chr(13) & Chr(10)
  PrintStatusMsg ("* FRAME TRANSFER * IMAGE MODE * AUTO SHUTTER *")
  InitializeAndorMCD         'Initialize AndorMCD system
End Sub

Sub InitializeAndorMCD()
'**************************************************************
' Initialize AndorMCD system.  The way to "read" this code,
' assuming no error occurs, is simply:
' 1) Initialize AndorMCD hardware.
' 2) Read in the CCD sensor format.
' 3) Set Acquisition mode to Single Scan.
' 4) Set binning pattern to Image.
'**************************************************************

  If (vbInitialize() = LOCALERROR) Then
    Exit Sub
  End If
  If (vbGetDetector() = LOCALERROR) Then
    Exit Sub
  End If
  If (vbSetAcquisition() = LOCALERROR) Then
    Exit Sub
  End If
  If (vbSetReadout() = LOCALERROR) Then
    Exit Sub
  End If
End Sub

Function vbAbortAcq()
'**************************************************************
' Tells AndorMCD to abort acquisition.
'**************************************************************
  vbAbortAcq = Not LOCALERROR
  test = AbortAcquisition()
  If (test <> DRV_SUCCESS) Then
    buffer = "Abort ERROR: "
    vbAbortAcq = LOCALERROR
    Select Case (test)
      Case DRV_IDLE
        buffer = buffer & "AndorMCD isn't acquiring data."
      Case DRV_VXDNOTINSTALLED
        buffer = buffer & "VxD not loaded"
      Case Else
        buffer = buffer & "Unknown Abort error."
    End Select
  Else
    buffer = "Aborting acquisition."
  End If
  PrintStatusMsg (buffer)
End Function

Function vbGetDetector()
'**************************************************************
' Gets the CCD chip format in pixels.  Needs the file
' "Detector.ini".
'**************************************************************
  Dim xpixels As Long
  Dim ypixels As Long
  vbGetDetector = Not LOCALERROR
  test = GetDetector(xpixels, ypixels)
  If test = DRV_SUCCESS Then
    buffer = "Getting Detector format"
    ebStatusBox.text = buf
    naYPixels = ypixels
    naXPixels = xpixels
  Else
    buffer = "Format ERROR: Can't read CCD format."
    vbGetDetector = LOCALERROR
  End If
  PrintStatusMsg (buffer)
End Function

Function vbGetStatus()
'***************************************************************
'Interrogates AndorMCD to determine if acquisition is complete
'***************************************************************
  Dim status1 As Long
  Dim status2 As Long
  Dim status3 As Long
  vbGetStatus = Not LOCALERROR
  test = GetStatus(status1)
  If (test <> DRV_SUCCESS) Then
    vbGetStatus = LOCALERROR
    buffer = "Data ERROR: Can't get current status of drivers."
    PrintStatusMsg (buffer)
  End If
  If (status1 = DRV_IDLE) Then
    If (LoadData() = LOCALERROR) Then
      PrintStatusMsg ("ERROR: Can't load in data.")
    End If
    StartTimer = XOFF
  Else
    vbGetStatus = LOCALERROR
  End If
End Function

Function vbGetTimings()
'****************************************************************
'Get actual Exposure time used by AndorMCD.  AndorMCD
'defaults to a minimum default exposure time should you attempt
'to enter too low a value, therefore need to retrieve the actual
'value used.
'****************************************************************
  vbGetTimings = Not LOCALERROR
  Dim exposure As Single
  Dim accumTime As Single
  Dim kineticTime As Single
  test = GetAcquisitionTimings(exposure, accumTime, kineticTime)
  If (test <> DRV_SUCCESS) Then
    vbGetTimings = LOCALERROR
    buf = "Timings ERROR: Can't get timings."
  Else
    buf = "**Actual Exposure Time = " & Str(exposure) & " secs"
  End If
  ebStatusBox.text = buf
End Function

Function vbInitialize()
'**************************************************************
' Initializes the AndorMCD system.  Need the files "Detector.ini
' and "pci_29k.cof" in YOUR current working directory.
'
' NOTE: The A/D converter in the AndorMCD card takes ~ 2 secs
' to autocalibrate, thus the initializing procedure lasts ~ 2secs.
'**************************************************************
  vbInitialize = Not LOCALERROR
  test = Initialize("")
  If (test <> DRV_SUCCESS) Then
    buffer = "Initialize ERROR: "
    vbInitialize = LOCALERROR
    Select Case (test)
      Case DRV_INIERROR
        buffer = buffer & "Unable to load 'Detector.ini'."
      Case DRV_COFERROR
        buffer = buffer & "Unable to load 'pci_29k.cof'."
      Case DRV_VXDNOTLOADED
        buffer = buffer & "VxD not loaded"
      Case DRV_ERROR_ACK
        buffer = buffer & "Unable to communicate with card."
      Case Else
        buffer = buffer & "Unknown Initialize error."
    End Select
  Else
    buffer = "Initializing AndorMCD system"
  End If
  PrintStatusMsg (buffer)
End Function

Function vbSetAcquisition()
'**************************************************************
' Configure InstaSpec to operate in Frame transfer mode.
'**************************************************************
  vbSetAcquisition = Not LOCALERROR
  test = SetAcquisitionMode(6)      'Frame transfer
  If test = DRV_SUCCESS Then
    buffer = "Set Acquisition Mode to Frame transfer"
  Else
    vbSetAcquisition = LOCALERROR
    buffer = "Acquisition mode ERROR: "
    Select Case (test)
      Case DRV_INVALID
        buffer = buffer & "Invalid acquisition mode"
      Case DRV_ACQUIRING
        buffer = buffer & "Acquisition in progress."
      Case Else
        buffer = buffer & "Unknown Acquisition error."
    End Select
  End If
  PrintStatusMsg (buffer)
End Function

Function vbSetExposureTime()
'**************************************************************
' Configure AndorMCD with user's exposure time.
'
' AndorMCD defaults to a minimum exposure time should you
' attempt to enter too low a value, therefore need to retrieve
' actual value used, as in GetTimings().
'**************************************************************
  vbSetExposureTime = Not LOCALERROR
  
  buffer = ebExposureTime.text
  exposure = Val(buffer)
  test = SetExposureTime(exposure)
  If (test <> DRV_SUCCESS) Then
    vbSetExposureTime = LOCALERROR
    buffer = "Exposure time ERROR:"
    Select Case (test)
      Case DRV_NOT_INITIALIZED
        buffer = buffer & " AndorMCD system isn't initialized."
      Case DRV_ACQUIRING
        buffer = buffer & " Exposure time Warning" & newLine
        buffer = buffer & "AndorMCD is currently acquiring data"
      Case DRV_ERROR_ACK
        buffer = buffer & " Exposure time not accepted"
      Case Else
        buffer = buffer & "Unknown Exposure Time Error."
    End Select
    PrintStatusMsg (buffer)
  End If
End Function

Function vbSetNumber()
  vbSetNumber = Not LOCALERROR
  
  buffer = ebNumber.text
  nNumber = Val(buffer)
  test = SetNumberKinetics(nNumber)
  If (test <> DRV_SUCCESS) Then
    vbSetNumber = LOCALERROR
    buffer = "Number in series ERROR:"
    Select Case (test)
      Case DRV_NOT_INITIALIZED
        buffer = buffer & " AndorMCD system isn't initialized."
      Case DRV_ACQUIRING
        buffer = buffer & " Number in series Warning" & newLine
        buffer = buffer & "AndorMCD is currently acquiring data"
      Case DRV_ERROR_ACK
        buffer = buffer & " Number in series not accepted"
      Case Else
        buffer = buffer & "Unknown number in series Error."
    End Select
    PrintStatusMsg (buffer)
  End If
End Function

Function vbSetNumberAccum()
  vbSetNumberAccum = Not LOCALERROR
  
  nNumber = 1
  test = SetNumberAccumulations(nNumber)
  If (test <> DRV_SUCCESS) Then
    vbSetNumberAccum = LOCALERROR
    buffer = "Number in accumulation ERROR:"
    Select Case (test)
      Case DRV_NOT_INITIALIZED
        buffer = buffer & " AndorMCD system isn't initialized."
      Case DRV_ACQUIRING
        buffer = buffer & " Number in accumulation Warning" & newLine
        buffer = buffer & "AndorMCD is currently acquiring data"
      Case DRV_ERROR_ACK
        buffer = buffer & " Number in accumulation not accepted"
      Case Else
        buffer = buffer & "Unknown number in accumulation Error."
    End Select
    PrintStatusMsg (buffer)
  End If
End Function

Function vbSetReadout()
'**************************************************************
' Configure AndorMCD to Full Resolution Image.
'**************************************************************
  vbSetReadout = Not LOCALERROR
  test = SetReadMode(4)              'Full Image
  If test = DRV_SUCCESS Then
    buffer = "Set Readout Mode to Full Resolution Image"
  Else
    vbSetReadout = LOCALERROR
    buffer = "Readout mode ERROR: "
    Select Case (test)
      Case DRV_P1INVALID
        buffer = buffer & "Invalid readout mode."
      Case DRV_ERROR_ACK
        buffer = buffer & "Unable to communicate with card."
      Case Else
        buffer = buffer & "Unknown readout mode error"
    End Select
  End If
  PrintStatusMsg (buffer)
End Function

Function vbSetShutter()
'*****************************************************************
'Configure shutter in auto mode (shutter opens for
'the period "Exposure Time" defined by the user).
'MUST also incorporate the "Time to open shutter"
'(which defines the finite time period to fully open
'the shutter) and "shutter opens on HIGH or LOW TTL "
'pulse.
'*****************************************************************

  vbSetShutter = Not LOCALERROR
  index = cbShutterTTL.ListIndex
  If (index <> 0 And index <> 1) Then
    index = 0       'default = TTL Low
  End If
  OpenTime = Val(ebShutterTime.text)
  ShutterType = 0
  test = SetShutter(index, ShutterType, OpenTime, OpenTime)
  If (test <> DRV_SUCCESS) Then
    buffer = "Shutter ERROR: "
    vbSetShutter = LOCALERROR
    Select Case (test)
      Case P1INVALID
        buffer = buffer & "Invalid type. "
      Case P2INVALID
        buffer = buffer & "Invalid mode"
      Case P3INVALID
        buffer = buffer & "Invalid closing time"
      Case P4INVALID
        buffer = buffer & "Invalid opening time"
      Case Else
        buffer = buffer & "Unknown error"
    End Select
  Else
    buffer = "Shutter properly configured."
  End If
  PrintStatusMsg (buffer)
End Function

Function vbSetTimings()
'**************************************************************
' MUST set exposure time before using the driver call
' "GetAcquisitionTimings()" which retrieves the actual timings
' calculated by AndorMCD.
'
' See comments at top of vbSetExposureTime() function.
'**************************************************************
  vbSetTimings = Not LOCALERROR
  If (vbSetExposureTime() = LOCALERROR) Then
    vbSetTimings = LOCALERROR
    Exit Function
  End If
End Function

Function vbSetTrigger()
'************************************************************************
'Tells AndorMCD the type of trigger pulse to expect.  Internal means
'the computer generates its own trigger and External means the user is
'generating his/her own trigger pulse.
'************************************************************************

  vbSetTrigger = Not LOCALERROR
  index = cbTrigger.ListIndex
  If (index <> 0 And index <> 1) Then
    index = 0       'default = Internal
  End If
  test = SetTriggerMode(index)
  If test = DRV_SUCCESS Then
    Select Case (index)
      Case 0
        buffer = "Set Trigger Mode to Internal"
      Case 1
        buffer = "Set Trigger Mode to External" & newLine
        buffer = buffer & "Note: You must supply the External Trigger!"
    End Select
  Else
    vbSetTrigger = LOCALERROR
    buffer = "Trigger mode ERROR: "
    Select Case (test)
      Case DRV_ERROR_ACK
        buffer = buffer & newLine & "Unable to communicate with card"
      Case DRV_P1INVALID
        buffer = buffer & newLine
        buffer = buffer & "Trigger mode invalid"
    End Select
  End If
  PrintStatusMsg (buffer)
End Function

Function vbSetImage()
'**************************************************************
' MUST call SetImage before calling StartAcquisition
'**************************************************************
  vbSetImage = Not LOCALERROR
  test = SetImage(1, 1, 1, naXPixels, 1, naYPixels)
  If (test <> DRV_SUCCESS) Then
    vbSetImage = LOCALERROR
    buffer = "SetImage ERROR:"
    Select Case (test)
      Case DRV_NOT_INITIALIZED
        buffer = buffer & " InstaSpec system isn't initialized."
      Case DRV_ACQUIRING
        buffer = buffer & " Exposure time Warning" & newLine
        buffer = buffer & " InstaSpec is currently acquiring data"
      Case DRV_P1INVALID
        buffer = buffer & " Binning parameters invalid"
      Case DRV_P2INVALID
        buffer = buffer & " Binning parameters invalid"
      Case DRV_P3INVALID
        buffer = buffer & " Sub-area co-ordinate is invalid"
      Case DRV_P4INVALID
        buffer = buffer & " Sub-area co-ordinate is invalid"
      Case DRV_P5INVALID
        buffer = buffer & " Sub-area co-ordinate is invalid"
      Case DRV_P6INVALID
        buffer = buffer & " Sub-area co-ordinate is invalid"
      Case Else
        buffer = buffer & " Unknown SetImage Error."
    End Select
    PrintStatusMsg (buffer)
  End If
End Function

Function vbStartAcq()
'**************************************************************
' Tells AndorMCD to begin Acquisition upon receipt of a trigger
' pulse (either Internal or External.
'**************************************************************
  vbStartAcq = Not LOCALERROR
  test = StartAcquisition()
  If (test <> DRV_SUCCESS) Then
    buffer = "Acquisition ERROR: "
    vbStartAcq = LOCALERROR
    Select Case (test)
      Case DRV_VXDNOTINSTALLED
        buffer = " VxD not loaded."
      Case DRV_INIERROR
        buffer = "Error reading 'Detector.ini'."
      Case DRV_ACQERROR
        buffer = "Acquisition Settings invalid."
      Case DRV_ERROR_ACK
        buffer = "Can't communicate with card."
      Case Else
        buffer = "Unknown Acquisition Error."
    End Select
  Else
    buffer = "Starting acquisition..."
  End If
  PrintStatusMsg (buffer)
End Function


Function LoadData()
'**************************************************************
' After IMAGEGetStatus() confirms the data acquisition is
' COMPLETE then LoadData() gets the data from the AndorMCD
' drivers and sends it to the graph plotting routine.
'
'Visual Basic 3.0 has a limitation in the the number of elements
'it can store in an array: ie 65536 elements (which = one
'dimension). But it can store up to a maximum of 60 such
'dimensions so for a CCD sensor of format 1024x256 pixels
'(=262144 elements) its possible to create a 2D array to store
'the data.
'
'For the CCD sensor example above a 2D array of size 1024 x 256
'would easily meet the Visual Basic constraints.

'**************************************************************
  LoadData = Not LOCALERROR
  
  nNumber = Val(ebNumber.text)
  Dim nElements As Long
  nElements = naXPixels * naYPixels * nNumber
  ReDim bData(1 To nElements)
  test = GetAcquiredData(bData(1), nElements)
  
  If test = DRV_P2INVALID Then
    buffer = "ERROR: aData size is incorrect"
    LoadData = LOCALERROR
    PrintStatusMsg (buffer)
    Exit Function
  End If
  PrintStatusMsg ("Acquired data!")
  PlotData
End Function

Sub pbAbortAcq_Click(index As Integer)
'**************************************************************
'  Response function for "Abort Acq" button.  Switches OFF the
'  timer flag if appropriate and tells AndorMCD to abort
'  acquisition.
'**************************************************************
  If (StartTimer = XON) Then
    StartTimer = XOFF
  End If
  If (vbAbortAcq() = LOCALERROR) Then
    Exit Sub
  End If
End Sub

Sub pbClose_Click(index As Integer)
'**************************************************************
' Closes down the Image application
'**************************************************************
  test = ShutDown()
  If (test <> DRV_SUCCESS) Then
    PrintStatusMsg ("ERROR: Can't close AndorMCD system down properly")
    Exit Sub
  End If
  End
End Sub


Sub pbStartAcq_Click(index As Integer)
'*************************************************************************************
'This routine is the heart of the Image application.  It configures the AndorMCD
'system with the user's choices and tells it to begin the acquisition upon arrival
'of a trigger pulse (may be Internal or External).  NB if you choose External
'triggering then YOU must supply the trigger pulse to the AndorMCD system.

'The computer is programmed to monitor the state of the acquisition every (eg) 100
'millisecs: this ensures the acquisition is complete before reading in the data.
'Thus every 100 ms the computer is directed to the Timer procedure and hence to
'vbGetStatus().

'After successfully acquiring the data the time "flag" (ie StartTimer) is switched
'off in readiness for a new scan.
'**************************************************************************************
  If (StartTimer = XON) Then
    PrintStatusMsg ("Warning: Already acquiring data...")
    Exit Sub
  End If
  If (StartTimer = XOFF) Then
    If (vbSetTimings() = LOCALERROR) Then
      Exit Sub
    End If
    If (vbSetNumber() = LOCALERROR) Then
      Exit Sub
    End If
    If (vbSetNumberAccum() = LOCALERROR) Then
      Exit Sub
    End If
    If (vbGetTimings() = LOCALERROR) Then
      Exit Sub
    End If
    If (vbSetTrigger() = LOCALERROR) Then
      Exit Sub
    End If
    If (vbSetImage() = LOCALERROR) Then
      Exit Sub
    End If
    If (vbSetShutter() = LOCALERROR) Then
      Exit Sub
    End If
    If (vbStartAcq() = LOCALERROR) Then
      Exit Sub
    Else
      StartTimer = XON 'Switch ON flag to begin monitoring acquisition
    End If
  End If
End Sub

Sub PlotData()
'**************************************************************
' Configures the graph display, finds max and min data values
' and plots the scan data to screen.
'**************************************************************
  Dim aYScale As Double
  Dim bYScale As Double
  Dim cYScale As Double
  Dim b As Long
  Dim min As Long
  Dim max As Long

  min = 1
  max = 255
  
  index = Val(ebCCDScan.text)
  GetCCDData (index)
  
  aMinY = aData(280, 144)
  aMaxY = aData(280, 144)
  
  For i = 5 To naXPixels - 5
    For j = 5 To naYPixels - 5
      If (aData(i, j) >= aMaxY) Then aMaxY = aData(i, j)
      If (aData(i, j) <= aMinY) Then aMinY = aData(i, j)
    Next
  Next
  If (aMaxY = aMinY) Then aMaxY = aMaxY + 1
  aYScale = CDbl(max - min) / CDbl(aMaxY - aMinY)
  
  For i = 1 To naXPixels
    For j = 1 To naYPixels
      aData(i, j) = min + aYScale * (aData(i, j) - aMinY)
    Next
  Next
  
  For i = 0 To Picture2.ScaleWidth
    For j = 0 To Picture2.ScaleHeight
      b = aData(CLng(i * (naXPixels - 1) / Picture2.ScaleWidth + 1), CLng(j * (naYPixels - 1) / Picture2.ScaleHeight + 1))
      c0& = b + 256 * (b + (256 * b))
      Picture2.PSet (i, j), c0&
    Next
  Next
End Sub

Sub PrintStatusMsg(buffer As String)
'**************************************************************
' Updates the StatusBox with messages corresponding to the
' application flow.
'**************************************************************
  buf = buf & newLine & buffer
  ebStatusBox.text = buf
End Sub

Private Sub pbUpdate_Click()
  PlotData
End Sub

Sub Timer1_Timer()
'**************************************************************
' Response function to application timer.  Every (eg) 100 ms
' the computer is directed to this function which in turn
' monitors the acquisition status.
'**************************************************************
  If (StartTimer = XON) Then
    If (vbGetStatus() = LOCALERROR) Then
    End If
  End If
End Sub
Sub GetCCDData(index As Long)
  ReDim aData(1 To naXPixels, 1 To naYPixels)
  start = (index - 1) * naXPixels * naYPixels
  For i = 1 To naXPixels
    For j = 1 To naYPixels
      aData(i, j) = bData(start + i + (j - 1) * naXPixels)
    Next j
  Next i
End Sub

Private Sub ebCCDScan_Change()
'********************************************************************
'   Prevents user from accidentally entering an erroneous value
'********************************************************************
  index = Val(ebCCDScan.text)
  nNumber = Val(ebNumber.text)
  If (index < 1 Or index > nNumber) Then
    ebCCDScan.text = Str(1)
  End If
End Sub

Private Sub ebNumber_Change()
  index = Val(ebCCDScan.text)
  nNumber = Val(ebNumber.text)
  If (index < 1 Or index > nNumber) Then
    ebCCDScan.text = Str(1)
  End If
End Sub

