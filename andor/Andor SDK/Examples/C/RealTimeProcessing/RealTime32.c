//---------------------------------------------------------------------------
#pragma hdrstop      
#include "atmcd32d.h"   
#include "stdio.h"

//---------------------------------------------------------------------------

#pragma argsused
int main(int argc, char* argv[])
{
  unsigned int ui_error;
  //These are defines for the values of the actual filters being used
  const int RECURSIVEFILTER = 5;
  const int FRAMEAVERAGINGFILTER = 6;

  int i_xpixels,  i_ypixels, i_FrameAveragingFactor, i_RecursiveFactor, i_temp;

  //the number of fames being averaged and the recursive averaging factor being used.
  i_FrameAveragingFactor = 4;
  i_RecursiveFactor = 3;

  //initialise and set up the acquisition parameters
  ui_error = Initialize("");
  printf("%d\n", ui_error);
  ui_error = GetDetector(&i_xpixels, &i_ypixels);
  printf("%d\n", ui_error);
  ui_error = SetExposureTime(0);
  printf("%d\n", ui_error);
  ui_error = SetReadMode(4);
  printf("%d\n", ui_error);
  ui_error = SetAcquisitionMode(5);
  printf("%d\n", ui_error);
  ui_error = SetImage(1, 1, 1, i_xpixels, 1, i_ypixels);
  printf("%d\n", ui_error);

  //Set the filter to recursive filter and check it
  ui_error = Filter_SetDataAveragingMode(RECURSIVEFILTER);
  printf("%d\n", ui_error);
  ui_error = Filter_GetDataAveragingMode(&i_temp);
  printf("%d %s\n", ui_error, (i_temp == RECURSIVEFILTER)? "Success" : "Failure");
  //Set the recursive averaging factor  and check it
  ui_error = Filter_SetAveragingFactor(i_RecursiveFactor);
  printf("%d\n", ui_error);
  ui_error = Filter_GetAveragingFactor(&i_temp);
  printf("%d %s\n", ui_error, (i_temp == i_RecursiveFactor)? "Success" : "Failure");
  
  //Set the filter to frame averaging filter and  and check it
  ui_error = Filter_SetDataAveragingMode(FRAMEAVERAGINGFILTER);
  printf("%d\n", ui_error);
  ui_error = Filter_GetDataAveragingMode(&i_temp);
  printf("%d %s\n", ui_error, (i_temp == FRAMEAVERAGINGFILTER)? "Success" : "Failure");
  //Set the number of frames being averaged and check it
  ui_error = Filter_SetAveragingFrameCount(i_FrameAveragingFactor);
  printf("%d\n", ui_error);
  ui_error = Filter_GetAveragingFrameCount(&i_temp);
  printf("%d %s\n", ui_error, (i_temp == i_FrameAveragingFactor)? "Success" : "Failure");
  
  return 0;
}
//---------------------------------------------------------------------------

