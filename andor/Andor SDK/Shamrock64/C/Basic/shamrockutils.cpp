
#include <stdio.h>
#include <conio.h>

#include "ShamrockCIF.h"
#include "ShamrockUtils.h"

int OptionsMenu(int device);

void ShowFunctionReturn(char *text, int error)
{
  char buffer [SHAMROCK_ERRORLENGTH];
  char buffer2 [128];
  int buffer2len;

  strcpy(buffer2, text);
  buffer2len = strlen(buffer2);
  strcat(buffer2, " ");
  for(int i=buffer2len; i<23; i++)
    strcat(buffer2, "-");
  strcat(buffer2, "> ");
  ShamrockGetFunctionReturnDescription(error, buffer, SHAMROCK_ERRORLENGTH);
  printf("\n%s%s", buffer2, buffer);
  return;
}

void exitApp(char *text)
{
  printf("\n\n%s", text);
  printf("\nPress any key to EXIT this console window");
  getch();
  return;
}

char Wait4Key()
{
  char ch;
  while(1){
    if(kbhit()){
      ch = (char)getch();
      printf("%c\n\n-------------------------------------------------------------------\n", ch);
      break;
    }
  }
  return ch;
}

int ShowMenu(int optionsNumber, char *text)
{
  int ReturnValue;
  char ch, *menuType;

  menuType = strstr(text, "ANY OTHER KEY");

  printf("\n\n\n\n\t\t0 - PREVIOUS MENU");
  if(menuType == NULL)
    printf("%s", text);
  printf("\n\t   RETURN - EXIT");
  if(menuType != NULL)
    printf("%s", text);
  printf("\n\n\t\t");

  ch = Wait4Key();

  ReturnValue = ch-48;

  switch (ch){
    case '\r': ReturnValue = SHAMROCK_SUCCESS; break;
    case '0': ReturnValue = PREVIOUS_MENU; break;
    default: if(ReturnValue < 1 || ReturnValue > optionsNumber)
               ReturnValue = NOT_DONE_YET;
             break;
  }

  printf("\n\n");
  return ReturnValue;
}

char* ToBeOrNotToBe(int exists)
{
  if(exists == 1)
    return "IS";
  else
    return "is NOT";
}

int RunWhichShamrockMenu(int nodevices, int *device)
{
  char ch;
  int temp;
  if(nodevices == 1){
    printf("\n\t1 Shamrock found");
    *device = 0;
  }
  else {
    printf("\n\n\n\t%d Shamrocks found\n\n", nodevices);
    for(int i=0; i<nodevices; i++)
      printf("\tPress %d to select Shamrock no %d\n", i+1, i+1);
    ch = Wait4Key();
    temp = ch-48-1; //'0' in ASCII has a value of 48
    if(temp < 0 || temp > nodevices-1)
      return SHAMROCK_P1INVALID;
    *device = temp;
    printf("\n\nShamrock no %d selected", *device+1);
  }
  return SHAMROCK_SUCCESS;
}

int RunMenu()
{
  int ReturnValue, nodevices, device;

  ReturnValue = NOT_DONE_YET;
  while(ReturnValue == NOT_DONE_YET){
    // how many Shamrocks are there
    ReturnValue = ShamrockGetNumberDevices(&nodevices);
    ShowFunctionReturn("GetNumberDevices", ReturnValue);

    //if unsuccessful or no shamrock found: exit
    if(ReturnValue != SHAMROCK_SUCCESS){
      exitApp("\nCannot find number of devices. Please re-initialize system.");
      return ReturnValue;
    }
    if(nodevices == 0){
      exitApp("\nCannot find any device ?");
      return SHAMROCK_COMMUNICATION_ERROR;
    }

    //if more than 1 Shamrock found, choose system to control
    while (1){
      ReturnValue = RunWhichShamrockMenu(nodevices, &device);
      if(ReturnValue == SHAMROCK_SUCCESS)
        break;
      else
        printf("\n\nThis option is not valid. Please choose a valid option.\n\n");
    }

    //options menu
    ReturnValue = OptionsMenu(device);
  }

  return SHAMROCK_SUCCESS;
}