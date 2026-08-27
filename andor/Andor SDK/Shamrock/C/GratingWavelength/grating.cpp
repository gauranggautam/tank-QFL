#include "ShamrockUtils.h"
#include "ShamrockParams.h"
#include "ShamrockGrating.h"
#include "ShamrockWavelength.h"

int OptionsMenu(int device)
{
  int ReturnValue = NOT_DONE_YET;
  while(ReturnValue == NOT_DONE_YET){
    ReturnValue = ShowMenu(3, "\n\t\t1 - SHAMROCK DESCRIPTION \n\t\t2 - GRATINGS \n\t\t3 - WAVELENGTH");
    switch (ReturnValue){
      case 1: ReturnValue = ShamrockParams(device); break;
      case 2: ReturnValue = GratingParams(device); break;
      case 3: ReturnValue = WavelengthParams(device); break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}


