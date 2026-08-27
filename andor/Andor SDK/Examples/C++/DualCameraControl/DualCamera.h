#ifndef MAIN_H
#define MAIN_H

//---------------------------------------------------
#include <iostream>
#include "CImg.h"
#include "ATMCD32D.H"

using namespace cimg_library;
//---------------------------------------------------

//Saturation Level
float f_saturationLevel;

//Error Flag
bool b_gblerrorFlag = false;

//Acquisition Parameters Struct
struct AcqParams
{
  int   i_readMode;
  int   i_acquisitionMode;
  float f_exposureTime;
}acqParams;

//Function Prototypes
void SetUpCamera(long _l_handle, AcqParams params);
void GetInput(long _l_numCams, long* _lp_cameras);
void AcquireImage(long _l_handle);
void DisplayImage(long * _lp_data, int _i_x, int _i_y);
bool CheckError(unsigned int _ui_err, const char* _cp_func);
void GetHandles(long _l_numCams, long* _lp_cameras);
void InitializeCameras(long _l_numCams, long* _lp_cameras);
void ShutDownCameras(long _l_numCams, long* _lp_cameras);

//---------------------------------------------------
#endif
