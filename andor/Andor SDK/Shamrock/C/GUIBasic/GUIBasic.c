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
int xWidth=560;    // width of application window passed to common.c
int yHeight=300;   // height of application window passed to common.c
//******************************************************************************

extern int    NoDevices; // No. of available Shamrocks
extern int    device;    // current device
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
              pbReIni,
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

  // Create windows for each control and store the handle names
  stInit=CreateWindow("STATIC","Initialization Information",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,2,180,18,hwnd,0,hInstance,NULL);
  ebInit=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        10,20,320,40,hwnd,0,hInstance,NULL);
  stDevice=CreateWindow("STATIC","Current Shamrock:",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,85,180,20,hwnd,0,hInstance,NULL);
  cbDevice=CreateWindow("COMBOBOX","0",
                        WS_CHILD|WS_VISIBLE|CBS_DROPDOWNLIST,
                        135,80,40,100,hwnd,0,hInstance,NULL);
  stSerial=CreateWindow("STATIC","Serial Number",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,120,180,18,hwnd,0,hInstance,NULL);
  ebSerial=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        135,120,100,20,hwnd,0,hInstance,NULL);
  stFocalL=CreateWindow("STATIC","Focal Length",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,145,180,18,hwnd,0,hInstance,NULL);
  ebFocalL=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        135,145,100,20,hwnd,0,hInstance,NULL);
  stAngDev=CreateWindow("STATIC","Angular Deviation",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,170,180,18,hwnd,0,hInstance,NULL);
  ebAngDev=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        135,170,100,20,hwnd,0,hInstance,NULL);
  stFocalT=CreateWindow("STATIC","Focal Tilt",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        10,195,180,18,hwnd,0,hInstance,NULL);
  ebFocalT=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|WS_DISABLED,
                        135,195,100,20,hwnd,0,hInstance,NULL);
  stStatus=CreateWindow("STATIC","Status",
                        WS_CHILD|WS_VISIBLE|SS_LEFT,
                        340,2,60,18,hwnd,0,hInstance,NULL);
  ebStatus=CreateWindow("EDIT","",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|ES_LEFT|ES_MULTILINE|WS_DISABLED,
                        340,20,200,240,hwnd,0,hInstance,NULL);
  pbReIni=CreateWindow("BUTTON","Re-Initialize",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        140,235,90,25,hwnd,0,hInstance,NULL);
  pbClose=CreateWindow("BUTTON","Close",
                        WS_CHILD|WS_VISIBLE|WS_BORDER|BS_PUSHBUTTON,
                        240,235,90,25,hwnd,0,hInstance,NULL);
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
  int DeviceCounter;

  if(!errorFlag){
    wsprintf(aInitializeString,"Shamrocks found: %d", NoDevices);
    SendMessage(ebInit, WM_SETTEXT, 0, (LPARAM)(LPSTR)aInitializeString);
    // Add options to Device combo box
    for(DeviceCounter=0; DeviceCounter<NoDevices; DeviceCounter++){
      wsprintf(aBuffer,"%d", DeviceCounter+1);
      SendMessage(cbDevice, CB_ADDSTRING, 0, (LPARAM)(LPSTR)aBuffer);
    }
    // Select default device
    device = 0;
    UpdateShamrockParameters();
    wsprintf(aBuffer,"1");
    SendMessage(cbDevice, CB_SELECTSTRING,0,(LPARAM)(LPSTR)aBuffer);
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
  int error;

  if(lparam==(LPARAM)cbDevice){    // Set device
    GetWindowText(cbDevice,aBuffer,16);
    device = atoi(aBuffer)-1;
    if(oldDevice != device)
      UpdateShamrockParameters();
  }

  if(lparam==(LPARAM)pbReIni){     // ReInitialize
    wsprintf(aBuffer,"\r\nRe-Initializing ...");
    SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)aBuffer);
    UpdateWindow(hwnd);             // Sends WM_PAINT message
    error=ShamrockClose();
    if(error != SHAMROCK_SUCCESS)
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"Close Error:\r\nplease re-start the application");
    sleep(2);
    error=ShamrockInitialize("..\\");
    if(error != SHAMROCK_SUCCESS)
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"Initialize Error:\r\nplease re-start the application");
    error=ShamrockGetNumberDevices(&NoDevices);
    if(error != SHAMROCK_SUCCESS)
      SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)(LPSTR)"General Error:\r\nplease re-start the application");
    SendMessage(cbDevice, CB_RESETCONTENT, 0, 0);
    SetupWindows();
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

  // Update text box
  SendMessage(ebStatus,WM_SETTEXT,0,(LPARAM)buffer);

  return;
}
