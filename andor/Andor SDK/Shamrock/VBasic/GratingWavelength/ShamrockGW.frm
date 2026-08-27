VERSION 5.00
Begin VB.Form ini 
   BackColor       =   &H00808000&
   Caption         =   "Shamrock Visual Basic Example"
   ClientHeight    =   7335
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   9390
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
   ScaleHeight     =   489
   ScaleMode       =   3  'Pixel
   ScaleWidth      =   626
   Begin VB.PictureBox bmpShamrock 
      Height          =   2295
      Left            =   120
      Negotiate       =   -1  'True
      Picture         =   "ShamrockGW.frx":0000
      ScaleHeight     =   4500
      ScaleMode       =   0  'User
      ScaleWidth      =   8000
      TabIndex        =   53
      Top             =   1200
      Width           =   3975
   End
   Begin VB.Frame frGratings 
      BackColor       =   &H00808000&
      Caption         =   "Gratings"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6375
      Left            =   6360
      TabIndex        =   44
      Top             =   120
      Width           =   2895
      Begin VB.TextBox ebSetDetectorOffset 
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
         Left            =   1920
         TabIndex        =   25
         Top             =   5400
         Width           =   850
      End
      Begin VB.CommandButton pbSetDetectorOffset 
         Caption         =   "Set detector offset"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   345
         Left            =   120
         TabIndex        =   24
         Top             =   5400
         Width           =   1575
      End
      Begin VB.TextBox ebSetGratingOffset 
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
         Left            =   1920
         TabIndex        =   23
         Top             =   4920
         Width           =   850
      End
      Begin VB.CommandButton pbSetGratingOffset 
         Caption         =   "Set grating offset"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   345
         Left            =   120
         TabIndex        =   22
         Top             =   4920
         Width           =   1575
      End
      Begin VB.TextBox ebSetGrating 
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
         Left            =   1920
         TabIndex        =   21
         Top             =   4440
         Width           =   850
      End
      Begin VB.CommandButton pbSetGrating 
         Caption         =   "Set grating"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   345
         Left            =   120
         TabIndex        =   20
         Top             =   4440
         Width           =   1575
      End
      Begin VB.TextBox ebDetectorOffset 
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
         Left            =   1920
         Locked          =   -1  'True
         TabIndex        =   17
         Top             =   3540
         Width           =   850
      End
      Begin VB.Frame frGratingInfo 
         BackColor       =   &H00808000&
         Caption         =   "Grating Information"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   1935
         Left            =   120
         TabIndex        =   48
         Top             =   1440
         Width           =   2655
         Begin VB.TextBox ebGratingOffset 
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
            Left            =   1560
            Locked          =   -1  'True
            TabIndex        =   16
            Top             =   1440
            Width           =   850
         End
         Begin VB.TextBox ebLines 
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
            Left            =   1560
            Locked          =   -1  'True
            TabIndex        =   13
            Top             =   360
            Width           =   850
         End
         Begin VB.TextBox ebBlaze 
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
            Left            =   1560
            Locked          =   -1  'True
            TabIndex        =   14
            Top             =   720
            Width           =   850
         End
         Begin VB.TextBox ebHome 
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
            Left            =   1560
            Locked          =   -1  'True
            TabIndex        =   15
            Top             =   1080
            Width           =   850
         End
         Begin VB.Label stGratingOffset 
            BackColor       =   &H00808000&
            Caption         =   "Offset (steps)"
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
            TabIndex        =   52
            Top             =   1500
            Width           =   1185
         End
         Begin VB.Label stLines 
            BackColor       =   &H00808000&
            Caption         =   "Lines/mm"
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
            TabIndex        =   51
            Top             =   420
            Width           =   1185
         End
         Begin VB.Label stBlaze 
            BackColor       =   &H00808000&
            Caption         =   "Blaze (nm)"
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
            TabIndex        =   50
            Top             =   780
            Width           =   1185
         End
         Begin VB.Label stHome 
            BackColor       =   &H00808000&
            Caption         =   "Home (steps)"
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
            TabIndex        =   49
            Top             =   1140
            Width           =   1185
         End
      End
      Begin VB.TextBox ebTurretSettings 
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
         Left            =   1920
         Locked          =   -1  'True
         TabIndex        =   10
         Top             =   300
         Width           =   850
      End
      Begin VB.TextBox ebNoGratings 
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
         Left            =   1920
         Locked          =   -1  'True
         TabIndex        =   11
         Top             =   660
         Width           =   850
      End
      Begin VB.TextBox ebCurrentGrating 
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
         Left            =   1920
         Locked          =   -1  'True
         TabIndex        =   12
         Top             =   1020
         Width           =   850
      End
      Begin VB.CommandButton pbSetTurret 
         Caption         =   "Set turret"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   345
         Left            =   120
         TabIndex        =   18
         Top             =   3960
         Width           =   1575
      End
      Begin VB.TextBox ebSetTurret 
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
         Left            =   1920
         TabIndex        =   19
         Top             =   3960
         Width           =   850
      End
      Begin VB.CommandButton pbResetWl 
         Caption         =   "Reset wavelength"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   345
         Left            =   120
         TabIndex        =   26
         Top             =   5880
         Width           =   2655
      End
      Begin VB.Label stDetectorOffset 
         BackColor       =   &H00808000&
         Caption         =   "Detector Offset"
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
         TabIndex        =   54
         Top             =   3600
         Width           =   1785
      End
      Begin VB.Label stTurretSettings 
         BackColor       =   &H00808000&
         Caption         =   "Turret Settings"
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
         TabIndex        =   47
         Top             =   360
         Width           =   1785
      End
      Begin VB.Label stNoGratings 
         BackColor       =   &H00808000&
         Caption         =   "Number of Gratings"
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
         TabIndex        =   46
         Top             =   720
         Width           =   1785
      End
      Begin VB.Label stCurrentGrating 
         BackColor       =   &H00808000&
         Caption         =   "Current Grating"
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
         TabIndex        =   45
         Top             =   1080
         Width           =   1785
      End
   End
   Begin VB.Frame frWavelength 
      BackColor       =   &H00808000&
      Caption         =   "Wavelength (nm)"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   2415
      Left            =   3240
      TabIndex        =   40
      Top             =   4560
      Width           =   2895
      Begin VB.CommandButton pbGotoZeroOrder 
         Caption         =   "Goto zero order"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   345
         Left            =   120
         TabIndex        =   32
         Top             =   1920
         Width           =   2655
      End
      Begin VB.TextBox ebGotoWl 
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
         Left            =   1920
         TabIndex        =   31
         Top             =   1440
         Width           =   850
      End
      Begin VB.CommandButton pbGotoWl 
         Caption         =   "Goto wavelength"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   345
         Left            =   120
         TabIndex        =   30
         Top             =   1440
         Width           =   1575
      End
      Begin VB.TextBox ebMaxWl 
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
         Left            =   1920
         Locked          =   -1  'True
         TabIndex        =   29
         Top             =   1020
         Width           =   850
      End
      Begin VB.TextBox ebMinWl 
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
         Left            =   1920
         Locked          =   -1  'True
         TabIndex        =   28
         Top             =   660
         Width           =   850
      End
      Begin VB.TextBox ebCurrentWl 
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
         Left            =   1920
         Locked          =   -1  'True
         TabIndex        =   27
         Top             =   300
         Width           =   850
      End
      Begin VB.Label stMaxWl 
         BackColor       =   &H00808000&
         Caption         =   "Max Wavelength"
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
         TabIndex        =   43
         Top             =   1080
         Width           =   1785
      End
      Begin VB.Label stMinWl 
         BackColor       =   &H00808000&
         Caption         =   "Min Wavelength"
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
         TabIndex        =   42
         Top             =   720
         Width           =   1785
      End
      Begin VB.Label stCurrentWl 
         BackColor       =   &H00808000&
         Caption         =   "Current Wavelength"
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
         TabIndex        =   41
         Top             =   360
         Width           =   1785
      End
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
      Left            =   7680
      TabIndex        =   33
      Top             =   6720
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
      Picture         =   "ShamrockGW.frx":1DBFE
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
      TabIndex        =   35
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
         TabIndex        =   38
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
         TabIndex        =   37
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
         TabIndex        =   36
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
      TabIndex        =   39
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
      TabIndex        =   34
      Top             =   120
      Width           =   1800
   End
End
Attribute VB_Name = "ini"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'This application is a basic example of how to build an
'interface using the SDK to operate one or more Shamrocks.
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

Private Sub pbSetTurret_Click()
  ReturnValue = ShamrockSetTurret(device, Val(ebSetTurret.text))
  EvaluateAction ("Set Turret")
  startgratings
End Sub

Private Sub pbSetGrating_Click()
  ReturnValue = ShamrockSetGrating(device, Val(ebSetGrating.text))
  EvaluateAction ("Set Grating")
  startgratings
End Sub

Private Sub pbSetGratingOffset_Click()
  ReturnValue = ShamrockSetGratingOffset(device, Grating, Val(ebSetGratingOffset.text))
  EvaluateAction ("Set Grating Offset")
  startgratings
End Sub

Private Sub pbSetDetectorOffset_Click()
  ReturnValue = ShamrockSetDetectorOffset(device, Val(ebSetDetectorOffset.text))
  EvaluateAction ("Set Detector Offset")
  startgratings
End Sub

Private Sub pbResetWl_Click()
  ReturnValue = ShamrockWavelengthReset(device)
  EvaluateAction ("Reset Wavelength")
  startgratings
End Sub

Private Sub pbGotoWl_Click()
  ReturnValue = ShamrockSetWavelength(device, Val(ebGotoWl.text))
  EvaluateAction ("Set Wavelength")
  startwavelength
End Sub

Private Sub pbGotoZeroOrder_Click()
  ReturnValue = ShamrockGotoZeroOrder(device)
  EvaluateAction ("Goto Zero Order")
  startwavelength
End Sub
