//------------------------------------------------------------------------------
//  PROJECT:		32-bit Driver Example Code
//
//  Copyright 1998. All Rights Reserved
//
//  FILE:				Common.c
//  AUTHOR:			Paul McKernon
//
//  OVERVIEW:		This file is common to all the C examples and initiates the main
//							window. Through calls to xxxxwndw.c it sets up the control
//							windows also and fills then with their default values.
//------------------------------------------------------------------------------

#include <windows.h>            // required for all Windows applications
#include "common.h"             // definitions of application name etc
#include "atmcd32d.h"        		// Andor functions
#include <stdio.h>

extern void 			FreeBuffers(void);  			// Free allocated memory
extern BOOL 			CreateWindows(void);			// Create control windows
extern void				PaintDataWindow(void);
extern void				ProcessTimer(WPARAM);
extern void				ProcessPushButtons(LPARAM);
extern BOOL       ProcessMessages(UINT message, WPARAM wparam, LPARAM lparam);

BOOL	 						InitApplication(HINSTANCE);
BOOL 							InitInstance(HINSTANCE, int);
LRESULT CALLBACK 	WndProc(HWND, UINT, WPARAM, LPARAM);

HINSTANCE 				hInst;            				// current instance

AndorCapabilities caps;                     // AndorCapabilities structure
char              model[32];                // headmodel
int 							gblXPixels;       				// dims of
int								gblYPixels;       				// CCD chip
int               VSnumber;                 // Vertical Speed Index
int               HSnumber;                 // Horizontal Speed Index
int               ADnumber;                 // AD Index

char 							szAppName[9];     				// The name of this application
char 							szTitle[80];      				// The title bar text

HWND  						hwnd; 										// Main window handle.


#pragma argsused

//------------------------------------------------------------------------------
//	FUNCTION NAME:	WinMain()
//
//  RETURNS:				If the function terminates before entering the message loop,
//      						return FALSE.
//    							Otherwise, return the WPARAM value sent by the WM_QUIT
//									message.
//
//  LAST MODIFIED:	PMcK	11/11/98
//
//  DESCRIPTION:		calls initialization function, processes message loop
//
//                  Windows recognizes this function by name as the initial
//									entry point for the program.  This function calls the
//									application initialization routine, if no other instance of
//									the program is running, and always calls the instance
//									initialization routine.  It then executes a	message
//									retrieval and dispatch loop that is the top-level control
//    							structure for the remainder of execution.  The loop is
//									terminated when a WM_QUIT  message is received, at which
//									time this function exits the application instance by
//									returning the value passed by PostQuitMessage().
//
//    							If the function must abort before entering the message loop,
//									it returns the conventional value NULL.
//
//
//	ARGUMENTS: 			hInstance - The handle to the instance of this application
//									that is currently being executed.
//
//    							hPrevInstance - The handle to the instance of this
//									application that was last executed.  If this is the only
//									instance of this application executing, hPrevInstance is
//									NULL. In Win32 applications, this parameter is always NULL.
//
//    							lpCmdLine - A pointer to a null terminated string specifying
//									the command line of the application.
//
//    							nCmdShow - Specifies how the main window is to be diplayed.
//------------------------------------------------------------------------------
int APIENTRY WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
{
  MSG 				msg;
  HANDLE 			hAccelTable;
  char 				aBuffer[256];
  int					errorValue;
  extern int 	acquisitionMode;   // read from xxxxWndw.c
  extern int 	readMode;          // read from xxxxWndw.c
  extern BOOL errorFlag;
  int 				test,test2;
  float       speed, STemp;
  int         iSpeed, iAD, nAD, index;

  caps.ulSize = sizeof(AndorCapabilities);

  errorFlag=FALSE;

  // Other instances of app running?
  if (!hPrevInstance){

    // Initialize shared things
    if (!InitApplication(hInstance)){

      return FALSE;               	// Exits if unable to initialize
    }

    GetCurrentDirectory(256,aBuffer);// Look in current working directory
                                    // for driver files

    errorValue=Initialize(aBuffer);  // Initialize driver in current directory
    wsprintf(aBuffer,"Initialization errors:\n");

    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Initialize Error\n");
      errorFlag=TRUE;
    }

    // Get camera capabilities
    errorValue=GetCapabilities(&caps);
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Get Andor Capabilities information Error\n");
      errorFlag=TRUE;
    }

    // Get Head Model
    errorValue=GetHeadModel(model);
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Get Head Model information Error\n");
      errorFlag=TRUE;
    }

    // Get detector information
    errorValue=GetDetector(&gblXPixels,&gblYPixels);
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Get Detector information Error\n");
      errorFlag=TRUE;
    }

    // Set acquisition mode to required setting specified in xxxxWndw.c
    errorValue=SetAcquisitionMode(acquisitionMode);
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Set Acquisition Mode Error\n");
      errorFlag=TRUE;
    }

    // Set read mode to required setting specified in xxxxWndw.c
    errorValue=SetReadMode(readMode);
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Set Read Mode Error\n");
      errorFlag=TRUE;
    }

    // Set Vertical speed to recommended
    GetFastestRecommendedVSSpeed(&VSnumber, &speed);
    errorValue=SetVSSpeed(VSnumber);
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Set Vertical Speed Error\n");
      errorFlag=TRUE;
    }

    // Set Horizontal Speed to max
    STemp = 0;
    HSnumber = 0;
    ADnumber = 0;
    errorValue = GetNumberADChannels(&nAD);
    if (errorValue != DRV_SUCCESS){
      strcat(aBuffer,  "Get number AD Channel Error\n");
      errorFlag = TRUE;
    }
    else {
      for (iAD = 0; iAD < nAD; iAD++) {
        GetNumberHSSpeeds(iAD, 0, &index);
        for (iSpeed = 0; iSpeed < index; iSpeed++) {
          GetHSSpeed(iAD, 0, iSpeed, &speed);
          if(speed > STemp){
            STemp = speed;
            HSnumber = iSpeed;
            ADnumber = iAD;
          }
        }
      }
    }

    errorValue=SetADChannel(ADnumber);
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Set AD Channel Error\n");
      errorFlag=TRUE;
    }
    
    errorValue=SetHSSpeed(0,HSnumber);
    if(errorValue!=DRV_SUCCESS){
      strcat(aBuffer,"Set Horizontal Speed Error\n");
      errorFlag=TRUE;
    }

    if (caps.ulSetFunctions & AC_SETFUNCTION_BASELINECLAMP) {
      errorValue=SetBaselineClamp(1);
      if(errorValue!=DRV_SUCCESS){
        strcat(aBuffer,"Set Baseline Clamp Error\n");
        errorFlag=TRUE;
      }
    }

    if(errorFlag)
      MessageBox(GetActiveWindow(),aBuffer,"Error!",MB_OK);
  }

  // Perform initializations that apply to a specific instance
  if (!InitInstance(hInstance, nCmdShow)){

    return FALSE;
  }


  // Wait for 2 seconds to allow MCD to calibrate fully before allowing an
  // acquisition to begin
  test=GetTickCount();
  do{
  	test2=GetTickCount()-test;
  }while(test2<2000);


  hAccelTable = LoadAccelerators(hInstance, szAppName);

  // Acquire and dispatch messages until a WM_QUIT message is received.
  while (GetMessage(&msg, NULL, 0, 0)){

    //
    // **TODO** Add other Translation functions (for modeless dialogs
    //  and/or MDI windows) here.
    //

    if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg)){

      TranslateMessage(&msg);
      DispatchMessage(&msg);
    }
  }
  //
  // **TODO** Call module specific instance free/delete functions here.
  //

  // shut down system
  if (caps.ulSetFunctions & AC_SETFUNCTION_TEMPERATURE) {
    errorValue=CoolerOFF();        // Switch off cooler (if used)
    if(errorValue!=DRV_SUCCESS)
      MessageBox(GetActiveWindow(),"Error switching cooler off","Error",MB_OK);
  }

  errorValue=ShutDown();
  if(errorValue!=DRV_SUCCESS)
    MessageBox(GetActiveWindow(),"Error shutting down","Error",MB_OK);

  FreeBuffers();      // frees memory used by image buffers in xxxxWndw.c

  // Returns the value from PostQuitMessage
  return msg.wParam;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	InitApplication()
//
//  RETURNS:				TRUE: Success
//									FALSE: Initialization failed
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:		Initializes window data and registers window class.
//
//									This function is called at initialization time only if no
//									other instances of the application are running. This
//									function performs initialization tasks that can be done once
//									for any	number of running instances.
//
//  							  In this case, we initialize a window class by filling out a
//									data structure of type WNDCLASS and calling the Windows
//									RegisterClass() function.  Since all instances of this
//									application use the same window class, we only need to do
//									this when the first instance is	initialized.
//
//	ARGUMENTS: 			hInstance - The handle to the instance of this application
//															that is currently being executed.
//									nCmdShow - Specifies how the main window is to be diplayed.
//------------------------------------------------------------------------------

BOOL InitApplication(HINSTANCE hInstance)
{
  WNDCLASSEX wc;

  // Load the application name and description strings.

  LoadString(hInstance, IDS_APPNAME, szAppName, sizeof(szAppName));
  LoadString(hInstance, IDS_DESCRIPTION, szTitle, sizeof(szTitle));

  // Fill in window class structure with parameters that describe the
  // main window.

  wc.cbSize        = sizeof(WNDCLASSEX);
  wc.style         = CS_HREDRAW | CS_VREDRAW; // Class style(s).
  wc.lpfnWndProc   = (WNDPROC)WndProc;        // Window Procedure
  wc.cbClsExtra    = 0;                       // No per-class extra data.
  wc.cbWndExtra    = 0;                       // No per-window extra data.
  wc.hInstance     = hInstance;               // Owner of this class
  wc.hIcon         = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_APPICON));
  wc.hCursor       = LoadCursor(NULL, IDC_ARROW); // Cursor
  wc.hbrBackground = (HBRUSH)(5);
  wc.lpszMenuName  = szAppName;               // Menu name from .RC
  wc.lpszClassName = szAppName;               // Name to register as
  wc.hIconSm       = NULL;

  // Register the window class and return FALSE if unsuccesful.

  if (!RegisterClassEx(&wc)){

    if (!RegisterClass((LPWNDCLASS)&wc.style))
      return FALSE;
  }
  //
  // **TODO** Call module specific application initialization functions here.
  //

  return TRUE;
}

//------------------------------------------------------------------------------
//	FUNCTION NAME:	InitInstance()
//
//  RETURNS:				TRUE: Success
//									FALSE: Initialization failed
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:		Saves instance handle and creates main window. This function
//									is called at initialization time for every instance of this
//									application.  This function performs initialization tasks
//									that cannot be shared by multiple instances.
//
//									In this case, we save the instance handle in a static
//									variable and create and display the main program window.
//
//	ARGUMENTS: 			hInstance - The handle to the instance of this application
//															that is currently being executed.
//									nCmdShow - Specifies how the main window is to be diplayed.
//------------------------------------------------------------------------------

BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
  extern int xWidth;       // Width  of app window, specified in xxxxWndw.c
  extern int yHeight;      // Height of app window, specified in xxxxWndw.c

  // Save the instance handle in static variable, which will be used in
  // many subsequence calls from this application to Windows.

  hInst = hInstance; // Store instance handle in our global variable

  // Create a main window for this application instance.
  hwnd = CreateWindow(szAppName,         // See RegisterClass() call.
                      szTitle,           // Text for window title bar.
                      WS_OVERLAPPEDWINDOW, // Window style.
                      0,0,    				 	 // Use default positioning
                      xWidth,yHeight,  	 // Use smallest size of screen possible
                      NULL,              // Overlapped has no parent.
                      NULL,              // Use the window class menu.
                      hInstance,
                      NULL);

  // If window could not be created, return "failure"
  if (!hwnd)
    return FALSE;

  // Create windows, return false if any errors. This function is defined in
  // xxxxWndw.c
  if(CreateWindows()==FALSE)
    return FALSE;

  // Make the window visible; update its client area; and return "success"
  ShowWindow(hwnd, nCmdShow); // Show the window
  UpdateWindow(hwnd);         // Sends WM_PAINT message

  // Window is open

  return TRUE;                // We succeeded...
}


//------------------------------------------------------------------------------
//	FUNCTION NAME:	WndProc()
//
//  RETURNS:				Depends on the message number.
//
//  LAST MODIFIED:	PMcK	03/11/98
//
//  DESCRIPTION:		Processes messages
//  								Messages:			WM_COMMAND    - exit command
//    														WM_DESTROY    - destroy window
//
//	ARGUMENTS: 			hwnd     - window handle
//    							uMessage - message number
//    							wparam   - additional information (dependant of message number)
//    							lparam   - additional information (dependant of message number)
//------------------------------------------------------------------------------

LRESULT CALLBACK WndProc(HWND hwnd,
                         UINT uMessage,
                         WPARAM wparam,
                         LPARAM lparam)
{

  switch (uMessage){

    //
    // **TODO** Add cases here for application messages
    //
    case WM_CTLCOLORSTATIC:
      SetBkMode((HDC)wparam,TRANSPARENT);
      return(GetStockObject(DC_BRUSH));

    case WM_PAINT:

      PaintDataWindow();
      break;

    case WM_TIMER:

      ProcessTimer(wparam);
      break;


    case WM_COMMAND: // message: command from application menu

      ProcessPushButtons(lparam);
      return DefWindowProc(hwnd, uMessage, wparam, lparam);

    case WM_DESTROY:  // message: window being destroyed
      PostQuitMessage(0);
      break;

		default:          // Passes it on if unproccessed
      if(!ProcessMessages(uMessage, wparam, lparam))
      return DefWindowProc(hwnd, uMessage, wparam, lparam);
  }
  return 0;
}
