//------------------------------------------------------------------------------
//  PROJECT:		32-bit Driver Example Code ---- Full Vertical Binning
//
//  Copyright 1998. All Rights Reserved
//
//  FILE:				FVBWndw.c
//  AUTHOR:			Paul McKernon
//
//  OVERVIEW:		This Project shows how to set up the Andor MCD to take a single
//							FVB acquisition and display it on the screen. It will
//							familiarise you with using the Andor MCD driver library.
//------------------------------------------------------------------------------

#include <windows.h>            // required for all Windows applications
#include "atmcd32d.h"

// Function Prototypes
BOOL CreateWindows(void);            // Create control windows and allocate handles
void SetupWindows(void);             // Initialize control windows
void SetWindowsToDefault(char[256]);  // Fills windows with default values
void SetSystem(void);                // Sets hardware parameters
void ProcessTimer(WPARAM);        // Handles WM_TIMER messages
void ProcessPushButtons(LPARAM);  // Processes button presses
void UpdateDialogWindows(void);      // refreshes all windows
void FillRectangle(void);            // clears paint area
BOOL AcquireImageData(void);         // Acquires data from card
void PaintDataWindow(void);       // Prepares paint area on screen
BOOL DrawLines(long*,long*);				 // paints data to screen
int AllocateBuffers(void);           // Allocates memory for buffers
void FreeBuffers(void);              // Frees allocated memory
BOOL ProcessMessages(UINT message, WPARAM wparam, LPARAM lparam){return FALSE;} // No messages to process in this example

// Set up acquisition parameters here to be set in common.c *****************
int acquisitionMode=1;
int readMode=0;
int xWidth=640;   // width of application window passed to common.c
int yHeight=480;  // height of application window passed to common.c
//******************************************************************************



extern int gblXPixels; 			// Get dims from cooler.c
extern int gblYPixels;

// Declare Image Buffers
long *pImageArray = NULL;	 // main image buffer read from card
POINT *pPointsArray=NULL;	 // points data required to draw one polyline

int timer=100;         		 // ID of timer that checks status before acquisition

BOOL errorFlag;						 // Tells us if initialization failed in common.c
BOOL gblData=FALSE;    		 // flag is set when first acquisition is taken, tells
													 // system that there is data to display
RECT rect;						 		 // Dims of paint area

extern HWND hwnd;          // Handle to main application

HWND				ebInit,        // handles for the individual
            stInit,        // windows such as edit boxes
            ebExposure,    // and comboboxes etc.
            stExposure,
            cbTrigger,
            stTrigger,
            ebStatus,
            stStatus,
            pbStart,
            pbAbort,
            pbClose,
            st1,
            stWidth,
            stGateMode,
            cbGateMode,
            stGain,
            ebGain;


extern HINSTANCE hInst;// Current Instance

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
                        10,2,180,18,hwnd,0,hInstance,NULL);
  ebInit=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                        10,20,315,40,hwnd,0,hInstance,NULL);
  stExposure=CreateWindow("STATIC","Exposure time (secs):",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,140,160,20,hwnd,0,hInstance,NULL);
  ebExposure=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                        270,140,50,20,hwnd,0,hInstance,NULL);
  stTrigger=CreateWindow("STATIC","Trigger Mode:",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,180,180,20,hwnd,0,hInstance,NULL);
  cbTrigger=CreateWindow("COMBOBOX","",
                        WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
                        220,180,100,80,hwnd,0,hInstance,NULL);
  ebStatus=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_MULTILINE,
                        340,20,270,240,hwnd,0,hInstance,NULL);
  pbStart=CreateWindow("BUTTON","Start Acq",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        10,240,100,30,hwnd,0,hInstance,NULL);
  pbAbort=CreateWindow("BUTTON","Abort Acq",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        115,240,100,30,hwnd,0,hInstance,NULL);
  pbClose=CreateWindow("BUTTON","Close",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        220,240,100,30,hwnd,0,hInstance,NULL);
  stStatus=CreateWindow("STATIC","Status",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        340,2,60,18,hwnd,0,hInstance,NULL);
  st1=CreateWindow("STATIC","1",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        0,430,20,20,hwnd,0,hInstance,NULL);
  stWidth=CreateWindow("STATIC",aBuffer,
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        580,430,40,20,hwnd,0,hInstance,NULL);

  stGateMode=CreateWindow("STATIC","GateMode",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,70,160,20,hwnd,0,hInstance,NULL);
                        
  cbGateMode=CreateWindow("COMBOBOX","",
                        WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
                        200,70,100,80,hwnd,0,hInstance,NULL);

  stGain=CreateWindow("STATIC","Gain",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,100,160,20,hwnd,0,hInstance,NULL);

  ebGain=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_MULTILINE,
                        200,100,100,20,hwnd,0,hInstance,NULL);

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
//									data.
//
//	ARGUMENTS: 			char aInitializeString: Message to be displayed in init
//																					edit box
//------------------------------------------------------------------------------

void SetWindowsToDefault(char aInitializeString[256])
{
  char aBuffer[256];
  char aBuffer2[256];

  // add *autoshutter and send to window
  strcat(aInitializeString,"*Auto Shutter");
  SendMessage(ebInit, WM_SETTEXT, 0, (LPARAM)(LPSTR)aInitializeString);

  // Fill in default exposure time
  wsprintf(aBuffer,"0.1");
  SendMessage(ebExposure, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Add options to GateMode combo box
  wsprintf(aBuffer,"CW on");
  SendMessage(cbGateMode, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"CW off");
  SendMessage(cbGateMode, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"D Gate");
  SendMessage(cbGateMode, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);

  // Select default GateMode
  wsprintf(aBuffer,"CW on");
  SendMessage(cbGateMode, CB_SELECTSTRING,0,(LPARAM)(LPSTR)aBuffer);

  // Fill in default exposure time
  wsprintf(aBuffer,"1");
  SendMessage(ebGain, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Add options to trigger combo box
  wsprintf(aBuffer,"Internal");
  SendMessage(cbTrigger, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"External");
  SendMessage(cbTrigger, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);

  // Select default trigger
  wsprintf(aBuffer,"Internal");
  SendMessage(cbTrigger, CB_SELECTSTRING,0,(LPARAM)(LPSTR)aBuffer);

  // Print Status messages
  wsprintf(aBuffer,"Initializing Andor MCD system\r\n");
  strcat(aBuffer,"Single Scan Selected\r\n");
  strcat(aBuffer,"Set to FVB Mode\r\n");
  wsprintf(aBuffer2,"Size of CCD: %d x %d\r\n",gblXPixels,gblYPixels);
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
//  DESCRIPTION:    This function sets up the acquisition hardware settings such
//									as exposure time and trigger etc and starts the acquisition.
//									It also starts a timer to check when the acquisition has
//									finished (when getStatus = DRV_IDLE).
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void SetSystem(void)
{
  float		fExposure,fAccumTime,fKineticTime;
  int 		errorValue;
  int 		trig;
  char 		aBuffer[256];
  char 		aBuffer2[256];
  int gatemode,intGain;
  long info;
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

  //set gatemode and gain
  GetWindowText(cbGateMode,aBuffer2,10);
  if(strcmp(aBuffer2,"CW on")==0){
    gatemode=3;
    strcat(aBuffer,"Gatemode set to cw on\r\n");
  }
  if(strcmp(aBuffer2,"CW off")==0){
    gatemode=4;
    strcat(aBuffer,"Gatemode set to cw off\r\n");
  }
  if(strcmp(aBuffer2,"D Gate")==0){
    gatemode=2;
    strcat(aBuffer,"Gatemode set to Direct Gate\r\n");
  }
  errorValue=SetGateMode(gatemode);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set Gate Mode Error\r\n");

  //SetGain
  GetWindowText(ebGain,aBuffer2, 10);
  intGain=atof(aBuffer2);
  errorValue = SetGain(intGain);
  if (errorValue != DRV_SUCCESS)
    wsprintf(aBuffer,"Set Gain error\r\n");

  errorValue = GetCameraInformation(0,&info);
  if (errorValue != DRV_SUCCESS)
    wsprintf(aBuffer,"USB camera not seup right\r\n");
  if ( info != 7)
    wsprintf(aBuffer,"Error GetUSBCameraInfo\r\n");

  if (errorValue != DRV_SUCCESS){
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    UpdateWindow(ebStatus);
    return;
  }




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
  errorValue=SetTriggerMode(trig);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set Trigger Mode Error\r\n");

  // Starting the acquisition also starts a timer which checks the card status
  // When the acquisition is complete the data is read from the card and
  // displayed in the paint area.
  errorValue=StartAcquisition();
  if(trig==1)
    strcat(aBuffer,"Waiting for external trigger\r\n");
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
	int 		errorValue;
  char 		aBuffer[256];
  int 		status;

  if(lparam==(LPARAM)pbStart){  // Start acquisition button is pressed
    gblData=TRUE;								// tells system an acq has taken place
    GetStatus(&status);
    if(status==DRV_IDLE){
      SetSystem();              // Set hardware and start acquisition
      FillRectangle();          // clear window ready for data trace
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
      gblData=FALSE;    // tell system no acq data in place
    }
    // or else let user know none is in progress
    else{
      wsprintf(aBuffer,"System not Acquiring");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    }
  }

  if(lparam==(LPARAM)pbClose){ // close application
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
  UpdateWindow(cbTrigger);
  UpdateWindow(stTrigger);
  UpdateWindow(ebStatus);
  UpdateWindow(stStatus);
  UpdateWindow(pbStart);
  UpdateWindow(pbAbort);
  UpdateWindow(pbClose);
  UpdateWindow(st1);
  UpdateWindow(stWidth);
  UpdateWindow(stGateMode);
  UpdateWindow(cbGateMode);
  UpdateWindow(stGain);
  UpdateWindow(ebGain);
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	FillRectangle()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function paints a white rectangle onto which we paint
//									the data trace.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void FillRectangle(void)
{
  HGDIOBJ 	prevObject;
  HBRUSH 		fill;
  HDC 			hdcRect;

  rect.left=10;        // Co-ordinates of paint area
  rect.top=279;
  rect.right=610;
  rect.bottom=431;

  hdcRect=GetDC(hwnd);
  fill=CreateSolidBrush(0xFFFFFF);   			// Select white brush
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
  long 		MaxValue;
  long		MinValue;

  size=AllocateBuffers();  // Allocate memory for image data. Size is returned
                           // for GetAcquiredData which needs the buffer size

  errorValue=GetAcquiredData(pImageArray,size);
  if(errorValue!=DRV_SUCCESS){
    wsprintf(aBuffer,"Acquisition error!");
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    return FALSE;
  }

  // Display data and query max data value to be displayed in status box
  FillRectangle(); 
  if(DrawLines(&MaxValue,&MinValue)==FALSE){
    KillTimer(hwnd,timer);
    wsprintf(aBuffer, "Data range is zero");
   	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);         
    return FALSE;
  }

  KillTimer(hwnd,timer);

  if(!gblData){                             // If there is no data the acq has
    wsprintf(aBuffer,"Acquisition aborted"); // been aborted
  }
  else{
    // tell user acquisition is complete
    wsprintf(aBuffer,"Acquisition complete !\r\n");
    strcat(aBuffer,"Fully Vertically Binned Scan taken\r\n\r\n");
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
  HANDLE 				hBmp;        		// handle to Andor bitmap
  HDC 					hBitmapDC;
  HDC						hMemDC;
  PAINTSTRUCT 	PtrStr;
  long 					MaxValue;
  long 					MinValue;
  int						bitmapWidth=266;
  int						bitmapHeight=64;

  // Redraw all dialog elements
  UpdateDialogWindows();
  FillRectangle();

  // Paint bitmap onto screen until first acquisition is taken
  if(!gblData || pImageArray==NULL){
    hBmp=LoadBitmap(hInst,"Andortch");
    hBitmapDC=BeginPaint(hwnd,&PtrStr);
    hMemDC=CreateCompatibleDC(hBitmapDC);
    SelectObject(hMemDC,hBmp);

    //Place Bitmap in center of paint area
    BitBlt(hBitmapDC,
           rect.left+(((rect.right-rect.left)-266)/2),   // x
           rect.top+(((rect.bottom-rect.top)-66)/2),     // y
           bitmapWidth,                                  // width
           bitmapHeight,                                 // height
           hMemDC,0,0,SRCCOPY);
    DeleteDC(hMemDC);
    EndPaint(hwnd,&PtrStr);
  }
  // When data is available paint it onto the screen using drawlines()
  else{
    if(DrawLines(&MaxValue,&MinValue)==FALSE){    // maxvalue is not used in this case
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
//									FALSE: One or more Polylines failed to draw
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function paints the data traces onto the screen using
//									a blue pen. The pen must be set back to the original each
//									time it is used
//
//	ARGUMENTS: 			long *pMaxDataValue: 		This returns the max value to be
//																					displayed in the status box.
//------------------------------------------------------------------------------

BOOL DrawLines(long *pMaxDataValue,long *pMinDataValue)
{
  HGDIOBJ 	prevObject;
  HDC 			hdc;
  HPEN 			hpen;
  int 			i;
  float 		xScale;
  BOOL 			bRetValue=TRUE;
  long 			MaxValue=1;
  long			MinValue=65536;
  int 			width,height;

  if(gblData && pImageArray!=NULL){
    hdc=GetDC(hwnd);
    hpen=CreatePen(PS_SOLID,0,0xFF0000);    // Select blue pen to draw lines
    prevObject=SelectObject(hdc,hpen);

    // get width and height of paint area
    width=rect.right-rect.left;
    height=rect.bottom-rect.top-2;

    // Scale width into available space
    xScale=(float)gblXPixels/(float)width;

    // Find max value and scale data to fill rect
    for(i=0;i<gblXPixels;i++){
      if(pImageArray[i]>MaxValue)
        MaxValue=pImageArray[i];
      if(pImageArray[i]<MinValue)
        MinValue=pImageArray[i];
    }

    if(MaxValue == MinValue)
    	return FALSE;
      
    // Create an array of (x,y) points for the polyline
    for(i=0;i<gblXPixels;i++){
      pPointsArray[i].x=rect.left+(int)((float)i/(float)xScale);
      pPointsArray[i].y=(rect.bottom-1-((pImageArray[i]-MinValue)*height/(MaxValue-MinValue)));
    }

    MoveToEx(hdc,pPointsArray[0].x,pPointsArray[0].y,NULL);    // start line at point[0]
    if(PolylineTo(hdc,pPointsArray,(DWORD)gblXPixels)==FALSE)   // Draw polyline
      bRetValue=FALSE;
    SelectObject(hdc,prevObject);
    ReleaseDC(hwnd,hdc);
    DeleteObject(hpen);

    *pMaxDataValue=MaxValue;    // tell acquiredata function the max value so
                               // that it can display it in the status box
    *pMinDataValue=MinValue;    // tell acquiredata function the max value so
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

	size=gblXPixels;  // only 1 horizontal line of data for FVB

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
//  DESCRIPTION:    This function frees the memory allocated to each buffer and
//									is called when the application exits.
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
