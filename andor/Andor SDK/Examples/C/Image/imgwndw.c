//------------------------------------------------------------------------------
//  PROJECT:		32-bit Driver Example Code ---- Full Image Acquisition
//
//  Copyright 1998. All Rights Reserved
//
//  FILE:				ImgWndw.c
//  AUTHOR:			Paul McKernon
//
//  OVERVIEW:		This Project shows how to set up the Andor MCD to take a single
//							image acquisition and display 3 tracks from it. It will
//							familiarise you with using the Andor MCD driver library.
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
BOOL DrawLines(long*,long*); 			// paints data to screen
int AllocateBuffers(void);        // Allocates memory for buffers
void FreeBuffers(void);           // Frees allocated memory
void PaintImage(long maxValue, long minValue, int Start); //Display data on screen
void CreateIdentityPalette(HDC ScreenDC); //Palette for PaintData()
BOOL ProcessMessages(UINT message, WPARAM wparam, LPARAM lparam){return FALSE;} // No messages to process in this example


// Set up acquisition parameters here to be set in common.c *****************
int acquisitionMode=1;
int readMode=4;
int xWidth=630;   // width of application window passed to common.c
int yHeight=521;  // height of application window passed to common.c
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
            ebOpenClose,
            stOpenClose,
            cbTTL,
            stTTL,
            cbTrigger,
            stTrigger,
            ebStatus,
            stStatus,
            pbStart,
            pbAbort,
            pbClose;

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
    											10,2,180,18,hwnd,0,hInstance,NULL);
		ebInit=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
            							10,20,310,40,hwnd,0,hInstance,NULL);
		stExposure=CreateWindow("STATIC","Exposure time (secs):",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
     						 					10,80,160,20,hwnd,0,hInstance,NULL);
  	ebExposure=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
  										 		270,80,50,20,hwnd,0,hInstance,NULL);
  	stOpenClose=CreateWindow("STATIC","Open / Close Time (msecs):",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													10,120,180,20,hwnd,0,hInstance,NULL);
		ebOpenClose=CreateWindow("EDIT","0",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
													270,120,50,20,hwnd,0,hInstance,NULL);
		stTTL=CreateWindow("STATIC","Shutter opens on:",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
  												10,160,180,20,hwnd,0,hInstance,NULL);
		cbTTL=CreateWindow("COMBOBOX","",
    											WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
    											220,160,100,80,hwnd,0,hInstance,NULL);
  	stTrigger=CreateWindow("STATIC","Trigger Mode:",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													10,200,180,20,hwnd,0,hInstance,NULL);
  	cbTrigger=CreateWindow("COMBOBOX","",
    											WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
													220,200,100,80,hwnd,0,hInstance,NULL);
    ebStatus=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_AUTOVSCROLL|ES_MULTILINE,
													10,330,600,150,hwnd,0,hInstance,NULL);
    pbStart=CreateWindow("BUTTON","Start Acq",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													10,261,90,30,hwnd,0,hInstance,NULL);
    pbAbort=CreateWindow("BUTTON","Abort Acq",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													125,261,90,30,hwnd,0,hInstance,NULL);
    pbClose=CreateWindow("BUTTON","Close",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													240,261,90,30,hwnd,0,hInstance,NULL);
    stStatus=CreateWindow("STATIC","Status",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													10,310,60,18,hwnd,0,hInstance,NULL);

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
  wsprintf(aBuffer,"0");
  SendMessage(ebOpenClose, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Add TTL options to combobox
  wsprintf(aBuffer,"High");
  SendMessage(cbTTL, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"Low");
  SendMessage(cbTTL, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);

  // Select high as default
  wsprintf(aBuffer,"High");
  SendMessage(cbTTL, CB_SELECTSTRING,0,(LPARAM)(LPSTR)aBuffer);

  // Add trigger options to combobox
  wsprintf(aBuffer,"Internal");
  SendMessage(cbTrigger, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"External");
  SendMessage(cbTrigger, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);

  // Select internal as default
  wsprintf(aBuffer,"Internal");
  SendMessage(cbTrigger, CB_SELECTSTRING,0,(LPARAM)(LPSTR)aBuffer);

  // Print Status messages
  wsprintf(aBuffer,"Head Model %s\r\n", model);
  strcat(aBuffer,"Initializing Andor MCD system\r\n");
  strcat(aBuffer,"Single Scan Selected\r\n");
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
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetSystem()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function sets up the acquisition settings exposure time
//									shutter, trigger and starts an acquisition. It also starts a
//									timer to check when the acquisition has finished.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void SetSystem(void)
{
  float		fExposure,fAccumTime,fKineticTime;
  int 		errorValue;
  int 		openclose,ttl,shutter,trig;
  char 		aBuffer[256];
  char 		aBuffer2[256];

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

  // Get open close time
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

  // Get trigger selection and set
  GetWindowText(cbTrigger,aBuffer2,10);
  if(strcmp(aBuffer2,"Internal")==0){
    trig=0;
    strcat(aBuffer,"Trigger set to Internal\r\n");
  }
  if(strcmp(aBuffer2,"External")==0){
    trig=1;
    strcat(aBuffer,"Trigger set to External\r\n");
  }
  errorValue=SetTriggerMode(trig);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set Trigger Mode Error\r\n");

  // This function only needs to be called when acquiring an image. It sets
  // the horizontal and vertical binning and the area of the image to be
  // captured. In this example it is set to 1x1 binning and is acquiring the
  // whole image
  SetImage(1,1,1,gblXPixels,1,gblYPixels);

  // Starting the acquisition also starts a timer which checks the card status
  // When the acquisition is complete the data is read from the card and
  // displayed in the paint area.
  errorValue=StartAcquisition();
  if(trig==1)
    strcat(aBuffer,"Waiting for external trigger\r\n");
  if(errorValue!=DRV_SUCCESS){
    strcat(aBuffer,"Start acquisition error");
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

  if(lparam==(LPARAM)pbStart){  // Start acquisition button is pressed
    gblData=TRUE;           // tells system an acq has taken place
    GetStatus(&status);
    if(status==DRV_IDLE){
      SetSystem();          // Set hardware and start acquisition
      FillRectangle();      // clear window ready for data trace
    }
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
  UpdateWindow(ebOpenClose);
  UpdateWindow(stOpenClose);
  UpdateWindow(cbTTL);
  UpdateWindow(stTTL);
  UpdateWindow(cbTrigger);
  UpdateWindow(stTrigger);
  UpdateWindow(ebStatus);
  UpdateWindow(stStatus);
  UpdateWindow(pbStart);
  UpdateWindow(pbAbort);
  UpdateWindow(pbClose);
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
  long 		MaxValue;
  long		MinValue;

  size=AllocateBuffers();	 // Allocate memory for image data. Size is returned
                           // for GetAcquiredData which needs the buffer size

  errorValue=GetAcquiredData(pImageArray,size);
  if(errorValue!=DRV_SUCCESS){
    wsprintf(aBuffer,"Acquisition error!");
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    return FALSE;
  }

  // Display data and query max data value to be displayed in status box
  FillRectangle();
  if(!DrawLines(&MaxValue,&MinValue)){
    KillTimer(hwnd,timer);
    wsprintf(aBuffer, "Data range is zero");
   	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);         
    return FALSE;
  }

  KillTimer(hwnd,timer);                   	// kill status timer

  // tell user acquisition is complete
  if(!gblData){														  // If there is no data the acq has
    wsprintf(aBuffer,"Acquisition aborted"); // been aborted
  }
  else{
    // tell user acquisition is complete
    wsprintf(aBuffer,"Acquisition complete !\r\n");
    wsprintf(aBuffer2,"Full image acquired\r\n\r\n");
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
	HANDLE 			hBmp;              // handle to Andor bitmap
  HDC 				hBitmapDC;
  HDC 				hMemDC;
  PAINTSTRUCT PtrStr;
  long				MaxValue;
  long				MinValue;
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
    if(DrawLines(&MaxValue,&MinValue)==FALSE){    	// values is not used in this case
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

BOOL DrawLines(long *pMaxDataValue,long *pMinDataValue)
{
  int 			i;
  BOOL 			bRetValue=TRUE;
  long 			MaxValue=1;
  long      MinValue=65536;

  if(gblData && pImageArray!=NULL){

    // Find max value and scale data to fill rect
    for(i=0;i<(gblXPixels*gblYPixels);i++){
      if(pImageArray[i]>MaxValue)
        MaxValue=pImageArray[i];
      if(pImageArray[i]<MinValue)
        MinValue=pImageArray[i];
    }

    if(MaxValue == MinValue)
    	return FALSE;

    PaintImage(MaxValue, MinValue, 0); //Display image

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

	FreeBuffers();

	size=gblXPixels*gblYPixels;  // Needs to hold full image

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
  if (lvRunning == FALSE) {// if the screensaver is not running, plot data.
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


