#include <stdio.h>
#include <iostream.h>

#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockFilter.h"


int FilterParams(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int IsFilter;

  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShamrockFilterIsPresent(device,&IsFilter);
    ShowFunctionReturn("FilterIsPresent", ReturnValue);

    printf("\n\tFilter %s present", ToBeOrNotToBe(IsFilter));

    if(IsFilter == 0)
      return ShowMenu(0, "");

    GetFilter(device);

    ReturnValue = ShowMenu(2, "\n\t\t1 - CHANGE FILTER \n\t\t2 - CHANGE CURRENT FILTER DESCRIPTION");
    switch (ReturnValue){
      case 1: ReturnValue = ChangeFilter(device); break;
      case 2: ReturnValue = ChangeFilterInfo(device); break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int GetFilter(int device)
{
  int ReturnValue, filter;

  ReturnValue = ShamrockGetFilter(device, &filter);
  ShowFunctionReturn("GetFilter", ReturnValue);
  printf("\n\tCurrent filter: %d", filter);
  if(ReturnValue != SHAMROCK_SUCCESS)
    return ReturnValue;

  char info[128];
  ReturnValue = ShamrockGetFilterInfo(device, filter, info);
  ShowFunctionReturn("GetFilterInfo", ReturnValue);
  printf("\n\tFilter description: %s", info);

  return ReturnValue;
}

int ChangeFilter(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int input;
  char ch;
  while(ReturnValue == NOT_DONE_YET){
    GetFilter(device);
    printf("\n\nPlease input the desired filter (1-6): ");
    ch =  Wait4Key();
    input = ch-48; //'0' in ASCII has a value of 48
    ReturnValue = ShamrockSetFilter(device, input);
    ShowFunctionReturn("SetFilter", ReturnValue);
    if(ReturnValue == SHAMROCK_P2INVALID)
      printf("\t Invalid filter");
    GetFilter(device);
    ReturnValue = ShowMenu(0, "\n    ANY OTHER KEY - CHANGE FILTER");
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int ChangeFilterInfo(int device)
{
  int ReturnValue, filter;

  ReturnValue = ShamrockGetFilter(device, &filter);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("Couldn't communicate with the Shamrock");
    return NOT_DONE_YET;
  }

  char input[256];
  printf("\nPlease input the new filter description: ");
  cin >> input;
  ReturnValue = ShamrockSetFilterInfo(device, filter, input);
  ShowFunctionReturn("SetFilterInfo", ReturnValue);

  return NOT_DONE_YET;
}

