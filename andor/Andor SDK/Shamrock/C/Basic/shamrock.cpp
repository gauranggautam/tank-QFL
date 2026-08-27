#include <stdio.h>
#include "ShamrockCIF.h"
#include "ShamrockUtils.h"

void main()
{
  int ReturnValue;
  printf("Andor Technology\nShamrock SDK\n");

  //initialize Shamrock
  ReturnValue = ShamrockInitialize("");
  ShowFunctionReturn("Initialize", ReturnValue);

  //if Shamrock cannot be initialized: exit
  if(ReturnValue != SHAMROCK_SUCCESS){
    exitApp("\n\nCannot initialize Shamrock. Please ensure that it is connected and powered, and that the Shamrock drivers are correctly installed");
    return;
  }

  //run option menu
  RunMenu();

  //exit
  ReturnValue = ShamrockClose();
  ShowFunctionReturn("Close", ReturnValue);
  printf("\n\n");
  Sleep(2000);
  return;
}


