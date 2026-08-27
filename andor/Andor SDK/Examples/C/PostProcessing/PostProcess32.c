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

  int i, i_size, i_NumImages, i_buffersize, i_FrameAveragingFactor, i_RecursiveFactor,  i_xpixels,  i_ypixels;
  long *p_inputFrames, *p_outputFrames1, *p_outputFrames2, *p_tempPoint;
  //The number of frames being taken,
  i_NumImages = 10;
  //the number of fames being averaged and the recursive averaging factor being used.
  i_FrameAveragingFactor = 4;
  i_RecursiveFactor = 4;

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

  //create buffers to hold the image data.
  i_size = i_xpixels * i_ypixels;
  i_buffersize = i_size*i_NumImages;
  p_inputFrames = malloc(i_buffersize * sizeof(long));
  p_outputFrames1 = malloc(i_buffersize * sizeof(long));
  p_outputFrames2 = malloc(i_buffersize * sizeof(long));
  p_tempPoint = p_inputFrames;

  //acquire a set of frames
  ui_error = StartAcquisition();
  printf("%d\n", ui_error);
  for (i = 0; i < i_NumImages; i++) {
    WaitForAcquisition();
    ui_error = GetMostRecentImage(p_inputFrames, i_size);
    if (ui_error == DRV_SUCCESS) {
      p_inputFrames += i_size;
    }
  }
  ui_error = AbortAcquisition();
  printf("%d\n", ui_error);
  p_inputFrames = p_tempPoint;

  //process the set of frames using the Recursive filter
  ui_error = PostProcessDataAveraging(p_inputFrames, p_outputFrames1, i_buffersize, i_NumImages, RECURSIVEFILTER, i_ypixels, i_xpixels, i_FrameAveragingFactor, i_RecursiveFactor);
  printf("%d\n", ui_error);    
  //process the set of frames using the Frame Averaging filter
  ui_error = PostProcessDataAveraging(p_inputFrames, p_outputFrames2, i_buffersize, i_NumImages, FRAMEAVERAGINGFILTER, i_ypixels, i_xpixels, i_FrameAveragingFactor, i_RecursiveFactor);
  printf("%d\n", ui_error);

  free(p_inputFrames);
  free(p_outputFrames1);
  free(p_outputFrames2);

  return 0;
}
//---------------------------------------------------------------------------

