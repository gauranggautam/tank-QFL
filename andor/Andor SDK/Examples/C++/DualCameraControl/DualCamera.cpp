//---------------------------------------------------------------------------
//Controling Multiple Cameras
//NOTE: The CImg library will not compile with Borland or Embarcadero RAD Studio
//---------------------------------------------------------------------------
#include "DualCamera.h"
//---------------------------------------------------------------------------

int main()
{
  unsigned int ui_error;
  long i_numCams;
  
  ui_error = GetAvailableCameras(&i_numCams);
  CheckError(ui_error,"GetAvailableCameras");
  long* lp_cameras = new long [i_numCams];

  GetHandles(i_numCams, lp_cameras);                //Get Camera Handles
  printf("%i Camera Handles Acquired\n\n",i_numCams);

  InitializeCameras(i_numCams, lp_cameras);        //Initialize Cameras
  printf("Cameras Initialized\n\n");


  acqParams.i_readMode        = 4;                   //Image
  acqParams.i_acquisitionMode = 1;                   //Single Scan
  acqParams.f_exposureTime    = 0.35f;
  
  for(int i = 0; i < i_numCams; i++){
	  SetUpCamera(lp_cameras[i], acqParams);
  }

  if(!b_gblerrorFlag){
	GetInput(i_numCams, lp_cameras);
  }

  ShutDownCameras(i_numCams, lp_cameras);          //Shut Down All Cameras
  printf("Cameras Shutdown\n\n");

  if(lp_cameras != NULL) {
    delete [] lp_cameras;      //Free memory used by cameras array
  }

  system("PAUSE");
  return 0;
}

//Returns True if function call was successful
bool CheckError(unsigned int _ui_err, const char* _cp_func)
{
  bool b_ret;

  if(_ui_err == DRV_SUCCESS) {
    b_ret = true;
  }
  else {
    printf("ERROR - %s -- %i\n\n",_cp_func,_ui_err);
	b_gblerrorFlag = true;
    b_ret = false;
  }
  return b_ret;
}

//Get the Handle for each Camera
void GetHandles(long _l_numCams, long* _lp_cameras)
{
  unsigned int ui_error;
  long l_handle;

  for(int i = 0; i < _l_numCams; i++) {
    ui_error = GetCameraHandle(i,&l_handle);
    if(CheckError(ui_error, "GetCameraHandle")) {
      _lp_cameras[i] = l_handle;
    }
  }
}

//Initialize each camera
void InitializeCameras(long _l_numCams, long* _lp_cameras)
{
  unsigned int ui_error;
  for(int i = 0; i < _l_numCams; i++) {
    ui_error = SetCurrentCamera(_lp_cameras[i]);
    CheckError(ui_error, "SetCurrentCamera");

    ui_error = Initialize("");
	CheckError(ui_error, "Initialize");
  }
}

//Set Acquisition Paramaters
void SetUpCamera(long _l_handle, AcqParams params)
{
  unsigned int ui_error;

  ui_error = SetCurrentCamera(_l_handle);
  CheckError(ui_error, "SetCurrentCamera");

  ui_error = SetReadMode(params.i_readMode);   
  CheckError(ui_error, "SetReadMode");

  ui_error = SetFullImage(1,1);
  CheckError(ui_error, "SetFullImage");

  ui_error = SetAcquisitionMode(params.i_acquisitionMode);
  CheckError(ui_error, "SetAcquisitionMode");

  ui_error = SetExposureTime(params.f_exposureTime);
  CheckError(ui_error, "SetExposureTime");

  //Use Andor Capibilities to test if camera has a shutter
  AndorCapabilities* caps = new AndorCapabilities();
  caps->ulSize = sizeof(AndorCapabilities);

  ui_error = GetCapabilities(caps);
  CheckError(ui_error,"GetCapabilities");

  if(caps->ulFeatures & AC_FEATURES_SHUTTER) {
 
	//If a shutter is present set is to always open
    ui_error = SetShutter(1,1,10,10);
    CheckError(ui_error,"SetShutter");
  }

}

//Get User Input
void GetInput(long _l_numCams, long* _lp_cameras)
{
  int i_input;

  printf("\n");
  for(int i = 0; i < _l_numCams; i++) {
    SetCurrentCamera(_lp_cameras[i]);
	int i_serial;
	GetCameraSerialNumber(&i_serial);
	printf("Acquire with %i - %i \n", i_serial, i);
  }
  printf("Shutdown Cameras = Any Other Key\n\n");
  printf("Choose Option - ");
  std::cin  >> i_input;

  printf("\n\n");

  for(int i = 0; i < _l_numCams; i++)
  {
	if(i_input == i)
	{
      AcquireImage(_lp_cameras[i]);
	  GetInput(_l_numCams, _lp_cameras);
	}
  }
}

//Take Acquisition
void AcquireImage(long _l_handle)
{
  unsigned int ui_error;
  int i_x,i_y;
  unsigned long ul_size;

  ui_error = SetCurrentCamera(_l_handle);
  CheckError(ui_error, "SetCurrentCamera");

  ui_error = GetDetector(&i_x,&i_y);
  CheckError(ui_error, "GetDetector");
  ul_size = i_x*i_y;
  long * lp_data = new long[ul_size];

  ui_error = StartAcquisition();
  CheckError(ui_error, "StartAcquisition");

  ui_error = WaitForAcquisition();
  CheckError(ui_error, "WaitForAcquisition");

  ui_error = GetMostRecentImage(lp_data,ul_size);
  CheckError(ui_error,"GetMostRecentImage");
  
  //Find the maximum possible counts per pixel, i.e. the saturation level
  int i_depth(0);
  ui_error = GetBitDepth(0, &i_depth);
  CheckError(ui_error,"GetBitDepth");
  f_saturationLevel = 1;
  for(int i = 0; i < i_depth; ++i){
   f_saturationLevel *= 2; 
  }

  DisplayImage(lp_data, i_x, i_y);

  if(lp_data) delete[] lp_data;
}

//Draw Image using the CImg library
void DisplayImage(long * _lp_data, int _i_xPx, int _i_yPx)
{
  //Using third party Package 'CImg'

  //Create a CImg Object the width and height of the sensor, 2 Dimensional, one color chanel per pixel, pixels defaulted to 0(black) 
  CImg<float> img(_i_xPx,_i_yPx,1,1,0);

  //fill the img window in black
  img.fill(0);

  int i_counter = 0;
  for(int y = 0; y < _i_yPx;++y)
  {
	for(int x = 0; x < _i_xPx; x++)
	{
	  unsigned char _ucp_grayScale[] = {255,255,255};         //define the colour white
	  float f_intensity = _lp_data[i_counter]/f_saturationLevel;   //Calculate pixel intensity
	  img.draw_point(x,y,_ucp_grayScale,f_intensity);           //Draw Pixel
	  i_counter++;
    }
  }
  img.display("Image");
}

//ShutDown Both Cameras
void ShutDownCameras(long l_numCams, long* lp_cameras)
{
  unsigned int ui_error;
  for(int i = 0; i < l_numCams; i++) {
    ui_error = SetCurrentCamera(lp_cameras[i]);
    CheckError(ui_error, "SetCurrentCamera");

    ShutDown();
    CheckError(ui_error, "ShutDown");
  }
}

//---------------------------------------------------------------------------