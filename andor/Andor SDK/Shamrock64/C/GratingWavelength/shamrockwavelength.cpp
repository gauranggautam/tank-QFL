
#include <stdio.h>
#include <iostream.h>

#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockWavelength.h"


int WavelengthParams(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int IsWavelength;

  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShamrockWavelengthIsPresent(device,&IsWavelength);
    ShowFunctionReturn("WavelengthIsPresent", ReturnValue);

    printf("\n\tWavelength drive %s present", ToBeOrNotToBe(IsWavelength));

    if(IsWavelength == 0)
      return ShowMenu(0, "");

    GetWavelength(device);

    ReturnValue = ShowMenu(2, "\n\t\t1 - SET WAVELENGTH \n\t\t2 - GO TO ZERO ORDER");
    switch (ReturnValue){
      case 1: ReturnValue = SetWavelength(device); break;
      case 2: ReturnValue = GoToZeroOrder(device); break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int GetWavelength(int device)
{
  int ReturnValue, grating = 1, atZeroOrder = 0;
  float wavelength, Min, Max;

  ReturnValue = ShamrockGetGrating(device, &grating);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("Could't communicate with Shamrock");
    return NOT_DONE_YET;
  }

  ReturnValue = ShamrockGetWavelength(device, &wavelength);
  ShowFunctionReturn("GetWavelength", ReturnValue);
  printf("\n\tGrating %d wavelength (nm): %f", grating, wavelength);

  ReturnValue = ShamrockGetWavelengthLimits(device, grating, &Min, &Max);
  ShowFunctionReturn("GetWavelengthLimits", ReturnValue);
  printf("\n\tGrating %d min wavelength (nm): %f", grating, Min);
  printf("\n\t  max wavelength (nm): %f", Max);

  ReturnValue = ShamrockAtZeroOrder(device, &atZeroOrder);
  ShowFunctionReturn("AtZeroOrder", ReturnValue);
  printf("\n\tGrating %s at zero order", ToBeOrNotToBe(atZeroOrder));
  return NOT_DONE_YET;
}

int SetWavelength(int device)
{
  int ReturnValue;
  float input;

  printf("\n\nPlease input the desired wavelength in nm: ");
  cin >> input;

  ReturnValue = ShamrockSetWavelength(device, input);
  ShowFunctionReturn("SetWavelength", ReturnValue);
  if(ReturnValue == SHAMROCK_P2INVALID)
    printf("\t Invalid wavelength");

  return NOT_DONE_YET;
}

int GoToZeroOrder(int device)
{
  int ReturnValue;

  ReturnValue =  ShamrockGotoZeroOrder(device);
  ShowFunctionReturn("GotoZeroOrder", ReturnValue);

  return NOT_DONE_YET;
}
