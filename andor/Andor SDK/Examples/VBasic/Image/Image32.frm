VERSION 5.00
Object = "{0842D103-1E19-101B-9AAF-1A1626551E7C}#1.0#0"; "graph32.ocx"
Begin VB.Form Form1 
   BackColor       =   &H00808000&
   Caption         =   "Instaspec Visual Basic Example Drivers:- Image"
   ClientHeight    =   6525
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   8295
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
   ScaleHeight     =   6525
   ScaleWidth      =   8295
   StartUpPosition =   3  'Windows Default
   Begin VB.PictureBox Picture1 
      BackColor       =   &H80000005&
      Height          =   975
      Left            =   120
      Picture         =   "Image32.frx":0000
      ScaleHeight     =   915
      ScaleWidth      =   3915
      TabIndex        =   17
      Top             =   120
      Width           =   3975
   End
   Begin VB.CommandButton pbDisplayRow 
      Caption         =   "&Display Row"
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
      Left            =   6840
      TabIndex        =   8
      Top             =   2640
      Width           =   1212
   End
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
      Height          =   852
      Left            =   4200
      TabIndex        =   15
      Top             =   2400
      Width           =   3975
      Begin VB.TextBox ebCCDRow 
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
         Left            =   1800
         TabIndex        =   7
         Text            =   "1"
         Top             =   360
         Width           =   732
      End
      Begin VB.Label lblDisplayRow 
         BackColor       =   &H00808000&
         Caption         =   "Row of the image to display on the screen"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   8.25
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   570
         Left            =   120
         TabIndex        =   16
         Top             =   120
         Width           =   1695
      End
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
      Top             =   1920
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
      Top             =   2280
      Width           =   1692
   End
   Begin GraphLib.Graph DataDisplay 
      Height          =   3015
      Left            =   120
      TabIndex        =   13
      Top             =   3360
      Width           =   8055
      _Version        =   65536
      _ExtentX        =   14208
      _ExtentY        =   5318
      _StockProps     =   96
      BorderStyle     =   1
      Background      =   7
      DrawStyle       =   0
      GraphStyle      =   4
      GraphType       =   6
      GridStyle       =   3
      LabelEvery      =   100
      NumPoints       =   1024
      PatternedLines  =   1
      RandomData      =   0
      ThickLines      =   0
      TickEvery       =   10
      Ticks           =   0
      YAxisMax        =   1
      YAxisStyle      =   2
      YAxisTicks      =   5
      ColorData       =   0
      ExtraData       =   0
      ExtraData[]     =   1
      FontFamily      =   4
      FontSize        =   4
      FontSize[0]     =   200
      FontSize[1]     =   150
      FontSize[2]     =   100
      FontSize[3]     =   100
      FontStyle       =   4
      GraphData       =   1
      GraphData[]     =   1024
      GraphData[0,0]  =   0
      GraphData[0,1]  =   0
      GraphData[0,2]  =   0
      GraphData[0,3]  =   0
      GraphData[0,4]  =   0
      GraphData[0,5]  =   0
      GraphData[0,6]  =   0
      GraphData[0,7]  =   0
      GraphData[0,8]  =   0
      GraphData[0,9]  =   0
      GraphData[0,10] =   0
      GraphData[0,11] =   0
      GraphData[0,12] =   0
      GraphData[0,13] =   0
      GraphData[0,14] =   0
      GraphData[0,15] =   0
      GraphData[0,16] =   0
      GraphData[0,17] =   0
      GraphData[0,18] =   0
      GraphData[0,19] =   0
      GraphData[0,20] =   0
      GraphData[0,21] =   0
      GraphData[0,22] =   0
      GraphData[0,23] =   0
      GraphData[0,24] =   0
      GraphData[0,25] =   0
      GraphData[0,26] =   0
      GraphData[0,27] =   0
      GraphData[0,28] =   0
      GraphData[0,29] =   0
      GraphData[0,30] =   0
      GraphData[0,31] =   0
      GraphData[0,32] =   0
      GraphData[0,33] =   0
      GraphData[0,34] =   0
      GraphData[0,35] =   0
      GraphData[0,36] =   0
      GraphData[0,37] =   0
      GraphData[0,38] =   0
      GraphData[0,39] =   0
      GraphData[0,40] =   0
      GraphData[0,41] =   0
      GraphData[0,42] =   0
      GraphData[0,43] =   0
      GraphData[0,44] =   0
      GraphData[0,45] =   0
      GraphData[0,46] =   0
      GraphData[0,47] =   0
      GraphData[0,48] =   0
      GraphData[0,49] =   0
      GraphData[0,50] =   0
      GraphData[0,51] =   0
      GraphData[0,52] =   0
      GraphData[0,53] =   0
      GraphData[0,54] =   0
      GraphData[0,55] =   0
      GraphData[0,56] =   0
      GraphData[0,57] =   0
      GraphData[0,58] =   0
      GraphData[0,59] =   0
      GraphData[0,60] =   0
      GraphData[0,61] =   0
      GraphData[0,62] =   0
      GraphData[0,63] =   0
      GraphData[0,64] =   0
      GraphData[0,65] =   0
      GraphData[0,66] =   0
      GraphData[0,67] =   0
      GraphData[0,68] =   0
      GraphData[0,69] =   0
      GraphData[0,70] =   0
      GraphData[0,71] =   0
      GraphData[0,72] =   0
      GraphData[0,73] =   0
      GraphData[0,74] =   0
      GraphData[0,75] =   0
      GraphData[0,76] =   0
      GraphData[0,77] =   0
      GraphData[0,78] =   0
      GraphData[0,79] =   0
      GraphData[0,80] =   0
      GraphData[0,81] =   0
      GraphData[0,82] =   0
      GraphData[0,83] =   0
      GraphData[0,84] =   0
      GraphData[0,85] =   0
      GraphData[0,86] =   0
      GraphData[0,87] =   0
      GraphData[0,88] =   0
      GraphData[0,89] =   0
      GraphData[0,90] =   0
      GraphData[0,91] =   0
      GraphData[0,92] =   0
      GraphData[0,93] =   0
      GraphData[0,94] =   0
      GraphData[0,95] =   0
      GraphData[0,96] =   0
      GraphData[0,97] =   0
      GraphData[0,98] =   0
      GraphData[0,99] =   0
      GraphData[0,100]=   0
      GraphData[0,101]=   0
      GraphData[0,102]=   0
      GraphData[0,103]=   0
      GraphData[0,104]=   0
      GraphData[0,105]=   0
      GraphData[0,106]=   0
      GraphData[0,107]=   0
      GraphData[0,108]=   0
      GraphData[0,109]=   0
      GraphData[0,110]=   0
      GraphData[0,111]=   0
      GraphData[0,112]=   0
      GraphData[0,113]=   0
      GraphData[0,114]=   0
      GraphData[0,115]=   0
      GraphData[0,116]=   0
      GraphData[0,117]=   0
      GraphData[0,118]=   0
      GraphData[0,119]=   0
      GraphData[0,120]=   0
      GraphData[0,121]=   0
      GraphData[0,122]=   0
      GraphData[0,123]=   0
      GraphData[0,124]=   0
      GraphData[0,125]=   0
      GraphData[0,126]=   0
      GraphData[0,127]=   0
      GraphData[0,128]=   0
      GraphData[0,129]=   0
      GraphData[0,130]=   0
      GraphData[0,131]=   0
      GraphData[0,132]=   0
      GraphData[0,133]=   0
      GraphData[0,134]=   0
      GraphData[0,135]=   0
      GraphData[0,136]=   0
      GraphData[0,137]=   0
      GraphData[0,138]=   0
      GraphData[0,139]=   0
      GraphData[0,140]=   0
      GraphData[0,141]=   0
      GraphData[0,142]=   0
      GraphData[0,143]=   0
      GraphData[0,144]=   0
      GraphData[0,145]=   0
      GraphData[0,146]=   0
      GraphData[0,147]=   0
      GraphData[0,148]=   0
      GraphData[0,149]=   0
      GraphData[0,150]=   0
      GraphData[0,151]=   0
      GraphData[0,152]=   0
      GraphData[0,153]=   0
      GraphData[0,154]=   0
      GraphData[0,155]=   0
      GraphData[0,156]=   0
      GraphData[0,157]=   0
      GraphData[0,158]=   0
      GraphData[0,159]=   0
      GraphData[0,160]=   0
      GraphData[0,161]=   0
      GraphData[0,162]=   0
      GraphData[0,163]=   0
      GraphData[0,164]=   0
      GraphData[0,165]=   0
      GraphData[0,166]=   0
      GraphData[0,167]=   0
      GraphData[0,168]=   0
      GraphData[0,169]=   0
      GraphData[0,170]=   0
      GraphData[0,171]=   0
      GraphData[0,172]=   0
      GraphData[0,173]=   0
      GraphData[0,174]=   0
      GraphData[0,175]=   0
      GraphData[0,176]=   0
      GraphData[0,177]=   0
      GraphData[0,178]=   0
      GraphData[0,179]=   0
      GraphData[0,180]=   0
      GraphData[0,181]=   0
      GraphData[0,182]=   0
      GraphData[0,183]=   0
      GraphData[0,184]=   0
      GraphData[0,185]=   0
      GraphData[0,186]=   0
      GraphData[0,187]=   0
      GraphData[0,188]=   0
      GraphData[0,189]=   0
      GraphData[0,190]=   0
      GraphData[0,191]=   0
      GraphData[0,192]=   0
      GraphData[0,193]=   0
      GraphData[0,194]=   0
      GraphData[0,195]=   0
      GraphData[0,196]=   0
      GraphData[0,197]=   0
      GraphData[0,198]=   0
      GraphData[0,199]=   0
      GraphData[0,200]=   0
      GraphData[0,201]=   0
      GraphData[0,202]=   0
      GraphData[0,203]=   0
      GraphData[0,204]=   0
      GraphData[0,205]=   0
      GraphData[0,206]=   0
      GraphData[0,207]=   0
      GraphData[0,208]=   0
      GraphData[0,209]=   0
      GraphData[0,210]=   0
      GraphData[0,211]=   0
      GraphData[0,212]=   0
      GraphData[0,213]=   0
      GraphData[0,214]=   0
      GraphData[0,215]=   0
      GraphData[0,216]=   0
      GraphData[0,217]=   0
      GraphData[0,218]=   0
      GraphData[0,219]=   0
      GraphData[0,220]=   0
      GraphData[0,221]=   0
      GraphData[0,222]=   0
      GraphData[0,223]=   0
      GraphData[0,224]=   0
      GraphData[0,225]=   0
      GraphData[0,226]=   0
      GraphData[0,227]=   0
      GraphData[0,228]=   0
      GraphData[0,229]=   0
      GraphData[0,230]=   0
      GraphData[0,231]=   0
      GraphData[0,232]=   0
      GraphData[0,233]=   0
      GraphData[0,234]=   0
      GraphData[0,235]=   0
      GraphData[0,236]=   0
      GraphData[0,237]=   0
      GraphData[0,238]=   0
      GraphData[0,239]=   0
      GraphData[0,240]=   0
      GraphData[0,241]=   0
      GraphData[0,242]=   0
      GraphData[0,243]=   0
      GraphData[0,244]=   0
      GraphData[0,245]=   0
      GraphData[0,246]=   0
      GraphData[0,247]=   0
      GraphData[0,248]=   0
      GraphData[0,249]=   0
      GraphData[0,250]=   0
      GraphData[0,251]=   0
      GraphData[0,252]=   0
      GraphData[0,253]=   0
      GraphData[0,254]=   0
      GraphData[0,255]=   0
      GraphData[0,256]=   0
      GraphData[0,257]=   0
      GraphData[0,258]=   0
      GraphData[0,259]=   0
      GraphData[0,260]=   0
      GraphData[0,261]=   0
      GraphData[0,262]=   0
      GraphData[0,263]=   0
      GraphData[0,264]=   0
      GraphData[0,265]=   0
      GraphData[0,266]=   0
      GraphData[0,267]=   0
      GraphData[0,268]=   0
      GraphData[0,269]=   0
      GraphData[0,270]=   0
      GraphData[0,271]=   0
      GraphData[0,272]=   0
      GraphData[0,273]=   0
      GraphData[0,274]=   0
      GraphData[0,275]=   0
      GraphData[0,276]=   0
      GraphData[0,277]=   0
      GraphData[0,278]=   0
      GraphData[0,279]=   0
      GraphData[0,280]=   0
      GraphData[0,281]=   0
      GraphData[0,282]=   0
      GraphData[0,283]=   0
      GraphData[0,284]=   0
      GraphData[0,285]=   0
      GraphData[0,286]=   0
      GraphData[0,287]=   0
      GraphData[0,288]=   0
      GraphData[0,289]=   0
      GraphData[0,290]=   0
      GraphData[0,291]=   0
      GraphData[0,292]=   0
      GraphData[0,293]=   0
      GraphData[0,294]=   0
      GraphData[0,295]=   0
      GraphData[0,296]=   0
      GraphData[0,297]=   0
      GraphData[0,298]=   0
      GraphData[0,299]=   0
      GraphData[0,300]=   0
      GraphData[0,301]=   0
      GraphData[0,302]=   0
      GraphData[0,303]=   0
      GraphData[0,304]=   0
      GraphData[0,305]=   0
      GraphData[0,306]=   0
      GraphData[0,307]=   0
      GraphData[0,308]=   0
      GraphData[0,309]=   0
      GraphData[0,310]=   0
      GraphData[0,311]=   0
      GraphData[0,312]=   0
      GraphData[0,313]=   0
      GraphData[0,314]=   0
      GraphData[0,315]=   0
      GraphData[0,316]=   0
      GraphData[0,317]=   0
      GraphData[0,318]=   0
      GraphData[0,319]=   0
      GraphData[0,320]=   0
      GraphData[0,321]=   0
      GraphData[0,322]=   0
      GraphData[0,323]=   0
      GraphData[0,324]=   0
      GraphData[0,325]=   0
      GraphData[0,326]=   0
      GraphData[0,327]=   0
      GraphData[0,328]=   0
      GraphData[0,329]=   0
      GraphData[0,330]=   0
      GraphData[0,331]=   0
      GraphData[0,332]=   0
      GraphData[0,333]=   0
      GraphData[0,334]=   0
      GraphData[0,335]=   0
      GraphData[0,336]=   0
      GraphData[0,337]=   0
      GraphData[0,338]=   0
      GraphData[0,339]=   0
      GraphData[0,340]=   0
      GraphData[0,341]=   0
      GraphData[0,342]=   0
      GraphData[0,343]=   0
      GraphData[0,344]=   0
      GraphData[0,345]=   0
      GraphData[0,346]=   0
      GraphData[0,347]=   0
      GraphData[0,348]=   0
      GraphData[0,349]=   0
      GraphData[0,350]=   0
      GraphData[0,351]=   0
      GraphData[0,352]=   0
      GraphData[0,353]=   0
      GraphData[0,354]=   0
      GraphData[0,355]=   0
      GraphData[0,356]=   0
      GraphData[0,357]=   0
      GraphData[0,358]=   0
      GraphData[0,359]=   0
      GraphData[0,360]=   0
      GraphData[0,361]=   0
      GraphData[0,362]=   0
      GraphData[0,363]=   0
      GraphData[0,364]=   0
      GraphData[0,365]=   0
      GraphData[0,366]=   0
      GraphData[0,367]=   0
      GraphData[0,368]=   0
      GraphData[0,369]=   0
      GraphData[0,370]=   0
      GraphData[0,371]=   0
      GraphData[0,372]=   0
      GraphData[0,373]=   0
      GraphData[0,374]=   0
      GraphData[0,375]=   0
      GraphData[0,376]=   0
      GraphData[0,377]=   0
      GraphData[0,378]=   0
      GraphData[0,379]=   0
      GraphData[0,380]=   0
      GraphData[0,381]=   0
      GraphData[0,382]=   0
      GraphData[0,383]=   0
      GraphData[0,384]=   0
      GraphData[0,385]=   0
      GraphData[0,386]=   0
      GraphData[0,387]=   0
      GraphData[0,388]=   0
      GraphData[0,389]=   0
      GraphData[0,390]=   0
      GraphData[0,391]=   0
      GraphData[0,392]=   0
      GraphData[0,393]=   0
      GraphData[0,394]=   0
      GraphData[0,395]=   0
      GraphData[0,396]=   0
      GraphData[0,397]=   0
      GraphData[0,398]=   0
      GraphData[0,399]=   0
      GraphData[0,400]=   0
      GraphData[0,401]=   0
      GraphData[0,402]=   0
      GraphData[0,403]=   0
      GraphData[0,404]=   0
      GraphData[0,405]=   0
      GraphData[0,406]=   0
      GraphData[0,407]=   0
      GraphData[0,408]=   0
      GraphData[0,409]=   0
      GraphData[0,410]=   0
      GraphData[0,411]=   0
      GraphData[0,412]=   0
      GraphData[0,413]=   0
      GraphData[0,414]=   0
      GraphData[0,415]=   0
      GraphData[0,416]=   0
      GraphData[0,417]=   0
      GraphData[0,418]=   0
      GraphData[0,419]=   0
      GraphData[0,420]=   0
      GraphData[0,421]=   0
      GraphData[0,422]=   0
      GraphData[0,423]=   0
      GraphData[0,424]=   0
      GraphData[0,425]=   0
      GraphData[0,426]=   0
      GraphData[0,427]=   0
      GraphData[0,428]=   0
      GraphData[0,429]=   0
      GraphData[0,430]=   0
      GraphData[0,431]=   0
      GraphData[0,432]=   0
      GraphData[0,433]=   0
      GraphData[0,434]=   0
      GraphData[0,435]=   0
      GraphData[0,436]=   0
      GraphData[0,437]=   0
      GraphData[0,438]=   0
      GraphData[0,439]=   0
      GraphData[0,440]=   0
      GraphData[0,441]=   0
      GraphData[0,442]=   0
      GraphData[0,443]=   0
      GraphData[0,444]=   0
      GraphData[0,445]=   0
      GraphData[0,446]=   0
      GraphData[0,447]=   0
      GraphData[0,448]=   0
      GraphData[0,449]=   0
      GraphData[0,450]=   0
      GraphData[0,451]=   0
      GraphData[0,452]=   0
      GraphData[0,453]=   0
      GraphData[0,454]=   0
      GraphData[0,455]=   0
      GraphData[0,456]=   0
      GraphData[0,457]=   0
      GraphData[0,458]=   0
      GraphData[0,459]=   0
      GraphData[0,460]=   0
      GraphData[0,461]=   0
      GraphData[0,462]=   0
      GraphData[0,463]=   0
      GraphData[0,464]=   0
      GraphData[0,465]=   0
      GraphData[0,466]=   0
      GraphData[0,467]=   0
      GraphData[0,468]=   0
      GraphData[0,469]=   0
      GraphData[0,470]=   0
      GraphData[0,471]=   0
      GraphData[0,472]=   0
      GraphData[0,473]=   0
      GraphData[0,474]=   0
      GraphData[0,475]=   0
      GraphData[0,476]=   0
      GraphData[0,477]=   0
      GraphData[0,478]=   0
      GraphData[0,479]=   0
      GraphData[0,480]=   0
      GraphData[0,481]=   0
      GraphData[0,482]=   0
      GraphData[0,483]=   0
      GraphData[0,484]=   0
      GraphData[0,485]=   0
      GraphData[0,486]=   0
      GraphData[0,487]=   0
      GraphData[0,488]=   0
      GraphData[0,489]=   0
      GraphData[0,490]=   0
      GraphData[0,491]=   0
      GraphData[0,492]=   0
      GraphData[0,493]=   0
      GraphData[0,494]=   0
      GraphData[0,495]=   0
      GraphData[0,496]=   0
      GraphData[0,497]=   0
      GraphData[0,498]=   0
      GraphData[0,499]=   0
      GraphData[0,500]=   0
      GraphData[0,501]=   0
      GraphData[0,502]=   0
      GraphData[0,503]=   0
      GraphData[0,504]=   0
      GraphData[0,505]=   0
      GraphData[0,506]=   0
      GraphData[0,507]=   0
      GraphData[0,508]=   0
      GraphData[0,509]=   0
      GraphData[0,510]=   0
      GraphData[0,511]=   0
      GraphData[0,512]=   0
      GraphData[0,513]=   0
      GraphData[0,514]=   0
      GraphData[0,515]=   0
      GraphData[0,516]=   0
      GraphData[0,517]=   0
      GraphData[0,518]=   0
      GraphData[0,519]=   0
      GraphData[0,520]=   0
      GraphData[0,521]=   0
      GraphData[0,522]=   0
      GraphData[0,523]=   0
      GraphData[0,524]=   0
      GraphData[0,525]=   0
      GraphData[0,526]=   0
      GraphData[0,527]=   0
      GraphData[0,528]=   0
      GraphData[0,529]=   0
      GraphData[0,530]=   0
      GraphData[0,531]=   0
      GraphData[0,532]=   0
      GraphData[0,533]=   0
      GraphData[0,534]=   0
      GraphData[0,535]=   0
      GraphData[0,536]=   0
      GraphData[0,537]=   0
      GraphData[0,538]=   0
      GraphData[0,539]=   0
      GraphData[0,540]=   0
      GraphData[0,541]=   0
      GraphData[0,542]=   0
      GraphData[0,543]=   0
      GraphData[0,544]=   0
      GraphData[0,545]=   0
      GraphData[0,546]=   0
      GraphData[0,547]=   0
      GraphData[0,548]=   0
      GraphData[0,549]=   0
      GraphData[0,550]=   0
      GraphData[0,551]=   0
      GraphData[0,552]=   0
      GraphData[0,553]=   0
      GraphData[0,554]=   0
      GraphData[0,555]=   0
      GraphData[0,556]=   0
      GraphData[0,557]=   0
      GraphData[0,558]=   0
      GraphData[0,559]=   0
      GraphData[0,560]=   0
      GraphData[0,561]=   0
      GraphData[0,562]=   0
      GraphData[0,563]=   0
      GraphData[0,564]=   0
      GraphData[0,565]=   0
      GraphData[0,566]=   0
      GraphData[0,567]=   0
      GraphData[0,568]=   0
      GraphData[0,569]=   0
      GraphData[0,570]=   0
      GraphData[0,571]=   0
      GraphData[0,572]=   0
      GraphData[0,573]=   0
      GraphData[0,574]=   0
      GraphData[0,575]=   0
      GraphData[0,576]=   0
      GraphData[0,577]=   0
      GraphData[0,578]=   0
      GraphData[0,579]=   0
      GraphData[0,580]=   0
      GraphData[0,581]=   0
      GraphData[0,582]=   0
      GraphData[0,583]=   0
      GraphData[0,584]=   0
      GraphData[0,585]=   0
      GraphData[0,586]=   0
      GraphData[0,587]=   0
      GraphData[0,588]=   0
      GraphData[0,589]=   0
      GraphData[0,590]=   0
      GraphData[0,591]=   0
      GraphData[0,592]=   0
      GraphData[0,593]=   0
      GraphData[0,594]=   0
      GraphData[0,595]=   0
      GraphData[0,596]=   0
      GraphData[0,597]=   0
      GraphData[0,598]=   0
      GraphData[0,599]=   0
      GraphData[0,600]=   0
      GraphData[0,601]=   0
      GraphData[0,602]=   0
      GraphData[0,603]=   0
      GraphData[0,604]=   0
      GraphData[0,605]=   0
      GraphData[0,606]=   0
      GraphData[0,607]=   0
      GraphData[0,608]=   0
      GraphData[0,609]=   0
      GraphData[0,610]=   0
      GraphData[0,611]=   0
      GraphData[0,612]=   0
      GraphData[0,613]=   0
      GraphData[0,614]=   0
      GraphData[0,615]=   0
      GraphData[0,616]=   0
      GraphData[0,617]=   0
      GraphData[0,618]=   0
      GraphData[0,619]=   0
      GraphData[0,620]=   0
      GraphData[0,621]=   0
      GraphData[0,622]=   0
      GraphData[0,623]=   0
      GraphData[0,624]=   0
      GraphData[0,625]=   0
      GraphData[0,626]=   0
      GraphData[0,627]=   0
      GraphData[0,628]=   0
      GraphData[0,629]=   0
      GraphData[0,630]=   0
      GraphData[0,631]=   0
      GraphData[0,632]=   0
      GraphData[0,633]=   0
      GraphData[0,634]=   0
      GraphData[0,635]=   0
      GraphData[0,636]=   0
      GraphData[0,637]=   0
      GraphData[0,638]=   0
      GraphData[0,639]=   0
      GraphData[0,640]=   0
      GraphData[0,641]=   0
      GraphData[0,642]=   0
      GraphData[0,643]=   0
      GraphData[0,644]=   0
      GraphData[0,645]=   0
      GraphData[0,646]=   0
      GraphData[0,647]=   0
      GraphData[0,648]=   0
      GraphData[0,649]=   0
      GraphData[0,650]=   0
      GraphData[0,651]=   0
      GraphData[0,652]=   0
      GraphData[0,653]=   0
      GraphData[0,654]=   0
      GraphData[0,655]=   0
      GraphData[0,656]=   0
      GraphData[0,657]=   0
      GraphData[0,658]=   0
      GraphData[0,659]=   0
      GraphData[0,660]=   0
      GraphData[0,661]=   0
      GraphData[0,662]=   0
      GraphData[0,663]=   0
      GraphData[0,664]=   0
      GraphData[0,665]=   0
      GraphData[0,666]=   0
      GraphData[0,667]=   0
      GraphData[0,668]=   0
      GraphData[0,669]=   0
      GraphData[0,670]=   0
      GraphData[0,671]=   0
      GraphData[0,672]=   0
      GraphData[0,673]=   0
      GraphData[0,674]=   0
      GraphData[0,675]=   0
      GraphData[0,676]=   0
      GraphData[0,677]=   0
      GraphData[0,678]=   0
      GraphData[0,679]=   0
      GraphData[0,680]=   0
      GraphData[0,681]=   0
      GraphData[0,682]=   0
      GraphData[0,683]=   0
      GraphData[0,684]=   0
      GraphData[0,685]=   0
      GraphData[0,686]=   0
      GraphData[0,687]=   0
      GraphData[0,688]=   0
      GraphData[0,689]=   0
      GraphData[0,690]=   0
      GraphData[0,691]=   0
      GraphData[0,692]=   0
      GraphData[0,693]=   0
      GraphData[0,694]=   0
      GraphData[0,695]=   0
      GraphData[0,696]=   0
      GraphData[0,697]=   0
      GraphData[0,698]=   0
      GraphData[0,699]=   0
      GraphData[0,700]=   0
      GraphData[0,701]=   0
      GraphData[0,702]=   0
      GraphData[0,703]=   0
      GraphData[0,704]=   0
      GraphData[0,705]=   0
      GraphData[0,706]=   0
      GraphData[0,707]=   0
      GraphData[0,708]=   0
      GraphData[0,709]=   0
      GraphData[0,710]=   0
      GraphData[0,711]=   0
      GraphData[0,712]=   0
      GraphData[0,713]=   0
      GraphData[0,714]=   0
      GraphData[0,715]=   0
      GraphData[0,716]=   0
      GraphData[0,717]=   0
      GraphData[0,718]=   0
      GraphData[0,719]=   0
      GraphData[0,720]=   0
      GraphData[0,721]=   0
      GraphData[0,722]=   0
      GraphData[0,723]=   0
      GraphData[0,724]=   0
      GraphData[0,725]=   0
      GraphData[0,726]=   0
      GraphData[0,727]=   0
      GraphData[0,728]=   0
      GraphData[0,729]=   0
      GraphData[0,730]=   0
      GraphData[0,731]=   0
      GraphData[0,732]=   0
      GraphData[0,733]=   0
      GraphData[0,734]=   0
      GraphData[0,735]=   0
      GraphData[0,736]=   0
      GraphData[0,737]=   0
      GraphData[0,738]=   0
      GraphData[0,739]=   0
      GraphData[0,740]=   0
      GraphData[0,741]=   0
      GraphData[0,742]=   0
      GraphData[0,743]=   0
      GraphData[0,744]=   0
      GraphData[0,745]=   0
      GraphData[0,746]=   0
      GraphData[0,747]=   0
      GraphData[0,748]=   0
      GraphData[0,749]=   0
      GraphData[0,750]=   0
      GraphData[0,751]=   0
      GraphData[0,752]=   0
      GraphData[0,753]=   0
      GraphData[0,754]=   0
      GraphData[0,755]=   0
      GraphData[0,756]=   0
      GraphData[0,757]=   0
      GraphData[0,758]=   0
      GraphData[0,759]=   0
      GraphData[0,760]=   0
      GraphData[0,761]=   0
      GraphData[0,762]=   0
      GraphData[0,763]=   0
      GraphData[0,764]=   0
      GraphData[0,765]=   0
      GraphData[0,766]=   0
      GraphData[0,767]=   0
      GraphData[0,768]=   0
      GraphData[0,769]=   0
      GraphData[0,770]=   0
      GraphData[0,771]=   0
      GraphData[0,772]=   0
      GraphData[0,773]=   0
      GraphData[0,774]=   0
      GraphData[0,775]=   0
      GraphData[0,776]=   0
      GraphData[0,777]=   0
      GraphData[0,778]=   0
      GraphData[0,779]=   0
      GraphData[0,780]=   0
      GraphData[0,781]=   0
      GraphData[0,782]=   0
      GraphData[0,783]=   0
      GraphData[0,784]=   0
      GraphData[0,785]=   0
      GraphData[0,786]=   0
      GraphData[0,787]=   0
      GraphData[0,788]=   0
      GraphData[0,789]=   0
      GraphData[0,790]=   0
      GraphData[0,791]=   0
      GraphData[0,792]=   0
      GraphData[0,793]=   0
      GraphData[0,794]=   0
      GraphData[0,795]=   0
      GraphData[0,796]=   0
      GraphData[0,797]=   0
      GraphData[0,798]=   0
      GraphData[0,799]=   0
      GraphData[0,800]=   0
      GraphData[0,801]=   0
      GraphData[0,802]=   0
      GraphData[0,803]=   0
      GraphData[0,804]=   0
      GraphData[0,805]=   0
      GraphData[0,806]=   0
      GraphData[0,807]=   0
      GraphData[0,808]=   0
      GraphData[0,809]=   0
      GraphData[0,810]=   0
      GraphData[0,811]=   0
      GraphData[0,812]=   0
      GraphData[0,813]=   0
      GraphData[0,814]=   0
      GraphData[0,815]=   0
      GraphData[0,816]=   0
      GraphData[0,817]=   0
      GraphData[0,818]=   0
      GraphData[0,819]=   0
      GraphData[0,820]=   0
      GraphData[0,821]=   0
      GraphData[0,822]=   0
      GraphData[0,823]=   0
      GraphData[0,824]=   0
      GraphData[0,825]=   0
      GraphData[0,826]=   0
      GraphData[0,827]=   0
      GraphData[0,828]=   0
      GraphData[0,829]=   0
      GraphData[0,830]=   0
      GraphData[0,831]=   0
      GraphData[0,832]=   0
      GraphData[0,833]=   0
      GraphData[0,834]=   0
      GraphData[0,835]=   0
      GraphData[0,836]=   0
      GraphData[0,837]=   0
      GraphData[0,838]=   0
      GraphData[0,839]=   0
      GraphData[0,840]=   0
      GraphData[0,841]=   0
      GraphData[0,842]=   0
      GraphData[0,843]=   0
      GraphData[0,844]=   0
      GraphData[0,845]=   0
      GraphData[0,846]=   0
      GraphData[0,847]=   0
      GraphData[0,848]=   0
      GraphData[0,849]=   0
      GraphData[0,850]=   0
      GraphData[0,851]=   0
      GraphData[0,852]=   0
      GraphData[0,853]=   0
      GraphData[0,854]=   0
      GraphData[0,855]=   0
      GraphData[0,856]=   0
      GraphData[0,857]=   0
      GraphData[0,858]=   0
      GraphData[0,859]=   0
      GraphData[0,860]=   0
      GraphData[0,861]=   0
      GraphData[0,862]=   0
      GraphData[0,863]=   0
      GraphData[0,864]=   0
      GraphData[0,865]=   0
      GraphData[0,866]=   0
      GraphData[0,867]=   0
      GraphData[0,868]=   0
      GraphData[0,869]=   0
      GraphData[0,870]=   0
      GraphData[0,871]=   0
      GraphData[0,872]=   0
      GraphData[0,873]=   0
      GraphData[0,874]=   0
      GraphData[0,875]=   0
      GraphData[0,876]=   0
      GraphData[0,877]=   0
      GraphData[0,878]=   0
      GraphData[0,879]=   0
      GraphData[0,880]=   0
      GraphData[0,881]=   0
      GraphData[0,882]=   0
      GraphData[0,883]=   0
      GraphData[0,884]=   0
      GraphData[0,885]=   0
      GraphData[0,886]=   0
      GraphData[0,887]=   0
      GraphData[0,888]=   0
      GraphData[0,889]=   0
      GraphData[0,890]=   0
      GraphData[0,891]=   0
      GraphData[0,892]=   0
      GraphData[0,893]=   0
      GraphData[0,894]=   0
      GraphData[0,895]=   0
      GraphData[0,896]=   0
      GraphData[0,897]=   0
      GraphData[0,898]=   0
      GraphData[0,899]=   0
      GraphData[0,900]=   0
      GraphData[0,901]=   0
      GraphData[0,902]=   0
      GraphData[0,903]=   0
      GraphData[0,904]=   0
      GraphData[0,905]=   0
      GraphData[0,906]=   0
      GraphData[0,907]=   0
      GraphData[0,908]=   0
      GraphData[0,909]=   0
      GraphData[0,910]=   0
      GraphData[0,911]=   0
      GraphData[0,912]=   0
      GraphData[0,913]=   0
      GraphData[0,914]=   0
      GraphData[0,915]=   0
      GraphData[0,916]=   0
      GraphData[0,917]=   0
      GraphData[0,918]=   0
      GraphData[0,919]=   0
      GraphData[0,920]=   0
      GraphData[0,921]=   0
      GraphData[0,922]=   0
      GraphData[0,923]=   0
      GraphData[0,924]=   0
      GraphData[0,925]=   0
      GraphData[0,926]=   0
      GraphData[0,927]=   0
      GraphData[0,928]=   0
      GraphData[0,929]=   0
      GraphData[0,930]=   0
      GraphData[0,931]=   0
      GraphData[0,932]=   0
      GraphData[0,933]=   0
      GraphData[0,934]=   0
      GraphData[0,935]=   0
      GraphData[0,936]=   0
      GraphData[0,937]=   0
      GraphData[0,938]=   0
      GraphData[0,939]=   0
      GraphData[0,940]=   0
      GraphData[0,941]=   0
      GraphData[0,942]=   0
      GraphData[0,943]=   0
      GraphData[0,944]=   0
      GraphData[0,945]=   0
      GraphData[0,946]=   0
      GraphData[0,947]=   0
      GraphData[0,948]=   0
      GraphData[0,949]=   0
      GraphData[0,950]=   0
      GraphData[0,951]=   0
      GraphData[0,952]=   0
      GraphData[0,953]=   0
      GraphData[0,954]=   0
      GraphData[0,955]=   0
      GraphData[0,956]=   0
      GraphData[0,957]=   0
      GraphData[0,958]=   0
      GraphData[0,959]=   0
      GraphData[0,960]=   0
      GraphData[0,961]=   0
      GraphData[0,962]=   0
      GraphData[0,963]=   0
      GraphData[0,964]=   0
      GraphData[0,965]=   0
      GraphData[0,966]=   0
      GraphData[0,967]=   0
      GraphData[0,968]=   0
      GraphData[0,969]=   0
      GraphData[0,970]=   0
      GraphData[0,971]=   0
      GraphData[0,972]=   0
      GraphData[0,973]=   0
      GraphData[0,974]=   0
      GraphData[0,975]=   0
      GraphData[0,976]=   0
      GraphData[0,977]=   0
      GraphData[0,978]=   0
      GraphData[0,979]=   0
      GraphData[0,980]=   0
      GraphData[0,981]=   0
      GraphData[0,982]=   0
      GraphData[0,983]=   0
      GraphData[0,984]=   0
      GraphData[0,985]=   0
      GraphData[0,986]=   0
      GraphData[0,987]=   0
      GraphData[0,988]=   0
      GraphData[0,989]=   0
      GraphData[0,990]=   0
      GraphData[0,991]=   0
      GraphData[0,992]=   0
      GraphData[0,993]=   0
      GraphData[0,994]=   0
      GraphData[0,995]=   0
      GraphData[0,996]=   0
      GraphData[0,997]=   0
      GraphData[0,998]=   0
      GraphData[0,999]=   0
      GraphData[0,1000]=   0
      GraphData[0,1001]=   0
      GraphData[0,1002]=   0
      GraphData[0,1003]=   0
      GraphData[0,1004]=   0
      GraphData[0,1005]=   0
      GraphData[0,1006]=   0
      GraphData[0,1007]=   0
      GraphData[0,1008]=   0
      GraphData[0,1009]=   0
      GraphData[0,1010]=   0
      GraphData[0,1011]=   0
      GraphData[0,1012]=   0
      GraphData[0,1013]=   0
      GraphData[0,1014]=   0
      GraphData[0,1015]=   0
      GraphData[0,1016]=   0
      GraphData[0,1017]=   0
      GraphData[0,1018]=   0
      GraphData[0,1019]=   0
      GraphData[0,1020]=   0
      GraphData[0,1021]=   0
      GraphData[0,1022]=   0
      GraphData[0,1023]=   0
      LabelText       =   0
      LegendText      =   0
      PatternData     =   1
      SymbolData      =   0
      XPosData        =   1
      XPosData[]      =   1024
      XPosData[0,0]   =   0
      XPosData[0,1]   =   1000
      XPosData[0,2]   =   0
      XPosData[0,3]   =   0
      XPosData[0,4]   =   0
      XPosData[0,5]   =   0
      XPosData[0,6]   =   0
      XPosData[0,7]   =   0
      XPosData[0,8]   =   0
      XPosData[0,9]   =   0
      XPosData[0,10]  =   0
      XPosData[0,11]  =   0
      XPosData[0,12]  =   0
      XPosData[0,13]  =   0
      XPosData[0,14]  =   0
      XPosData[0,15]  =   0
      XPosData[0,16]  =   0
      XPosData[0,17]  =   0
      XPosData[0,18]  =   0
      XPosData[0,19]  =   0
      XPosData[0,20]  =   0
      XPosData[0,21]  =   0
      XPosData[0,22]  =   0
      XPosData[0,23]  =   0
      XPosData[0,24]  =   0
      XPosData[0,25]  =   0
      XPosData[0,26]  =   0
      XPosData[0,27]  =   0
      XPosData[0,28]  =   0
      XPosData[0,29]  =   0
      XPosData[0,30]  =   0
      XPosData[0,31]  =   0
      XPosData[0,32]  =   0
      XPosData[0,33]  =   0
      XPosData[0,34]  =   0
      XPosData[0,35]  =   0
      XPosData[0,36]  =   0
      XPosData[0,37]  =   0
      XPosData[0,38]  =   0
      XPosData[0,39]  =   0
      XPosData[0,40]  =   0
      XPosData[0,41]  =   0
      XPosData[0,42]  =   0
      XPosData[0,43]  =   0
      XPosData[0,44]  =   0
      XPosData[0,45]  =   0
      XPosData[0,46]  =   0
      XPosData[0,47]  =   0
      XPosData[0,48]  =   0
      XPosData[0,49]  =   0
      XPosData[0,50]  =   0
      XPosData[0,51]  =   0
      XPosData[0,52]  =   0
      XPosData[0,53]  =   0
      XPosData[0,54]  =   0
      XPosData[0,55]  =   0
      XPosData[0,56]  =   0
      XPosData[0,57]  =   0
      XPosData[0,58]  =   0
      XPosData[0,59]  =   0
      XPosData[0,60]  =   0
      XPosData[0,61]  =   0
      XPosData[0,62]  =   0
      XPosData[0,63]  =   0
      XPosData[0,64]  =   0
      XPosData[0,65]  =   0
      XPosData[0,66]  =   0
      XPosData[0,67]  =   0
      XPosData[0,68]  =   0
      XPosData[0,69]  =   0
      XPosData[0,70]  =   0
      XPosData[0,71]  =   0
      XPosData[0,72]  =   0
      XPosData[0,73]  =   0
      XPosData[0,74]  =   0
      XPosData[0,75]  =   0
      XPosData[0,76]  =   0
      XPosData[0,77]  =   0
      XPosData[0,78]  =   0
      XPosData[0,79]  =   0
      XPosData[0,80]  =   0
      XPosData[0,81]  =   0
      XPosData[0,82]  =   0
      XPosData[0,83]  =   0
      XPosData[0,84]  =   0
      XPosData[0,85]  =   0
      XPosData[0,86]  =   0
      XPosData[0,87]  =   0
      XPosData[0,88]  =   0
      XPosData[0,89]  =   0
      XPosData[0,90]  =   0
      XPosData[0,91]  =   0
      XPosData[0,92]  =   0
      XPosData[0,93]  =   0
      XPosData[0,94]  =   0
      XPosData[0,95]  =   0
      XPosData[0,96]  =   0
      XPosData[0,97]  =   0
      XPosData[0,98]  =   0
      XPosData[0,99]  =   0
      XPosData[0,100] =   0
      XPosData[0,101] =   0
      XPosData[0,102] =   0
      XPosData[0,103] =   0
      XPosData[0,104] =   0
      XPosData[0,105] =   0
      XPosData[0,106] =   0
      XPosData[0,107] =   0
      XPosData[0,108] =   0
      XPosData[0,109] =   0
      XPosData[0,110] =   0
      XPosData[0,111] =   0
      XPosData[0,112] =   0
      XPosData[0,113] =   0
      XPosData[0,114] =   0
      XPosData[0,115] =   0
      XPosData[0,116] =   0
      XPosData[0,117] =   0
      XPosData[0,118] =   0
      XPosData[0,119] =   0
      XPosData[0,120] =   0
      XPosData[0,121] =   0
      XPosData[0,122] =   0
      XPosData[0,123] =   0
      XPosData[0,124] =   0
      XPosData[0,125] =   0
      XPosData[0,126] =   0
      XPosData[0,127] =   0
      XPosData[0,128] =   0
      XPosData[0,129] =   0
      XPosData[0,130] =   0
      XPosData[0,131] =   0
      XPosData[0,132] =   0
      XPosData[0,133] =   0
      XPosData[0,134] =   0
      XPosData[0,135] =   0
      XPosData[0,136] =   0
      XPosData[0,137] =   0
      XPosData[0,138] =   0
      XPosData[0,139] =   0
      XPosData[0,140] =   0
      XPosData[0,141] =   0
      XPosData[0,142] =   0
      XPosData[0,143] =   0
      XPosData[0,144] =   0
      XPosData[0,145] =   0
      XPosData[0,146] =   0
      XPosData[0,147] =   0
      XPosData[0,148] =   0
      XPosData[0,149] =   0
      XPosData[0,150] =   0
      XPosData[0,151] =   0
      XPosData[0,152] =   0
      XPosData[0,153] =   0
      XPosData[0,154] =   0
      XPosData[0,155] =   0
      XPosData[0,156] =   0
      XPosData[0,157] =   0
      XPosData[0,158] =   0
      XPosData[0,159] =   0
      XPosData[0,160] =   0
      XPosData[0,161] =   0
      XPosData[0,162] =   0
      XPosData[0,163] =   0
      XPosData[0,164] =   0
      XPosData[0,165] =   0
      XPosData[0,166] =   0
      XPosData[0,167] =   0
      XPosData[0,168] =   0
      XPosData[0,169] =   0
      XPosData[0,170] =   0
      XPosData[0,171] =   0
      XPosData[0,172] =   0
      XPosData[0,173] =   0
      XPosData[0,174] =   0
      XPosData[0,175] =   0
      XPosData[0,176] =   0
      XPosData[0,177] =   0
      XPosData[0,178] =   0
      XPosData[0,179] =   0
      XPosData[0,180] =   0
      XPosData[0,181] =   0
      XPosData[0,182] =   0
      XPosData[0,183] =   0
      XPosData[0,184] =   0
      XPosData[0,185] =   0
      XPosData[0,186] =   0
      XPosData[0,187] =   0
      XPosData[0,188] =   0
      XPosData[0,189] =   0
      XPosData[0,190] =   0
      XPosData[0,191] =   0
      XPosData[0,192] =   0
      XPosData[0,193] =   0
      XPosData[0,194] =   0
      XPosData[0,195] =   0
      XPosData[0,196] =   0
      XPosData[0,197] =   0
      XPosData[0,198] =   0
      XPosData[0,199] =   0
      XPosData[0,200] =   0
      XPosData[0,201] =   0
      XPosData[0,202] =   0
      XPosData[0,203] =   0
      XPosData[0,204] =   0
      XPosData[0,205] =   0
      XPosData[0,206] =   0
      XPosData[0,207] =   0
      XPosData[0,208] =   0
      XPosData[0,209] =   0
      XPosData[0,210] =   0
      XPosData[0,211] =   0
      XPosData[0,212] =   0
      XPosData[0,213] =   0
      XPosData[0,214] =   0
      XPosData[0,215] =   0
      XPosData[0,216] =   0
      XPosData[0,217] =   0
      XPosData[0,218] =   0
      XPosData[0,219] =   0
      XPosData[0,220] =   0
      XPosData[0,221] =   0
      XPosData[0,222] =   0
      XPosData[0,223] =   0
      XPosData[0,224] =   0
      XPosData[0,225] =   0
      XPosData[0,226] =   0
      XPosData[0,227] =   0
      XPosData[0,228] =   0
      XPosData[0,229] =   0
      XPosData[0,230] =   0
      XPosData[0,231] =   0
      XPosData[0,232] =   0
      XPosData[0,233] =   0
      XPosData[0,234] =   0
      XPosData[0,235] =   0
      XPosData[0,236] =   0
      XPosData[0,237] =   0
      XPosData[0,238] =   0
      XPosData[0,239] =   0
      XPosData[0,240] =   0
      XPosData[0,241] =   0
      XPosData[0,242] =   0
      XPosData[0,243] =   0
      XPosData[0,244] =   0
      XPosData[0,245] =   0
      XPosData[0,246] =   0
      XPosData[0,247] =   0
      XPosData[0,248] =   0
      XPosData[0,249] =   0
      XPosData[0,250] =   0
      XPosData[0,251] =   0
      XPosData[0,252] =   0
      XPosData[0,253] =   0
      XPosData[0,254] =   0
      XPosData[0,255] =   0
      XPosData[0,256] =   0
      XPosData[0,257] =   0
      XPosData[0,258] =   0
      XPosData[0,259] =   0
      XPosData[0,260] =   0
      XPosData[0,261] =   0
      XPosData[0,262] =   0
      XPosData[0,263] =   0
      XPosData[0,264] =   0
      XPosData[0,265] =   0
      XPosData[0,266] =   0
      XPosData[0,267] =   0
      XPosData[0,268] =   0
      XPosData[0,269] =   0
      XPosData[0,270] =   0
      XPosData[0,271] =   0
      XPosData[0,272] =   0
      XPosData[0,273] =   0
      XPosData[0,274] =   0
      XPosData[0,275] =   0
      XPosData[0,276] =   0
      XPosData[0,277] =   0
      XPosData[0,278] =   0
      XPosData[0,279] =   0
      XPosData[0,280] =   0
      XPosData[0,281] =   0
      XPosData[0,282] =   0
      XPosData[0,283] =   0
      XPosData[0,284] =   0
      XPosData[0,285] =   0
      XPosData[0,286] =   0
      XPosData[0,287] =   0
      XPosData[0,288] =   0
      XPosData[0,289] =   0
      XPosData[0,290] =   0
      XPosData[0,291] =   0
      XPosData[0,292] =   0
      XPosData[0,293] =   0
      XPosData[0,294] =   0
      XPosData[0,295] =   0
      XPosData[0,296] =   0
      XPosData[0,297] =   0
      XPosData[0,298] =   0
      XPosData[0,299] =   0
      XPosData[0,300] =   0
      XPosData[0,301] =   0
      XPosData[0,302] =   0
      XPosData[0,303] =   0
      XPosData[0,304] =   0
      XPosData[0,305] =   0
      XPosData[0,306] =   0
      XPosData[0,307] =   0
      XPosData[0,308] =   0
      XPosData[0,309] =   0
      XPosData[0,310] =   0
      XPosData[0,311] =   0
      XPosData[0,312] =   0
      XPosData[0,313] =   0
      XPosData[0,314] =   0
      XPosData[0,315] =   0
      XPosData[0,316] =   0
      XPosData[0,317] =   0
      XPosData[0,318] =   0
      XPosData[0,319] =   0
      XPosData[0,320] =   0
      XPosData[0,321] =   0
      XPosData[0,322] =   0
      XPosData[0,323] =   0
      XPosData[0,324] =   0
      XPosData[0,325] =   0
      XPosData[0,326] =   0
      XPosData[0,327] =   0
      XPosData[0,328] =   0
      XPosData[0,329] =   0
      XPosData[0,330] =   0
      XPosData[0,331] =   0
      XPosData[0,332] =   0
      XPosData[0,333] =   0
      XPosData[0,334] =   0
      XPosData[0,335] =   0
      XPosData[0,336] =   0
      XPosData[0,337] =   0
      XPosData[0,338] =   0
      XPosData[0,339] =   0
      XPosData[0,340] =   0
      XPosData[0,341] =   0
      XPosData[0,342] =   0
      XPosData[0,343] =   0
      XPosData[0,344] =   0
      XPosData[0,345] =   0
      XPosData[0,346] =   0
      XPosData[0,347] =   0
      XPosData[0,348] =   0
      XPosData[0,349] =   0
      XPosData[0,350] =   0
      XPosData[0,351] =   0
      XPosData[0,352] =   0
      XPosData[0,353] =   0
      XPosData[0,354] =   0
      XPosData[0,355] =   0
      XPosData[0,356] =   0
      XPosData[0,357] =   0
      XPosData[0,358] =   0
      XPosData[0,359] =   0
      XPosData[0,360] =   0
      XPosData[0,361] =   0
      XPosData[0,362] =   0
      XPosData[0,363] =   0
      XPosData[0,364] =   0
      XPosData[0,365] =   0
      XPosData[0,366] =   0
      XPosData[0,367] =   0
      XPosData[0,368] =   0
      XPosData[0,369] =   0
      XPosData[0,370] =   0
      XPosData[0,371] =   0
      XPosData[0,372] =   0
      XPosData[0,373] =   0
      XPosData[0,374] =   0
      XPosData[0,375] =   0
      XPosData[0,376] =   0
      XPosData[0,377] =   0
      XPosData[0,378] =   0
      XPosData[0,379] =   0
      XPosData[0,380] =   0
      XPosData[0,381] =   0
      XPosData[0,382] =   0
      XPosData[0,383] =   0
      XPosData[0,384] =   0
      XPosData[0,385] =   0
      XPosData[0,386] =   0
      XPosData[0,387] =   0
      XPosData[0,388] =   0
      XPosData[0,389] =   0
      XPosData[0,390] =   0
      XPosData[0,391] =   0
      XPosData[0,392] =   0
      XPosData[0,393] =   0
      XPosData[0,394] =   0
      XPosData[0,395] =   0
      XPosData[0,396] =   0
      XPosData[0,397] =   0
      XPosData[0,398] =   0
      XPosData[0,399] =   0
      XPosData[0,400] =   0
      XPosData[0,401] =   0
      XPosData[0,402] =   0
      XPosData[0,403] =   0
      XPosData[0,404] =   0
      XPosData[0,405] =   0
      XPosData[0,406] =   0
      XPosData[0,407] =   0
      XPosData[0,408] =   0
      XPosData[0,409] =   0
      XPosData[0,410] =   0
      XPosData[0,411] =   0
      XPosData[0,412] =   0
      XPosData[0,413] =   0
      XPosData[0,414] =   0
      XPosData[0,415] =   0
      XPosData[0,416] =   0
      XPosData[0,417] =   0
      XPosData[0,418] =   0
      XPosData[0,419] =   0
      XPosData[0,420] =   0
      XPosData[0,421] =   0
      XPosData[0,422] =   0
      XPosData[0,423] =   0
      XPosData[0,424] =   0
      XPosData[0,425] =   0
      XPosData[0,426] =   0
      XPosData[0,427] =   0
      XPosData[0,428] =   0
      XPosData[0,429] =   0
      XPosData[0,430] =   0
      XPosData[0,431] =   0
      XPosData[0,432] =   0
      XPosData[0,433] =   0
      XPosData[0,434] =   0
      XPosData[0,435] =   0
      XPosData[0,436] =   0
      XPosData[0,437] =   0
      XPosData[0,438] =   0
      XPosData[0,439] =   0
      XPosData[0,440] =   0
      XPosData[0,441] =   0
      XPosData[0,442] =   0
      XPosData[0,443] =   0
      XPosData[0,444] =   0
      XPosData[0,445] =   0
      XPosData[0,446] =   0
      XPosData[0,447] =   0
      XPosData[0,448] =   0
      XPosData[0,449] =   0
      XPosData[0,450] =   0
      XPosData[0,451] =   0
      XPosData[0,452] =   0
      XPosData[0,453] =   0
      XPosData[0,454] =   0
      XPosData[0,455] =   0
      XPosData[0,456] =   0
      XPosData[0,457] =   0
      XPosData[0,458] =   0
      XPosData[0,459] =   0
      XPosData[0,460] =   0
      XPosData[0,461] =   0
      XPosData[0,462] =   0
      XPosData[0,463] =   0
      XPosData[0,464] =   0
      XPosData[0,465] =   0
      XPosData[0,466] =   0
      XPosData[0,467] =   0
      XPosData[0,468] =   0
      XPosData[0,469] =   0
      XPosData[0,470] =   0
      XPosData[0,471] =   0
      XPosData[0,472] =   0
      XPosData[0,473] =   0
      XPosData[0,474] =   0
      XPosData[0,475] =   0
      XPosData[0,476] =   0
      XPosData[0,477] =   0
      XPosData[0,478] =   0
      XPosData[0,479] =   0
      XPosData[0,480] =   0
      XPosData[0,481] =   0
      XPosData[0,482] =   0
      XPosData[0,483] =   0
      XPosData[0,484] =   0
      XPosData[0,485] =   0
      XPosData[0,486] =   0
      XPosData[0,487] =   0
      XPosData[0,488] =   0
      XPosData[0,489] =   0
      XPosData[0,490] =   0
      XPosData[0,491] =   0
      XPosData[0,492] =   0
      XPosData[0,493] =   0
      XPosData[0,494] =   0
      XPosData[0,495] =   0
      XPosData[0,496] =   0
      XPosData[0,497] =   0
      XPosData[0,498] =   0
      XPosData[0,499] =   0
      XPosData[0,500] =   0
      XPosData[0,501] =   0
      XPosData[0,502] =   0
      XPosData[0,503] =   0
      XPosData[0,504] =   0
      XPosData[0,505] =   0
      XPosData[0,506] =   0
      XPosData[0,507] =   0
      XPosData[0,508] =   0
      XPosData[0,509] =   0
      XPosData[0,510] =   0
      XPosData[0,511] =   0
      XPosData[0,512] =   0
      XPosData[0,513] =   0
      XPosData[0,514] =   0
      XPosData[0,515] =   0
      XPosData[0,516] =   0
      XPosData[0,517] =   0
      XPosData[0,518] =   0
      XPosData[0,519] =   0
      XPosData[0,520] =   0
      XPosData[0,521] =   0
      XPosData[0,522] =   0
      XPosData[0,523] =   0
      XPosData[0,524] =   0
      XPosData[0,525] =   0
      XPosData[0,526] =   0
      XPosData[0,527] =   0
      XPosData[0,528] =   0
      XPosData[0,529] =   0
      XPosData[0,530] =   0
      XPosData[0,531] =   0
      XPosData[0,532] =   0
      XPosData[0,533] =   0
      XPosData[0,534] =   0
      XPosData[0,535] =   0
      XPosData[0,536] =   0
      XPosData[0,537] =   0
      XPosData[0,538] =   0
      XPosData[0,539] =   0
      XPosData[0,540] =   0
      XPosData[0,541] =   0
      XPosData[0,542] =   0
      XPosData[0,543] =   0
      XPosData[0,544] =   0
      XPosData[0,545] =   0
      XPosData[0,546] =   0
      XPosData[0,547] =   0
      XPosData[0,548] =   0
      XPosData[0,549] =   0
      XPosData[0,550] =   0
      XPosData[0,551] =   0
      XPosData[0,552] =   0
      XPosData[0,553] =   0
      XPosData[0,554] =   0
      XPosData[0,555] =   0
      XPosData[0,556] =   0
      XPosData[0,557] =   0
      XPosData[0,558] =   0
      XPosData[0,559] =   0
      XPosData[0,560] =   0
      XPosData[0,561] =   0
      XPosData[0,562] =   0
      XPosData[0,563] =   0
      XPosData[0,564] =   0
      XPosData[0,565] =   0
      XPosData[0,566] =   0
      XPosData[0,567] =   0
      XPosData[0,568] =   0
      XPosData[0,569] =   0
      XPosData[0,570] =   0
      XPosData[0,571] =   0
      XPosData[0,572] =   0
      XPosData[0,573] =   0
      XPosData[0,574] =   0
      XPosData[0,575] =   0
      XPosData[0,576] =   0
      XPosData[0,577] =   0
      XPosData[0,578] =   0
      XPosData[0,579] =   0
      XPosData[0,580] =   0
      XPosData[0,581] =   0
      XPosData[0,582] =   0
      XPosData[0,583] =   0
      XPosData[0,584] =   0
      XPosData[0,585] =   0
      XPosData[0,586] =   0
      XPosData[0,587] =   0
      XPosData[0,588] =   0
      XPosData[0,589] =   0
      XPosData[0,590] =   0
      XPosData[0,591] =   0
      XPosData[0,592] =   0
      XPosData[0,593] =   0
      XPosData[0,594] =   0
      XPosData[0,595] =   0
      XPosData[0,596] =   0
      XPosData[0,597] =   0
      XPosData[0,598] =   0
      XPosData[0,599] =   0
      XPosData[0,600] =   0
      XPosData[0,601] =   0
      XPosData[0,602] =   0
      XPosData[0,603] =   0
      XPosData[0,604] =   0
      XPosData[0,605] =   0
      XPosData[0,606] =   0
      XPosData[0,607] =   0
      XPosData[0,608] =   0
      XPosData[0,609] =   0
      XPosData[0,610] =   0
      XPosData[0,611] =   0
      XPosData[0,612] =   0
      XPosData[0,613] =   0
      XPosData[0,614] =   0
      XPosData[0,615] =   0
      XPosData[0,616] =   0
      XPosData[0,617] =   0
      XPosData[0,618] =   0
      XPosData[0,619] =   0
      XPosData[0,620] =   0
      XPosData[0,621] =   0
      XPosData[0,622] =   0
      XPosData[0,623] =   0
      XPosData[0,624] =   0
      XPosData[0,625] =   0
      XPosData[0,626] =   0
      XPosData[0,627] =   0
      XPosData[0,628] =   0
      XPosData[0,629] =   0
      XPosData[0,630] =   0
      XPosData[0,631] =   0
      XPosData[0,632] =   0
      XPosData[0,633] =   0
      XPosData[0,634] =   0
      XPosData[0,635] =   0
      XPosData[0,636] =   0
      XPosData[0,637] =   0
      XPosData[0,638] =   0
      XPosData[0,639] =   0
      XPosData[0,640] =   0
      XPosData[0,641] =   0
      XPosData[0,642] =   0
      XPosData[0,643] =   0
      XPosData[0,644] =   0
      XPosData[0,645] =   0
      XPosData[0,646] =   0
      XPosData[0,647] =   0
      XPosData[0,648] =   0
      XPosData[0,649] =   0
      XPosData[0,650] =   0
      XPosData[0,651] =   0
      XPosData[0,652] =   0
      XPosData[0,653] =   0
      XPosData[0,654] =   0
      XPosData[0,655] =   0
      XPosData[0,656] =   0
      XPosData[0,657] =   0
      XPosData[0,658] =   0
      XPosData[0,659] =   0
      XPosData[0,660] =   0
      XPosData[0,661] =   0
      XPosData[0,662] =   0
      XPosData[0,663] =   0
      XPosData[0,664] =   0
      XPosData[0,665] =   0
      XPosData[0,666] =   0
      XPosData[0,667] =   0
      XPosData[0,668] =   0
      XPosData[0,669] =   0
      XPosData[0,670] =   0
      XPosData[0,671] =   0
      XPosData[0,672] =   0
      XPosData[0,673] =   0
      XPosData[0,674] =   0
      XPosData[0,675] =   0
      XPosData[0,676] =   0
      XPosData[0,677] =   0
      XPosData[0,678] =   0
      XPosData[0,679] =   0
      XPosData[0,680] =   0
      XPosData[0,681] =   0
      XPosData[0,682] =   0
      XPosData[0,683] =   0
      XPosData[0,684] =   0
      XPosData[0,685] =   0
      XPosData[0,686] =   0
      XPosData[0,687] =   0
      XPosData[0,688] =   0
      XPosData[0,689] =   0
      XPosData[0,690] =   0
      XPosData[0,691] =   0
      XPosData[0,692] =   0
      XPosData[0,693] =   0
      XPosData[0,694] =   0
      XPosData[0,695] =   0
      XPosData[0,696] =   0
      XPosData[0,697] =   0
      XPosData[0,698] =   0
      XPosData[0,699] =   0
      XPosData[0,700] =   0
      XPosData[0,701] =   0
      XPosData[0,702] =   0
      XPosData[0,703] =   0
      XPosData[0,704] =   0
      XPosData[0,705] =   0
      XPosData[0,706] =   0
      XPosData[0,707] =   0
      XPosData[0,708] =   0
      XPosData[0,709] =   0
      XPosData[0,710] =   0
      XPosData[0,711] =   0
      XPosData[0,712] =   0
      XPosData[0,713] =   0
      XPosData[0,714] =   0
      XPosData[0,715] =   0
      XPosData[0,716] =   0
      XPosData[0,717] =   0
      XPosData[0,718] =   0
      XPosData[0,719] =   0
      XPosData[0,720] =   0
      XPosData[0,721] =   0
      XPosData[0,722] =   0
      XPosData[0,723] =   0
      XPosData[0,724] =   0
      XPosData[0,725] =   0
      XPosData[0,726] =   0
      XPosData[0,727] =   0
      XPosData[0,728] =   0
      XPosData[0,729] =   0
      XPosData[0,730] =   0
      XPosData[0,731] =   0
      XPosData[0,732] =   0
      XPosData[0,733] =   0
      XPosData[0,734] =   0
      XPosData[0,735] =   0
      XPosData[0,736] =   0
      XPosData[0,737] =   0
      XPosData[0,738] =   0
      XPosData[0,739] =   0
      XPosData[0,740] =   0
      XPosData[0,741] =   0
      XPosData[0,742] =   0
      XPosData[0,743] =   0
      XPosData[0,744] =   0
      XPosData[0,745] =   0
      XPosData[0,746] =   0
      XPosData[0,747] =   0
      XPosData[0,748] =   0
      XPosData[0,749] =   0
      XPosData[0,750] =   0
      XPosData[0,751] =   0
      XPosData[0,752] =   0
      XPosData[0,753] =   0
      XPosData[0,754] =   0
      XPosData[0,755] =   0
      XPosData[0,756] =   0
      XPosData[0,757] =   0
      XPosData[0,758] =   0
      XPosData[0,759] =   0
      XPosData[0,760] =   0
      XPosData[0,761] =   0
      XPosData[0,762] =   0
      XPosData[0,763] =   0
      XPosData[0,764] =   0
      XPosData[0,765] =   0
      XPosData[0,766] =   0
      XPosData[0,767] =   0
      XPosData[0,768] =   0
      XPosData[0,769] =   0
      XPosData[0,770] =   0
      XPosData[0,771] =   0
      XPosData[0,772] =   0
      XPosData[0,773] =   0
      XPosData[0,774] =   0
      XPosData[0,775] =   0
      XPosData[0,776] =   0
      XPosData[0,777] =   0
      XPosData[0,778] =   0
      XPosData[0,779] =   0
      XPosData[0,780] =   0
      XPosData[0,781] =   0
      XPosData[0,782] =   0
      XPosData[0,783] =   0
      XPosData[0,784] =   0
      XPosData[0,785] =   0
      XPosData[0,786] =   0
      XPosData[0,787] =   0
      XPosData[0,788] =   0
      XPosData[0,789] =   0
      XPosData[0,790] =   0
      XPosData[0,791] =   0
      XPosData[0,792] =   0
      XPosData[0,793] =   0
      XPosData[0,794] =   0
      XPosData[0,795] =   0
      XPosData[0,796] =   0
      XPosData[0,797] =   0
      XPosData[0,798] =   0
      XPosData[0,799] =   0
      XPosData[0,800] =   0
      XPosData[0,801] =   0
      XPosData[0,802] =   0
      XPosData[0,803] =   0
      XPosData[0,804] =   0
      XPosData[0,805] =   0
      XPosData[0,806] =   0
      XPosData[0,807] =   0
      XPosData[0,808] =   0
      XPosData[0,809] =   0
      XPosData[0,810] =   0
      XPosData[0,811] =   0
      XPosData[0,812] =   0
      XPosData[0,813] =   0
      XPosData[0,814] =   0
      XPosData[0,815] =   0
      XPosData[0,816] =   0
      XPosData[0,817] =   0
      XPosData[0,818] =   0
      XPosData[0,819] =   0
      XPosData[0,820] =   0
      XPosData[0,821] =   0
      XPosData[0,822] =   0
      XPosData[0,823] =   0
      XPosData[0,824] =   0
      XPosData[0,825] =   0
      XPosData[0,826] =   0
      XPosData[0,827] =   0
      XPosData[0,828] =   0
      XPosData[0,829] =   0
      XPosData[0,830] =   0
      XPosData[0,831] =   0
      XPosData[0,832] =   0
      XPosData[0,833] =   0
      XPosData[0,834] =   0
      XPosData[0,835] =   0
      XPosData[0,836] =   0
      XPosData[0,837] =   0
      XPosData[0,838] =   0
      XPosData[0,839] =   0
      XPosData[0,840] =   0
      XPosData[0,841] =   0
      XPosData[0,842] =   0
      XPosData[0,843] =   0
      XPosData[0,844] =   0
      XPosData[0,845] =   0
      XPosData[0,846] =   0
      XPosData[0,847] =   0
      XPosData[0,848] =   0
      XPosData[0,849] =   0
      XPosData[0,850] =   0
      XPosData[0,851] =   0
      XPosData[0,852] =   0
      XPosData[0,853] =   0
      XPosData[0,854] =   0
      XPosData[0,855] =   0
      XPosData[0,856] =   0
      XPosData[0,857] =   0
      XPosData[0,858] =   0
      XPosData[0,859] =   0
      XPosData[0,860] =   0
      XPosData[0,861] =   0
      XPosData[0,862] =   0
      XPosData[0,863] =   0
      XPosData[0,864] =   0
      XPosData[0,865] =   0
      XPosData[0,866] =   0
      XPosData[0,867] =   0
      XPosData[0,868] =   0
      XPosData[0,869] =   0
      XPosData[0,870] =   0
      XPosData[0,871] =   0
      XPosData[0,872] =   0
      XPosData[0,873] =   0
      XPosData[0,874] =   0
      XPosData[0,875] =   0
      XPosData[0,876] =   0
      XPosData[0,877] =   0
      XPosData[0,878] =   0
      XPosData[0,879] =   0
      XPosData[0,880] =   0
      XPosData[0,881] =   0
      XPosData[0,882] =   0
      XPosData[0,883] =   0
      XPosData[0,884] =   0
      XPosData[0,885] =   0
      XPosData[0,886] =   0
      XPosData[0,887] =   0
      XPosData[0,888] =   0
      XPosData[0,889] =   0
      XPosData[0,890] =   0
      XPosData[0,891] =   0
      XPosData[0,892] =   0
      XPosData[0,893] =   0
      XPosData[0,894] =   0
      XPosData[0,895] =   0
      XPosData[0,896] =   0
      XPosData[0,897] =   0
      XPosData[0,898] =   0
      XPosData[0,899] =   0
      XPosData[0,900] =   0
      XPosData[0,901] =   0
      XPosData[0,902] =   0
      XPosData[0,903] =   0
      XPosData[0,904] =   0
      XPosData[0,905] =   0
      XPosData[0,906] =   0
      XPosData[0,907] =   0
      XPosData[0,908] =   0
      XPosData[0,909] =   0
      XPosData[0,910] =   0
      XPosData[0,911] =   0
      XPosData[0,912] =   0
      XPosData[0,913] =   0
      XPosData[0,914] =   0
      XPosData[0,915] =   0
      XPosData[0,916] =   0
      XPosData[0,917] =   0
      XPosData[0,918] =   0
      XPosData[0,919] =   0
      XPosData[0,920] =   0
      XPosData[0,921] =   0
      XPosData[0,922] =   0
      XPosData[0,923] =   0
      XPosData[0,924] =   0
      XPosData[0,925] =   0
      XPosData[0,926] =   0
      XPosData[0,927] =   0
      XPosData[0,928] =   0
      XPosData[0,929] =   0
      XPosData[0,930] =   0
      XPosData[0,931] =   0
      XPosData[0,932] =   0
      XPosData[0,933] =   0
      XPosData[0,934] =   0
      XPosData[0,935] =   0
      XPosData[0,936] =   0
      XPosData[0,937] =   0
      XPosData[0,938] =   0
      XPosData[0,939] =   0
      XPosData[0,940] =   0
      XPosData[0,941] =   0
      XPosData[0,942] =   0
      XPosData[0,943] =   0
      XPosData[0,944] =   0
      XPosData[0,945] =   0
      XPosData[0,946] =   0
      XPosData[0,947] =   0
      XPosData[0,948] =   0
      XPosData[0,949] =   0
      XPosData[0,950] =   0
      XPosData[0,951] =   0
      XPosData[0,952] =   0
      XPosData[0,953] =   0
      XPosData[0,954] =   0
      XPosData[0,955] =   0
      XPosData[0,956] =   0
      XPosData[0,957] =   0
      XPosData[0,958] =   0
      XPosData[0,959] =   0
      XPosData[0,960] =   0
      XPosData[0,961] =   0
      XPosData[0,962] =   0
      XPosData[0,963] =   0
      XPosData[0,964] =   0
      XPosData[0,965] =   0
      XPosData[0,966] =   0
      XPosData[0,967] =   0
      XPosData[0,968] =   0
      XPosData[0,969] =   0
      XPosData[0,970] =   0
      XPosData[0,971] =   0
      XPosData[0,972] =   0
      XPosData[0,973] =   0
      XPosData[0,974] =   0
      XPosData[0,975] =   0
      XPosData[0,976] =   0
      XPosData[0,977] =   0
      XPosData[0,978] =   0
      XPosData[0,979] =   0
      XPosData[0,980] =   0
      XPosData[0,981] =   0
      XPosData[0,982] =   0
      XPosData[0,983] =   0
      XPosData[0,984] =   0
      XPosData[0,985] =   0
      XPosData[0,986] =   0
      XPosData[0,987] =   0
      XPosData[0,988] =   0
      XPosData[0,989] =   0
      XPosData[0,990] =   0
      XPosData[0,991] =   0
      XPosData[0,992] =   0
      XPosData[0,993] =   0
      XPosData[0,994] =   0
      XPosData[0,995] =   0
      XPosData[0,996] =   0
      XPosData[0,997] =   0
      XPosData[0,998] =   0
      XPosData[0,999] =   0
      XPosData[0,1000]=   0
      XPosData[0,1001]=   0
      XPosData[0,1002]=   0
      XPosData[0,1003]=   0
      XPosData[0,1004]=   0
      XPosData[0,1005]=   0
      XPosData[0,1006]=   0
      XPosData[0,1007]=   0
      XPosData[0,1008]=   0
      XPosData[0,1009]=   0
      XPosData[0,1010]=   0
      XPosData[0,1011]=   0
      XPosData[0,1012]=   0
      XPosData[0,1013]=   0
      XPosData[0,1014]=   0
      XPosData[0,1015]=   0
      XPosData[0,1016]=   0
      XPosData[0,1017]=   0
      XPosData[0,1018]=   0
      XPosData[0,1019]=   0
      XPosData[0,1020]=   0
      XPosData[0,1021]=   0
      XPosData[0,1022]=   0
      XPosData[0,1023]=   0
   End
   Begin VB.Timer Timer1 
      Interval        =   100
      Left            =   5160
      Top             =   1200
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
      Top             =   2760
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
      Top             =   2760
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
      Top             =   2760
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
      Top             =   1560
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
      Text            =   "0.1"
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
      Height          =   2295
      Left            =   4200
      MultiLine       =   -1  'True
      TabIndex        =   14
      Top             =   120
      Width           =   3975
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
      TabIndex        =   11
      Top             =   1920
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
      TabIndex        =   12
      Top             =   2280
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
      TabIndex        =   10
      Top             =   1560
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
      TabIndex        =   9
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
'This application demonstrates how to program InstaSpec to
'acquire a Single Scan, Full Resolution Image.  The main priority,
'however, is to demonstrate how to configure InstaSpec to incorporate
'a shutter.
'The use of a shutter when acquiring data (other than FVB scans)
'is essential to prevent smearing the data whilst binning it from
'the sensor.
'
'The user may specify the exposure time,type of Trigger
'pulse (either Internal or External) and type of TTL pulse to
'open the shutter with.  Internal Trigger is the simplest
'triggering option and allows the computer to generate its
'own trigger pulse.  In External trigger mode the user MUST
'supply their own triggering pulse (eg from a laser or lamp
'source).
'
'All InstaSpec driver calls are in functions preceded by the
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

  pbDisplayRow.Enabled = False
  newLine = Chr(13) & Chr(10)
  PrintStatusMsg ("* SINGLE SCAN * IMAGE MODE * AUTO SHUTTER *")
  InitializeInstaSpec         'Initialize InstaSpec system
End Sub

Sub InitializeInstaSpec()
'**************************************************************
' Initialize InstaSpec system.  The way to "read" this code,
' assuming no error occurs, is simply:
' 1) Initialize InstaSpec hardware.
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

Sub ebCCDRow_Change()
  row = Val(ebCCDRow.text)
  If (row < 1 Or row > nYPixels) Then
    ebCCDRow.text = Str(1)
  End If
End Sub

Function vbAbortAcq()
'**************************************************************
' Tells InstaSpec to abort acquisition.
'**************************************************************
  vbAbortAcq = Not LOCALERROR
  test = AbortAcquisition()
  If (test <> DRV_SUCCESS) Then
    buffer = "Abort ERROR: "
    vbAbortAcq = LOCALERROR
    Select Case (test)
      Case DRV_IDLE
        buffer = buffer & "InstaSpec isn't acquiring data."
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
    nYPixels = ypixels
    nXPixels = xpixels
  Else
    buffer = "Format ERROR: Can't read CCD format."
    vbGetDetector = LOCALERROR
  End If
  PrintStatusMsg (buffer)
End Function

Function vbGetStatus()
'***************************************************************
'Interrogates InstaSpec to determine if acquisition is complete
'***************************************************************
  Dim status As Long
  vbGetStatus = Not LOCALERROR
  test = GetStatus(status)
  If (test <> DRV_SUCCESS) Then
    vbGetStatus = LOCALERROR
    buffer = "Data ERROR: Can't get current status of drivers."
    PrintStatusMsg (buffer)
  End If
  If (status = DRV_IDLE) Then
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
'Get actual Exposure time used by InstaSpec.  InstaSpec
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
    buf = newLine & "**Actual Exposure Time = " & Str(exposure) & " secs"
    buf = buf & newLine
  End If
  ebStatusBox.text = buf
End Function

Function vbInitialize()
'**************************************************************
' Initializes the InstaSpec system.  Need the files "Detector.ini
' and "pci_29k.cof" in YOUR current working directory.
'
' NOTE: The A/D converter in the InstaSpec card takes ~ 2 secs
' to autocalibrate, thus the initializing procedure lasts ~ 2secs.
'**************************************************************
  test = Initialize("")
  vbInitialize = Not LOCALERROR
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
    buffer = "Initializing InstaSpec system"
  End If
  PrintStatusMsg (buffer)
End Function

Function vbSetAcquisition()
'**************************************************************
' Configure InstaSepc to operate in Single Scan mode.
'**************************************************************
  vbSetAcquisition = Not LOCALERROR
  test = SetAcquisitionMode(1)      'Single Scan
  If test = DRV_SUCCESS Then
    buffer = "Set Acquisition Mode to Single Scan"
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
' Configure InstaSpec with user's exposure time.
'
' InstaSpec defaults to a minimum exposure time should you
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
        buffer = buffer & " InstaSpec system isn't initialized."
      Case DRV_ACQUIRING
        buffer = buffer & " Exposure time Warning" & newLine
        buffer = buffer & "InstaSpec is currently acquiring data"
      Case DRV_ERROR_ACK
        buffer = buffer & " Exposure time not accepted"
      Case Else
        buffer = buffer & "Unknown Exposure Time Error."
    End Select
    PrintStatusMsg (buffer)
  End If
End Function

Function vbSetReadout()
'**************************************************************
' Configure InstaSpec to Full Resolution Image.
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
' calculated by InstaSpec.
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
'Tells InstaSpec the type of trigger pulse to expect.  Internal means
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
  test = SetImage(1, 1, 1, nXPixels, 1, nYPixels)
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
' Tells InstaSpec to begin Acquisition upon receipt of a trigger
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

Sub GetRowCCDData(row As Long)
'*********************************************************************
'Visual Basic 3.0 has a limitation in the the number of elements it can
'store in an array: ie 65536 elements (which = one dimension).
'But it can store up to a maximum of 60 such dimensions so for a CCD
'sensor of format 1024x256 pixels (=262144 elements) its possible to
'create a 2D array to store the data.
'
'For the CCD sensor example above a 2D array of size 1024 x 256
'would easily meet the Visual Basic constraints.

'This function assumes the array 2D format matches the CCD chip format
'and retrieves a full row of the CCD from the 2D array aData.
'*********************************************************************
  ReDim aRowData(nXPixels)
  For i = 1 To nXPixels
    aRowData(i) = aData(i, row)
  Next i
End Sub

Function LoadData()
'**************************************************************
' After IMAGEGetStatus() confirms the data acquisition is
' COMPLETE then LoadData() gets the data from the InstaSpec
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
  ReDim aData(1 To nXPixels, 1 To nYPixels)
  test = GetAcquiredData(aData(1, 1), nXPixels * nYPixels)
  If test = DRV_P2INVALID Then
    buffer = "ERROR: aData size is too small"
    LoadData = LOCALERROR
    PrintStatusMsg (buffer)
    Exit Function
  Else
    PrintStatusMsg ("Acquired data!")
    PlotData
  End If
End Function

Sub pbAbortAcq_Click(index As Integer)
'**************************************************************
'  Response function for "Abort Acq" button.  Switches OFF the
'  timer flag if appropriate and tells InstaSpec to abort
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
    PrintStatusMsg ("ERROR: Can't close InstaSpec system down properly")
    Exit Sub
  End If
  End
End Sub

Sub pbDisplayRow_Click()
  PlotData
End Sub

Sub pbStartAcq_Click(index As Integer)
'*************************************************************************************
'This routine is the heart of the Image application.  It configures the InstaSpec
'system with the user's choices and tells it to begin the acquisition upon arrival
'of a trigger pulse (may be Internal or External).  NB if you choose External
'triggering then YOU must supply the trigger pulse to the InstaSpec system.

'The computer is programmed to monitor the state of the acquisition every (eg) 100
'millisecs: this ensures the acquisition is complete before reading in the data.
'Thus every 100 ms the computer is directed to the Timer procedure and hence to
'vbGetStatus().

'After successfully acquiring the data the time "flag" (ie StartTimer) is switched
'off in readiness for a new scan.
'**************************************************************************************
  pbDisplayRow.Enabled = False
  If (StartTimer = XON) Then
    PrintStatusMsg ("Warning: Already acquiring data...")
    Exit Sub
  End If
  If (StartTimer = XOFF) Then
    DataDisplay.DrawMode = 1 '   EraseOldgraph
    If (vbSetTimings() = LOCALERROR) Then
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
  DataDisplay.DataReset = 9
  DataDisplay.PatternData = 0
  DataDisplay.NumPoints = nXPixels
  index = Val(ebCCDRow.text)
  GetRowCCDData (index)
  For i = 1 To nXPixels
    DataDisplay.GraphData = aRowData(i)
  Next i
  MinY = aRowData(1)
  MaxY = aRowData(1)
  For i = 1 To nXPixels
    If (aRowData(i) >= MaxY) Then
      MaxY = aRowData(i)
    End If
    If (aRowData(i) <= MinY) Then
      MinY = aRowData(i)
    End If
  Next i
  DataDisplay.NumSets = 1
  DataDisplay.YAxisMin = MinY
  DataDisplay.YAxisMax = MaxY
  DataDisplay.YAxisStyle = 2
  DataDisplay.Ticks = 0
  DataDisplay.TickEvery = 100
  DataDisplay.DrawMode = 2
  pbDisplayRow.Enabled = True
End Sub

Sub PrintStatusMsg(buffer As String)
'**************************************************************
' Updates the StatusBox with messages corresponding to the
' application flow.
'**************************************************************
  buf = buf & newLine & buffer
  ebStatusBox.text = buf
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


