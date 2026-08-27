
#include <stdio.h>
#include <conio.h>
#include <iostream.h>

#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockSlit.h"


int SlitParams(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int IsInputSlit, IsOutputSlit;
  char buffer[512];

  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShamrockSlitIsPresent(device,&IsInputSlit);
    ShowFunctionReturn("SlitIsPresent", ReturnValue);

    printf("\n\t INPUT Slit %s present", ToBeOrNotToBe(IsInputSlit));

    ReturnValue = ShamrockOutputSlitIsPresent(device,&IsOutputSlit);
    ShowFunctionReturn("OutputSlitIsPresent", ReturnValue);

    printf("\n\t OUTPUT Slit %s present", ToBeOrNotToBe(IsOutputSlit));

    if(IsInputSlit == 0 && IsOutputSlit == 0)
      return ShowMenu(0, "");

    if(IsInputSlit == 1)
      GetInputSlit(device);

    if(IsOutputSlit == 1)
      GetOutputSlit(device);

    strcpy(buffer, "");
    if(IsInputSlit == 1)
      strcat(buffer, "\n\t\t1 - SET INPUT SLIT WIDTH");
    if(IsOutputSlit == 1)
      strcat(buffer, "\n\t\t1 - SET OUTPUT SLIT WIDTH");

    ReturnValue = ShowMenu(2, buffer);
    switch (ReturnValue){
      case 1: if(IsInputSlit == 1)
                  ReturnValue = ModifyInputSlit(device);
                else
                  ReturnValue = NOT_DONE_YET;
                break;
      case 2: if(IsOutputSlit == 1)
                  ReturnValue = ModifyOutputSlit(device);
                else
                  ReturnValue = NOT_DONE_YET;
                break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int GetInputSlit(int device)
{
  int ReturnValue;
  float width;

  ReturnValue = ShamrockGetSlit(device, &width);
  ShowFunctionReturn("GetSlit", ReturnValue);
  printf("\n\t Input Slit width: %f", width);
  return ReturnValue;
}

int GetOutputSlit(int device)
{
  int ReturnValue;
  float width;

  ReturnValue = ShamrockGetOutputSlit(device, &width);
  ShowFunctionReturn("GetOutputSlit", ReturnValue);
  printf("\n\tOutput Slit width: %f", width);
  return ReturnValue;
}

int ModifyInputSlit(int device)
{
  int ReturnValue = NOT_DONE_YET;
  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShowMenu(2,"\n\t\t1 - SET INPUT SLIT WIDTH \n\t\t2 - RESET INPUT SLIT WIDTH");
    switch (ReturnValue){
      case 1: ReturnValue = InputInputSlit(device); break;
      case 2: ReturnValue = ShamrockSlitReset(device);
                ShowFunctionReturn("SlitReset", ReturnValue);
                GetInputSlit(device);
                ReturnValue = NOT_DONE_YET;
                break;
      default: break;
    }
  }

  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;

}

int InputInputSlit(int device)
{
  int ReturnValue;
  float input;

  printf("\n\nPlease input the value for the input slit width in um: ");
  cin >> input;
  ReturnValue = ShamrockSetSlit(device, input);
  ShowFunctionReturn("SetSlit", ReturnValue);
  if(ReturnValue == SHAMROCK_P2INVALID)
    printf("\t Invalid width");
  GetInputSlit(device);
  return NOT_DONE_YET;
}

int ModifyOutputSlit(int device)
{
  int ReturnValue = NOT_DONE_YET;
  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShowMenu(2, "\n\t\t1 - SET OUTPUT SLIT WIDTH \n\t\t2 - RESET OUTPUT SLIT WIDTH");
    switch (ReturnValue){
      case 1: ReturnValue = InputOutputSlit(device); break;
      case 2: ReturnValue = ShamrockOutputSlitReset(device);
                ShowFunctionReturn("OutputSlitReset", ReturnValue);
                GetOutputSlit(device);
                ReturnValue = NOT_DONE_YET;
                break;
      default: break;
    }
  }

  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;

  return ReturnValue;
}

int InputOutputSlit(int device)
{
  int ReturnValue;
  float input;

  printf("\n\nPlease input the value for the output slit width in um: ");
  cin >> input;
  ReturnValue = ShamrockSetOutputSlit(device, input);
  ShowFunctionReturn("SetOutputSlit", ReturnValue);
  if(ReturnValue == SHAMROCK_P2INVALID)
    printf("\t Invalid width");
  GetOutputSlit(device);
  return NOT_DONE_YET;
}

