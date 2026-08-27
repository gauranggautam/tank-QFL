#include <stdio.h>
#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockParams.h"


int ShamrockParams(int device)
{
  int ReturnValue = NOT_DONE_YET;
  char serial[64];
  float FocalLength, AngularDeviation, FocalTilt;

  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShamrockGetSerialNumber(device,serial);
    ShowFunctionReturn("GetSerialNumber", ReturnValue);
    printf("\n\t Serial Number: %s", serial);

    ShamrockEepromGetOpticalParams(device, &FocalLength, &AngularDeviation, &FocalTilt);
    ShowFunctionReturn("EepromGetOpticalParams", ReturnValue);
    printf("\n\tFocal Length: %f", FocalLength);
    printf("\n\tAngular Deviation: %f", AngularDeviation);
    printf("\n\tFocal Tilt: %f", FocalTilt);
    ReturnValue = ShowMenu(0,"");
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}