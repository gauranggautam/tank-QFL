//------------------------------------------------------------------------------
//  PROJECT:		32-bit Driver Example Code ---- Full Image Acquisition
//
//  Copyright 1998. All Rights Reserved
//
//  FILE:			mechellewndw.c
//  AUTHOR:			Dermot McCluskey
//
//  OVERVIEW:		This Project shows how to set up the Andor MCD to take a single
//						image acquisition. From there it will show how to use the Mechelle
//                SDK to produce a spectrum and to calibrate the image. It will
//						familiarise you with using the Andor MCD driver library.
//------------------------------------------------------------------------------

#include <windows.h>            // required for all Windows applications
#include "atmcd32d.h"           // Andor function definitions
#include <stdio.h>
#include "atmechelle.h"

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
int AllocateBuffers(void);        // Allocates memory for buffers
int AllocateMechelleBuffers(void);        // Allocates memory for buffers
void FreeBuffers(void);           // Frees allocated memory
BOOL InitializeMechelle(void);
BOOL DoesFileEvenExist(char * filepath);
BOOL CalibrateMechelle(void);
BOOL SaveCalibrationMechelle(void);
BOOL DrawSpectrograph(long*,long*);  // draws the mechelle spectrograph
BOOL SetCalibrationMechelle(void);
BOOL RestoreCalibrationMechelle(void);
BOOL ProcessMessages(UINT message, WPARAM wparam, LPARAM lparam){return FALSE;} // No messages to process in this example

// Set up acquisition parameters here to be set in common.c *****************
int acquisitionMode=2;
int readMode=4;
int xWidth=640;		 // width of application window passed to common.c
int yHeight=640;   // height of application window passed to common.c
long XMLArraySize=0;
//******************************************************************************

extern int 	gblXPixels;     // Get dims from common.c
extern int 	gblYPixels;

// Declare Image Buffers
long 				*pImageArray=NULL;    // main image buffer read from card
int 				*pintImageArray=NULL;    // main image buffer read from card
//long 				*pTempImageArray=NULL;// one line of image of the mechelle spectrograph
POINT 			*pPointsArray;   // points data required to draw one polyline
SpectralData   *gpspectrum;//structre required by mechelle
int giSpectrumLength;
int *pMechelleSpectrumArray;  //max value got from the XML file

HINSTANCE hinst;

int 				gblNoTracks=1; 	 // Number of tracks for this example
int 				timer=100;     	 // ID of timer that checks status before acquisition

BOOL 				errorFlag;		 	 // Tells us if initialization failed in common.c
BOOL 				gblData=FALSE; 	 // flag is set when first acquisition is taken, tells
											 		 	 //	system that there is data to display
int gimageArraysizeint;
int gimageArraysizelong;
int gBufferSize;

RECT 				rect;					 	 // Dims of paint area

extern HWND hwnd;          	 // Handle to main application

HWND			ebInit,      	 	 // handles for the individual
            stInit,     	   // windows such as edit boxes
            ebExposure,  	 	 // and comboboxes etc.
            stExposure,
            ebCooler,
            stCooler,
            ebCoolerTemp,
            cbTemperature,
            stTemperature,
            stAccumNo,
            ebAccumNo,
            ebGain,
            stGain,
            ebStatus,
            stStatus,
            pbStart,
            pbAbort,
            pbClose,
            st1,
            stWidth,
            pbInitMechelle,
            ebMechelle,
            stMechelleXML,
            ebMechelleCalibFile,
            pbCalibrateMechelle,
            ebSearchArea,
            stSearchArea,
            pbSaveCalibration,
            pbSetCalibration,
            pbRestoreCalibration,
            stWidth,
            stInitMechelle;

extern 			HINSTANCE hInst;       // Current Instance

//Global flags to ensure that operations are only done if we are ready for them.
BOOL bMechelleInitialized;
BOOL bAcquisitionDone;
BOOL BSuccessfulCalibration;
char gMechelleInitFile[512];


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
		char 			aBuffer[256];

		wsprintf(aBuffer,"%d",gblXPixels);   // to be placed in txtWidth

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
  	stCooler=CreateWindow("STATIC","Cooler state/required temp",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													10,120,180,20,hwnd,0,hInstance,NULL);
		ebCooler=CreateWindow("EDIT","0",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
													200,120,50,20,hwnd,0,hInstance,NULL);
		ebCoolerTemp=CreateWindow("EDIT","0",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
													270,120,50,20,hwnd,0,hInstance,NULL);
		stTemperature=CreateWindow("STATIC","Actual Temperature",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
  												10,150,180,20,hwnd,0,hInstance,NULL);
		cbTemperature=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
    											200,150,100,20,hwnd,0,hInstance,NULL);

   stAccumNo=CreateWindow("STATIC","No in Accum",
     											WS_CHILD|WS_VISIBLE|SS_LEFT,
  		 										10,180,180,20,hwnd,0,hInstance,NULL);

   ebAccumNo=CreateWindow("EDIT","No in Accum",
   											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
  		 										200,180,60,20,hwnd,0,hInstance,NULL);

  	stGain=CreateWindow("STATIC","Gain :",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													10,210,180,20,hwnd,0,hInstance,NULL);
  	ebGain=CreateWindow("EDIT","",
   											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
													220,210,100,20,hwnd,0,hInstance,NULL);
    ebStatus=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_AUTOVSCROLL|ES_MULTILINE,
													340,20,270,240,hwnd,0,hInstance,NULL);

    pbStart=CreateWindow("BUTTON","Start Acq",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													10,240,90,30,hwnd,0,hInstance,NULL);
    pbAbort=CreateWindow("BUTTON","Abort Acq",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													120,240,90,30,hwnd,0,hInstance,NULL);
    pbClose=CreateWindow("BUTTON","Close",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													230,240,90,30,hwnd,0,hInstance,NULL);


  	stMechelleXML=CreateWindow("STATIC","XML file:",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
                                    //xcord ycord width height
													10,290,30,30,hwnd,0,hInstance,NULL);

    ebMechelle=CreateWindow("EDIT","",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_AUTOVSCROLL|ES_MULTILINE,
													45,290,560,25,hwnd,0,hInstance,NULL);


    pbInitMechelle=CreateWindow("BUTTON","Init Mechelle",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													10,330,140,30,hwnd,0,hInstance,NULL);
    stInitMechelle=CreateWindow("STATIC","Init mechelle with XML file above",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
                                    //xcord ycord width height
													180,330,400,30,hwnd,0,hInstance,NULL);

		ebMechelleCalibFile=CreateWindow("EDIT","",
    												WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
    											120,380,120,25,hwnd,0,hInstance,NULL);

     	stSearchArea=CreateWindow("STATIC","Search Area:",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
                                    //xcord ycord width height
													260,380,90,25,hwnd,0,hInstance,NULL);

        ebSearchArea=CreateWindow("EDIT","",
    												WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
													360,380,60,25,hwnd,0,hInstance,NULL);


     pbCalibrateMechelle=CreateWindow("BUTTON","Calibrate",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													10,380,90,30,hwnd,0,hInstance,NULL);

       pbSaveCalibration=CreateWindow("BUTTON","Save Calibration",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
													10,420,120,30,hwnd,0,hInstance,NULL);

       pbSetCalibration=CreateWindow("BUTTON","SetCalibration",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
	  												250,420,120,30,hwnd,0,hInstance,NULL);
       pbRestoreCalibration=CreateWindow("BUTTON","RestoreCalibration",
    											WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
		  											380,420,130,30,hwnd,0,hInstance,NULL);


    stStatus=CreateWindow("STATIC","Status",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													340,2,60,18,hwnd,0,hInstance,NULL);
		st1=CreateWindow("STATIC","1",
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													0,580,20,20,hwnd,0,hInstance,NULL);
		stWidth=CreateWindow("STATIC",aBuffer,
    											WS_CHILD|WS_VISIBLE|SS_LEFT,
													580,580,40,20,hwnd,0,hInstance,NULL);

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
	char 	aBuffer[512];
  char 	aBuffer2[512];

	// add *autoshutter and send to window
  strcat(aInitializeString,"*Auto Shutter");
  SendMessage(ebInit, WM_SETTEXT, 0, (LPARAM)(LPSTR)aInitializeString);

  // Fill in default exposure time
  wsprintf(aBuffer,"1");
  SendMessage(ebExposure, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);
  wsprintf(aBuffer,"On");
  SendMessage(ebCooler, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  // Add temperature to
  wsprintf(aBuffer,"0");
  SendMessage(cbTemperature, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);
  CoolerON();
  SetTemperature(0);



  // Add tGain default
  wsprintf(aBuffer,"200");
  SendMessage(ebGain, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);


  // Print Status messages
  wsprintf(aBuffer,"Initializing Andor MCD system\r\n");
  strcat(aBuffer,"Single Scan Selected\r\n");
  strcat(aBuffer,"Set to Image Mode\r\n");
  wsprintf(aBuffer2,"Size of CCD: %d x %d\r\n",gblXPixels,gblYPixels);
  strcat(aBuffer,aBuffer2);
  SendMessage(ebStatus, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  //get a default file for the mechelle xml file

  //GetCurrentDirectory(512,aBuffer);// Look in current working directory
  //strcat(aBuffer,"\\mechelle\\AndorMechelleGNR\\GNRAndorDV.xml");
  strcpy(aBuffer,"C:\\Program Files\\Andor iStar\\Mechelle\\Mechelle 5000\\Mechelle5000.xml");

  SendMessage(ebMechelle, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  wsprintf(aBuffer,"30");
  SendMessage(ebSearchArea, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  //initialize mechelle flags
  bMechelleInitialized = FALSE;
  bAcquisitionDone = FALSE;
  BSuccessfulCalibration = FALSE;

  //accumulation
  wsprintf(aBuffer,"1");
  SendMessage(ebAccumNo, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);



  gBufferSize=AllocateBuffers();	 // Allocate memory for image data. Size is returned
                           // for GetAcquiredData which needs the buffer size

}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetSystem()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:    This function sets up the acquisition settings exposure time
//									shutter, triggerGain and starts an acquisition. It also starts a
//									timer to check when the acquisition has finished.
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

void SetSystem(void)
{
  float		fExposure,fAccumTime,fKineticTime;
  int 		errorValue;
  int 		noofaccums,temperature,gain;
  char 		aBuffer[256];
  char 		aBuffer2[256];
  char text[50];
  unsigned __int64 gateWidth;

  // Set Exposure Time
  GetWindowText(ebExposure,aBuffer2,5);
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


  // Get cooler state
  GetWindowText(ebCooler,aBuffer2,10);
  if ((strcmp(aBuffer2,"on")==0) || (strcmp(aBuffer2,"On")==0) || (strcmp(aBuffer2,"ON")==0))
  {
  	 CoolerON();
    strcat(aBuffer,"Cooler On\r\n");
    sprintf(text,"On");
    SendMessage(ebCooler, WM_SETTEXT, 0, (LPARAM)(LPSTR)text);
  }
  else
  {
    strcat(aBuffer,"Cooler Off\r\n");
    CoolerOFF();
    sprintf(text,"Off");
    SendMessage(ebCooler, WM_SETTEXT, 0, (LPARAM)(LPSTR)text);

  }
  // Get temperature level
  GetWindowText(ebCoolerTemp,aBuffer2,10);
  temperature = atoi( aBuffer2);
  if (( temperature < -40) || ( temperature > 50))
       temperature = 5;

  errorValue = SetTemperature(temperature);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set SetTemperature Error\r\n");

  // Get Gain
  GetWindowText(ebGain,aBuffer2,10);
  gain = atoi( aBuffer2);
  if (( gain < 0) || ( gain > 255))
       gain = 5;
  errorValue=SetGain(gain);


  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"SetGain Error\r\n");

  // This function only needs to be called when acquiring an image. It sets
  // the horizontal and vertical binning and the area of the image to be
  // captured. In this example it is set to 1x1 binning and is acquiring the
  // whole image
  SetImage(1,1,1,gblXPixels,1,gblYPixels);

  // Starting the acquisition also starts a timer which checks the card status
  // When the acquisition is complete the data is read from the card and
  // displayed in the paint area.

  //Set Horizontal Speed
  errorValue = SetHorizontalSpeed(0);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set SetHorizontalSpeed Error\r\n");

    //number of accum
  GetWindowText(ebAccumNo,aBuffer2,10);
  noofaccums = atoi(aBuffer2);

  if((noofaccums <= 0) || (noofaccums> 1000)) {
    noofaccums = 5;
    sprintf(text,"%d",noofaccums);
    SendMessage(ebAccumNo, WM_SETTEXT, 0, (LPARAM)(LPSTR)text);
  }

  errorValue = SetNumberAccumulations(noofaccums);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set SetNumberAccumulations Error\r\n");

  sprintf(text,"Set Number of Accumulations to %d\r\n",noofaccums);
  strcat(aBuffer,text);

  //just setting up a few to defaults
  errorValue = SetGateMode(5); //for istar only
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set SetGateMode Error\r\n");

  errorValue = SetShutter(1, 0, 10, 10) ;
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set SetShutter Error\r\n");


  gateWidth = fExposure * 1e12; //to convert to picoseconds
  errorValue = SetDDGGateTime(0, gateWidth);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set SetDDGTimes Error\r\n");

  errorValue = SetTriggerMode(0);
  if(errorValue!=DRV_SUCCESS)
    strcat(aBuffer,"Set SetDDGTriggerMode Error\r\n");

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
        if(AcquireImageData()==FALSE)
        {
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

  if(lparam==(LPARAM)pbInitMechelle){   // init mechelle
        wsprintf(aBuffer,"Trying to Initialise Mechelle");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);

      InitializeMechelle();
  }

  if(lparam==(LPARAM)pbCalibrateMechelle){   // calibrate mechelle
        wsprintf(aBuffer,"Trying to Calibrate Mechelle");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      CalibrateMechelle();
  }

  if(lparam==(LPARAM)pbSaveCalibration){   // calibrate mechelle
        wsprintf(aBuffer,"Trying to Save Calibration for Mechelle");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      SaveCalibrationMechelle();
  }

  if(lparam==(LPARAM)pbSetCalibration){   // set default calibration
      wsprintf(aBuffer,"Trying to Save Default Calibration to Mechelle EEPROM");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      if (SetCalibrationMechelle())
        wsprintf(aBuffer,"Success Saving to EEPROM");
      else
        wsprintf(aBuffer,"Failed Saving to EEPROM");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);

  }
  if(lparam==(LPARAM)pbRestoreCalibration){   // Restore default calibration
        wsprintf(aBuffer,"Trying to Restore Default Calibration from Mechelle EEPROM");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      RestoreCalibrationMechelle();
      if (RestoreCalibrationMechelle())
        wsprintf(aBuffer,"Success Restoring to EEPROM");
      else
        wsprintf(aBuffer,"Failed Restoring to EEPROM");
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);

  }


}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	SetCalibrationMechelle()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	DMC 10/03/2004
//
//  DESCRIPTION:    This function will try and save the current calibration
//                 parameters to the mechelle eeprom so the user can restore
//                 if problems are found later
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

BOOL SetCalibrationMechelle()
{
  unsigned int ret= MechelleBackupCalibration();
  if (ret == DRV_SUCCESS)
    return TRUE;
  else return FALSE;
}
//------------------------------------------------------------------------------
//	FUNCTION NAME:	RestoreCalibrationMechelle()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	DMC 10/03/2004
//
//  DESCRIPTION:    This function will try and restore the  calibration
//                 parameters saved int the mechelle eeprom so the user have
//                 a starting point he/she knows works.
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

BOOL RestoreCalibrationMechelle()
{
  unsigned int ret= MechelleRestoreCalibration();
  if (ret == DRV_SUCCESS)
    return TRUE;
  else return FALSE;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	InitializeMechelle()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	DMC 10/03/2004
//
//  DESCRIPTION:    This function will Initialise Mechelle, it needs an XML file
//                  it gets here from the edit box ebMechelle
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

BOOL InitializeMechelle()
{
  //Check if the xml file exactly exists before trying to initialise with it
  char aBuffer[512];
  unsigned int ret;

  if (bMechelleInitialized)
  {
     wsprintf(aBuffer,"Already Initialized, please restart if you require new XML file");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }

  GetWindowText(ebMechelle,gMechelleInitFile,500);
  if (!DoesFileEvenExist( gMechelleInitFile))
  {

     wsprintf(aBuffer,"Not a valid XML file for Mechelle Init");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }
  //File exists so call mechelle initialize stuff

   ret = MechelleInit( gblXPixels,gblYPixels,gMechelleInitFile,&XMLArraySize);
  if (ret == DRV_GENERAL_ERRORS)
  {
     wsprintf(aBuffer,"Error Initializing Mechelle");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }
  else
  {
     bMechelleInitialized = TRUE;
     wsprintf(aBuffer,"Mechelle Initialized");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);

     AllocateMechelleBuffers();
  }

  wsprintf(aBuffer,"HgAr 1 line.wcl");
  SendMessage(ebMechelleCalibFile, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);

  return TRUE;

}
//------------------------------------------------------------------------------
//	FUNCTION NAME:	SaveCalibrationMechelle()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	DMC 10/03/2004
//
//  DESCRIPTION:    This function will save the internal values of the mechelle driver
//                  after a valid calibration
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------
BOOL SaveCalibrationMechelle(void)
{
  char aBuffer[512];
  float newtemp;
  
  if (!bMechelleInitialized)
  {
     wsprintf(aBuffer,"Need to initialize mechelle before continuing");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }
  if (!bAcquisitionDone)
  {
     wsprintf(aBuffer,"Need to have acquired a full image before calibrating");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }
  if (!BSuccessfulCalibration)
  {
     wsprintf(aBuffer,"Need to have had a successful calibration first");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }

  if (MechelleGetInternalTemperature(&newtemp) == DRV_GENERAL_ERRORS)
  {
     wsprintf(aBuffer,"Error Saving Calibration Temperature");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
  }

  if (MechelleSaveCalibration(&newtemp) == DRV_GENERAL_ERRORS)
  {
     wsprintf(aBuffer,"Error Saving Calibration");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }
  else
  {
     wsprintf(aBuffer,"Successful: Calibration saved");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
  }

  return TRUE;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	CalibrateMechelle()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	DMC 10/03/2004
//
//  DESCRIPTION:    This function will save the internal values of the mechelle driver
//                  after a valid calibration
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

BOOL CalibrateMechelle(void)
{
  char aBuffer[512];
  char aBuffer2[1024];
  char temp[256];
  int loop;
  char areatext[10];
  int isearcharea;
  char dir[256];
  char fileName[256];
  char ext[10];
  char drive[10];
 CalibrationData calibrationResults[20];
 int numberOfLines;


  if (!bAcquisitionDone)
  {
     wsprintf(aBuffer,"Need to acquire a full image before calibrating");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }
  if (!bMechelleInitialized)
  {
     wsprintf(aBuffer,"Need to initialize mechelle before continuing");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;
  }

  //here we need to get the wcl file from user and add rest of path to it to get actual path and file to pass to mechelle

  _splitpath(gMechelleInitFile,drive,dir,fileName,ext);

  strcpy(aBuffer,drive);
  strcat(aBuffer,dir);
  strcat(aBuffer,"calibration\\");
  GetWindowText(ebMechelleCalibFile,aBuffer2,100);
  strcat(aBuffer,aBuffer2);

  if (!DoesFileEvenExist(aBuffer))
  {
     wsprintf(aBuffer2,"ERROR    %s",aBuffer);
     strcat( aBuffer2, "    ******Does not Exist");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer2);
     return FALSE;
  }


  GetWindowText(ebSearchArea,areatext,10);
  isearcharea=atoi(areatext);
  if (( isearcharea < 0 ) || (isearcharea > 200))
  {
        isearcharea = 50;
        wsprintf(areatext,"50");
        SendMessage(ebSearchArea, WM_SETTEXT, 0, (LPARAM)(LPSTR)areatext);

  }

  //Pass in the last image acquired (remember converted to integer)

  if (MechelleCalibrate(aBuffer,&isearcharea,pintImageArray ,calibrationResults, &numberOfLines) == DRV_GENERAL_ERRORS)
  {
     wsprintf(aBuffer2,"ERROR Mechelle_calibrate function failed");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer2);
  }
  else
  {
     if (numberOfLines > 0 )
     {
       BSuccessfulCalibration = TRUE;
       wsprintf(aBuffer2,"Mechelle Calibration Lines found := %d ::",numberOfLines);
       for (loop = 0; loop < numberOfLines; loop++)
       {
         //This example displayed the residuals received for each line
         //See Structure CalibrationData for all data returned.

         sprintf(temp,"%.2f %.2f ::",calibrationResults[loop].residualX,calibrationResults[loop].residualY);
         strcat(aBuffer2,temp);
       }
     }

     else
     {
     		wsprintf(aBuffer2,"No lines found during calibration");
     		SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer2);
       	BSuccessfulCalibration = FALSE;
     }

     SendMessage(ebStatus, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer2);

  }

  return TRUE;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	DoesFileEvenExist()
//
//  RETURNS:				NONE
//
//  LAST MODIFIED:	DMC 10/03/2004
//
//  DESCRIPTION:    This function will check that the file entered exists
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------
BOOL DoesFileEvenExist(char * filepath)
{
   HANDLE spool;
 //open spool file for reading
  spool = CreateFile(filepath, GENERIC_READ, 0, NULL, OPEN_EXISTING, 0, NULL);
  if(spool == INVALID_HANDLE_VALUE)
  {
     CloseHandle(spool);
   return FALSE;
  }

       CloseHandle(spool);
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
  UpdateWindow(ebCooler);
  UpdateWindow(stCooler);
  UpdateWindow(ebCoolerTemp);
  UpdateWindow(cbTemperature);
  UpdateWindow(stTemperature);
  UpdateWindow(stAccumNo);
  UpdateWindow(ebAccumNo);
  UpdateWindow(ebGain);
  UpdateWindow(stGain);
  UpdateWindow(ebStatus);
  UpdateWindow(stStatus);
  UpdateWindow(pbStart);
  UpdateWindow(pbAbort);
  UpdateWindow(pbClose);
  UpdateWindow(st1);
  UpdateWindow(stWidth);
  UpdateWindow(pbInitMechelle);
  UpdateWindow(ebMechelle);
  UpdateWindow(stMechelleXML);
  UpdateWindow(ebMechelleCalibFile);
  UpdateWindow(pbCalibrateMechelle);
  UpdateWindow(ebSearchArea);

  UpdateWindow(pbSetCalibration);
  UpdateWindow(pbRestoreCalibration);

  UpdateWindow(stSearchArea);
  UpdateWindow(pbSaveCalibration);
  UpdateWindow(stInitMechelle);

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
  rect.top=500;
  rect.right=610;
  rect.bottom=580;

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
  int 		errorValue;
  unsigned int ret_code;
  char 		aBuffer[256];
  char 		aBuffer2[256];
  long 		MaxValue;
  long		MinValue;
  int       index;
  int q;
  int temperature;
  float fCurrentTemperature;
  float fSavedTemperature;
  int PixelAdjustX,PixelAdjustY;

  float tempDiff;
  double wlCalibCoefs[4]; //For mechelle needed to help plot graph in our Release software

  GetTemperature(&temperature);
  wsprintf(aBuffer,"%d",temperature);
  SendMessage(cbTemperature, WM_SETTEXT, 0, (LPARAM)(LPSTR)aBuffer);




  errorValue=GetAcquiredData(pImageArray,gBufferSize);
  if(errorValue!=DRV_SUCCESS){
    wsprintf(aBuffer,"Acquisition error!");
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
    bAcquisitionDone = TRUE;
  }
  SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);

  //Now we need to get the image ready for mechelle

  // cast and copy image

  for(index= 0; index < gBufferSize;index++ )
  {
  	 pintImageArray[index] = (int) pImageArray[index];
  }

  fCurrentTemperature = 34.6f;
  MechelleGetInternalTemperature(&fCurrentTemperature);

  MechelleGetSavedCalibrationTemperature(&fSavedTemperature);
  tempDiff = fCurrentTemperature - fSavedTemperature;
  //do we want to adjust image due to a temperature change in the mechelle?
   ret_code = MechelleImageTemperatureAdjust(pintImageArray,&fCurrentTemperature,&PixelAdjustX,&PixelAdjustY);
   if ((ret_code != DRV_SUCCESS) && (ret_code != MECHELLE_NOTEMPERATUREDIFFERENCE)) {
     wsprintf(aBuffer,"Error Temperature Adjust problems, Leaving as is");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
  }
  else {
    sprintf(aBuffer," %s %.1f Degrees Cel. Image Moved  x=%d,y=%d","Temperature Adjusted, difference =",tempDiff,PixelAdjustX,PixelAdjustY);
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
  }

  if (!bMechelleInitialized)
     return TRUE;

  //Now call function to produce our spectrum
  if (MechelleGenerateSpectrum(pintImageArray,gpspectrum,&giSpectrumLength,wlCalibCoefs) == DRV_GENERAL_ERRORS)
  {
     wsprintf(aBuffer,"Error Mechelle_Provide_Spectrum");
     SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
     return FALSE;

  }
  //We are now free to use the data in  mp_spectrumAfterConvert and the wlCalibCoefs to draw or spectrum
  // Display data and query max data value to be displayed in status box

 	for(q=0; q < giSpectrumLength;q++)
  	{
     		pMechelleSpectrumArray[q] = gpspectrum[q].intensity;
         if (pMechelleSpectrumArray[q] < 0)
           pMechelleSpectrumArray[q] = 0;
  	}


  FillRectangle();
  if(!DrawSpectrograph(&MaxValue,&MinValue)){
    KillTimer(hwnd,timer);
    wsprintf(aBuffer, "Data range is zero");
   	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    return FALSE;
  }


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
  int					i;
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
    for(i=0;i<gblNoTracks;i++){
      if(DrawSpectrograph(&MaxValue,&MinValue)==FALSE){    	// values is not used in this case
        char aBuffer[20];
      	wsprintf(aBuffer, "Data range is zero");
      	SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
      }
    }
  }

  // tell system that window is redrawn
  ValidateRect(hwnd,NULL);
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	DrawSpectrograph()
//
//  RETURNS:				TRUE: Function succeeded
//									FALSE: One or more Polylines failed to draw
//
//  LAST MODIFIED:	DMC	12/03/04
//
//  DESCRIPTION:    This function will draw the spectraph
//
//	ARGUMENTS: 			long *ppMaxDataValue: 		This returns the max value to be
//																					displayed in the status box.
//------------------------------------------------------------------------------

BOOL DrawSpectrograph(long *pMaxDataValue,long *pMinDataValue)
{
  HGDIOBJ 	prevObject;
  HDC 			hdc;
  HPEN 			hpen;
  int 			i;
  int 			trackHeight;
  BOOL 			bRetValue=TRUE;
  float 		xScale;
  long 			MaxValue=1;
  long      MinValue=65536;
  int 			width,height;
  int value;


  if(gblData && pMechelleSpectrumArray!=NULL){
    hdc=GetDC(hwnd);
    hpen=CreatePen(PS_SOLID,0,0xFF0000);   // Select blue pen to draw lines
    prevObject=SelectObject(hdc,hpen);

		// get width and height of paint area
    width=rect.right-rect.left;
    height=rect.bottom-rect.top-4;

    // Scale width into available space
    xScale=(float)giSpectrumLength/(float)width;

    // Find max value and scale data to fill rect
    for(i=0;i<(giSpectrumLength);i++){
      if(pMechelleSpectrumArray[i]>MaxValue)
        MaxValue=pMechelleSpectrumArray[i];
      if(pMechelleSpectrumArray[i]<MinValue)
        MinValue=pMechelleSpectrumArray[i];
    }

    if(MaxValue == MinValue)
    	return FALSE;

    // Scale height into available space
    trackHeight=height/gblNoTracks;

    // Create an array of (x,y) points for the polyline
    if (giSpectrumLength >= XMLArraySize)
    {
        return FALSE;

    }



    for(i=0;i<giSpectrumLength;i++){

        // Copy the required track into a temp buffer
        value=((pMechelleSpectrumArray[i]-MinValue)*trackHeight/(MaxValue-MinValue));

        pPointsArray[i].x=rect.left+(int)((float)i/xScale);
        pPointsArray[i].y=rect.bottom-1-value;

        if  (pPointsArray[0].x == 2)
               trackHeight=height/gblNoTracks;
    }

    MoveToEx(hdc,pPointsArray[0].x,pPointsArray[0].y,NULL);     // start line at point[0]
    if(PolylineTo(hdc,pPointsArray,(DWORD)giSpectrumLength)==FALSE)   // Draw polyline
        bRetValue=FALSE;

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
	size=gblXPixels*gblYPixels;  // Needs to hold full image

   gimageArraysizelong = size*sizeof(long);
   gimageArraysizeint = size*sizeof(int);

  // only allocate if necessary
  if(!pImageArray)
  	pImageArray=malloc(gimageArraysizelong);


  if(!pintImageArray)
  	pintImageArray=malloc(gimageArraysizeint);

//  if(!pPointsArray)
//  	pPointsArray=malloc(XMLArraySize*sizeof(POINT));

  return size;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	AllocateMechelleBuffers()
//
//  RETURNS:				int 0 error 1 OK
//
//  LAST MODIFIED:
//
//  DESCRIPTION:    This function allocates enough memory for mechelle arrays
//
//	ARGUMENTS: 			NONE
//------------------------------------------------------------------------------

int AllocateMechelleBuffers(void)
{

  if(!gpspectrum)
      gpspectrum = malloc(XMLArraySize*sizeof(SpectralData)) ;

  if(!pMechelleSpectrumArray)
      pMechelleSpectrumArray = malloc(XMLArraySize*sizeof(int)) ; //value got from the xml file

  if(!pPointsArray)
  	pPointsArray=malloc(XMLArraySize*sizeof(POINT));

  return 1;
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

  if(pintImageArray){
    free(pintImageArray);
    pintImageArray = NULL;
  }

  if(gpspectrum){
    free(gpspectrum);
    gpspectrum = NULL;
  }
  if(pMechelleSpectrumArray){
    free(pMechelleSpectrumArray);
    pMechelleSpectrumArray = NULL;
  }
}
