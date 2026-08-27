
#include <stdio.h>

#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockFlipper.h"


int FlipperParams(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int IsFlipper;

  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShamrockFlipperIsPresent(device,&IsFlipper);
    ShowFunctionReturn("FlipperIsPresent", ReturnValue);

    printf("\n\tFlipper %s present", ToBeOrNotToBe(IsFlipper));

    if(IsFlipper == 0)
      return ShowMenu(0, "");

    GetFlipper(device);

    ReturnValue = ShowMenu(2, "\n\t\t1 - SWITCH PORT \n\t\t2 - RESET PORT");
    switch (ReturnValue){
      case 1: ReturnValue = SwitchFlipper(device); break;
      case 2: ReturnValue = ResetFlipper(device); break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int GetFlipper(int device)
{
  int ReturnValue, port;

  ReturnValue = ShamrockGetPort(device, &port);
  ShowFunctionReturn("GetPort", ReturnValue);
  printf("\n\tFlipper port: %d", port);
  if(ReturnValue != SHAMROCK_SUCCESS)
    return ReturnValue;

  float Low, High;
  ReturnValue = ShamrockGetCCDLimits(device, port, &Low, &High);
  ShowFunctionReturn("GetCCDLimits(", ReturnValue);
  printf("\n\tLow CCD limit: %f", Low);
  printf("\n\tHigh CCD limit: %f", High);

  return ReturnValue;
}

int SwitchFlipper(int device)
{
  int ReturnValue, currentport, port;

  ReturnValue = ShamrockGetPort(device, &currentport);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't switch the flipper !");
    return NOT_DONE_YET;
  }
  if(currentport == 1)
    port = 2;
  else
    port = 1;

  ReturnValue = ShamrockSetPort(device, port);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't switch the flipper !");
    return NOT_DONE_YET;
  }
  ShowFunctionReturn("SetPort", ReturnValue);
  printf("\n\tPort changed to %d", port);
  return NOT_DONE_YET;
}

int ResetFlipper(int device)
{
  int ReturnValue, port;

  ReturnValue = ShamrockFlipperReset(device);
  ShowFunctionReturn("FlipperReset", ReturnValue);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't reset the flipper !");
    return NOT_DONE_YET;
  }

  ReturnValue = ShamrockGetPort(device, &port);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't switch the flipper !");
    return NOT_DONE_YET;
  }

  printf("\n\tCurrent port is %d", port);
  
  return NOT_DONE_YET;
}

