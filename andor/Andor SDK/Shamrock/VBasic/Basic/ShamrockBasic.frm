VERSION 5.00
Begin VB.Form ini 
   BackColor       =   &H00808000&
   Caption         =   "Shamrock Visual Basic Example"
   ClientHeight    =   5175
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   6375
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
   ScaleHeight     =   345
   ScaleMode       =   3  'Pixel
   ScaleWidth      =   425
   Begin VB.PictureBox bmpShamrock 
      Height          =   2295
      Left            =   120
      Negotiate       =   -1  'True
      Picture         =   "ShamrockBasic.frx":0000
      ScaleHeight     =   4500
      ScaleMode       =   0  'User
      ScaleWidth      =   8000
      TabIndex        =   17
      Top             =   1200
      Width           =   3975
   End
   Begin VB.TextBox ebSerialNumber 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   285
      Left            =   4320
      Locked          =   -1  'True
      TabIndex        =   6
      Top             =   1080
      Width           =   1740
   End
   Begin VB.ComboBox cbDevice 
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
      Left            =   4320
      TabIndex        =   5
      Text            =   "Choose Shamrock"
      Top             =   360
      Width           =   1785
   End
   Begin VB.CommandButton pbCloseControls 
      Caption         =   "&Close Controls"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   4440
      TabIndex        =   10
      Top             =   4440
      Width           =   1575
   End
   Begin VB.CommandButton pbOpenControls 
      Caption         =   "&Open Controls"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   1320
      TabIndex        =   3
      Top             =   3600
      Width           =   1575
   End
   Begin VB.CommandButton pbInitialize 
      Caption         =   "&Initialize"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   120
      TabIndex        =   2
      Top             =   3600
      Width           =   975
   End
   Begin VB.CommandButton pbExit 
      Caption         =   "&Exit"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   3120
      TabIndex        =   4
      Top             =   3600
      Width           =   975
   End
   Begin VB.PictureBox Picture 
      BackColor       =   &H80000005&
      Height          =   1005
      Left            =   120
      Picture         =   "ShamrockBasic.frx":1DBFE
      ScaleHeight     =   63
      ScaleMode       =   3  'Pixel
      ScaleWidth      =   261
      TabIndex        =   0
      TabStop         =   0   'False
      Top             =   120
      Width           =   3975
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
      Height          =   2295
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   1
      TabStop         =   0   'False
      Top             =   1200
      Width           =   3975
   End
   Begin VB.Frame frOpticalParams 
      BackColor       =   &H00808000&
      Caption         =   "Optical Parameters"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   2535
      Left            =   4320
      TabIndex        =   12
      Top             =   1560
      Width           =   1815
      Begin VB.TextBox ebFocalLength 
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   120
         Locked          =   -1  'True
         TabIndex        =   7
         Top             =   600
         Width           =   1620
      End
      Begin VB.TextBox ebAngularDev 
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   120
         Locked          =   -1  'True
         TabIndex        =   8
         Top             =   1320
         Width           =   1620
      End
      Begin VB.TextBox ebFocalTilt 
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   120
         Locked          =   -1  'True
         TabIndex        =   9
         Top             =   2040
         Width           =   1620
      End
      Begin VB.Label stFocalLength 
         BackColor       =   &H00808000&
         Caption         =   "Focal Length"
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
         TabIndex        =   15
         Top             =   360
         Width           =   1620
      End
      Begin VB.Label stAngularDev 
         BackColor       =   &H00808000&
         Caption         =   "Angular Deviation"
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
         Top             =   1080
         Width           =   1620
      End
      Begin VB.Label stFocalTilt 
         BackColor       =   &H00808000&
         Caption         =   "Focal Tilt"
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
         TabIndex        =   13
         Top             =   1800
         Width           =   1620
      End
   End
   Begin VB.Label stSerialNumber 
      BackColor       =   &H00808000&
      Caption         =   "Serial Number"
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
      Left            =   4320
      TabIndex        =   16
      Top             =   840
      Width           =   1620
   End
   Begin VB.Label stDevice 
      BackColor       =   &H00808000&
      Caption         =   "Current Shamrock"
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
      Left            =   4320
      TabIndex        =   11
      Top             =   120
      Width           =   1800
   End
End
Attribute VB_Name = "ini"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'This application is a basic example of how to use the SDK to
'create an interface to operate one or more Shamrocks.
'
'NB The dimensions of the Windows interface were devised for
'a Windows monitor with 1024x768 pixels.  The application will
'work with other configurations (eg SVGA 640x480) but may
'appear large.
'

Sub Form_Load()
'**************************************************************
' Initializing routine called before the Window interface
' is displayed
'**************************************************************
  IsIni = 0
  TextLineCounter = 0
  device = -1
  newLine = Chr(13) & Chr(10)
  bmpShamrock.Visible = True
  ebStatusBox.Visible = False
  InitializeAccessoriesPresence
  ShowControls (False)
  pbOpenControls.Enabled = False
End Sub

Private Sub pbInitialize_Click()
'**************************************************************
' Initialize Shamrock driver and locates any available Shamrock
'**************************************************************
  If IsIni <> 0 Then
    PrintStatusMsg ("Shamrock driver already initialized")
    Exit Sub
  Else
    bmpShamrock.Visible = False
    ebStatusBox.Visible = True
  End If
    
  PrintStatusMsg ("Initializing ...")
  ReturnValue = ShamrockInitialize("")
  If ReturnValue = SHAMROCK_SUCCESS Then
    PrintStatusMsg ("Locating available Shamrocks ...")
    ReturnValue = ShamrockGetNumberDevices(noDevices)
  Else
    PrintStatusMsg ("ERROR: Can't initialize")
    Exit Sub
  End If
  
  If ReturnValue = SHAMROCK_SUCCESS Then
    Select Case (noDevices)
      Case 0
        PrintStatusMsg ("ERROR: No available Shamrock found")
        Exit Sub
      Case 1
        PrintStatusMsg ("1 Shamrock found")
      Case Else
        temp = Str(noDevices) & " Shamrocks found"
        PrintStatusMsg (temp)
    End Select
  Else
    temp = "ERROR: ShamrockGetNumberDevices returns " & Str(ReturnValue)
    PrintStatusMsg (temp)
    Exit Sub
  End If
  
  For i = 1 To noDevices
    temp = "# " & Str(i)
    cbDevice.AddItem temp
  Next i
    
  pbOpenControls.Enabled = True
  IsIni = 1
End Sub

Private Sub pbOpenControls_Click()
'**************************************************************
' Opens Shamrock controls
'**************************************************************
  ShowControls (True)
End Sub

Private Sub cbDevice_Click()
  GetShamrockInfo
End Sub

Private Sub pbCloseControls_Click()
'**************************************************************
' Closes Shamrock controls
'**************************************************************
  ShowControls (False)

End Sub

Private Sub pbExit_Click()
'**************************************************************
' Closes down this example
'**************************************************************
  ReturnValue = ShamrockClose()
  If (ReturnValue <> SHAMROCK_SUCCESS) Then
    PrintStatusMsg ("ERROR: Can't shut the system down properly")
    Exit Sub
  End If
  End
End Sub

Sub PrintStatusMsg(buffer As String)
'**************************************************************
' Updates the StatusBox with messages corresponding to the
' application flow. If there are more than 100 lines of messages
' the message box is cleared.
'**************************************************************
  If TextLineCounter > 100 Then
    buf = "..."
    TextLineCounter = 0
  End If
  buf = buf & newLine & buffer
  ebStatusBox.text = buf
  ebStatusBox.SelStart = Len(ebStatusBox.text)
  DoEvents
  TextLineCounter = TextLineCounter + 1
End Sub

