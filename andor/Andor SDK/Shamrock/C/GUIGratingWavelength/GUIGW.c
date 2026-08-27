//------------------------------------------------------------------------------
//  PROJECT:       Basic Shamrock SDK Graphic C example
//
//  Copyright 2005. All Rights Reserved
//
//  FILE:          ShamrockBasic.c
//  AUTHOR:        Elm Costa i Bricha
//
//  OVERVIEW:      This Project shows how to Initialize one or more Shamrocks and
//                 to read the Serial Number and Optical Parameters.
//                 It will familiarise you with using the Shamrock SDK library.
//------------------------------------------------------------------------------

#include <windows.h>                // required for all Windows applications
#include <stdio.h>                  // required for sprintf()
#include <dos.h>                    // required for sleep()
#include "ShamrockCIF.h"            // Andor function definitions

// Function Prototypes
BOOL CreateWindows(void);           // Create control windows and allocate handles
void SetupWindows(void);            // Initialize control windows
void ProcessPushButtons(LPARAM);    // Processes button presses
void UpdateShamrockParameters(void);// Updates Shamrock Parameters

// Set up window dimensions here to be set in ShamrockGUI.c ********************
int xWidth=505;    // width of application window passed to common.c
int yHeight=470;   // height of application window passed to common.c
//******************************************************************************

extern int    NoDevices; // No. of available Shamrocks
extern int    device;    // current device
int           turret;    // current turret settings
int           grating;   // current grating
BOOL errorFlag;          // Tells us if initialization failed in common.c

extern HWND   hwnd;      // Handle to main application

HWND          ebInit,    // handles for the individual
              stInit,    // windows such as edit boxes
              stDevice,  // and comboboxes etc.
              cbDevice,
              stSerial,
              ebSerial,
              stFocalL,
              ebFocalL,
              stAngDev,
              ebAngDev,
              stFocalT,
              ebFocalT,
              ebStatus,
              stStatus,
              stTurret,
              cbTurret,
              stGrat,
              cbGrat,
              stLines,
              ebLines,
              stBlaze,
              ebBlaze,
              stHome,
              ebHome,
              stOffset,
              ebOffset,
              pbSetOffset,
              ebSetOffset,
              stWaveL,
              ebWaveL,
              stMinWave,
              ebMinWave,
              stMaxWave,
              ebMaxWave,
              pbGotoWave,
              ebGotoWave,
              pbResetWave,
              pbClose;

extern HINSTANCE hInst;  // Current Instance

//------------------------------------------------------------------------------
//  FUNCTION NAME: CreateWindows()
//
//  RETURNS:       TRUE: Successful
//                 FALSE: Unsuccessful
//
//  LAST MODIFIED: ECiB 31/01/05
//
//  DESCRIPTION:   This function creates the individual controls placed in the
//                 main window. i.e. Comboboxes, edit boxes etc. When they are
//                 created they are issued a handle which is stored in it's
//                 global variable.
//
//  ARGUMENTS:     NONE
//------------------------------------------------------------------------------

BOOL CreateWindows(void)
{
  HINSTANCE 	hInstance=hInst;

  // Coordinates of grouped elements in the main window
  int stCol = 10, sndCol = 260;
  int xOpt = stCol, yOpt = 140;
  int xGrat = stCol, yGrat = 260;
  int xWave =sndCol, yWave = 260;

  // Create windows for each control and store the handle names
  stInit=CreateWindow("STATIC","Initialization Information",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        stCol,2,180,18,hwnd,0,hInstance,NULL);
  ebInit=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        stCol,20,225,40,hwnd,0,hInstance,NULL);
  stStatus=CreateWindow("STATIC","Status",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        sndCol,2,60,18,hwnd,0,hInstance,NULL);
  ebStatus=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_MULTILINE|WS_DISABLED,
                        sndCol,20,225,215,hwnd,0,hInstance,NULL);
  stDevice=CreateWindow("STATIC","Current Shamrock:",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        stCol,85,180,20,hwnd,0,hInstance,NULL);
  cbDevice=CreateWindow("COMBOBOX","0",
                        WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
                        stCol+125,80,40,100,hwnd,0,hInstance,NULL);
  stSerial=CreateWindow("STATIC","Serial Number",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xOpt,yOpt,180,18,hwnd,0,hInstance,NULL);
  ebSerial=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xOpt+125,yOpt,100,20,hwnd,0,hInstance,NULL);
  stFocalL=CreateWindow("STATIC","Focal Length",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xOpt,yOpt+25,180,18,hwnd,0,hInstance,NULL);
  ebFocalL=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xOpt+125,yOpt+25,100,20,hwnd,0,hInstance,NULL);
  stAngDev=CreateWindow("STATIC","Angular Deviation",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xOpt,yOpt+50,180,18,hwnd,0,hInstance,NULL);
  ebAngDev=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xOpt+125,yOpt+50,100,20,hwnd,0,hInstance,NULL);
  stFocalT=CreateWindow("STATIC","Focal Tilt",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xOpt,yOpt+75,180,18,hwnd,0,hInstance,NULL);
  ebFocalT=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xOpt+125,yOpt+75,100,20,hwnd,0,hInstance,NULL);
  stTurret=CreateWindow("STATIC","Current turret",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xGrat,yGrat,150,18,hwnd,0,hInstance,NULL);
  cbTurret=CreateWindow("COMBOBOX","0",
                        WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
                        xGrat+125,yGrat-5,40,100,hwnd,0,hInstance,NULL);
  stGrat=CreateWindow("STATIC","Current grating",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xGrat,yGrat+25,150,18,hwnd,0,hInstance,NULL);
  cbGrat=CreateWindow("COMBOBOX","0",
                        WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
                        xGrat+125,yGrat+20,40,100,hwnd,0,hInstance,NULL);
  stLines=CreateWindow("STATIC","Lines / mm",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xGrat,yGrat+50,150,18,hwnd,0,hInstance,NULL);
  ebLines=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xGrat+125,yGrat+50,100,20,hwnd,0,hInstance,NULL);
  stBlaze=CreateWindow("STATIC","Blaze (nm)",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xGrat,yGrat+75,150,18,hwnd,0,hInstance,NULL);
  ebBlaze=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xGrat+125,yGrat+75,100,20,hwnd,0,hInstance,NULL);
  stHome=CreateWindow("STATIC","Home (steps)",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xGrat,yGrat+100,150,18,hwnd,0,hInstance,NULL);
  ebHome=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xGrat+125,yGrat+100,100,20,hwnd,0,hInstance,NULL);
  stOffset=CreateWindow("STATIC","Offset (steps)",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xGrat,yGrat+125,150,18,hwnd,0,hInstance,NULL);
  ebOffset=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xGrat+125,yGrat+125,100,20,hwnd,0,hInstance,NULL);
  pbSetOffset=CreateWindow("BUTTON","Set Offset",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        xGrat,yGrat+150,120,25,hwnd,0,hInstance,NULL);
  ebSetOffset=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                        xGrat+125,yGrat+150,100,25,hwnd,0,hInstance,NULL);
  stWaveL=CreateWindow("STATIC","Current wavelength",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xWave,yWave,150,18,hwnd,0,hInstance,NULL);
  ebWaveL=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xWave+145,yWave,80,20,hwnd,0,hInstance,NULL);
  stMinWave=CreateWindow("STATIC","Minimum wavelength",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xWave,yWave+25,150,18,hwnd,0,hInstance,NULL);
  ebMinWave=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xWave+145,yWave+25,80,20,hwnd,0,hInstance,NULL);
  stMaxWave=CreateWindow("STATIC","Maximum wavelength",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        xWave,yWave+50,150,18,hwnd,0,hInstance,NULL);
  ebMaxWave=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        xWave+145,yWave+50,80,20,hwnd,0,hInstance,NULL);
  pbGotoWave=CreateWindow("BUTTON","Go to wavelength",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        xWave,yWave+75,140,25,hwnd,0,hInstance,NULL);
  ebGotoWave=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT,
                        xWave+145,yWave+75,80,25,hwnd,0,hInstance,NULL);
  pbResetWave=CreateWindow("BUTTON","Reset wavelengtt",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        xWave,yWave+105,225,25,hwnd,0,hInstance,NULL);
  pbClose=CreateWindow("BUTTON","Close",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        sndCol+150,410,75,25,hwnd,0,hInstance,NULL);
  SetupWindows();      // fill windows with default data

  return TRUE;
}

//------------------------------------------------------------------------------
//  FUNCTION NAME: SetupWindows()
//
//  RETURNS:       NONE
//
//  LAST MODIFIED: ECiB 31/01/05
//
//  DESCRIPTION:   This function fills the created windows with their initial
//                 default settings.
//
//  ARGUMENTS:     NONE
//------------------------------------------------------------------------------

void SetupWindows(void)
{
  char aInitializeString[256], aBuffer[16];
  int Counter, errorValue;
  int noGratings;

  if(!errorFlag){
    wsprintf(aInitializeString,"Shamrocks found: %d", NoDevices);
    SendMessage(ebInit, WM_SETTEXT, 0, (LPARAM)(LPSTR)aInitializeString);
    // Add options to Device combo box
    for(Counter=0; Counter<NoDevices; Counter++){
      wsprintf(aBuffer,"%d", Counter+1);
      SendMessage(cbDevice, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
    }
    // Select default device
    device = 0;
    wsprintf(aBuffer,"1");
    SendMessage(cbDevice, CB_SELECTSTRING,0,(LPARAM)(LPSTR)aBuffer);

    // Add options to Turret combo box
    for(Counter=0; Counter<3; Counter++){ //By default there are 3 turrets settings
      wsprintf(aBuffer,"%d", Counter+1);
      SendMessage(cbTurret, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
    }

    // Add options to Grating combo box
    errorValue=ShamrockGetNumberGratings(device, &noGratings);
    if(errorValue != SHAMROCK_SUCCESS)
      noGratings = 0;
    for(Counter=0; Counter<noGratings; Counter++){
      wsprintf(aBuffer,"%d", Counter+1);
      SendMessage(cbGrat, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
    }

    UpdateShamrockParameters();
  }
  // Could not initialize
  else{
  	wsprintf(aInitializeString,"Initialization failed");
   SendMessage(ebStatus, WM_SETTEXT, 0, (LPARAM)(LPSTR)aInitializeString);
  }
  return;
}

//------------------------------------------------------------------------------
//  FUNCTION NAME: ProcessPushButtons()
//
//  RETURNS:       NONE
//
//  LAST MODIFIED: ECiB 31/01/05
//
//  DESCRIPTION:   This function handles the messages sent by the pushbuttons
//
//  ARGUMENTS:     LPARAM lparam: The button id
//------------------------------------------------------------------------------

void ProcessPushButtons(LPARAM lparam)
{
  char aBuffer[256];
  int oldDevice = device;
  int oldTurret=turret, oldGrating=grating;
  float offset, wavelength;

  if(lparam==(LPARAM)cbDevice){    // Set device
    GetWindowText(cbDevice,aBuffer,16);
    device = atoi(aBuffer)-1;
    if(oldDevice != device)
      UpdateShamrockParameters();
  }

  if(lparam==(LPARAM)cbTurret){    // Set turret
    GetWindowText(cbTurret,aBuffer,16);
    turret = atoi(aBuffer);
    if(oldTurret != turret){
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"\r\nAttempting to change turret ...");
      UpdateWindow(hwnd);             // Sends WM_PAINT message
      ShamrockSetTurret(device, turret);
      UpdateShamrockParameters();
    }
  }

  if(lparam==(LPARAM)cbGrat){    // Set grating
    GetWindowText(cbGrat,aBuffer,16);
    grating = atoi(aBuffer);
    if(oldGrating != grating){
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"\r\nAttempting to change grating ...");
      UpdateWindow(hwnd);             // Sends WM_PAINT message
      ShamrockSetGrating(device, grating);
      UpdateShamrockParameters();
    }
  }

  if(lparam==(LPARAM)pbSetOffset){  // Set grating offset
    GetWindowText(ebSetOffset,aBuffer,16);
    offset = atof(aBuffer);
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"\r\nAttempting to change offset ...");
    UpdateWindow(hwnd);             // Sends WM_PAINT message
    ShamrockSetGratingOffset(device, grating, offset);
    UpdateShamrockParameters();
  }

  if(lparam==(LPARAM)pbGotoWave){  // Set wavelength
    GetWindowText(ebGotoWave,aBuffer,16);
    wavelength = atof(aBuffer);
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"\r\nAttempting to set wavelength ...");
    UpdateWindow(hwnd);             // Sends WM_PAINT message
    ShamrockSetWavelength(device, wavelength);
    UpdateShamrockParameters();
  }

  if(lparam==(LPARAM)pbResetWave){  // Reset wavelength
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"\r\nAttempting to reset wavelength ...");
    UpdateWindow(hwnd);             // Sends WM_PAINT message
    ShamrockGotoZeroOrder(device);
    UpdateShamrockParameters();
  }

  if(lparam==(LPARAM)pbClose){     // Close
    wsprintf(aBuffer,"\r\nShutting down ...");
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    DestroyWindow(hwnd);
  }
  return;
}

//------------------------------------------------------------------------------
//  FUNCTION NAME: UpdateShamrockParameters()
//
//  RETURNS:       NONE
//
//  LAST MODIFIED: ECiB 31/01/05
//
//  DESCRIPTION:   This function updates the Shamrock parameters.
//
//  ARGUMENTS:     NONE
//------------------------------------------------------------------------------

void UpdateShamrockParameters(void)
{
  char buffer[256], buffer2[32], serial[16];
  float FocalLength, AngularDeviation, FocalTilt;
  float Lines;
  int Home, Offset;
  char Blaze[32];
  float wavelength, Min, Max;
  int errorValue;

  wsprintf(buffer,"\r\nCurrent Shamrock: #%d",device+1);
  SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)buffer);

  // Get Serial Number
  errorValue=ShamrockGetSerialNumber(device, serial);
  if(errorValue == SHAMROCK_SUCCESS){
    strcat(buffer, "\r\nGot Serial Number");
    SendMessage(ebSerial, WM_SETTEXT, 0, (LPARAM)serial);
  }
  else
    strcat(buffer, "\r\nCouldn't get Serial Number");

  // Get Optical Parameters
  errorValue=ShamrockEepromGetOpticalParams(device, &FocalLength, &AngularDeviation, &FocalTilt);
  if(errorValue == SHAMROCK_SUCCESS){
    strcat(buffer, "\r\nGot Optical Parameters");
    sprintf(buffer2,"%g",FocalLength);
    SendMessage(ebFocalL, WM_SETTEXT, 0, (LPARAM)buffer2);
    sprintf(buffer2,"%g",AngularDeviation);
    SendMessage(ebAngDev, WM_SETTEXT, 0, (LPARAM)buffer2);
    sprintf(buffer2,"%g",FocalTilt);
    SendMessage(ebFocalT, WM_SETTEXT, 0, (LPARAM)buffer2);
  }
  else
    strcat(buffer, "\r\nCouldn't get Optical Parameters");

  // Get Turret
  errorValue=ShamrockGetTurret(device, &turret);
  if(errorValue == SHAMROCK_SUCCESS){
    strcat(buffer, "\r\nGot Turret");
    sprintf(buffer2,"%d",turret);
    SendMessage(cbTurret, CB_SELECTSTRING,0,(LPARAM)buffer2);
  }
  else
    strcat(buffer, "\r\nCouldn't get Turret");

  // Get Grating
  errorValue=ShamrockGetGrating(device, &grating);
  if(errorValue == SHAMROCK_SUCCESS){
    strcat(buffer, "\r\nGot Grating");
    sprintf(buffer2,"%d",grating);
    SendMessage(cbGrat, CB_SELECTSTRING,0,(LPARAM)buffer2);
  }
  else
    strcat(buffer, "\r\nCouldn't get Grating");

  // Get Grating Info
  errorValue=ShamrockGetGratingInfo(device, grating, &Lines,  Blaze, &Home, &Offset);
  if(errorValue == SHAMROCK_SUCCESS){
    strcat(buffer, "\r\nGot Grating Information");
    sprintf(buffer2,"%g",Lines);
    SendMessage(ebLines, WM_SETTEXT,0,(LPARAM)buffer2);
    SendMessage(ebBlaze, WM_SETTEXT,0,(LPARAM)Blaze);
    sprintf(buffer2,"%d",Home);
    SendMessage(ebHome, WM_SETTEXT,0,(LPARAM)buffer2);
    sprintf(buffer2,"%d",Offset);
    SendMessage(ebOffset, WM_SETTEXT,0,(LPARAM)buffer2);
  }
  else
    strcat(buffer, "\r\nCouldn't get Grating Information");

  // Get Wavelength and Wavelength Limits
  errorValue=ShamrockGetWavelength(device, &wavelength);
  if(errorValue == SHAMROCK_SUCCESS){
    strcat(buffer, "\r\nGot Wavelength");
    sprintf(buffer2,"%g",wavelength);
    SendMessage(ebWaveL, WM_SETTEXT, 0, (LPARAM)buffer2);
  }
  else
    strcat(buffer, "\r\nCouldn't get Wavelength");

  errorValue=ShamrockGetWavelengthLimits(device, grating, &Min, &Max);
  if(errorValue == SHAMROCK_SUCCESS){
    strcat(buffer, "\r\nGot Wavelength Limits");
    sprintf(buffer2,"%g",Min);
    SendMessage(ebMinWave, WM_SETTEXT, 0, (LPARAM)buffer2);
    sprintf(buffer2,"%g",Max);
    SendMessage(ebMaxWave, WM_SETTEXT, 0, (LPARAM)buffer2);
  }
  else
    strcat(buffer, "\r\nCouldn't get Wavelength Limits");

  // Update text box
  SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)buffer);

  return;
}
