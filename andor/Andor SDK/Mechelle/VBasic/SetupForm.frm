VERSION 5.00
Begin VB.Form SetupForm 
   Caption         =   "Setup"
   ClientHeight    =   4050
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   6870
   LinkTopic       =   "Form2"
   ScaleHeight     =   4050
   ScaleWidth      =   6870
   StartUpPosition =   3  'Windows Default
   Begin VB.TextBox txtSpectrumFile 
      Height          =   375
      Left            =   120
      TabIndex        =   7
      Text            =   "C:\Program Files\Andor iStar\Drivers\Examples\VBasic\spectrum.txt"
      Top             =   2520
      Width           =   6615
   End
   Begin VB.TextBox txtXmlFile 
      Height          =   375
      Left            =   120
      TabIndex        =   6
      Text            =   "C:\Program Files\Andor iStar\Mechelle\Mechelle 5000\Mechelle5000.xml"
      Top             =   1200
      Width           =   6615
   End
   Begin VB.TextBox StatusText 
      Height          =   375
      Left            =   2040
      TabIndex        =   4
      Text            =   "Text1"
      Top             =   120
      Width           =   3975
   End
   Begin VB.CommandButton CancelButton 
      Caption         =   "Close"
      Height          =   375
      Left            =   3600
      TabIndex        =   3
      Top             =   3240
      Width           =   1215
   End
   Begin VB.CommandButton OkButton 
      Caption         =   "Apply"
      Height          =   375
      Left            =   1800
      TabIndex        =   2
      Top             =   3240
      Width           =   1215
   End
   Begin VB.Label Label3 
      BackColor       =   &H00808000&
      Caption         =   "Status"
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
      Left            =   720
      TabIndex        =   5
      Top             =   120
      Width           =   855
   End
   Begin VB.Label Label2 
      BackColor       =   &H00808000&
      Caption         =   "Spectrum File Name"
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
      TabIndex        =   1
      Top             =   2160
      Width           =   2415
   End
   Begin VB.Label Label1 
      BackColor       =   &H00808000&
      Caption         =   "&XML file"
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
      TabIndex        =   0
      Top             =   840
      Width           =   855
   End
End
Attribute VB_Name = "SetupForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub CancelButton_Click()
Unload Me
End Sub



Private Sub Form_Load()
  szExecutable = App.path
If bMechelleInitialized = False Then
  StatusText.text = "Mechelle Not Initialized"
Else
  StatusText.text = "Mechelle Initialized"
End If

txtXmlFile.text = szMechInitDir
txtSpectrumFile.text = szSpectrumSaveFileName


End Sub


Private Sub OkButton_Click()
 If bMechelleInitialized = True Then
    StatusText.text = "Mechelle Already Initialized"
    Exit Sub
 End If
  
 

 ErrorString = MechelleInit(nXPixels, nYPixels, txtXmlFile.text, iMaxArraySize)
 buffer = "Status :" & ErrorString
 bMechelleInitialized = True
 
 If (ErrorString <> MECHELLE_SUCCESS) Then
   bMechelleInitialized = False
   StatusText.text = "Mechelle init ERROR " + buffer
 Else
   StatusText.text = "Mechelle init SUCCESS " + buffer
 End If
 
 szMechInitDir = txtXmlFile.text
 
 szSpectrumSaveFileName = txtSpectrumFile.text
 

End Sub

Private Sub XMLdir_Change()

End Sub

Private Sub XMLfile_Click()

End Sub
