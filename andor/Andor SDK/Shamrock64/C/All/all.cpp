#include "ShamrockCIF.h"
#include "ShamrockUtils.h"
#include "ShamrockParams.h"
#include "ShamrockGrating.h"
#include "ShamrockWavelength.h"
#include "ShamrockSlit.h"
#include "ShamrockShutter.h"
#include "ShamrockFlipper.h"
#include "ShamrockFilter.h"
#include "ShamrockAccessory.h"


int OptionsMenu(int device)
{
  int ReturnValue = NOT_DONE_YET;
  char buffer[512];
  while(ReturnValue == NOT_DONE_YET){
    strcpy(buffer, "\n\t\t1 - SHAMROCK DESCRIPTION \n\t\t2 - GRATINGS \n\t\t3 - WAVELENGTH \n\t\t4 - SLIT");
    strcat(buffer, "\n\t\t5 - SHUTTER \n\t\t6 - FLIPPER \n\t\t7 - FILTER \n\t\t8 - ACCESSORY");
    ReturnValue = ShowMenu(8, buffer);
    switch (ReturnValue){
      case 1: ReturnValue = ShamrockParams(device); break;
      case 2: ReturnValue = GratingParams(device); break;
      case 3: ReturnValue = WavelengthParams(device); break;
      case 4: ReturnValue = SlitParams(device); break;
      case 5: ReturnValue = ShutterParams(device); break;
      case 6: ReturnValue = FlipperParams(device); break;
      case 7: ReturnValue = FilterParams(device); break;
      case 8: ReturnValue = AccessoryParams(device); break;
      default: break;
    }
  }
  if(ReturnValue == PREVIOUS_MENU)
    ReturnValue = NOT_DONE_YET;
  return ReturnValue;
}



