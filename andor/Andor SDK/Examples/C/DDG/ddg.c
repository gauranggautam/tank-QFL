//------------------------------------------------------------------------------
//  PROJECT:		32-bit Driver Example Code ---- Digital Delay Generator Acquisitions
//
//  Copyright 2001. All Rights Reserved
//
//  FILE:				ddg32.c
//  AUTHOR:			Ian McClenahan
//
//  OVERVIEW:		This Project shows how to set up the Andor MCD to take a DDG
//							kinetic series acquisition. It will
//							familiarise you with using the Andor MCD driver library.
//------------------------------------------------------------------------------

#include <windows.h>            	// required for all Windows applications
#include <stdio.h>              // required for sprintf()
#include "atmcd32d.h"           // Andor function definitions

// Function Prototypes
BOOL CreateWindows(void);         // Create control windows and allocate handles
void SetupWindows(void);          // Initialize control windows
void SetWindowsToDefault(char[256]);// Fills windows with default values
void SetSystem(void);             // Sets hardware parameters
void ProcessTimer(WPARAM);        // Handles WM_TIMER messages
void ProcessPushButtons(LPARAM);  // Processes button presses
void UpdateDialogWindows(void);   // refreshes all windows
void FillRectangle(void);         // clears paint area
BOOL AcquireImageData(void);      // Acquires data from card
void PaintDataWindow(void);       // Prepares paint area on screen
BOOL DrawLines(int scanNo,long*,long*); // paints data to screen
int AllocateBuffers(void);        // Allocates memory for buffers
void FreeBuffers(void);           // Frees allocated memory
BOOL SetupKinetics(char *string);    // Set up kinetic series parameters
BOOL ProcessMessages(UINT message, WPARAM wparam, LPARAM lparam){return FALSE;} // No messages to process in this example

// Set up acquisition parameters here to be set in common.c *****************
int acquisitionMode=3;
int readMode=0;
int xWidth=640;   // width of application window passed to common.c
int yHeight=520;  // height of application window passed to common.c
//******************************************************************************

extern AndorCapabilities caps;         // Get AndorCapabilities structure from common.c
extern char              model[32];    // Get Head Model from common.c
extern int 	             gblXPixels;   // Get dims from common.c
extern int               gblYPixels;
extern int               VSnumber;     // Get speeds from common.c
extern int               HSnumber;
extern int               ADnumber;

// Declare Image Buffers
long *pImageArray;     		 // main image buffer read from card
POINT *pPointsArray;        		 // points data required to draw one polyline

int timer=100;         		 // ID of timer that checks status before acquisition
int timer2=200;

BOOL errorFlag;				   // Tells us if initialization failed in common.c
BOOL gblData=FALSE;    		 // flag is set when first acquisition is taken, tells system that there is data to display

RECT rect;             		 // Dims of paint area

extern HWND hwnd;          // handles for the individual

HWND				ebInit,        // windows such as edit boxes
            stInit,       // and comboboxes etc.
            ebExposure,
            stExposure,
            ebT0,
            stT0,
            ebT1,
            stT1,
            ebT2,
            stT2,
            stStep,
            ebStep,
            stGain,
            ebGain,
            ebNoScans,
            stNoScans,
						ebKineticCycleTime,
            stKineticCycleTime,
            cbTrigger,
            stTrigger,
            ckbIntelligate,
            ckbProp,
            ebStatus,
            stStatus,
            ebIOC,
            stIOC,
            ckbIOC,
            pbStart,
            pbAbort,
            pbClose,
            pbFindPulse,
            stSelScan,
            ebSelScan,
            pbShowScanUp,
            pbShowScanDown,
            st1,
            stWidth,
            stFrame,
            stIOCFrame;

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
  int top = 50;
  char 				aBuffer[256];
  HINSTANCE 	hInstance=hInst;


  wsprintf(aBuffer,"%d",gblXPixels);     // to be placed in txtWidth

  // Create windows for each control and store the handle names
  stInit=CreateWindow("STATIC","Initialization Information",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,2,200,18,hwnd,0,hInstance,NULL);
  ebInit=CreateWindow("EDIT","",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          10,20,320,20,hwnd,0,hInstance,NULL);

  stExposure=CreateWindow("STATIC","Exposure time (secs):", WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  ebExposure=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,250,top,80,20,hwnd,0,hInstance,NULL);top+=20;
  stT0=CreateWindow("STATIC","Output A Delay (nsecs):",WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  ebT0=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,250,top,80,20,hwnd,0,hInstance,NULL);top+=20;
  stT1=CreateWindow("STATIC","Delay (psecs):",WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  ebT1=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,250,top,80,20,hwnd,0,hInstance,NULL);top+=20;
  stT2=CreateWindow("STATIC","Pulse Width (psecs):",WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  ebT2=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,250,top,80,20,hwnd,0,hInstance,NULL);top+=20;
  stStep=CreateWindow("STATIC","Gate Step (psecs):",WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  ebStep=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,250,top,80,20,hwnd,0,hInstance,NULL);top+=20;
  stGain=CreateWindow("STATIC","Gain (0-255):",WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  ebGain=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,250,top,80,20,hwnd,0,hInstance,NULL);top+=20;
  stNoScans=CreateWindow("STATIC","# of Kinetic scans in series:",WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  ebNoScans=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,250,top,80,20,hwnd,0,hInstance,NULL);top+=20;
  stKineticCycleTime=CreateWindow("STATIC","Kinetic cycle time(secs):",WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  ebKineticCycleTime=CreateWindow("EDIT","0",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,250,top,80,20,hwnd,0,hInstance,NULL);top+=20;
  stTrigger=CreateWindow("STATIC","Trigger mode:",WS_CHILD|WS_VISIBLE|SS_LEFT,10,top,200,20,hwnd,0,hInstance,NULL);
  cbTrigger=CreateWindow("COMBOBOX","0",WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,250,top,80,100,hwnd,0,hInstance,NULL);top+=25;
  ckbIntelligate=CreateWindow("BUTTON","Intelligate",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,10,top,100,20,hwnd,0,hInstance,NULL);
  ckbProp=CreateWindow("BUTTON","Fast insertion delay",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,180,top,150,20,hwnd,0,hInstance,NULL);
  ebStatus=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_MULTILINE,340,20,270,150,hwnd,0,hInstance,NULL);
  top = 190;
  stIOCFrame=CreateWindow("STATIC","Status",WS_CHILD|WS_VISIBLE|SS_BLACKFRAME,340,185,270,50,hwnd,0,hInstance,NULL);
  ckbIOC=CreateWindow("BUTTON","Integrate on chip",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,345,top,140,20,hwnd,0,hInstance,NULL);top+=20;
  stIOC=CreateWindow("STATIC","Frequency (Hz):",WS_CHILD|WS_VISIBLE|SS_LEFT,345,top,190,20,hwnd,0,hInstance,NULL);
  ebIOC=CreateWindow("EDIT","",WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,535,top,70,20,hwnd,0,hInstance,NULL);

  pbStart=CreateWindow("BUTTON","Start Acq",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          10,270,80,30,hwnd,0,hInstance,NULL);
  pbAbort=CreateWindow("BUTTON","Abort Acq",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          90,270,80,30,hwnd,0,hInstance,NULL);
  pbClose=CreateWindow("BUTTON","Close",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          170,270,80,30,hwnd,0,hInstance,NULL);
  pbFindPulse=CreateWindow("BUTTON","Find Pulse",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          250,270,80,30,hwnd,0,hInstance,NULL);

  stStatus=CreateWindow("STATIC","Status",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          340,2,60,18,hwnd,0,hInstance,NULL);
  stFrame=CreateWindow("STATIC","Status",
                          WS_CHILD|WS_VISIBLE|SS_BLACKFRAME,
                          340,270,270,30,hwnd,0,hInstance,NULL);
  stSelScan=CreateWindow("STATIC","Kinetic Scan to display:",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          345,275,180,20,hwnd,0,hInstance,NULL);
  ebSelScan=CreateWindow("EDIT","0",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          525,275,45,20,hwnd,0,hInstance,NULL);
  pbShowScanUp=CreateWindow("BUTTON","+",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          575,273,20,12,hwnd,0,hInstance,NULL);
  pbShowScanDown=CreateWindow("BUTTON","-",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          575,286,20,12,hwnd,0,hInstance,NULL);
  st1=CreateWindow("STATIC","1",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          0,470,20,20,hwnd,0,hInstance,NULL);
  stWidth=CreateWindow("STATIC",aBuffer,
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          590,470,40,20,hwnd,0,hInstance,NULL);

  SetupWindows();      // fill windows with default data

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
  wsprintf(aBuffer,"0.021");
  SendMessage(ebExposure, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default
  wsprintf(aBuffer,"0");
  SendMessage(ebT0, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default
  wsprintf(aBuffer,"100000");
  SendMessage(ebT1, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default
  wsprintf(aBuffer,"5000");
  SendMessage(ebT2, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

    // Fill in default
  wsprintf(aBuffer,"5000");
  SendMessage(ebStep, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

    // Fill in default
  wsprintf(aBuffer,"80");
  SendMessage(ebGain, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default number of kinetic scans
  wsprintf(aBuffer,"5");
  SendMessage(ebNoScans, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default kinetic cycle time
  wsprintf(aBuffer,"2");
  SendMessage(ebKineticCycleTime, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Add options to trigger combo box
  wsprintf(aBuffer,"Internal");
  SendMessage(cbTrigger, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"External");
  SendMessage(cbTrigger, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);

  // Select default trigger
  wsprintf(aBuffer,"Internal");
  SendMessage(cbTrigger, CB_SELECTSTRING,0,(LPARAM)(LPSTR)aBuffer);

  // Fill in default
  wsprintf(aBuffer,"100");
  SendMessage(ebIOC, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default scan to display
  wsprintf(aBuffer,"1");
  SendMessage(ebSelScan, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Print Status messages
  wsprintf(aBuffer,"Head Model %s\r\n", model);
  strcat(aBuffer,"Initializing Andor MCD system\r\n");
  strcat(aBuffer,"Kinetics Selected\r\n");
  strcat(aBuffer,"Set to FVB Mode\r\n");
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

  SetTimer(hwnd,timer2,500,NULL);
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetSystem()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function sets up the acquisition settings exposure time
//									, trigger etc and starts an acquisition. It also starts a
//									timer to check when the acquisition has finished.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void SetSystem(void)
{
  float		fExposure,fAccumTime,fKineticTime;
  double  t0, t1, t2, step, freq;
  int 		trig, gain, errorValue;
  char 		aBuffer[256];
  char 		aBuffer2[256];
  BOOL    state;
  // Set Exposure Time
  GetWindowText(ebExposure,aBuffer2, 10);
  fExposure=atof(aBuffer2);
  errorValue = SetExposureTime(fExposure);
  if (errorValue != DRV_SUCCESS)
    wsprintf(aBuffer,"Exposure time error\r\n");

  // Set DDG Times
  GetWindowText(ebT0,aBuffer2,255);
  t0=strtod(aBuffer2, NULL);
  GetWindowText(ebT1,aBuffer2,255);
  t1=strtod(aBuffer2, NULL);
  GetWindowText(ebT2,aBuffer2,255);
  t2=strtod(aBuffer2, NULL);
  errorValue = SetDDGTimes(t0, t1, t2);
  if (errorValue != DRV_SUCCESS)
    wsprintf(aBuffer,"DDG time error\r\n");

  // Set Gate Step
  GetWindowText(ebStep,aBuffer2,255);
  step=strtod(aBuffer2, NULL);
  errorValue = SetDDGGateStep(step);
  if (errorValue != DRV_SUCCESS)
    wsprintf(aBuffer,"Gate step error\r\n");

  // Set Gain
  GetWindowText(ebGain,aBuffer2, 10);
  gain=atoi(aBuffer2);
  errorValue = SetDDGGain(gain);
  if (errorValue != DRV_SUCCESS)
    wsprintf(aBuffer,"Gain error\r\n");

  // Set trigger mode
  GetWindowText(cbTrigger,aBuffer2,10);
  if(strcmp(aBuffer2,"Internal")==0){
    trig=0;
    strcat(aBuffer,"Trigger set to Internal\r\n");
  }
  if(strcmp(aBuffer2,"External")==0){
    trig=1;
    strcat(aBuffer,"Trigger set to External\r\n");
  }
  errorValue=SetDDGTriggerMode(trig);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set Trigger Mode Error\r\n");

  // Set insertion delay
  state = SendMessage(ckbProp, BM_GETCHECK, 0, 0);
  errorValue=SetDDGInsertionDelay(state);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set Insertion Delay Error\r\n");

  // Set intelligate
  state = SendMessage(ckbIntelligate, BM_GETCHECK, 0, 0);
  errorValue=SetDDGIntelligate(state);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Intelligate Error\r\n");

  // Set ioc
  state = SendMessage(ckbIOC, BM_GETCHECK, 0, 0);
  errorValue=SetDDGIOC(state);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"IOC Error\r\n");
  else {
    GetWindowText(ebIOC,aBuffer2,255);
    freq = strtod(aBuffer2, NULL);
    SetDDGIOCFrequency(freq);
  }

  // This function sets up the kinetic series parameters
  if(SetupKinetics(aBuffer)){
    // It is necessary to get the actual times as the system will calculate the
    // nearest possible time. eg if you set exposure time to be 0, the system
    // will use the closest value (around 0.01s)
    GetAcquisitionTimings(&fExposure,&fAccumTime,&fKineticTime);
    wsprintf(aBuffer,"\r\nActual exposure time is ");
    gcvt(fExposure,5,aBuffer2);
    strcat(aBuffer,aBuffer2);
    strcat(aBuffer,"\r\n");

    strcat(aBuffer,"Actual kinetic cycle time is ");
    gcvt(fKineticTime,5,aBuffer2);
    strcat(aBuffer,aBuffer2);
    strcat(aBuffer,"\r\n");

    // Starting the acquisition also starts a timer which checks the card status
    // When the acquisition is complete the data is read from the card and
    // displayed in the paint area.
    errorValue=StartAcquisition();
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"\r\nStart acquisition error\r\n");
      AbortAcquisition();
      gblData=FALSE;
    }
    else{
      strcat(aBuffer,"\r\nStarting acquisition........");
      SetTimer(hwnd,timer,500,NULL);    // checks 10 times per second
    }
  }
  else{
    wsprintf(aBuffer,"Error setting Kinetic Series parameters");
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
  BOOL  state;
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
    case 200:
        state = SendMessage(ckbProp, BM_GETCHECK, 0, 0);
        if (state) SendMessage(ckbIntelligate, BM_SETCHECK, BST_UNCHECKED, 0);
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
	int		errorValue;
  char	aBuffer[256];
  int 	status;
  int 	scanNo;
  int		noScans;
  long 	MaxValue;
  long	MinValue;
  double delay, width;
  HCURSOR hNewCursor, hOldCursor;;

  if(lparam==(LPARAM)pbStart){  // Start acquisition button is pressed
    gblData=TRUE;							  // tells system an acq has taken place
    GetStatus(&status);
    if(status==DRV_IDLE){
      SetSystem();              // Set hardware and start acquisition
      FillRectangle();          // clear window ready for data trace
    }
    wsprintf(aBuffer,"1");
    SendMessage(ebSelScan,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
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

  if(lparam==(LPARAM)pbClose){
    KillTimer(hwnd, timer2);
    DestroyWindow(hwnd);
  }

  if(lparam==(LPARAM)pbFindPulse){
    hNewCursor = LoadCursor(NULL, IDC_WAIT);
    hOldCursor = SetCursor(hNewCursor);
    GetDDGPulse(1000000, 32000, &delay, &width);
    SetCursor(hOldCursor);

    // Fill in default
    gcvt(delay, 6, aBuffer);
    SendMessage(ebT1, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

    // Fill in default
    gcvt(width, 6, aBuffer);
    SendMessage(ebT2, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);
  }

  if(lparam==(LPARAM)pbShowScanUp){
    // only if data exists
    if(gblData){
      FillRectangle();     								 // clear window

      GetWindowText(ebNoScans,aBuffer,10);
      noScans=atoi(aBuffer);
      GetWindowText(ebSelScan,aBuffer,10);  // which accum to display
      scanNo=atoi(aBuffer);
      if((scanNo+1)>noScans)
        scanNo=noScans-1;
      DrawLines(scanNo+1,&MaxValue,&MinValue);         // draw accum data
      wsprintf(aBuffer,"%d",scanNo+1);
      SendMessage(ebSelScan,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    }
  }

  if(lparam==(LPARAM)pbShowScanDown){
    // only if data exists
    if(gblData){
      FillRectangle();     								 // clear window

      GetWindowText(ebSelScan,aBuffer,10);  // which accum to display
      scanNo=atoi(aBuffer);
      DrawLines(scanNo-1,&MaxValue,&MinValue);         // draw accum data
      if(scanNo==1)
        scanNo=2;
      wsprintf(aBuffer,"%d",scanNo-1);
      SendMessage(ebSelScan,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    }
  }
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetupKinetics()
//
//  RETURNS:				TRUE: parameters set successfully
//									FALSE: unsuccessful
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function sets up the kinetic series and accumulation
//									parameters and returns a string of information to be
//									displayed in the status edit box.
//
//	ARGUMENTS: 			char *string: string to be displayed in edit box
//------------------------------------------------------------------------------

BOOL SetupKinetics(char *string)
{
  int 		noScans;
  float 	kineticCycleTime;
  char 		aBuffer[256];
  char 		aBuffer2[256];
  int 		errorValue;

  // Clear message array
  strcpy(aBuffer, "");

  // Set number of accumulations
  errorValue=SetNumberAccumulations(1);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set number accumulations error\r\n");

  // Set accumulation cycle time

  errorValue=SetAccumulationCycleTime(0);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set accumulation cycle time error\r\n");

  // Get and set no of kinetic scans to be taken
  GetWindowText(ebNoScans,aBuffer2,10);
  noScans=atof(aBuffer2);
  wsprintf(aBuffer2,"\r\nNo of kinetic scans: %d\r\n",noScans);
  strcat(aBuffer,aBuffer2);
  errorValue=SetNumberKinetics(noScans);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set number kinetics error\r\n");

  // Get and set kinetic cycle time
  GetWindowText(ebKineticCycleTime,aBuffer2,10);
  kineticCycleTime=atof(aBuffer2);
  strcat(aBuffer,"Kinetic cycle time: ");
  strcat(aBuffer,aBuffer2);
  errorValue=SetKineticCycleTime(kineticCycleTime);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set kinetic cycle time error\r\n");

  // send the string back to SetSystem to be displayed
  strcpy(string,aBuffer);
  return TRUE;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	UpdateDialogWindows()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function updates the individual windows and is called
//									from inside the WM_PAINT message. This ensures that the
//									windows are present when the window is re-drawn.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void UpdateDialogWindows(void)
{
  UpdateWindow(ebInit);
  UpdateWindow(stInit);
  UpdateWindow(ebExposure);
  UpdateWindow(stExposure);
  UpdateWindow(ebT0);
  UpdateWindow(stT0);
  UpdateWindow(ebT1);
  UpdateWindow(stT1);
  UpdateWindow(ebT2);
  UpdateWindow(stT2);
  UpdateWindow(ebStep);
  UpdateWindow(stStep);
  UpdateWindow(ebGain);
  UpdateWindow(stGain);
  UpdateWindow(ebNoScans);
  UpdateWindow(stNoScans);
  UpdateWindow(ebKineticCycleTime);
  UpdateWindow(stKineticCycleTime);
  UpdateWindow(cbTrigger);
  UpdateWindow(stTrigger);
  UpdateWindow(ckbIntelligate);
  UpdateWindow(ckbProp);
  UpdateWindow(ebStatus);
  UpdateWindow(stStatus);
  UpdateWindow(ckbIOC);
  UpdateWindow(ebIOC);
  UpdateWindow(stIOC);
  UpdateWindow(pbStart);
  UpdateWindow(pbAbort);
  UpdateWindow(pbClose);
  UpdateWindow(pbFindPulse);
  UpdateWindow(ebSelScan);
  UpdateWindow(stSelScan);
  UpdateWindow(pbShowScanUp);
  UpdateWindow(pbShowScanDown);
  UpdateWindow(st1);
  UpdateWindow(stWidth);
  UpdateWindow(stFrame);
  UpdateWindow(stIOCFrame);
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
  rect.top=309;
  rect.right=610;
  rect.bottom=461;

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
  int 		scanNo,noScans;
  long 		MaxValue;
  long		MinValue;

  FreeBuffers();
  size=AllocateBuffers();  // Allocate memory for image data. Size is returned
                           // for GetAcquiredData which needs the buffer size

  errorValue=GetAcquiredData(pImageArray,size);
  if(errorValue!=DRV_SUCCESS){
    wsprintf(aBuffer,"Acquisition error!");
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    return FALSE;
  }

  // Display data and query max data value to be displayed in status box
  GetWindowText(ebNoScans,aBuffer,10);
  noScans=atoi(aBuffer);
  GetWindowText(ebSelScan,aBuffer,10);
  scanNo=atoi(aBuffer);
  FillRectangle();
  if(DrawLines(scanNo,&MaxValue,&MinValue)==FALSE){
    KillTimer(hwnd,timer);
    return FALSE;
  }

  KillTimer(hwnd,timer);                  	// kill status timer

  // tell user acquisition is complete
  if(!gblData){                         		// If there is no data the acq has
    wsprintf(aBuffer,"Acquisition aborted"); // been aborted
  }
  else{
    // tell user acquisition is complete
    wsprintf(aBuffer,"Acquisition complete !\r\n");
    strcat(aBuffer,"Fully Vertically Binned Scan taken\r\n");
    wsprintf(aBuffer2,"Kinetic scan #%d of %d displayed\r\n\r\n",scanNo,noScans);
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
  HDC	 					hBitmapDC;
  HDC						hMemDC;
  PAINTSTRUCT 	PtrStr;
  long					MaxValue;
  long					MinValue;
  char					aBuffer[256];
  int						scanNo;
  int						bitmapWidth=266;
  int 					bitmapHeight=64;

  // Redraw all dialog elements
  UpdateDialogWindows();       // Control windows
  FillRectangle();             // Paint area

  // Paint bitmap onto screen until first acquisition is taken
  if(!gblData || pImageArray==NULL){
    hBmp=LoadBitmap(hInst,"Andortch");
    hBitmapDC=BeginPaint(hwnd,&PtrStr);
    hMemDC=CreateCompatibleDC(hBitmapDC);
    SelectObject(hMemDC,hBmp);

    //Place Bitmap in center of paint area
    BitBlt(hBitmapDC,
           rect.left+(((rect.right-rect.left)-266)/2),  // x
           rect.top+(((rect.bottom-rect.top)-66)/2),    // y
           bitmapWidth,                                 // width
           bitmapHeight,                                // height
           hMemDC,0,0,SRCCOPY);
    DeleteDC(hMemDC);
    EndPaint(hwnd,&PtrStr);
  }
  // When data is available paint it onto the screen using drawlines()
  else{
    GetWindowText(ebSelScan,aBuffer,10);
    scanNo=atoi(aBuffer);

    DrawLines(scanNo,&MaxValue,&MinValue);  // maxvalue is not used in this case
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
//									a blue pen. The pen must be set back to the original after
//									each time it is used.
//
//	ARGUMENTS: 			int scanNo: 						track to be displayed
//									long *ppMaxDataValue: 		This returns the max value to be
//																					displayed in the status box.
//------------------------------------------------------------------------------

BOOL DrawLines(int scanNo,long* pMaxDataValue,long* pMinDataValue)
{
  HGDIOBJ 	prevObject;
  HDC 			hdc;
  HPEN 			hpen;
  int 			i;
  BOOL 			bRetValue=TRUE;
  float 		xScale;
  int 			noScans;
  char 			aBuffer[256];
  char 			aBuffer2[256];
  long 			MaxValue=1;
  long			MinValue=65536;
  int 			width,height;

  if(gblData && pImageArray!=NULL){
    hdc=GetDC(hwnd);
    hpen=CreatePen(PS_SOLID,0,0xFF0000);   // Select blue pen to draw lines
    prevObject=SelectObject(hdc,hpen);

    // If scan no is invalid, display scan no.1
    GetWindowText(ebNoScans,aBuffer,10);
    noScans=atoi(aBuffer);
    if(scanNo>noScans||scanNo<=0){
      scanNo=1;
    }

    // get width and height of paint area
    width=rect.right-rect.left;
    height=rect.bottom-rect.top-2;

    // Scale width into available space
    xScale=(float)gblXPixels/width;

    // Find max value and scale data to fill rect
    for(i=0;i<(gblXPixels);i++){
      if(pImageArray[i+(gblXPixels*(scanNo-1))]>MaxValue)
        MaxValue=pImageArray[i+(gblXPixels*(scanNo-1))];
      if(pImageArray[i+(gblXPixels*(scanNo-1))]<MinValue)
        MinValue=pImageArray[i+(gblXPixels*(scanNo-1))];
    }

    // Create an array of (x,y) points for the polyline
    for(i=0;i<gblXPixels;i++){
      pPointsArray[i].x=rect.left+(int)((float)i/xScale);
      pPointsArray[i].y=(rect.bottom-1)-((pImageArray[i+((scanNo-1)*gblXPixels)]-MinValue)*height)/(MaxValue-MinValue+1);
    }

    MoveToEx(hdc,pPointsArray[0].x,pPointsArray[0].y,NULL);      // start line at point[0]
    if(PolylineTo(hdc,pPointsArray,(DWORD)gblXPixels)==FALSE)   // Draw polyline
      bRetValue=FALSE;

    wsprintf(aBuffer,"Now displaying Kinetic scan #%d of %d\r\n",scanNo,noScans);
    wsprintf(aBuffer2,"Max data value is %d counts\r\n",MaxValue);
    strcat(aBuffer,aBuffer2);
    wsprintf(aBuffer2,"Min data value is %d counts\r\n",MinValue);
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
  int 	noKineticScans;
  char 	aBuffer[256];

  GetWindowText(ebNoScans,aBuffer,10);
  noKineticScans=atoi(aBuffer);

	size=gblXPixels*noKineticScans;
  // only allocate if necessary
	if(!pImageArray)
  	pImageArray=malloc(gblXPixels*noKineticScans*sizeof(long));
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
  if (pPointsArray) {
    free(pPointsArray);
    pPointsArray = NULL;
  }
  if (pImageArray) {
    free(pImageArray);
    pImageArray = NULL;
  }
}

