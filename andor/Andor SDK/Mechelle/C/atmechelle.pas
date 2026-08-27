unit atmechelle;

interface

const
    MECHELLE_ERROR_CODES =	20001;
    MECHELLE_SUCCESS =	20002;
    MECHELLE_NOTINITIALIZED =	20003;
    MECHELLE_DLLNOTFOUND = 21000;
    MECHELLE_ATMCD32DLLNOTFOUND = 21001;
    MECHELLE_TEMPERATUREERROR = 21002;
    MECHELLE_NOTEMPERATUREDIFFERENCE = 21003;

    function MechelleInit(width: Integer;height: Integer;directory: PChar;var MaxArraySize: Integer): integer; stdcall;
    function MechelleShutdown: integer; stdcall;
    function MechelleCalibrate(wclFileName: PChar;var searchArea: Integer;var imagePtr: Integer; calibrationResults: Pointer;var found_lines: Integer): integer; stdcall;
    function MechelleSaveCalibration(var newTemperature: Single): integer; stdcall;
    function MechelleGetCoordinates(var temp: Single, var wl: Single, var order: Integer, var x: Integer, var y: Integer): integer; stdcall;
    function MechelleGenerateSpectrum(var imagePtr: Integer; Spectrum: Pointer;var SpectrumLength: Integer ;var calibCoefs: Double ): integer; stdcall;
    function MechelleGenerateSpectrumEx(var imagePtr: Integer; Spectrum: Pointer;var SpectrumLength: Integer ;var calibCoefs: Double ): integer; stdcall;
    function MechelleGenerateLookupTable(directory: PChar; spectrumLength: Integer; mergedSpectrum: Pointer): integer; stdcall;
    function MechelleExtract(var imagePtr: Integer; spectrumLength: Integer; mergedSpectrum: Pointer): integer; stdcall;
    function MechelleSetBoxSize(x: Integer; y: Integer): integer; stdcall;
    function MechelleSetExtractionMode(mode: Integer): integer; stdcall;
    function MechelleSetNumberOrders(mode: Integer): integer; stdcall;
    function MechelleSetLogSeverity(mode: Integer): integer; stdcall;
    function MechelleSpectrumMaxArraySize(var maxarraysize: Integer): integer; stdcall;
    function MechelleImageTemperatureAdjust(var Image: Integer; currentTemp: Single; var pPixelAdjustX: Integer; var pPixelAdjustY: Integer): integer; stdcall;
    function MechelleGetSavedCalibrationTemperature(var calTemp: Single): integer; stdcall;
    function MechelleGetInternalTemperature(var calTemp: Single): integer; stdcall;
    function MechelleBackupCalibration: integer; stdcall;
    function MechelleRestoreCalibration: integer; stdcall;
    function MechelleGetInternalTemperature(var residual: Single): integer; stdcall;
    function MechelleGetOrderLineData(var nooforders: Integer; var nopointserorder: Integer; var loworder: Integer; var highorder: Integer): integer; stdcall;
    function MechelleGetOrderPoint(order: Integer; point: Integer; var x: Integer; var y: Integer): integer; stdcall;
    function MechelleGetOrderCenterWavelength(order: Integer; var x: Integer; var y: Integer): integer; stdcall;
        
implementation

    function MechelleInit; external 'atmechelle.dll' name 'MechelleInit';
    function MechelleShutdown; external 'atmechelle.dll' name 'MechelleShutdown';
    function MechelleCalibrate; external 'atmechelle.dll' name 'MechelleCalibrate';
    function MechelleSaveCalibration; external 'atmechelle.dll' name 'MechelleSaveCalibration';
    function MechelleGetCoordinates; external 'atmechelle.dll' name 'MechelleGetCoordinates';
    function MechelleGenerateSpectrum; external 'atmechelle.dll' name 'MechelleGenerateSpectrum';
    function MechelleGenerateSpectrumEx; external 'atmechelle.dll' name 'MechelleGenerateSpectrumEx';
    function MechelleGenerateLookupTable; external 'atmechelle.dll' name 'MechelleGenerateLookupTable';
    function MechelleExtract; external 'atmechelle.dll' name 'MechelleExtract';
    function MechelleSetBoxSize; external 'atmechelle.dll' name 'MechelleSetBoxSize';
    function MechelleSetExtractionMode; external 'atmechelle.dll' name 'MechelleSetExtractionMode';
    function MechelleSetNumberOrders; external 'atmechelle.dll' name 'MechelleSetNumberOrders';
    function MechelleSetLogSeverity; external 'atmechelle.dll' name 'MechelleSetLogSeverity';
    function MechelleSpectrumMaxArraySize; external 'atmechelle.dll' name 'MechelleSpectrumMaxArraySize';
    function MechelleImageTemperatureAdjust; external 'atmechelle.dll' name 'MechelleImageTemperatureAdjust';
    function MechelleGetSavedCalibrationTemperature; external 'atmechelle.dll' name 'MechelleGetSavedCalibrationTemperature';
    function MechelleGetInternalTemperature; external 'atmechelle.dll' name 'MechelleGetInternalTemperature';
    function MechelleBackupCalibration; external 'atmechelle.dll' name 'MechelleBackupCalibrationexternal';
    function MechelleRestoreCalibration; external 'atmechelle.dll' name 'MechelleRestoreCalibrationexternal';
    function MechelleGetPixelResidual; external 'atmechelle.dll' name 'MechelleGetPixelResidual';
    function MechelleGetOrderLineData; external 'atmechelle.dll' name 'MechelleGetOrderLineData';
    function MechelleGetOrderPoint; external 'atmechelle.dll' name 'MechelleGetOrderPoint';
    function MechelleGetOrderCenterWavelength; external 'atmechelle.dll' name 'MechelleGetOrderCenterWavelength';

end.


