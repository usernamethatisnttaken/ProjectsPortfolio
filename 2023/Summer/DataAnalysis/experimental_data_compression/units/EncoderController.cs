using System;
using System.IO.Enumeration;
/// <summary>
/// The main controller, controls the data stream, and connects everything.
/// </summary>
public class EncoderController {
    private readonly PixelbitEncoder pixelEncoder;
    private readonly ImageController imageEncoder;
    private readonly IOController<long[]> dataUncoded;
    private readonly IOController<byte> dataPixelCoded;
    private readonly GraphingController grapher;
    private readonly long[] controllerInfo;
    private DateTime tempStart;
    private DateTime timeElapsed;

    /// <param name="dataDistribution">The amount of channels that should be used for each value in the entry.</param>
    /// <param name="oFile">Output file name as .png.</param>
    /// <param name="iFile">Input file name as .csv. Optional</param>
    public EncoderController(int[] dataDistribution, string oFile, Module<long[]> input, GraphingController grapher) {
        dataUncoded = new IOController<long[]>(input);
        dataPixelCoded = new IOController<byte>();
        pixelEncoder = new PixelbitEncoder(dataDistribution, dataUncoded, dataPixelCoded);
        imageEncoder = new ImageController(oFile, dataPixelCoded);
        this.grapher = grapher;
        controllerInfo = new long[6];
        tempStart = DateTime.MinValue;
        timeElapsed = DateTime.MinValue;
    }

    /// <summary>
    /// Reads data from a CSV file.
    /// </summary>
    public void ReadData() {
        Console.WriteLine("Read started...");
        Thread.Sleep(LoadingBar.consoleAccessMs);
        ResumeTimer();
        dataUncoded.ReadFile();
        controllerInfo[0] = dataUncoded.Count();
        BreakTimer();
    }

    /// <summary>
    /// Encodes the data in an image.
    /// </summary>
    public void EncodeData() {
        Console.WriteLine("Encoding started...");
        Thread.Sleep(LoadingBar.consoleAccessMs);
        ResumeTimer();
        pixelEncoder.EncodeAllChannels();
        controllerInfo[1] = dataPixelCoded.Count() / pixelEncoder.BytesPerEntry() - 1;
        imageEncoder.SetDimensions(Utils.FindFactors(dataPixelCoded.Count() / pixelEncoder.BytesPerEntry() * ImageController.CHANNELS));
        imageEncoder.Flush();
        controllerInfo[2] = imageEncoder.HasWritten() ? 1 : 0;
        BreakTimer();
    }

    /// <summary>
    /// Decodes the data stored in an image.
    /// </summary>
    public void DecodeData() {
        Console.WriteLine("Decoding started...");
        Thread.Sleep(LoadingBar.consoleAccessMs);
        ResumeTimer();
        imageEncoder.Read();
        controllerInfo[3] = imageEncoder.HasRead() ? 1 : 0;
        pixelEncoder.DecodeAllChannels();
        controllerInfo[4] = dataUncoded.Count();
        BreakTimer();
    }

    public void GraphData() {
        Console.WriteLine("Graphing started...");
        grapher.Graph(dataUncoded.ViewData());
        controllerInfo[5] = 1;
        Console.WriteLine("Graphing done!\n");
    }

    /// <summary>
    /// Prints the controller's run info.
    /// </summary>
    public void PrintInfo() {
        if(dataUncoded.Count() != 0 || dataPixelCoded.Count() != 0) Console.WriteLine("GENERAL--");
        Console.WriteLine("    Done in " + timeElapsed.Second + "." + MathF.Round(timeElapsed.Millisecond, 6) + "s");

        if(controllerInfo[0] != 0 || controllerInfo[1] != 0 || controllerInfo[2] != 0) Console.WriteLine("ENCODING--");
        if(controllerInfo[0] != 0) Console.WriteLine("    Entries read: " + controllerInfo[0]);
        if(controllerInfo[1] != 0) Console.WriteLine("    Entries converted to pixelbits: " + controllerInfo[1]);
        if(controllerInfo[2] != 0) Console.WriteLine("    Data written to image: Yes");

        if(controllerInfo[3] != 0 || controllerInfo[4] != 0 || controllerInfo[5] != 0) Console.WriteLine("DECODING--");
        if(controllerInfo[3] != 0) Console.WriteLine("    Data read from image: Yes");
        if(controllerInfo[4] != 0) Console.WriteLine("    Entries converted from pixelbits: " + controllerInfo[4]);
        if(controllerInfo[5] != 0) Console.WriteLine("    Data graphed: Yes");
    }

    /// <summary>
    /// Starts/resumes the run timer.
    /// </summary>
    private void ResumeTimer() {
        tempStart = DateTime.Now;
    }

    /// <summary>
    /// Pauses/stops the run timer.
    /// </summary>
    private void BreakTimer() {
        timeElapsed += DateTime.Now - tempStart;
    }
}