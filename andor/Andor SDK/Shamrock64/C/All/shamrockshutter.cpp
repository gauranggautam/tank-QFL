
#include <stdio.h>
#include <conio.h>
#include <iostream.h>

#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockShutter.h"


int ShutterParams(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int IsShutter;

  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShamrockShutterIsPresent(device,&IsShutter);
    ShowFunctionReturn("ShutterIsPresent", ReturnValue);

    printf("\n\tShutter %s present", ToBeOrNotToBe(IsShutter));

    if(IsShutter == 0)
      return ShowMenu(0, "");

    GetShutter(device);

    ReturnValue = ShowMenu(2, "\n\t\t1 - CHECK MODE IS SUPPORTED \n\t\t2 - CHANGE SHUTTER MODE");
    switch (ReturnValue){
      case 1: ReturnValue = CheckMode(device); break;
      case 2: ReturnValue = ChangeMode(device); break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int GetShutter(int device)
{
  int ReturnValue, mode = -1;
  char buffer[16];

  ReturnValue = ShamrockGetShutter(device, &mode);
  ShowFunctionReturn("GetShutter", ReturnValue);
  if(mode == 0)
    strcpy(buffer, "closed");
  else if(mode == 1)
    strcpy(buffer, "opened");
  else
    strcpy(buffer, "unknown");
  printf("\n\tShutter mode: %d <-> %s", mode, buffer);
  return ReturnValue;
}

int CheckMode(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int input, possible = 0;

  while(ReturnValue == NOT_DONE_YET){
    printf("\n\nPlease input the Shutter mode to check: ");
    cin >> input;
    ReturnValue = ShamrockIsModePossible(device, input, &possible);
    ShowFunctionReturn("IsModePossible", ReturnValue);
    if(ReturnValue == SHAMROCK_P2INVALID)
      printf("\t Invalid mode");
    else
      printf("\n\tShutter mode %d %s possible", input, ToBeOrNotToBe(possible));

    GetShutter(device);
    ReturnValue = ShowMenu(0, "\n    ANY OTHER KEY - CHECK A SHUTTER MODE");
  }

  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;

  return ReturnValue;
}

int ChangeMode(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int input;

  while(ReturnValue == NOT_DONE_YET){
    GetShutter(device);
    printf("\n\nPlease input the shutter mode: ");
    cin >> input;
    ReturnValue = ShamrockSetShutter(device, input);
    ShowFunctionReturn("SetShutter", ReturnValue);
    if(ReturnValue == SHAMROCK_P2INVALID)
      printf("\t Invalid shutter mode");
    GetShutter(device);
    ReturnValue = ShowMenu(0, "\n    ANY OTHER KEY - CHANGE SHUTTER MODE");
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}
