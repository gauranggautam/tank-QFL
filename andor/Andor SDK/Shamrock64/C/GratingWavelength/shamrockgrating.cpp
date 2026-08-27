
#include <stdio.h>
#include <iostream.h>

#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockGrating.h"


int GratingParams(int device)
{
  int ReturnValue = NOT_DONE_YET, IsGrating;
  char buffer[512];

  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShamrockGratingIsPresent(device,&IsGrating);
    ShowFunctionReturn("GratingIsPresent", ReturnValue);
    printf("\n\t\tTurret %s present", ToBeOrNotToBe(IsGrating));

    if(IsGrating == 0)
      return ShowMenu(0, "");

    GetGrating(device);

    strcpy(buffer, "\n\t\t1 - SET DIFFERENT TURRET SETTING \n\t\t2 - SET GRATING \n\t\t3 - RESET WAVELENGTH");
    strcat(buffer, " \n\t\t4 - SET CURRENT GRATING OFFSET \n\t\t5 - SET DETECTOR OFFSET");
    ReturnValue = ShowMenu(5, buffer);
    switch (ReturnValue){
      case 1: ReturnValue = SetTurret(device); break;
      case 2: ReturnValue = SetGrating(device); break;
      case 3: ReturnValue = ResetWavelength(device); break;
      case 4: ReturnValue = GratingOffset(device); break;
      case 5: ReturnValue = DetectorOffset(device); break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int GetGrating(int device)
{
  int ReturnValue, turret, noGratings, grating, detectorOffset;
  float Lines;
  int Home, Offset;
  char Blaze[64];

  ReturnValue = ShamrockGetTurret(device, &turret);
  ShowFunctionReturn("GetTurret", ReturnValue);
  printf("\n\t\tTurret: %d", turret);

  ReturnValue = ShamrockGetNumberGratings(device, &noGratings);
  ShowFunctionReturn("GetNumberGratings", ReturnValue);
  printf("\n\t\tNumber of gratings: %d", noGratings);

  ReturnValue = ShamrockGetGrating(device, &grating);
  ShowFunctionReturn("GetGrating", ReturnValue);
  printf("\n\t\tGrating no: %d", grating);

  ReturnValue = ShamrockGetGratingInfo(device, grating, &Lines, Blaze, &Home, &Offset);
  ShowFunctionReturn("GetGratingInfo", ReturnValue);
  printf("\n\t\tGrating no: %d", grating);
  printf("\n\t\tlines/mm \t%f", Lines);
  printf("\n\t\tblaze    \t%s", Blaze);
  printf("\n\t\thome     \t%d", Home);
  printf("\n\t\toffset   \t%d", Offset);

  ReturnValue = ShamrockGetDetectorOffset(device, &detectorOffset);
  ShowFunctionReturn("GetDetectorOffset", ReturnValue);
  printf("\n\tDetector offset: %d", detectorOffset);

  return NOT_DONE_YET;
}

int SetTurret(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int turret, input;
  char ch;
  while(ReturnValue == NOT_DONE_YET){
    ShamrockGetTurret(device, &turret);
    printf("\n\nCurrent turret setting: %d", turret);
    printf("\nPlease input the desired turret setting (1-3): ");
    ch =  Wait4Key();
    input = ch-48; //'0' in ASCII has a value of 48
    ReturnValue = ShamrockSetTurret(device, input);
    ShowFunctionReturn("SetTurret", ReturnValue);
    if(ReturnValue == SHAMROCK_P2INVALID)
      printf("\t Invalid turret");
    GetGrating(device);
    ReturnValue = ShowMenu(0, "\n    ANY OTHER KEY - CHANGE TURRET SETTING");
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int SetGrating(int device)
{
  int ReturnValue = NOT_DONE_YET;
  int grating, input;
  char ch;
  while(ReturnValue == NOT_DONE_YET){
    ShamrockGetGrating(device, &grating);
    printf("\n\nCurrent grating: %d", grating);
    printf("\nPlease input the desired grating (1-3): ");
    ch =  Wait4Key();
    input = ch-48; //'0' in ASCII has a value of 48
    ReturnValue = ShamrockSetGrating(device, input);
    ShowFunctionReturn("SetGrating", ReturnValue);
    if(ReturnValue == SHAMROCK_P2INVALID)
      printf("\t Invalid Grating");
    GetGrating(device);
    ReturnValue = ShowMenu(0, "\n    ANY OTHER KEY - SET GRATING");
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}

int ResetWavelength(int device)
{
  int ReturnValue;
  float wavelength;

  ReturnValue = ShamrockGetWavelength(device, &wavelength);;
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't reset the wavelenght !");
    return NOT_DONE_YET;
  }
  printf("\n\nCurrent wavelength %f", wavelength);

  ReturnValue = ShamrockWavelengthReset(device);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't reset the wavelenght !");
    return NOT_DONE_YET;
  }
  ShowFunctionReturn("WavelengthReset", ReturnValue);

  ReturnValue = ShamrockGetWavelength(device, &wavelength);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't reset the wavelenght !");
    return NOT_DONE_YET;
  }
  printf("\t Wavelength now %f", wavelength);
  return NOT_DONE_YET;
}

int GratingOffset(int device)
{
  int ReturnValue, grating, input;

  printf("\n\nPlease input the desired grating offset in steps: ");
  cin >> input;

  ReturnValue = ShamrockGetGrating(device, &grating);
  if(ReturnValue != SHAMROCK_SUCCESS){
    printf("\t Couldn't set the grating offset !");
    return NOT_DONE_YET;
  }

  ReturnValue = ShamrockSetGratingOffset(device, grating, input);
  ShowFunctionReturn("SetGratingOffset", ReturnValue);
  if(ReturnValue == SHAMROCK_P2INVALID)
    printf("\t Invalid grating");
  else if(ReturnValue == SHAMROCK_P3INVALID)
    printf("\t Invalid offset");
    
  return NOT_DONE_YET;
}

int DetectorOffset(int device)
{
  int ReturnValue, input;

  printf("\n\nPlease input the desired grating offset in steps: ");
  cin >> input;

  ReturnValue = ShamrockSetDetectorOffset(device, input);
  ShowFunctionReturn("SetDetectorOffset", ReturnValue);
  if(ReturnValue == SHAMROCK_P2INVALID)
    printf("\t Invalid offset");

  return NOT_DONE_YET;
}


