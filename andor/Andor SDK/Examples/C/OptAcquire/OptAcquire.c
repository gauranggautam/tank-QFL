#include <stdio.h>
#pragma hdrstop
#include "atmcd32d.h"

static char * UserFile = "C:\\userconfig2.xml";
static const char* c_ROOTNODE                = "optacquire";
static const char* c_SUPPORTEDCAMERA         = "supported_camera";
static const char* c_SUPPORTEDCAMERA_ATT     = "type";
static const char* c_OUTPUTAMPLIFIER         = "output_amplifier";
static const char* c_FRAMETRANSFER           = "frame_transfer";
static const char* c_PREAMPLIFIERGAIN        = "preamplifier_gain";
static const char* c_SHIFTSPEED              = "shift_speed";
static const char* c_ELECTRONMULTIPLYINGGAIN = "electron_multiplying_gain";
static const char* c_READOUTRATE             = "readout_rate";
static const char* c_VERTICALCLOCKAMPLITUDE  = "vertical_clock_amplitude";
static const char* c_MODENAME                = "mode_name";
static const char* c_MODENAME_ATT            = "name";
static const char* c_MODEDESCRIPTION         = "mode_description";
static const char * pc_modeNameandParamDelim = ",";

//Function headers
unsigned int SetupOptAcquire(char* _pc_fileName, unsigned int _ui_fileNameLen);
unsigned int EnablePresetMode(const char* const _pc_modeName);
unsigned int EnableUserMode(const char* const _pc_modeName);
unsigned int PrintAllModeNames(void);
unsigned int PrintModeParams(const char* const _pc_modeName);
unsigned int PrintParamValue(const char* const _pc_modeName, const char* const _pc_paramName) ;
unsigned int PrintAllModeParams(void);
unsigned int AddNewMode(char* _pc_modeName, unsigned int _ui_modeNameLen,
                        char* _pc_modeDescription, unsigned int _ui_modeDescriptionLen,
                        char* _pc_amplifier,
                        char* _pc_frameTransfer,
                        unsigned int _ui_electronMultiplyingGain,
                        unsigned int _ui_readout_speed,
                        unsigned int _ui_verticalClockAmplitude,
                        float _f_preampSensitivity,
                        float _f_verticalShiftSpeed);
unsigned int DeleteMode(char* _pc_modeName, unsigned int _ui_modeNameLen);
unsigned int SaveToFile(char* _pc_modeName, unsigned int _ui_modeNameLen);



unsigned int SetupOptAcquire(char* _pc_fileName, unsigned int _ui_fileNameLen)
{
   return OA_Initialize(_pc_fileName, _ui_fileNameLen);
}

unsigned int EnablePresetMode(const char* const _pc_modeName){
  unsigned int ui_retVal;
  unsigned int ui_numberOfModes = 0;
  char * pc_acqModes;

  if(_pc_modeName != NULL) {
    //Uses supplied modename to enable mmode
    ui_retVal = OA_EnableMode(_pc_modeName);
      if(ui_retVal == DRV_SUCCESS) {
        printf("Enable Mode Successfull\n");
      }
  }
  else {
    //Get the number of available Preset modes for the current camera
    ui_retVal = OA_GetNumberOfPreSetModes(&ui_numberOfModes);
    if(ui_retVal == DRV_SUCCESS) {
      //Allocate enough memory to hold the list of Mode names
      pc_acqModes = malloc((ui_numberOfModes*255) + (ui_numberOfModes + (strlen(pc_modeNameandParamDelim))));
      //Get a list of Preset mode names
      ui_retVal = OA_GetPreSetModeNames(pc_acqModes);
      if(ui_retVal == DRV_SUCCESS) {
        char * pc_result;
        pc_result = strtok( pc_acqModes, pc_modeNameandParamDelim );
        //Enables the First Preset Mode
        ui_retVal = OA_EnableMode(pc_result);
        if(ui_retVal == DRV_SUCCESS) {
          printf("Enable Mode Successful\n");
        }
      }
      free(pc_acqModes);
    }
  }
  printf("\n");
  return ui_retVal;
}

unsigned int EnableUserMode(const char* const _pc_modeName){
  unsigned int ui_retVal;
  unsigned int ui_numberOfModes = 0;
  char * pc_acqModes;

  if(_pc_modeName != NULL) {
    //Uses supplied modename to enable mmode
    ui_retVal = OA_EnableMode(_pc_modeName);
      if(ui_retVal == DRV_SUCCESS) {
        printf("Enable Mode Successful\n");
      }
  }
  else {
    //Get the number of available User modes for the current camera
    ui_retVal = OA_GetNumberOfUserModes(&ui_numberOfModes);
    if(ui_retVal == DRV_SUCCESS && ui_numberOfModes > 0) {
      //Allocate enough memory to hold the list of Mode names
      pc_acqModes = malloc((ui_numberOfModes*255) + (ui_numberOfModes + (strlen(pc_modeNameandParamDelim))));
      //Get a list of User mode names
      ui_retVal = OA_GetUserModeNames(pc_acqModes);
      if(ui_retVal == DRV_SUCCESS) {
        char * pc_result;
        pc_result = strtok( pc_acqModes, pc_modeNameandParamDelim );
        //Enables the First User Mode
        ui_retVal = OA_EnableMode(pc_result);
        if(ui_retVal == DRV_SUCCESS) {
          printf("Enable Mode Successful\n");
        }
      }
      free(pc_acqModes);
    }
  }
  printf("\n");
  return ui_retVal;
}

unsigned int PrintAllModeNames(void) {
  unsigned int ui_retVal;
  unsigned int ui_numberOfModes = 0;
  char * pc_acqModes;

  //Get the number of available User modes for the current camera
  ui_retVal = OA_GetNumberOfUserModes(&ui_numberOfModes);
  if(ui_retVal == DRV_SUCCESS) {
    //Allocate enough memory to hold the list of Mode names
    pc_acqModes = malloc((ui_numberOfModes*255) + (ui_numberOfModes + (strlen(pc_modeNameandParamDelim))));
    //Get a list of User mode names
    ui_retVal = OA_GetUserModeNames(pc_acqModes);
    if(ui_retVal == DRV_SUCCESS) {
      //Print out User mode names
      unsigned int count = 1;
      char * pc_result;
      pc_result = strtok( pc_acqModes, pc_modeNameandParamDelim );
      printf("User Mode 0: %s \n", pc_result);
      while( pc_result != NULL && count != ui_numberOfModes ) {
        pc_result = strtok( NULL, pc_modeNameandParamDelim );
        printf("User Mode %d: %s \n", count, pc_result);
        count++;
      }
    }
    free(pc_acqModes);
  }

  //Get the number of available Preset modes for the current camera
  ui_retVal = OA_GetNumberOfPreSetModes(&ui_numberOfModes);
  if(ui_retVal == DRV_SUCCESS) {
    //Allocate enough memory to hold the list of Mode names
    pc_acqModes = malloc((ui_numberOfModes*255) + (ui_numberOfModes + (strlen(pc_modeNameandParamDelim))));
    //Get a list of Preset mode names
    ui_retVal = OA_GetPreSetModeNames(pc_acqModes);
    if(ui_retVal == DRV_SUCCESS) {
      //Print out Preset mode names
      unsigned int count = 1;
      char * pc_result;
      pc_result = strtok( pc_acqModes, pc_modeNameandParamDelim );
      printf("Preset Mode 0: %s \n", pc_result);
      while( pc_result != NULL && count != ui_numberOfModes ) {
        pc_result = strtok( NULL, pc_modeNameandParamDelim );
        printf("Preset Mode %d: %s \n", count, pc_result);
        count++;
      }
    }
    free(pc_acqModes);
  }
  printf("\n");
  return ui_retVal;
}

unsigned int PrintModeParams(const char* const _pc_modeName)
{
  unsigned int ui_retVal;
  unsigned int ui_numberOfParams = 0;
  char * pc_acqParams;
  unsigned int i;

  if(_pc_modeName != NULL) {
    //Get the number of available User modes for the current camera
    ui_retVal = OA_GetNumberOfAcqParams(_pc_modeName, &ui_numberOfParams);
    if(ui_retVal == DRV_SUCCESS) {
      //Allocate enough memory to hold the list of Mode names
      pc_acqParams = calloc (ui_numberOfParams, 256);
      //Get a list of User mode names
      ui_retVal = OA_GetModeAcqParams(_pc_modeName, pc_acqParams);
      if(ui_retVal == DRV_SUCCESS) {
        //Print out Parameter names
        unsigned int count = 1;
        char * pc_result;
        pc_result = strtok( pc_acqParams, pc_modeNameandParamDelim );
        PrintParamValue(_pc_modeName, pc_result);
        while( pc_result != NULL && count != ui_numberOfParams ) {
          pc_result = strtok( NULL, pc_modeNameandParamDelim );
          PrintParamValue(_pc_modeName, pc_result);
          count++;
        }
      }
      free(pc_acqParams);
    }
  }
  printf("\n");
  return ui_retVal;
}

unsigned int PrintParamValue(const char* const _pc_modeName, const char* const _pc_paramName) 
{
  unsigned int ui_retVal;
  int i_temp;
  float f_temp;
  char c_temp[256];
  memset(c_temp, '\0', 256);  
  if (0 == strcmp(_pc_paramName, "mode_description") || 0 == strcmp(_pc_paramName, "output_amplifier") || 0 == strcmp(_pc_paramName, "frame_transfer")) {
    //Use OA_GetString to get the string value of the parameter
    ui_retVal = OA_GetString(_pc_modeName, _pc_paramName, &c_temp[0], 256);
    printf("%s: %s \n", _pc_paramName, c_temp);
  }
  else if (0 == strcmp(_pc_paramName, "electron_multiplying_gain") || 0 == strcmp(_pc_paramName, "readout_rate") || 0 == strcmp(_pc_paramName, "vertical_clock_amplitude")) {
    //Use OA_GetInt to get the int value of the parameter
    ui_retVal = OA_GetInt(_pc_modeName, _pc_paramName, &i_temp);
    printf("%s: %d \n", _pc_paramName, i_temp);
  } 
  else if (0 == strcmp(_pc_paramName, "preamplifier_gain") || 0 == strcmp(_pc_paramName, "shift_speed")) {
    //Use OA_GetFloat to get the float value of the parameter
    ui_retVal = OA_GetFloat(_pc_modeName, _pc_paramName, &f_temp);
    printf("%s: %f \n", _pc_paramName, f_temp);
  }
  //printf("\n");
  return ui_retVal;
}

unsigned int PrintAllModeParams(void)
{
  unsigned int ui_retVal;
  unsigned int ui_numberOfModes;
  char * pc_acqModes;
  char ** ppc_acqModeNames;
  unsigned int i;

  //Get the number of available User modes for the current camera
  ui_retVal = OA_GetNumberOfUserModes(&ui_numberOfModes);
  if(ui_retVal == DRV_SUCCESS) {
    //Allocate enough memory to hold the list of Mode names
    pc_acqModes = calloc (ui_numberOfModes, 256);
    //Get a list of User mode names
    ui_retVal = OA_GetUserModeNames(pc_acqModes);
    if(ui_retVal == DRV_SUCCESS) {
      unsigned int count = 1;
      ppc_acqModeNames = (calloc (ui_numberOfModes, 256));
      ppc_acqModeNames[0] = strtok( pc_acqModes, pc_modeNameandParamDelim );
      while( count != ui_numberOfModes ) {
        ppc_acqModeNames[count] = strtok( NULL, pc_modeNameandParamDelim );
        count++;
      }

      //Print out User mode names
      for(i = 0; i < ui_numberOfModes; i++){
        PrintModeParams(ppc_acqModeNames[i]);
      }
      free(ppc_acqModeNames);
    }
    free(pc_acqModes);
  }

  //Get the number of available Preset modes for the current camera
  ui_retVal = OA_GetNumberOfPreSetModes(&ui_numberOfModes);
  if(ui_retVal == DRV_SUCCESS) {
    //Allocate enough memory to hold the list of Mode names
    pc_acqModes = calloc (ui_numberOfModes, 256);
    //Get a list of Preset mode names
    ui_retVal = OA_GetPreSetModeNames(pc_acqModes);
    if(ui_retVal == DRV_SUCCESS) {
      unsigned int count = 1;
      ppc_acqModeNames = (calloc (ui_numberOfModes, 256));
      ppc_acqModeNames[0] = strtok( pc_acqModes, pc_modeNameandParamDelim );
      while( count != ui_numberOfModes ) {
        ppc_acqModeNames[count] = strtok( NULL, pc_modeNameandParamDelim );
        count++;
      }

      //Print out Preset mode names
      for(i = 0; i < ui_numberOfModes; i++){
        PrintModeParams(ppc_acqModeNames[i]);
      }
      free(ppc_acqModeNames);
    }
    free(pc_acqModes);
  }
  printf("\n");
  return ui_retVal;
}

unsigned int AddNewMode(char* _pc_modeName, unsigned int _ui_modeNameLen,
                        char* _pc_modeDescription, unsigned int _ui_modeDescriptionLen,
                        char* _pc_amplifier,
                        char* _pc_frameTransfer,
                        unsigned int _ui_electronMultiplyingGain,
                        unsigned int _ui_readout_speed,
                        unsigned int _ui_verticalClockAmplitude,
                        float _f_preampSensitivity,
                        float _f_verticalShiftSpeed)
{
  
  unsigned int ui_retVal;

  ui_retVal = OA_AddMode(_pc_modeName, _ui_modeNameLen, _pc_modeDescription, _ui_modeDescriptionLen);
  if(ui_retVal == DRV_SUCCESS) {
    printf("New Mode successfully added\n");

    if(ui_retVal == DRV_SUCCESS) {
      ui_retVal = OA_SetString(_pc_modeName, c_OUTPUTAMPLIFIER, _pc_amplifier, 255);
    }
    if(ui_retVal == DRV_SUCCESS) {
      ui_retVal = OA_SetString(_pc_modeName, c_FRAMETRANSFER, _pc_frameTransfer, 255);
    }
    if(ui_retVal == DRV_SUCCESS) {
      ui_retVal = OA_SetInt(_pc_modeName, c_ELECTRONMULTIPLYINGGAIN, _ui_electronMultiplyingGain);
    }
    if(ui_retVal == DRV_SUCCESS) {
      ui_retVal = OA_SetInt(_pc_modeName, c_READOUTRATE, _ui_readout_speed);
    }
    if(ui_retVal == DRV_SUCCESS) {
      ui_retVal = OA_SetFloat(_pc_modeName, c_SHIFTSPEED,  _f_verticalShiftSpeed);
    }
    if(ui_retVal == DRV_SUCCESS) {
      ui_retVal = OA_SetFloat(_pc_modeName, c_PREAMPLIFIERGAIN, _f_preampSensitivity);
    }
    if(ui_retVal == DRV_SUCCESS) {
      ui_retVal = OA_SetInt(_pc_modeName, c_VERTICALCLOCKAMPLITUDE, _ui_verticalClockAmplitude);
    }
    if(ui_retVal == DRV_SUCCESS) {
    printf("All settings successfully set\n");
    }
  }
  printf("\n");
  return ui_retVal;
}

unsigned int DeleteMode(char* _pc_modeName, unsigned int _ui_modeNameLen)
{
  unsigned int ui_retVal;

  ui_retVal = OA_DeleteMode(_pc_modeName, _ui_modeNameLen);
  if(ui_retVal == DRV_SUCCESS) {
    printf("Mode \"%s\" Successfully Deleted\n", _pc_modeName);
  }
  printf("\n");
  return ui_retVal;
}

unsigned int SaveToFile(char* _pc_fileName, unsigned int _ui_modeNameLen)
{
  unsigned int ui_retVal;

  ui_retVal = OA_WriteToFile(_pc_fileName, _ui_modeNameLen);
  if(ui_retVal == DRV_SUCCESS) {
    printf("File \"%s\" Successfully Saved\n", _pc_fileName);
  }
  printf("\n");
  return ui_retVal;
}

int main(int argc, char* argv[])
{
  char c;
  unsigned int ui_retVal;
  ui_retVal = Initialize("");
  if(ui_retVal == DRV_SUCCESS) {
    ui_retVal = SetupOptAcquire(UserFile, strlen(UserFile));
    if(ui_retVal == DRV_SUCCESS) {
      EnablePresetMode(NULL);
      EnableUserMode(NULL);

      printf("############## PrintAllModeNames ############## \n");
      PrintAllModeNames();

      printf("############## PrintAllModeParams ############## \n");
      PrintAllModeParams();

      printf("############## AddNewMode ##############\n");
      ui_retVal = AddNewMode("New Mode 1", strlen(" New Mode 1"),
      "New Description 1", strlen("New Description 1"),
                "Electron Multiplying",
                "OFF", 300, 5, 0.5, 2.4, 0);
      if(ui_retVal == DRV_OA_MODE_ALREADY_EXISTS) printf("Mode Already Exists.\n");

      printf("############## PrintModeParams \"New Mode 1\" ##############\n");
      PrintModeParams("New Mode 1");

      printf("############## DeleteMode ##############\n");
      DeleteMode("New Mode 1", strlen("New Mode 1"));

      printf("############## AddNewMode ##############\n");
      ui_retVal = AddNewMode("New Mode 1", strlen(" New Mode 1"),
      "New Description 1", strlen("New Description 1"),
                "Electron Multiplying",
                "OFF", 300, 5, 0.5, 2.4, 0);
      if(ui_retVal == DRV_OA_MODE_ALREADY_EXISTS) printf("Mode Already Exists.\n");

      printf("############## AddNewMode ##############\n");
      ui_retVal = AddNewMode("New Mode 2", strlen(" New Mode 1"),
      "New Description 2", strlen("New Description 1"),
                "Electron Multiplying",
                "OFF", 300, 5, 0.5, 2.4, 0);
      if(ui_retVal == DRV_OA_MODE_ALREADY_EXISTS) printf("Mode Already Exists.\n");

      printf("############## AddNewMode ##############\n");
      ui_retVal = AddNewMode("New Mode 3", strlen(" New Mode 1"),
      "New Description 3", strlen("New Description 1"),
                "Electron Multiplying",
                "OFF", 300, 5, 0.5, 2.4, 0);
      if(ui_retVal == DRV_OA_MODE_ALREADY_EXISTS) printf("Mode Already Exists.\n");

      printf("############## SaveToFile ##############\n");
      SaveToFile(UserFile, strlen(UserFile));
    }
    else if (ui_retVal == DRV_OA_CAMERA_NOT_SUPPORTED) {
      printf("Camera doesn't support OptAcquire Functionality.\n");
    }
  }
  else {
    printf("Camera failed to initialize.\n");
  }

  printf("Press any key to exit.\n");
  scanf("%c", &c);
  ShutDown();
  return 0;
}

