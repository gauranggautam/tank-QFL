namespace atmechellecs {
    public interface IATMECHELLE {
        uint MechelleInit(int width, int height, string directory, ref int MaxArraySize);
        uint MechelleShutdown();

        uint MechelleCalibrate(string wclFileName, int searchArea,
            int[] imagePtr, mechelle.CalibrationData []calibrationResults,
            ref int found_lines);

        uint MechelleSaveCalibration(ref float newTemperature);

        uint MechelleGetCoordinates(float temp, float wl, int order, ref int x, ref int y);

        uint MechelleGenerateSpectrum(int[] imagePtr, ref mechelle.SpectralData []Spectrum,
            ref int SpectrumLength, ref double[] calibCoefs);

        uint MechelleGenerateSpectrumEx(int[] imagePtr, ref mechelle.SpectralData[] Spectrum,
            ref int SpectrumLength, ref double[] calibCoefs);

        uint MechelleExtract(int[] imageptr, int spectrumLength, ref mechelle.SpectralData[] Spectrum);
        uint MechelleSetBoxSize(int width, int height);
        uint MechelleSetExtractionMode(int mode);
        uint MechelleSetLogSeverity(int level);

        uint MechelleSetNumberOrders(int mode);
        uint MechelleGenerateLookupTable(string path, int SpectrumLength, mechelle.SpectralData[] Spectrum);

        uint MechelleSpectrumMaxArraySize(ref int maxarraysize);

        uint MechelleImageTemperatureAdjust(ref int[] Image, ref float currentTemp,
            ref int pPixelAdjustX, ref int pPixelAdjustY);

        uint MechelleGetSavedCalibrationTemperature(ref float calTemp);
        uint MechelleGetInternalTemperature(ref float calTemp);
        uint MechelleGetPixelResidual(ref float residual);

        uint MechelleGetOrderLineData(ref int nooforders, ref int nopointserorder, ref int loworder, ref int highorder);
        uint MechelleGetOrderPoint(int order, int point, ref int x, ref int y);
        uint MechelleGetOrderCenterWavelength(int order, ref int x, ref int y);
        uint MechelleBackupCalibration();
        uint MechelleRestoreCalibration();
    }
}