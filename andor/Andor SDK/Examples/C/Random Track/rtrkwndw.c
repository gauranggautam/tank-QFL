//------------------------------------------------------------------------------
//  PROJECT:		32-bit Driver Example Code ---- Random Track Acquisition(idus)
//
//  Copyright 1998. All Rights Reserved
//
//  FILE:			RtrkWndw.c
//  AUTHOR:			Dermot McCluskey
//
//  OVERVIEW:		This Project shows how to set up the Andor MCD to acquire a
//							number of tracks. It will	familiarise you with using the Andor
//							MCD driver library.
//------------------------------------------------------------------------------

#include <windows.h>            // required for all Windows applications
#include <stdio.h>              // required for sprintf()
#include "atmcd32d.h"           // Andor function definitions

// Function Prototypes
BOOL CreateWindows(void);            // Create control windows and allocate handles
void SetupWindows(void);             // Initialize control windows
void SetWindowsToDefault(char[256]);// Fills windows with default values
void SetSystem(void);                // Sets hardware parameters
void ProcessTimer(WPARAM);        // Handles WM_TIMER messages
void ProcessPushButtons(LPARAM);  // Processes button presses
void UpdateDialogWindows(void);      // refreshes all windows
void FillRectangle(void);            // clears paint area
BOOL AcquireImageData(void);         // Acquires data from card
void PaintDataWindow(void);       // Prepares paint area on screen
BOOL DrawLines(int trackNo,long*,long*);   // paints data to screen
int AllocateBuffers(void);           // Allocates memory for buffers
void FreeBuffers(void);              // Frees allocated memory
BOOL ProcessMessages(UINT message, WPARAM wparam, LPARAM lparam){return FALSE;} // No messages to process in this example
void AddNewTrack(void);
void ResetTracks(void);

// Set up acquisition parameters here to be set in common.c *****************
int acquisitionMode=1;   //single
int readMode=2;          //random
int xWidth=640;		 // width of application window passed to common.c
int yHeight=480;   // height of application window passed to common.c
//******************************************************************************

extern AndorCapabilities caps;         // Get AndorCapabilities structure from common.c
extern char              model[32];    // Get Head Model from common.c
extern int 	             gblXPixels;   // Get dims from common.c
extern int               gblYPixels;
extern int               VSnumber;     // Get speeds from common.c
extern int               HSnumber;
extern int               ADnumber;

//few globals fro rendom track
int iRandomTrackArray[60];
int iRandomTrackCount;
char displayBuf[512];
BOOL bTrackBeenAdded = FALSE;

// Declare Image Buffers
long *pImageArray = NULL;  // main image buffer read from card
POINT *pPointsArray = NULL;// points data required to draw one polyline

int timer=100;         		 // ID of timer that checks status before acquisition

BOOL errorFlag;				   	 // Tells us if initialization failed in common.c
BOOL gblData=FALSE;      	 // flag is set when first acquisition is taken, tells
											 		 //	system that there is data to display

RECT rect;             		 // dims of paint area

extern HWND hwnd;          // Handle to main application

HWND				ebInit,        // handles for the individual
            stInit,        // windows such as edit boxes
            ebExposure,    // and comboboxes etc.
            stExposure,
            stRandomTracks,
            stStartTrack,
            ebStartTrack,
            stEndTrack,
            ebEndTrack,
            ebOpenClose,
            stOpenClose,
            cbTTL,
            stTTL,
            ebStatus,
            stStatus,
            pbStart,
            pbAbort,
            pbClose,
            pbAddRandomTrack,
            pbResetRandomTrack,
            stSelTrack,
            ebSelTrack,
            pbShowTrackUp,
            pbShowTrackDown,
            st1,
            stWidth,
            stFrame;



extern HINSTANCE hInst;    // Current Instance

//------------------------------------------------------------------------------
//	FUNCTION NAME:	CreateWindows()
//
//  RETURNS:				TRUE: Successful
//									FALSE: Unsuccessful
//
//  LAST MODIFIED:	PMcK	09/11/98
//
//  DESCRIPTION:    This function creates the individual controls placed in the
//									main window. i.e. Comboboxes, edit boxes etc. When they are
//									created they are issued a handle which is stored in it's
//									global variable.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

BOOL CreateWindows(void)
{
  char 				aBuffer[256];
  HINSTANCE 	hInstance=hInst;

  wsprintf(aBuffer,"%d",gblXPixels);   // to be placed in txtWidth

  // Create windows for each control and store the handle names
  stInit=CreateWindow("STATIC","Initialization Information",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,2,300,18,hwnd,0,hInstance,NULL);
  ebInit=CreateWindow("EDIT","",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          10,20,320,20,hwnd,0,hInstance,NULL);
  stExposure=CreateWindow("STATIC","Exposure time (secs):",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,50,160,20,hwnd,0,hInstance,NULL);
  ebExposure=CreateWindow("EDIT","",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          270,50,50,20,hwnd,0,hInstance,NULL);

  stRandomTracks=CreateWindow("STATIC","Add Tracks 1 at a time",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,80,150,20,hwnd,0,hInstance,NULL);
  stStartTrack=CreateWindow("STATIC","Start Position",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          30,110,100,20,hwnd,0,hInstance,NULL);
  ebStartTrack=CreateWindow("EDIT","",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          130,110,50,20,hwnd,0,hInstance,NULL);
  stEndTrack=CreateWindow("STATIC","End Position",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          30,140,100,20,hwnd,0,hInstance,NULL);
  ebEndTrack=CreateWindow("EDIT","",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          130,140,50,20,hwnd,0,hInstance,NULL);
  pbAddRandomTrack=CreateWindow("BUTTON","AddTrack",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          230,90,90,30,hwnd,0,hInstance,NULL);
  pbResetRandomTrack=CreateWindow("BUTTON","Reset",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          230,130,90,30,hwnd,0,hInstance,NULL);
  stOpenClose=CreateWindow("STATIC","Open / Close Time (msecs):",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,170,180,20,hwnd,0,hInstance,NULL);
  ebOpenClose=CreateWindow("EDIT","0",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          270,170,50,20,hwnd,0,hInstance,NULL);
  stTTL=CreateWindow("STATIC","Shutter opens on:",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,200,180,20,hwnd,0,hInstance,NULL);
  cbTTL=CreateWindow("COMBOBOX","",
                          WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
                          240,200,80,60,hwnd,0,hInstance,NULL);
  ebStatus=CreateWindow("EDIT","",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_MULTILINE,
                          340,20,270,205,hwnd,0,hInstance,NULL);
  pbStart=CreateWindow("BUTTON","Start Acq",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          10,240,90,30,hwnd,0,hInstance,NULL);
  pbAbort=CreateWindow("BUTTON","Abort Acq",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          120,240,90,30,hwnd,0,hInstance,NULL);
  pbClose=CreateWindow("BUTTON","Close",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          230,240,90,30,hwnd,0,hInstance,NULL);
  stStatus=CreateWindow("STATIC","Status",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          340,2,60,18,hwnd,0,hInstance,NULL);
  stFrame=CreateWindow("STATIC","Status",
                          WS_CHILD|WS_VISIBLE|SS_BLACKFRAME,
                          340,240,270,30,hwnd,0,hInstance,NULL);
  stSelTrack=CreateWindow("STATIC","Acquired track to display?",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          345,247,180,20,hwnd,0,hInstance,NULL);
  ebSelTrack=CreateWindow("EDIT","0",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          538,245,45,20,hwnd,0,hInstance,NULL);
  pbShowTrackUp=CreateWindow("BUTTON","+",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          588,242,20,12,hwnd,0,hInstance,NULL);
  pbShowTrackDown=CreateWindow("BUTTON","-",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          588,256,20,12,hwnd,0,hInstance,NULL);
  st1=CreateWindow("STATIC","1",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,440,20,20,hwnd,0,hInstance,NULL);

  stWidth=CreateWindow("STATIC",aBuffer,WS_CHILD|WS_VISIBLE|SS_LEFT,
                                  590,440,40,20,hwnd,0,hInstance,NULL);

  SetupWindows();    	 // fill windows with default data

  iRandomTrackCount=0;

  return TRUE;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetupWindows()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	09/11/98
//
//  DESCRIPTION:    This function fills the created windows with their initial
//									data.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void SetupWindows(void)
{
  char 	aInitializeString[256];

  if(!errorFlag){
    // Fill Combo Boxes and Edit Boxes according to acquisition parameters
    switch(acquisitionMode){
      case 1:
        wsprintf(aInitializeString,"*SingleScan");
        break;
      case 2:
        wsprintf(aInitializeString,"*Accumulations");
        break;
      case 3:
        wsprintf(aInitializeString,"*Kinetics");
        break;
      default:
        wsprintf(aInitializeString,"DO NOT USE");
        break;
    }
    switch(readMode){
      case 0:
        strcat(aInitializeString,"*FVB");
        break;
      case 1:
        strcat(aInitializeString,"*MultiTrack");
        break;
      case 2:
        strcat(aInitializeString,"*RandomTrack");
        break;
      case 3:
        strcat(aInitializeString,"*SingleTrack");
        break;
      case 4:
        strcat(aInitializeString,"*Imaging");
        break;
      default:
        strcat(aInitializeString,"DO NOT USE");
        break;
    }
    SetWindowsToDefault(aInitializeString);
  }
  // Could not initialize
  else{
  	wsprintf(aInitializeString,"Initialization failed");
    SendMessage(ebStatus, WM_SETTEXT, 0, (LPARAM)(LPSTR)aInitializeString);
  }
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetWindowsToDefault()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	09/11/98
//
//  DESCRIPTION:    This function fills the created windows with their initial
//									default settings.
//
//	ARGUMENTS: 			Char aInitializeString: Message to be displayed in init
//																					edit box
//------------------------------------------------------------------------------

void SetWindowsToDefault(char aInitializeString[256])
{
  char aBuffer[256];
  char aBuffer2[256];
  float speed;
  
  // add *autoshutter and send to window
  strcat(aInitializeString,"*Auto Shutter");
  SendMessage(ebInit, WM_SETTEXT, 0, (LPARAM)(LPSTR)aInitializeString);

  // Fill in default exposure time
  wsprintf(aBuffer,"0.1");
  SendMessage(ebExposure, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default for random tracks
  wsprintf(aBuffer,"1");
  SendMessage(ebStartTrack, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"5");
  SendMessage(ebEndTrack, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);


  // Fill in default open close time
  wsprintf(aBuffer,"0");
  SendMessage(ebOpenClose, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default track to display
  wsprintf(aBuffer,"1");
  SendMessage(ebSelTrack, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Add options to ttl combobox
  wsprintf(aBuffer,"High");
  SendMessage(cbTTL, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"Low");
  SendMessage(cbTTL, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);

  // Select high as deault for ttl level
  wsprintf(aBuffer,"High");
  SendMessage(cbTTL, CB_SELECTSTRING,0,(LPARAM)(LPSTR)aBuffer);

  // Print Status messages
  wsprintf(aBuffer,"Head Model %s\r\n", model);
  strcat(aBuffer,"Initializing Andor MCD system\r\n");
  strcat(aBuffer,"Single Scan Selected\r\n");
  strcat(aBuffer,"Set to RandomTrack Mode\r\n");
  wsprintf(aBuffer2,"Size of CCD: %d x %d\r\n",gblXPixels,gblYPixels);
  strcat(aBuffer,aBuffer2);
  GetVSSpeed(VSnumber, &speed);
  sprintf(aBuffer2,"Vertical Speed set to %g microseconds per pixel shift\r\n",speed);
  strcat(aBuffer,aBuffer2);
  GetHSSpeed(ADnumber, 0, HSnumber, &speed);
  if(caps.ulCameraType == 1)       // if using an iXon the speed is given in MHz
    sprintf(aBuffer2,"Horizontal Speed set to %g MHz\r\n",speed);
  else
    sprintf(aBuffer2,"Horizontal Speed set to %g microseconds per pixel shift\r\n",speed);
  strcat(aBuffer,aBuffer2);
  SendMessage(ebStatus, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetSystem()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function sets up the acquisition settings exposure time
//									and shutter and starts an acquisition. It also starts a
//									timer to check when the acquisition has finished.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void SetSystem(void)
{
  float		fExposure,fAccumTime,fKineticTime;
  int 		errorValue;
  int 		openclose,ttl,shutter;
  char 		aBuffer[256];
  char 		aBuffer2[256];
  int 		bottom,gap;


  errorValue = SetRandomTracks((iRandomTrackCount)/2,&iRandomTrackArray[0]);
  if(errorValue!=DRV_SUCCESS) {
    strcat(aBuffer,"Set Random Track error\r\n");
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    UpdateWindow(ebStatus);
    return;
  }

  // Set Exposure Time
  GetWindowText(ebExposure,aBuffer2, 10);
  fExposure=atof(aBuffer2);
  errorValue = SetExposureTime(fExposure);
  if (errorValue != DRV_SUCCESS)
    wsprintf(aBuffer,"Exposure time error\r\n");

  // It is necessary to get the actual times as the system will calculate the
  // nearest possible time. eg if you set exposure time to be 0, the system
  // will use the closest value (around 0.01s)
  GetAcquisitionTimings(&fExposure,&fAccumTime,&fKineticTime);
  wsprintf(aBuffer,"Actual Exposure Time is ");
  gcvt(fExposure,5,aBuffer2);
  strcat(aBuffer,aBuffer2);
  strcat(aBuffer,"\r\n");

   // Set Shutter is made up of ttl level, shutter and open close time
  shutter=0;  // fully automatic!

  // Get Open close time
  GetWindowText(ebOpenClose,aBuffer2,10);
  openclose=atoi(aBuffer2);
  if(openclose==0)
    openclose=1;

  // Get ttl level
  GetWindowText(cbTTL,aBuffer2,10);
  if(strcmp(aBuffer2,"Low")==0)
    ttl=0;
  if(strcmp(aBuffer2,"High")==0)
    ttl=1;

  // Set shutter
  errorValue=SetShutter(ttl,shutter,openclose,openclose);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Shutter error\r\n");
  else
    strcat(aBuffer,"Shutter set to specifications\r\n");

  // Starting the acquisition also starts a timer which checks the card status
  // When the acquisition is complete the data is read from the card and
  // displayed in the paint area.
  errorValue=StartAcquisition();
  if(errorValue!=DRV_SUCCESS){
    strcat(aBuffer,"Start acquisition error\r\n");
    AbortAcquisition();
    gblData=FALSE;
  }
  else{
    strcat(aBuffer,"Starting acquisition........");
    SetTimer(hwnd,timer,100,NULL);
  }
  SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
  UpdateWindow(ebStatus);

}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	ProcessTimer()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	12/11/98
//
//  DESCRIPTION:    This function handles the messages sent by the timer(s)
//
//	ARGUMENTS: 			WPARAM wparam: The timer id
//------------------------------------------------------------------------------

void ProcessTimer(WPARAM wparam)
{
	int 	status;
  char 	aBuffer[256];

  switch(wparam){

    case 100:
      GetStatus(&status);
      if(status==DRV_IDLE){
        if(AcquireImageData()==FALSE){
          wsprintf(aBuffer,"Acquisition Error!");
          SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
        }
      }
      break;

    default:
    	break;
  }
}
  
//------------------------------------------------------------------------------
//	FUNCTION NAME:	ProcessPushButtons()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	12/11/98
//
//  DESCRIPTION:    This function handles the messages sent by the pushbuttons
//
//	ARGUMENTS: 			LPARAM lparam: The button id
//------------------------------------------------------------------------------

void ProcessPushButtons(LPARAM lparam)
{
	int 	errorValue;
  char	aBuffer[256];
  int 	status;
  int		trackNo;//,noTracks
  long	MaxValue;
  long	MinValue;

  if(lparam==(LPARAM)pbAddRandomTrack){
    AddNewTrack();
  }

  if(lparam==(LPARAM)pbResetRandomTrack){
    ResetTracks();
  }

  if(lparam==(LPARAM)pbStart){  // Start acquisition button is pressed
    if (bTrackBeenAdded == FALSE) {
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"No Tracks added yet");
      return;
    }
    gblData=TRUE;						// tells system an acq has taken place
    GetStatus(&status);
    if(status==DRV_IDLE){
      SetSystem();            	// Set hardware and start acquisition
      FillRectangle();        	// clear window ready for data trace
    }
    wsprintf(aBuffer,"1");       // Display track 1 after acq
    SendMessage(ebSelTrack,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
  }

  if(lparam==(LPARAM)pbAbort){
    // abort acquisition if in progress
    GetStatus(&status);
    if(status==DRV_ACQUIRING){
      errorValue=AbortAcquisition();
      if(errorValue!=DRV_SUCCESS){
        wsprintf(aBuffer,"Error aborting acquistion");
        SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      }
      else{
        wsprintf(aBuffer,"Aborting Acquisition");
        SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      }
      gblData=FALSE;    // tell system no acq data in place
    }
    // or else let user know none is in progress
    else{
      wsprintf(aBuffer,"System not Acquiring");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    }
  }

  if(lparam==(LPARAM)pbClose){  // close application
    DestroyWindow(hwnd);
  }

  if(lparam==(LPARAM)pbShowTrackUp){
    // only if data exists
    if(gblData){
      FillRectangle();     								 // clear window

      GetWindowText(ebSelTrack,aBuffer,10);  // which accum to display
      trackNo=atoi(aBuffer);
      if((trackNo+1)>iRandomTrackCount/2)
        trackNo=(iRandomTrackCount/2)-1;
      if(DrawLines(trackNo+1,&MaxValue,&MinValue)==FALSE){         // draw accum data
      	wsprintf(aBuffer, "Data range is zero");
      	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      }
      wsprintf(aBuffer,"%d",trackNo+1);
      SendMessage(ebSelTrack,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    }
  }

  if(lparam==(LPARAM)pbShowTrackDown){
    // only if data exists
    if(gblData){
      FillRectangle();     								 // clear window

      GetWindowText(ebSelTrack,aBuffer,10);  // which accum to display
      trackNo=atoi(aBuffer);
      if(DrawLines(trackNo-1,&MaxValue,&MinValue)==FALSE){         // draw accum data
      	wsprintf(aBuffer, "Data range is zero");
      	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      }
      if(trackNo==1)
        trackNo=2;
      wsprintf(aBuffer,"%d",trackNo-1);
      SendMessage(ebSelTrack,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    }
  }
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	ResetTracks()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:
//
//  DESCRIPTION:    This function will reset the counter for the number of tracks
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------
void ResetTracks(void)
{
  iRandomTrackCount=0;
  SendMessage(ebStatus, WM_SETTEXT, 0, (LPARAM)(LPSTR)"");
  bTrackBeenAdded = FALSE;

}


//------------------------------------------------------------------------------
//	FUNCTION NAME:	AddNewTrack()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:
//
//  DESCRIPTION:    This function will add a new track to the random track
//                  structure if its valid
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void AddNewTrack()
{
  int istartTrack,iendTrack;
  char aBuffer[100];
  char TBuffer[512];
  BOOL bInvalid = FALSE;

  if (iRandomTrackCount==0)
    strcpy(displayBuf,"");

  strcpy(TBuffer,"(");
  GetWindowText(ebStartTrack,aBuffer,10);
  strcat(TBuffer,aBuffer);
  strcat(TBuffer,",");
  istartTrack=atoi(aBuffer);

  GetWindowText(ebEndTrack,aBuffer,10);
  strcat(TBuffer,aBuffer);
  iendTrack=atoi(aBuffer);
  strcat(TBuffer,") ");


  if ((istartTrack < 1) || (iendTrack < 1))
    bInvalid = TRUE;

  if ((istartTrack >= gblYPixels) || (iendTrack >= gblYPixels))
    bInvalid = TRUE;

  if (iendTrack < istartTrack)
    bInvalid = TRUE;

  if (iRandomTrackCount > 0) {
    if (iendTrack <= iRandomTrackArray[iRandomTrackCount-1])
      bInvalid = TRUE;

    if (istartTrack <= iRandomTrackArray[iRandomTrackCount-1])
      bInvalid = TRUE;
  }

  if (bInvalid == TRUE) {
    SendMessage(ebStatus, WM_SETTEXT, 0, (LPARAM)(LPSTR)"Invalid track");
    return;
  }

  iRandomTrackArray[iRandomTrackCount] = istartTrack;
  iRandomTrackCount++;
  iRandomTrackArray[iRandomTrackCount] = iendTrack;
  iRandomTrackCount++;


  strcat(displayBuf,TBuffer);

  SendMessage(ebStatus, WM_SETTEXT, 0, (LPARAM)(LPSTR)displayBuf);

  bTrackBeenAdded = TRUE;





}


//------------------------------------------------------------------------------
//	FUNCTION NAME:	UpdateDialogWindows()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function updates the individual windows and is called
//									from inside the WM_PAINT message. This ensures that the windows
//									are present when the window is re-drawn.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void UpdateDialogWindows(void)
{
  UpdateWindow(ebInit);
  UpdateWindow(stInit);
  UpdateWindow(ebExposure);
  UpdateWindow(stExposure);
  UpdateWindow(stRandomTracks);
  UpdateWindow(stStartTrack);
  UpdateWindow(ebStartTrack);
  UpdateWindow(stEndTrack);
  UpdateWindow(ebEndTrack);
  UpdateWindow(pbAddRandomTrack);
  UpdateWindow(pbResetRandomTrack);
  UpdateWindow(ebOpenClose);
  UpdateWindow(stOpenClose);
  UpdateWindow(cbTTL);
  UpdateWindow(stTTL);
  UpdateWindow(ebStatus);
  UpdateWindow(stStatus);
  UpdateWindow(pbStart);
  UpdateWindow(pbAbort);
  UpdateWindow(pbClose);
  UpdateWindow(ebSelTrack);
  UpdateWindow(stSelTrack);
  UpdateWindow(pbShowTrackUp);
  UpdateWindow(pbShowTrackDown);
  UpdateWindow(st1);
  UpdateWindow(stWidth);
  UpdateWindow(stFrame);
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	FillRectangle()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function paints a white rectangle onto which we paint
//									the data traces.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void FillRectangle(void)
{
  HGDIOBJ 	prevObject;
  HBRUSH 		fill;
  HDC 			hdcRect;

  rect.left=10;
  rect.top=279;
  rect.right=610;
  rect.bottom=431;

  hdcRect=GetDC(hwnd);
  fill=CreateSolidBrush(0xFFFFFF);        // Select white brush
  prevObject=SelectObject(hdcRect,fill);
  FillRect(hdcRect,&rect,fill);           // Paint white rect
  SelectObject(hdcRect,prevObject);
  DeleteObject(fill);
  ReleaseDC(hwnd,hdcRect);
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	AcquireImageData()
//
//  RETURNS:				TRUE: Image data acquired and displayed successfully
//									FALSE: Error acquiring or displaying data
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function gets the acquired data from the card and
//									stores it in the global buffer pImageArray. It is called
//									from WM_TIMER after the acquisition is complete and goes on
//									to display the data	using DrawLines() and kill the timer.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

BOOL AcquireImageData(void)
{
  int 		size;
  int 		errorValue;
  char 		aBuffer[256];
  char 		aBuffer2[256];
  int 		trackNo;
  long 		MaxValue;
  long 		MinValue;

  size=AllocateBuffers();  // Allocate memory for image data. Size is returned
                           // for GetAcquiredData which needs the buffer size
  errorValue=GetAcquiredData(pImageArray,size);
  if(errorValue!=DRV_SUCCESS){
    wsprintf(aBuffer,"Acquisition error!");
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    return FALSE;
  }

  // Get selected track to display
  GetWindowText(ebSelTrack,aBuffer,10);
  trackNo=atoi(aBuffer);

  // Display data and query max data value to be displayed in status box
  FillRectangle();
  if(DrawLines(trackNo,&MaxValue,&MinValue)==FALSE){
    KillTimer(hwnd,timer);
    wsprintf(aBuffer, "Data range is zero");
   	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    return FALSE;
  }

  KillTimer(hwnd,timer);                    // kill status timer

  // If track not available, show track 1
  GetWindowText(ebStartTrack,aBuffer,10);

  if(trackNo>iRandomTrackCount/2||trackNo<=0)
    trackNo=1;

  // tell user acquisition is complete
  if(!gblData){                             // If there is no data the acq has
    wsprintf(aBuffer,"Acquisition aborted"); // been aborted
  }
  else{
    // tell user acquisition is complete
    wsprintf(aBuffer,"Acquisition complete !\r\n");
    strcat(aBuffer,"Random-Track Scan taken\r\n");
    wsprintf(aBuffer2,"Track #%d of %d displayed\r\n\r\n",trackNo,iRandomTrackCount/2);
    strcat(aBuffer,aBuffer2);
    wsprintf(aBuffer2,"Max data value is %d counts\r\n",MaxValue);
    strcat(aBuffer,aBuffer2);
    wsprintf(aBuffer2,"Min data value is %d counts",MinValue);
    strcat(aBuffer,aBuffer2);
  }
  SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);

  return TRUE;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	PaintDataWindow()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	12/11/98
//
//  DESCRIPTION:    This function handles the WM_PAINT messages sent by the
//									application. The WM_PAINT message repaints the screen when
//									the application opens and when you switch between
//									applications. When the app opens for the first time paint a
//									logo onto the paint area. When data is acquired paint it
//									instead.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void PaintDataWindow(void)
{
	HANDLE 				hBmp;           // handle to Andor bitmap
  HDC 					hBitmapDC;
  HDC 					hMemDC;
  PAINTSTRUCT 	PtrStr;
  long 					MaxValue;
  long 					MinValue;
  int						trackNo;
  char 					aBuffer[256];
  int 					bitmapWidth=266;
  int						bitmapHeight=64;

  // Redraw all dialog elements
  UpdateDialogWindows();        // Control windows
  FillRectangle();              // Paint area

  // Paint bitmap onto screen until first acquisition is taken
  if(!gblData || pImageArray==NULL){
    hBmp=LoadBitmap(hInst,"Andortch");
    hBitmapDC=BeginPaint(hwnd,&PtrStr);
    hMemDC=CreateCompatibleDC(hBitmapDC);
    SelectObject(hMemDC,hBmp);

    //Place Bitmap in center of paint area
    BitBlt(hBitmapDC,
           rect.left+(((rect.right-rect.left)-266)/2),
           rect.top+(((rect.bottom-rect.top)-66)/2),
           bitmapWidth,
           bitmapHeight,
           hMemDC,0,0,SRCCOPY);
    DeleteDC(hMemDC);
    EndPaint(hwnd,&PtrStr);
  }
  // When data is available paint it onto the screen using drawlines()
  else{
    GetWindowText(ebSelTrack,aBuffer,10);
    trackNo=atoi(aBuffer);

    if(DrawLines(trackNo,&MaxValue,&MinValue)==FALSE){ // maxvalue is not used in this case
    	wsprintf(aBuffer, "Data range is zero");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    }
  }

  // tell system that window is redrawn
  ValidateRect(hwnd,NULL);
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	DrawLines()
//
//  RETURNS:				TRUE: Function succeeded
//									FALSE: One or more Polylines failed to draw
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function paints the data traces onto the screen using
//									a blue pen. The pen must be set back to the original each
//									time is it used
//
//	ARGUMENTS: 			int trackNo: 						track to be displayed
//									long *ppMaxDataValue: 		This returns the max value to be
//																					displayed in the status box.
//------------------------------------------------------------------------------

BOOL DrawLines(int trackNo,long *pMaxDataValue,long *pMinDataValue)
{
  HGDIOBJ 	prevObject;
  HDC 			hdc;
  HPEN 			hpen;
  int 			i;
  BOOL 			bRetValue=TRUE;
  float 		xScale;
  char 			aBuffer[256];
  char 			aBuffer2[256];
  long 			MaxValue=1;
  long			MinValue=65536;
  int 			width,height;

  if(gblData && pImageArray!=NULL){
  	hdc=GetDC(hwnd);
    hpen=CreatePen(PS_SOLID,0,0xFF0000);   // Select blue pen to draw lines
    prevObject=SelectObject(hdc,hpen);

    // Show track 1 if selected value is not available
    GetWindowText(ebStartTrack,aBuffer,10);
    if(trackNo>(iRandomTrackCount/2)||trackNo<=0){
      trackNo=1;
    }

    // get width and height of paint area
    width=rect.right-rect.left;
    height=rect.bottom-rect.top-2;

    // Scale width into available space
    xScale=(float)gblXPixels/(float)width;


    // Find max value and scale data to fill rect. This is done for each track
    for(i=0;i<(gblXPixels);i++){
      if(pImageArray[i+(gblXPixels*(trackNo-1))]>MaxValue)
        MaxValue=pImageArray[i+(gblXPixels*(trackNo-1))];
      if(pImageArray[i+(gblXPixels*(trackNo-1))]<MinValue)
        MinValue=pImageArray[i+(gblXPixels*(trackNo-1))];
    }

    if(MaxValue == MinValue)
    	return FALSE;

    // Create an array of (x,y) points for the polyline
    for(i=0;i<gblXPixels;i++){
      pPointsArray[i].x=rect.left+(int)((float)i/xScale);
      pPointsArray[i].y=(rect.bottom-1)-((pImageArray[i+((trackNo-1)*gblXPixels)]-MinValue)*height)/(MaxValue-MinValue);
    }

    MoveToEx(hdc,pPointsArray[0].x,pPointsArray[0].y,NULL);     // start line at point[0]
    if(PolylineTo(hdc,pPointsArray,(DWORD)gblXPixels)==FALSE)  // Draw polyline
      bRetValue=FALSE;

    // Tell user which track is being displayed
    wsprintf(aBuffer,"Now displaying track #%d of %d\r\n\r\n",trackNo,iRandomTrackCount/2);
    wsprintf(aBuffer2,"Max data value is %d counts\r\n",MaxValue);
    strcat(aBuffer,aBuffer2);
    wsprintf(aBuffer2,"Min data value is %d counts",MinValue);
    strcat(aBuffer,aBuffer2);
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);

    SelectObject(hdc,prevObject);
    ReleaseDC(hwnd,hdc);
    DeleteObject(hpen);

    *pMaxDataValue=MaxValue;    // tell acquiredata function the max value so
                               // that it can display it in the status box
    *pMinDataValue=MinValue;    // tell acquiredata function the min value so
                               // that it can display it in the status box
  }
  else
  	bRetValue=FALSE;
  return bRetValue;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	AllocateBuffers()
//
//  RETURNS:				int size:  size of the image buffer
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function allocates enough memory for the buffers (if not
//									allocated already).
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

int AllocateBuffers(void)
{
	int 	size;
  int 	noTracks;


  noTracks=(iRandomTrackCount)/2;
  FreeBuffers();

	size=gblXPixels*noTracks;   // Buffer size is dependent on no of tracks

  // only allocate if necessary
	if(!pImageArray)
  	pImageArray=malloc(size*sizeof(long));
  if(!pPointsArray)
  	pPointsArray=malloc(gblXPixels*sizeof(POINT));

  return size;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	FreeBuffers()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function frees the memory allocated each buffer.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void FreeBuffers(void)
{
	// free all allocated memory
  if(pPointsArray){
    free(pPointsArray);
    pPointsArray = NULL;
  }
  if(pImageArray){
    free(pImageArray);
    pImageArray = NULL;
  }
}
