
#include <stdio.h>

#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockAccessory.h"

int AccessoryParams(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int IsAccessory;

  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShamrockAccessoryIsPresent(device,&IsAccessory);
    ShowFunctionReturn("AccessoryIsPresent", ReturnValue);

    printf("\n\tFilter %s present", ToBeOrNotToBe(IsAccessory));

    if(IsAccessory == 0)
      return ShowMenu(0, "");

    for(int line = 1; line <3; line++)
      GetAccessory(device, line);

    ReturnValue = ShowMenu(2, "\n\t\t1 - SWITCH LINE 1 \n\t\t2 - SWITCH LINE 2");
    switch (ReturnValue){
      case 1: ReturnValue = SwitchState(device, 1); break;
      case 2: ReturnValue = SwitchState(device, 2); break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int GetAccessory(int device, int line)
{
  int ReturnValue, state;

  ReturnValue = ShamrockGetAccessoryState(device, line, &state);
  ShowFunctionReturn("GetAccessoryState", ReturnValue);
  printf("\n\tState line %d: %d", line, state);

  return ReturnValue;
}

int SwitchState(int device, int line)
{
  int ReturnValue, currentstate, state;
  ReturnValue = ShamrockGetAccessoryState(device, line, &currentstate);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't switch the line %d state !", line);
    return NOT_DONE_YET;
  }
  if(currentstate == 1)
    state = 2;
  else
    state = 1;

  ReturnValue = ShamrockSetAccessory(device, line, state);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't switch the line %d state !", line);
    return NOT_DONE_YET;
  }
  ShowFunctionReturn("SetAccessory", ReturnValue);
  printf("\n\tLine %d state changed to %d", line, state);
  return NOT_DONE_YET;
}

