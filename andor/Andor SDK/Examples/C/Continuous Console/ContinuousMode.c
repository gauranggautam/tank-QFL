//
//  Continuous Mode SDK Example
//  D McCluskey Feb 07
//
// This console example demonstrates how to set up Run til abort SoftTrigger
// mode with the SDK
//

#include "atmcd32d.h"
#include <stdio.h>


unsigned int setUpShiftSpeeds(void);
unsigned int setupAcquisition(void);
unsigned int doAcquisition(void);

void main()
{
  unsigned int uiErrorCode;
  AndorCapabilities caps;
  int iContinuousModeAvailable=0;
  int ixSize, iySize;


  // Initialization
  uiErrorCode = Initialize("");
  printf("Initialize() returned %d\n", uiErrorCode);

  if (uiErrorCode == DRV_SUCCESS) {
    caps.ulSize = sizeof(AndorCapabilities);
    GetCapabilities(&caps);
    if (caps.ulTriggerModes & AC_TRIGGERMODE_CONTINUOUS) {
      printf("Correct Hardware for Continuous Mode\r\n");
      iContinuousModeAvailable = 1;
    }
    else
      printf("InCorrect Hardware for Continuous Mode\r\n");
  }

  if (iContinuousModeAvailable == 1){
    uiErrorCode = GetDetector( &ixSize, &iySize ) ;

    //set up modes so we go into Continuous mode
    if (uiErrorCode == DRV_SUCCESS)
      uiErrorCode = SetReadMode( 4 ) ;  //image

    if (uiErrorCode == DRV_SUCCESS)
      uiErrorCode = SetImage(1,1,1,ixSize,1,iySize) ;

    if (uiErrorCode == DRV_SUCCESS)
      uiErrorCode = SetAcquisitionMode( 5 ) ;  //Run Til Abort

    if (uiErrorCode == DRV_SUCCESS)
      uiErrorCode = SetFrameTransferMode (0); //ensure frame transfer is off

    if (uiErrorCode == DRV_SUCCESS)
      uiErrorCode = SetTriggerMode(10);  //Soft Trigger Mode

    //Now check everything is OK for Continuous mode
    if (uiErrorCode == DRV_SUCCESS) {
      uiErrorCode = IsTriggerModeAvailable(10);
      if (uiErrorCode != DRV_SUCCESS) {
        iContinuousModeAvailable = 2;
        printf("InCorrect settings for Continuous Mode\r\n");
      }
    }
    if (iContinuousModeAvailable == 1) {
      //Everything fine
      printf("Correct settings for Continuous Mode\r\n");

      uiErrorCode = setUpShiftSpeeds();
      if (uiErrorCode == DRV_SUCCESS)
        uiErrorCode = setupAcquisition();
      if (uiErrorCode == DRV_SUCCESS) {
        uiErrorCode = doAcquisition();

      }
    }
  }

  if (uiErrorCode == DRV_SUCCESS)
    printf("Successful run\n\n");


  printf("ShutDown()   returned %d\n", ShutDown());

  printf("Press Return to Exit\n");
  getchar();
}



unsigned int setUpShiftSpeeds(void)
{
  unsigned int uiErrorCode = DRV_SUCCESS;
  float fs;
  int iVHSIndex, nAD, iAD, iSpeed, index;
  float STemp = 0;
  int HSnumber = 0;
  int ADnumber = 0;

  if (uiErrorCode == DRV_SUCCESS)
    uiErrorCode = GetFastestRecommendedVSSpeed (&iVHSIndex,&fs);
  if (uiErrorCode == DRV_SUCCESS) {
    uiErrorCode = SetVSSpeed(iVHSIndex);
    printf("VS Speed set to %f\n",fs);
  }

  if (uiErrorCode == DRV_SUCCESS)
    uiErrorCode = GetNumberADChannels(&nAD);
  if (uiErrorCode == DRV_SUCCESS){
    for (iAD = 0; iAD < nAD; iAD++) {
      GetNumberHSSpeeds(iAD, 0, &index);
      for (iSpeed = 0; iSpeed < index; iSpeed++) {
        GetHSSpeed(iAD, 0, iSpeed, &fs);
        if(fs > STemp){
          STemp = fs;
          HSnumber = iSpeed;
          ADnumber = iAD;
        }
      }
    }
  }

  if (uiErrorCode == DRV_SUCCESS)
    uiErrorCode = SetADChannel(ADnumber);
  if (uiErrorCode == DRV_SUCCESS)
    uiErrorCode = SetHSSpeed(0, HSnumber);
  if (uiErrorCode == DRV_SUCCESS)
    uiErrorCode = GetHSSpeed(ADnumber, 0, HSnumber, &fs);
  if (uiErrorCode == DRV_SUCCESS) {
    printf("HS Speed set to %f\n",fs);
  }
  return uiErrorCode;
}

unsigned int setupAcquisition(void)
{
  unsigned int uiErrorCode;
  float fuserRing[8];
  float factualRing[8];
  int inumberExposures;
  int iloop;
  float fmin,fmax;

  //Setup Ring Exposure
  fuserRing[0] = 0.01;
  fuserRing[1] = 1.0;
  fuserRing[2] = 6.0;
  fuserRing[3] = 0.0001;

  uiErrorCode = SetRingExposureTimes( 4, &fuserRing[0]);
  if (uiErrorCode != DRV_SUCCESS) {
    printf("Error setting ring of exposures %d", uiErrorCode);
  }

  if (uiErrorCode == DRV_SUCCESS)
    uiErrorCode = GetNumberRingExposureTimes(&inumberExposures);

  if (uiErrorCode == DRV_SUCCESS)
    uiErrorCode = GetAdjustedRingExposureTimes(inumberExposures,factualRing);

  if (uiErrorCode == DRV_SUCCESS){
    uiErrorCode = GetRingExposureRange(&fmin,&fmax);
    if (uiErrorCode == DRV_SUCCESS)
      printf("Exposure Range is %f to %f\n",fmin,fmax);

    if (uiErrorCode == DRV_SUCCESS) {
      printf("Exposure Times\n");
      for (iloop=0;iloop<inumberExposures;iloop++) {
        printf("exp %d, user %f,  actual %f\n",iloop,fuserRing[iloop],factualRing[iloop]);
      }
    }
  }
  return uiErrorCode;
}

unsigned int doAcquisition(void)
{
  unsigned int uiErrorCode = DRV_SUCCESS;
  int iNumberacquisitions = 10;
  int iloop;
  long lTotalNumberAcq;

  if (uiErrorCode == DRV_SUCCESS)
    uiErrorCode = StartAcquisition();

  if (uiErrorCode == DRV_SUCCESS){
    for (iloop=0;iloop< iNumberacquisitions;iloop++) {
      uiErrorCode = SendSoftwareTrigger();
      if (uiErrorCode != DRV_SUCCESS) {
        printf("Error with SendSoftwareTrigger %d",uiErrorCode);
        AbortAcquisition();
        return uiErrorCode;
      }

      uiErrorCode = WaitForAcquisition();

      if (uiErrorCode == DRV_SUCCESS)
       uiErrorCode = GetTotalNumberImagesAcquired(&lTotalNumberAcq);
      if (uiErrorCode == DRV_SUCCESS)
        printf("Got image %d\n", lTotalNumberAcq);
    }
  }

  uiErrorCode = AbortAcquisition();

  return uiErrorCode;

}


// end of file
