//------------------------------------------------------------------------------
//  PROJECT:		32-bit Driver Example Code ---- Spooled Image Kinetic Series
//																							Acquisition
//
//  Copyright 1998. All Rights Reserved
//
//  FILE:				SplWndw.c
//  AUTHOR:			Barry Smyth
//
//  OVERVIEW:		This Project shows how to set up the Andor MCD to take a kinetic
//							series acquisition of images and display 3 tracks from each image.
//							It also allows the user to spool the data from the acquisition to
//							disk to reduce memory usage. It will familiarise you with using
//							the Andor MCD driver library.
//------------------------------------------------------------------------------

#include <windows.h>            // required for all Windows applications
#include <stdio.h>              // required for sprintf()
#include <math.h>               // required for ceil()
#include "atmcd32d.h"           // Andor function definitions

#define SPI_GETSCREENSAVERRUNNING 114  // screensaver running ID
#define Color 256                      // Number of colors in the palette

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
BOOL GetSpooledData(int scanNo);  //Gets an image from spool file on disk
void PaintImage(long maxValue, long minValue, int Start); //Display data on screen
void CreateIdentityPalette(HDC ScreenDC); //Palette for PaintData()
BOOL ProcessMessages(UINT message, WPARAM wparam, LPARAM lparam){return FALSE;} // No messages to process in this example

// Set up acquisition parameters here to be set in common.c *****************
int acquisitionMode=3;
int readMode=4;
int xWidth=630;		 // width of application window passed to common.c
int yHeight=580;   // height of application window passed to common.c
//******************************************************************************

extern AndorCapabilities caps;         // Get AndorCapabilities structure from common.c
extern char              model[32];    // Get Head Model from common.c
extern int 	             gblXPixels;   // Get dims from common.c
extern int               gblYPixels;
extern int               VSnumber;     // Get speeds from common.c
extern int               HSnumber;
extern int               ADnumber;

// Declare Image Buffers
long 				*pImageArray=NULL;    // main image buffer read from card

int 				timer=100;     	 // ID of timer that checks status before acquisition

BOOL 				errorFlag;		 	 // Tells us if initialization failed in common.c
BOOL 				gblData=FALSE; 	 // flag is set when first acquisition is taken, tells
											 		 	 //	system that there is data to display

RECT 				rect;					 	 // Dims of paint area


extern HWND hwnd;          	 // Handle to main application

HWND				ebInit,      	 	 // handles for the individual
						stInit,     	   // windows such as edit boxes
            ebExposure,  	 	 // and comboboxes etc.
            stExposure,
            ebNoScans,
            stNoScans,
						ebKineticCycleTime,
            stKineticCycleTime,
            ebStatus,
            stStatus,
            pbStart,
            pbAbort,
            pbClose,
            stSelScan,
            ebSelScan,
            pbShowScanUp,
            pbShowScanDown,
            stFrame,
            ebFileName,
            stFileName,
            cxSpool,
            stSpool;


extern 			HINSTANCE hInst;       // Current Instance

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
    HINSTANCE hInstance=hInst;

    // Create windows for each control and store the handle names
		stInit=CreateWindow("STATIC","Initialization Information",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
    											10,2,200,18,hwnd,0,hInstance,NULL);
		ebInit=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
            							10,20,320,20,hwnd,0,hInstance,NULL);
		stExposure=CreateWindow("STATIC","Exposure time (secs):",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
     						 					10,60,250,20,hwnd,0,hInstance,NULL);
  	ebExposure=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
  										 		280,60,50,20,hwnd,0,hInstance,NULL);
  	stNoScans=CreateWindow("STATIC","# of Kinetic scans in series:",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,100,250,20,hwnd,0,hInstance,NULL);
  	ebNoScans=CreateWindow("EDIT","",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          280,100,50,20,hwnd,0,hInstance,NULL);
  	stKineticCycleTime=CreateWindow("STATIC","Kinetic cycle time(secs):",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          10,140,250,20,hwnd,0,hInstance,NULL);
  	ebKineticCycleTime=CreateWindow("EDIT","0",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          280,140,50,20,hwnd,0,hInstance,NULL);
  	stSpool=CreateWindow("STATIC","Spool to Disk",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													10,180,160,20,hwnd,0,hInstance,NULL);
  	cxSpool=CreateWindow("BUTTON","",
    											WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,
													280,180,50,20,hwnd,0,hInstance,NULL);
  	stFileName=CreateWindow("STATIC","Filename stem:",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													10,220,70,20,hwnd,0,hInstance,NULL);
    ebFileName=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_AUTOVSCROLL|ES_MULTILINE,
													80,220,250,20,hwnd,0,hInstance,NULL);
    ebStatus=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_AUTOVSCROLL|ES_MULTILINE,
													10,389,600,150,hwnd,0,hInstance,NULL);
    pbStart=CreateWindow("BUTTON","Start Acq",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													10,330,90,30,hwnd,0,hInstance,NULL);
    pbAbort=CreateWindow("BUTTON","Abort Acq",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													125,330,90,30,hwnd,0,hInstance,NULL);
    pbClose=CreateWindow("BUTTON","Close",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													240,330,90,30,hwnd,0,hInstance,NULL);
    stStatus=CreateWindow("STATIC","Status",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													10,369,60,18,hwnd,0,hInstance,NULL);
		stFrame=CreateWindow("STATIC","Status",
                          WS_CHILD|WS_VISIBLE|SS_BLACKFRAME,
                          340,330,270,30,hwnd,0,hInstance,NULL);
  	stSelScan=CreateWindow("STATIC","Kinetic Scan to display:",
                          WS_CHILD|WS_VISIBLE|SS_LEFT,
                          345,335,180,20,hwnd,0,hInstance,NULL);
  	ebSelScan=CreateWindow("EDIT","0",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                          525,335,45,20,hwnd,0,hInstance,NULL);
  	pbShowScanUp=CreateWindow("BUTTON","+",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          575,333,20,12,hwnd,0,hInstance,NULL);
  	pbShowScanDown=CreateWindow("BUTTON","-",
                          WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                          575,346,20,12,hwnd,0,hInstance,NULL);

    SetupWindows();     // fill windows with default data

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
//									default settings.
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
//	ARGUMENTS: 			char aInitializeString: Message to be displayed in init
//																					edit box
//------------------------------------------------------------------------------

void SetWindowsToDefault(char aInitializeString[256])
{
	char 	aBuffer[256];
  char 	aBuffer2[256];
  float speed;

	// add *autoshutter and send to window
  strcat(aInitializeString,"*Auto Shutter");
  SendMessage(ebInit, WM_SETTEXT, 0, (LPARAM)(LPSTR)aInitializeString);

  // Fill in default exposure time
  wsprintf(aBuffer,"0.1");
  SendMessage(ebExposure, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default number of kinetic scans
  wsprintf(aBuffer,"3");
  SendMessage(ebNoScans, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default kinetic cycle time
  wsprintf(aBuffer,"5");
  SendMessage(ebKineticCycleTime, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Fill in default scan to display
  wsprintf(aBuffer,"1");
  SendMessage(ebSelScan, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Print Status messages
  wsprintf(aBuffer,"Head Model %s\r\n", model);
  strcat(aBuffer,"Initializing Andor MCD system\r\n");
  strcat(aBuffer,"Kinetic Series Selected\r\n");
  strcat(aBuffer,"Set to Image Mode\r\n");
  wsprintf(aBuffer2,"Size of CCD: %d x %d pixels\r\n",gblXPixels,gblYPixels);
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

  //Add default spool file stem
  SendMessage(ebFileName, WM_SETTEXT,0,(LPARAM)(LPSTR)"stem");

}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetSystem()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function sets up the acquisition settings exposure time
//									, kinetic series, image and starts an acquisition. It also
//									sets up the name to be used for spooling files if requested.
//                  and itialises the timer to check for completion of the
//									acquisition.
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void SetSystem(void)
{
  float		fExposure,fAccumTime,fKineticTime;
  int 		errorValue;
  char 		aBuffer[MAX_PATH];
  char 		aBuffer2[256];
  char 		aPath[MAX_PATH];

  //SetHorizontalSpeed(2); //temporary set to slowest speed

  // Set Exposure Time
  GetWindowText(ebExposure,aBuffer2, 10);
  fExposure=atof(aBuffer2);
  errorValue = SetExposureTime(fExposure);
  if (errorValue != DRV_SUCCESS)
    wsprintf(aBuffer,"Exposure time error\r\n");

  if(SetupKinetics(aBuffer)){

  	// It is necessary to get the actual times as the system will calculate the
  	// nearest possible time. eg if you set exposure time to be 0, the system
  	// will use the closest value (around 0.01s)
  	GetAcquisitionTimings(&fExposure,&fAccumTime,&fKineticTime);
  	wsprintf(aBuffer,"Actual Exposure Time is ");
  	gcvt(fExposure,5,aBuffer2);
  	strcat(aBuffer,aBuffer2);
  	strcat(aBuffer,"\r\n");

    strcat(aBuffer,"Actual kinetic cycle time is ");
    gcvt(fKineticTime,5,aBuffer2);
    strcat(aBuffer,aBuffer2);
    strcat(aBuffer,"\r\n");

  	// This function only needs to be called when acquiring an image. It sets
  	// the horizontal and vertical binning and the area of the image to be
  	// captured. In this example it is set to 1x1 binning and is acquiring the
  	// whole image
  	SetImage(1,1,1,gblXPixels,1,gblYPixels);

    //initialise spooling if selected
  	if( BST_CHECKED&&SendMessage(cxSpool,BM_GETSTATE,0,0)){
     	GetWindowText(ebFileName,aBuffer2,MAX_PATH);
     	strcpy(aPath,aBuffer2);
     	SetSpool(1,0,aPath,4); //Enabled, Mode 0, aPath stem and buffer size of 4
      strcat(aBuffer, "Spooling Enabled\r\n");
  	}else{
     	SetSpool(0,0,NULL,4);  //Disabled
      strcat(aBuffer, "Spooling Disabled\r\n");
    }

   	// Starting the acquisition also starts a timer which checks the card status
  	// When the acquisition is complete the data is read from the card and
  	// displayed in the paint area.
  	errorValue=StartAcquisition();
  	if(errorValue!=DRV_SUCCESS){
    	strcat(aBuffer,"Start acquisition error");
    	AbortAcquisition();
    	gblData=FALSE;
  	}
  	else{
    	strcat(aBuffer,"Starting acquisition........");
    	SetTimer(hwnd,timer,100,NULL);
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
	int		status;
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
	int		errorValue;
  char 	aBuffer[256];
  int 	status;
  int 	scanNo;
  int		noScans;
  long 	MaxValue;
  long	MinValue;

  if(lparam==(LPARAM)pbStart){  // Start acquisition button is pressed
    gblData=TRUE;           // tells system an acq has taken place
    GetStatus(&status);
    if(status==DRV_IDLE){
      SetSystem();          // Set hardware and start acquisition
      FillRectangle();      // clear window ready for data trace
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
      gblData=FALSE;   // tell system no acq data in place
    }
    // or else let user know none is in progress
    else{
      wsprintf(aBuffer,"System not Acquiring");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    }
  }

  if(lparam==(LPARAM)pbClose){   // close application
    DestroyWindow(hwnd);
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
      if(!DrawLines(scanNo+1,&MaxValue,&MinValue)){
      	wsprintf(aBuffer, "Data range is zero");
      	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);         // draw accum data
      }
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
      if(!DrawLines(scanNo-1,&MaxValue,&MinValue)){
      	wsprintf(aBuffer, "Data range is zero");
      	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);         // draw accum data
      }         // draw accum data
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
  UpdateWindow(ebNoScans);
  UpdateWindow(stNoScans);
  UpdateWindow(ebKineticCycleTime);
  UpdateWindow(stKineticCycleTime);
  UpdateWindow(ebStatus);
  UpdateWindow(stStatus);
  UpdateWindow(pbStart);
  UpdateWindow(pbAbort);
  UpdateWindow(pbClose);
  UpdateWindow(ebSelScan);
  UpdateWindow(stSelScan);
  UpdateWindow(pbShowScanUp);
  UpdateWindow(pbShowScanDown);
  UpdateWindow(stFrame);
  UpdateWindow(stSpool);
  UpdateWindow(cxSpool);
  UpdateWindow(stFileName);
  UpdateWindow(ebFileName);
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
  RECT 			dummy;

  rect.left=340;
  rect.top=20;
  rect.right=611;
  rect.bottom=291;
  dummy = rect;    // FillRect excludes the right and bottom borders
  dummy.right++;   // dummy paints over those too
  dummy.bottom++;

  hdcRect=GetDC(hwnd);
  fill=CreateSolidBrush(0xFFFFFF);        // Select white brush
  prevObject=SelectObject(hdcRect,fill);
  FillRect(hdcRect,&dummy,fill);           // Paint white rect
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
//									stores it in the global buffer pImageArray (unless Spooling
//									is enabled). It is called from WM_TIMER after the acquisition
//									is complete and goes onto display the data using DrawLines()
//                  and kill the timer.
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

  if(!gblData){														  // If there is no data the acq has
    wsprintf(aBuffer,"Acquisition aborted"); // been aborted
  }
  else{
  	size=AllocateBuffers();	 // Allocate memory for image data. Size is returned
                           // for GetAcquiredData which needs the buffer size

  	//Only get acquired data if spooling is disabled
  	if(! (BST_CHECKED&&SendMessage(cxSpool,BM_GETSTATE,0,0))){
  		errorValue=GetAcquiredData(pImageArray,size);
  		if(errorValue!=DRV_SUCCESS){
    		wsprintf(aBuffer,"Acquisition error!");
    		SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    		return FALSE;
  		}
  	}

  	// Display data and query max data value to be displayed in status box
  	GetWindowText(ebNoScans,aBuffer,10);
  	noScans=atoi(aBuffer);
  	GetWindowText(ebSelScan,aBuffer,10);
  	scanNo=atoi(aBuffer);
    FillRectangle();
  	if(!DrawLines(scanNo, &MaxValue,&MinValue)){
    	KillTimer(hwnd,timer);
    	wsprintf(aBuffer, "Data range is zero");
   		SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    	return FALSE;
  	}

  	KillTimer(hwnd,timer);                   	// kill status timer

    // tell user acquisition is complete
    wsprintf(aBuffer,"Acquisition complete !\r\n");
    wsprintf(aBuffer2,"Full image acquired\r\n\r\n");
    strcat(aBuffer,aBuffer2);
    wsprintf(aBuffer2,"Kinetic scan #%d of %d displayed\r\n\r\n",scanNo,noScans);
    strcat(aBuffer,aBuffer2);
    wsprintf(aBuffer2,"Max data value is %d counts\r\n",MaxValue);
    strcat(aBuffer,aBuffer2);
    wsprintf(aBuffer2,"Min data value is %d counts\r\n",MinValue);
    strcat(aBuffer,aBuffer2);
    if( BST_CHECKED&&SendMessage(cxSpool,BM_GETSTATE,0,0))
      strcat(aBuffer, "Retreiving Data from Spool Files");
  	else
    	strcat(aBuffer, "Retreiving Data from Memory");


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
	HANDLE 			hBmp;              // handle to Andor bitmap
  HDC 				hBitmapDC;
  HDC 				hMemDC;
  PAINTSTRUCT PtrStr;
  long				MaxValue;
  long				MinValue;
  char				aBuffer[256];
  int					scanNo;
  int 				bitmapWidth=266;
  int 				bitmapHeight=64;

  // Redraw all dialog elements
  UpdateDialogWindows();         // Control windows
  FillRectangle();               // Paint area

  // Paint bitmap onto screen until first acquisition is taken
  if(!gblData || pImageArray==NULL){
    hBmp=LoadBitmap(hInst,"Andortch");
    hBitmapDC=BeginPaint(hwnd,&PtrStr);
    hMemDC=CreateCompatibleDC(hBitmapDC);
    SelectObject(hMemDC,hBmp);

    //Place Bitmap in center of paint area
    BitBlt(hBitmapDC,
           rect.left+(((rect.right-rect.left)-266)/2),	 // x
           rect.top+(((rect.bottom-rect.top)-66)/2),     // y
           bitmapWidth,                                  // width
           bitmapHeight,                                 // height
           hMemDC,0,0,SRCCOPY);
    DeleteDC(hMemDC);
    EndPaint(hwnd,&PtrStr);
  }
  // When data is available paint it onto the screen using drawlines()
  else{
  	GetWindowText(ebSelScan,aBuffer,10);
    scanNo=atoi(aBuffer);

    if(DrawLines(scanNo, &MaxValue,&MinValue)==FALSE){    	// values is not used in this case
      char aBuffer[20];
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
//									FALSE: Data failed to display
//
//  LAST MODIFIED:	Elm	18/10/04
//
//  DESCRIPTION:    This function displays the data onto the screen using
//									PaintImage().
//
//	ARGUMENTS: 			int scanNo:             track to be displayed
//									long *ppMaxDataValue:   This returns the max value to be
//																					displayed in the status box.
//------------------------------------------------------------------------------

BOOL DrawLines(int scanNo,long* pMaxDataValue,long* pMinDataValue)
{
  int 			i;
  BOOL 			bRetValue=TRUE;
  int 			noScans;
  char 			aBuffer[256];
  char 			aBuffer2[256];
  long 			MaxValue=1;
  long			MinValue=65536;
  int 			start;

  if(gblData && pImageArray!=NULL){

    // If scan no is invalid, display scan no.1
    GetWindowText(ebNoScans,aBuffer,10);
    noScans=atoi(aBuffer);
    if(scanNo>noScans||scanNo<=0){
      scanNo=1;
    }

    // get the requested spooled image from file
    if( BST_CHECKED&&SendMessage(cxSpool,BM_GETSTATE,0,0)){
      start = 0;
    	if(!GetSpooledData(scanNo)) return FALSE;
    }
    else
      start = (scanNo-1)*gblXPixels*gblYPixels;

    // Find max value and scale data to fill rect
    for(i=start;i<start+(gblXPixels*gblYPixels);i++){
      if(pImageArray[i]>MaxValue)
        MaxValue=pImageArray[i];
      if(pImageArray[i]<MinValue)
        MinValue=pImageArray[i];
    }
    if(MaxValue == MinValue)
  		return FALSE;

    PaintImage(MaxValue, MinValue, start); //Display image

    wsprintf(aBuffer,"Now displaying Kinetic scan #%d of %d",scanNo,noScans);
    if( BST_CHECKED&&SendMessage(cxSpool,BM_GETSTATE,0,0))
      strcat(aBuffer, " from Spool Files\r\n");
  	else
    	strcat(aBuffer, " from Memory\r\n");
    wsprintf(aBuffer2,"Max data value is %d counts\r\n",MaxValue);
    strcat(aBuffer,aBuffer2);
    wsprintf(aBuffer2,"Min data value is %d counts\r\n",MinValue);
    strcat(aBuffer,aBuffer2);
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);

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
//	FUNCTION NAME:	GetSpooledData()
//
//  RETURNS:				BOOL success:  if image was succesfully loaded
//
//  LAST MODIFIED:	BS	11/10/01
//
//  DESCRIPTION:    Gets an image from a spool file on disk.
//
//	ARGUMENTS: 			int scanNo: The image number to retreive.
//------------------------------------------------------------------------------

BOOL GetSpooledData(int scanNo)
{
	char 		aBuffer[MAX_PATH];
  char 		aBuffer2[MAX_PATH];
  char aPath[MAX_PATH];
  HANDLE spool;
  int i;
  DWORD bytesRead;

  //Get the spool file name stem
  GetWindowText(ebFileName,aBuffer2,MAX_PATH);
  strcpy(aPath,aBuffer2);

  //Add index and postfix
  wsprintf(aBuffer, "%s%010u.dat", aPath, scanNo-1);

  //open spool file for reading
  spool = CreateFile(aBuffer, GENERIC_READ, 0, NULL, OPEN_EXISTING, 0, NULL);
  if(spool == INVALID_HANDLE_VALUE) return FALSE;

  //Read values into image buffer
  for(i=0;i<gblXPixels*gblYPixels;i++)
  	ReadFile(spool, &(pImageArray[i]), sizeof(long), &bytesRead, NULL);

  CloseHandle(spool);

  return TRUE;
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
  int		noKineticScans;
  char 	aBuffer[256];

  GetWindowText(ebNoScans,aBuffer,10);
  noKineticScans=atoi(aBuffer);

	FreeBuffers();

  if( BST_CHECKED&&SendMessage(cxSpool,BM_GETSTATE,0,0))
  	size=gblXPixels*gblYPixels;  // For Spooling only needs to hold one image
  else
  	size=gblXPixels*gblYPixels*noKineticScans; //Needs to hold all images

  // only allocate if necessary
	if(!pImageArray)
  	pImageArray=malloc(size*sizeof(long));

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
  if(pImageArray){
    free(pImageArray);
    pImageArray = NULL;
  }
}

void PaintImage(long maxValue, long minValue, int Start)
{
  HDC hDC;
  float xscale, yscale, zscale, modrange;
  double dTemp;
  int width, height;
  int i, j, x, z, iTemp;
	HANDLE hloc;
	PBITMAPINFO pbmi;
	WORD argbq[Color];
  BYTE *DataArray;
  BOOL lvRunning = FALSE;

  SystemParametersInfo(SPI_GETSCREENSAVERRUNNING, 0, &lvRunning, 0);
  if (lvRunning == FALSE) {
    hDC = GetDC(hwnd);
    CreateIdentityPalette(hDC);

    modrange     = maxValue - minValue;
    width        = rect.right - rect.left + 1;
    if(width%4)                 // width must be a multiple of 4,
      width += (4-width%4);     // otherwise StretchDIBits has problems
    height       = rect.bottom - rect.top + 1;
    xscale       = (float)(gblXPixels)/(float)(width);
    yscale       = (256.0)/(float)modrange;
    zscale       = (float)(gblYPixels)/(float)(height);

    for (i = 0; i < Color; i++) argbq[i] = (WORD)i;

    hloc = LocalAlloc(LMEM_ZEROINIT | LMEM_MOVEABLE,
      sizeof(BITMAPINFOHEADER) + (sizeof(WORD)*Color));

    pbmi = (PBITMAPINFO) LocalLock(hloc);
    pbmi->bmiHeader.biSize        = sizeof(BITMAPINFOHEADER);
    pbmi->bmiHeader.biPlanes      = 1;
    pbmi->bmiHeader.biBitCount    = 8;
    pbmi->bmiHeader.biCompression = BI_RGB;
    pbmi->bmiHeader.biClrUsed     = Color;
    pbmi->bmiHeader.biWidth       = width;
    pbmi->bmiHeader.biHeight      = height;
    memcpy(pbmi->bmiColors, argbq, sizeof(WORD) * Color);

    DataArray = (BYTE*)malloc(width * height * sizeof(BYTE));
    memset(DataArray, 255, width * height);

    for (i = 0; i < height; i++) {
      z = (int)(i * zscale);
      for (j = 0; j < width; j++) {
        x = (int)(j * xscale);
        dTemp = ceil(yscale * (pImageArray[Start + x + z * gblXPixels] - minValue));
        if (dTemp < 0) iTemp = 0;
        else if (dTemp > Color - 1) iTemp = Color - 1;
        else iTemp = (int)dTemp;
        DataArray[j + i * width] = (BYTE)iTemp;
      }
    }

    SetStretchBltMode(hDC,COLORONCOLOR);
    StretchDIBits(hDC, rect.left, rect.top, width, height, 0, 0, width, height,
    DataArray, (BITMAPINFO FAR*)pbmi, DIB_PAL_COLORS, SRCCOPY);

    free(DataArray);
    ReleaseDC(hwnd, hDC);
    LocalUnlock(hloc);
    LocalFree(hloc);
  }
}

void CreateIdentityPalette(HDC ScreenDC)
{
  HPALETTE AppPalette;
  struct {
	 WORD Version;
	 WORD NumberEntries;
	 PALETTEENTRY aEntries[256];
  } Palette = { 0x300, 256};
  int i;

  GetSystemPaletteEntries(ScreenDC, 0, 256, Palette.aEntries);

  for (i = 0; i < Color; i++) {
		Palette.aEntries[i].peRed = LOBYTE(i);
		Palette.aEntries[i].peGreen = LOBYTE(i);
		Palette.aEntries[i].peBlue = LOBYTE(i);
    Palette.aEntries[i].peFlags = PC_RESERVED;
  }

  AppPalette = CreatePalette((LOGPALETTE *)&Palette);
  SelectPalette(ScreenDC, AppPalette, TRUE);
  RealizePalette(ScreenDC);
}


