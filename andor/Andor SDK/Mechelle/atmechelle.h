#ifndef ATMECHELLEH
#define ATMECHELLEH

#if defined(__WIN32__) || defined(_WIN32)
#include <windows.h>
#define MECHELLE_DEF WINAPI
#else 
#define MECHELLE_DEF
#endif

#define MECHELLE_ERROR_CODES	20001
#define MECHELLE_SUCCESS	20002
#define MECHELLE_NOTINITIALIZED	20003
#define MECHELLE_DLLNOTFOUND    21000
#define MECHELLE_ATMCD32DLLNOTFOUND 21001
#define MECHELLE_TEMPERATUREERROR 21002
#define MECHELLE_NOTEMPERATUREDIFFERENCE 21003

#define MECHELLE_OVERLAP_REGIONS 120

//structures that the interface needs to know about
typedef struct {
  float wavelength;
  int intensity;
  int order;
  float lineWidth;
  float lineHeight;
  int error;
  float initialX;
  float initialY;
  float measuredX;
  float measuredY;
  float calculatedX;
  float calculatedY;
  float residualX;
  float residualY;
} CalibrationData;

typedef struct {
  int order;
  float intensity;
  float wavelength;
} SpectralData;

#ifdef __cplusplus
extern "C" {
#endif

unsigned int MECHELLE_DEF MechelleInit(int width,int height,char * directory, int *MaxArraySize);

unsigned int MECHELLE_DEF MechelleShutdown(void);

unsigned int MECHELLE_DEF MechelleCalibrate(const char* wclFileName,int searchArea,
                                int * imagePtr,CalibrationData * calibrationResults,
                                int * found_lines);

unsigned int MECHELLE_DEF MechelleSaveCalibration(float *newTemperature);

unsigned int MECHELLE_DEF MechelleGetCoordinates(float temp, float wl, int order, int* x, int* y);

unsigned int MECHELLE_DEF MechelleGenerateSpectrum(int * imagePtr, SpectralData *Spectrum,
                                  int *SpectrumLength,double * calibCoefs);
unsigned int MECHELLE_DEF MechelleGenerateSpectrumEx(int * imagePtr, SpectralData *Spectrum,
  int *SpectrumLength, double * calibCoefs);
unsigned int MECHELLE_DEF MechelleGenerateLookupTable(char* path, int spectrumLength, SpectralData * mergedSpectrum);
unsigned int MECHELLE_DEF MechelleExtract(int * imageptr, int spectrumLength, SpectralData * mergedSpectrum);
unsigned int MECHELLE_DEF MechelleSetBoxSize(int width, int height);
unsigned int MECHELLE_DEF MechelleSetExtractionMode(int mode);
unsigned int MECHELLE_DEF MechelleSetNumberOrders(int mode);
unsigned int MECHELLE_DEF MechelleSetLogSeverity(int level);

unsigned int MECHELLE_DEF MechelleSpectrumMaxArraySize(int *maxarraysize);

unsigned int MECHELLE_DEF MechelleImageTemperatureAdjust(int *Image,float currentTemp, int *pPixelAdjustX,int *pPixelAdjustY);

unsigned int MECHELLE_DEF MechelleGetSavedCalibrationTemperature(float *calTemp);

unsigned int MECHELLE_DEF MechelleGetInternalTemperature(float *calTemp);
unsigned int MECHELLE_DEF MechelleBackupCalibration(void);
unsigned int MECHELLE_DEF MechelleRestoreCalibration(void);

unsigned int MECHELLE_DEF MechelleGetPixelResidual(float *_f_residual);

unsigned int MECHELLE_DEF MechelleGetOrderLineData(int *nooforders, int *nopointserorder, int *loworder, int *highorder);
unsigned int MECHELLE_DEF MechelleGetOrderPoint(int order, int point, int *x, int *y);
unsigned int MECHELLE_DEF MechelleGetOrderCenterWavelength(int order, int *x, int *y);


#ifdef __cplusplus
}
#endif

#endif
