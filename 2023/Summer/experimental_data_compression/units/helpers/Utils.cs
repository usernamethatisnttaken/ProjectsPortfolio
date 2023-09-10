using System.Collections.Concurrent;
/// <summary>
/// A class full of miscellaneous utility functions.
/// </summary>
public static class Utils {
    private const int maxImgDims = 2048;
    private const int minImgDims = 4;

    /// <summary>
    /// Tries to find two similar factors of a number. Might actually need to be fixed.
    /// </summary>
    /// <param name="dataLength">The number to find factors of.</param>
    /// <returns>The factors.</returns>
    public static Vector4<int> FindFactors(long dataLength) {
        dataLength /= 2;
        double start = Math.Round(Math.Sqrt(dataLength));
        double lower = start - 1;
        double upper = start + 1;
        int maxY = (int)Math.Ceiling(dataLength / (double)maxImgDims);
        if(maxY > maxImgDims) maxY = maxImgDims;
        for(int i = 0; i < 100; i++) {
            if(dataLength % lower == 0) {
                if(lower > maxImgDims) {
                    Console.WriteLine("WARNING: Image size limit reached, not all data may be encoded");
                    return new(maxImgDims, maxY);
                } else if(lower <= minImgDims) {
                    return new((int)start, (int)Math.Ceiling(dataLength / start));
                } else return new((int)lower, (int)(dataLength / lower));
            }
            if(dataLength % upper == 0) {
                if(upper > maxImgDims) {
                    Console.WriteLine("WARNING: Image size limit reached, not all data may be encoded");
                    return new(maxImgDims, maxY);
                } else if(dataLength / upper <= minImgDims) {
                    return new((int)start, (int)Math.Ceiling(dataLength / start));
                } else return new((int)upper, (int)(dataLength / upper));
            }
            lower++; upper++;
        } return new((int)start, (int)Math.Ceiling(dataLength / start));
    }

    /// <summary>
    /// Sorts data.
    /// </summary>
    /// <param name="xData">x data.</param>
    /// <param name="yData">y data.</param>
    /// <param name="labelData">Data to sort by.</param>
    /// <param name="binSize">Bin size.</param>
    /// <returns></returns>
    #pragma warning disable CS8602
    public static Dictionary<long, LinkedList<double>[]> SortData(double[] xData, double[] yData, double[] labelData, long binSize) {
        Dictionary<long, LinkedList<double>[]> result = new();

        for(int i = 0; i < xData.Length; i++) {
            long bin = (long)Math.Round((double)(labelData[i] / binSize)) * binSize;
            if(!result.ContainsKey(bin)) result.Add(bin, new LinkedList<double>[]{new LinkedList<double>(), new LinkedList<double>()});
            result.TryGetValue(bin, out LinkedList<double>[]? temp);
            temp[0].AddLast(xData[i]);
            temp[1].AddLast(yData[i]);
        }
        return result;
    }
    #pragma warning restore CS8602
}

/// <summary>
/// A class full of miscellaneous generic utility functions.
/// </summary>
public static class Utils<T> {
    /// <summary>
    /// Prints an array.
    /// </summary>
    /// <param name="array">The data you want to print.</param>
    /// <param name="length">The amount of entries to include</param>
    /// <param name="write">Write to console?</param>
    /// <returns>The formatted array</returns>
    #pragma warning disable CS8602
    public static string PrintArray(T[] array, int length = -1, bool write = true) {
        if(length < 0) length = array.Length;
        int trimmed_results = array.Length - length;
        if(length > array.Length || trimmed_results == 0) length = array.Length;

        string result = "[";
        for(int i = 0; i < length; i++) {
            result += array[i].ToString();
            result += (i < length - 1) ? ", " : "";
        }
        if(length != array.Length) {
            result += " ... " + trimmed_results.ToString() + " more entr" + (trimmed_results == 1 ? "y" : "ies");
        } result += "]";
        if(write) Console.WriteLine(result);
        return result;
    }
    #pragma warning restore CS8602

    public static string PrintArray(IOController<T> array, int length = -1, bool write = true) {
        return PrintArray(array.ToArray(), length, write);
    }

    /// <summary>
    /// Copies the data from an array into another array at the given position.
    /// </summary>
    /// <param name="iData">The data to read from.</param>
    /// <param name="oData">The data to write to.</param>
    /// <param name="oIndex">Where to start writing.</param>
    public static void PatchArray(T[] iData, T[] oData, long oIndex) {
        for(int i = 0; i < iData.Length; i++) {
            oData[oIndex + i] = iData[i];
        }
    }

    /// <summary>
    /// Swaps the storage method of a 2D array from depth-width to width-depth or vice versa.
    /// </summary>
    /// <param name="iData">Input data.</param>
    /// <returns>Output 2D array.</returns>
    #pragma warning disable CS8602, CS8604
    public static double[][] SwapAxes(ConcurrentQueue<T[]> iData) {
        iData.TryPeek(out T[]? temp);
        double[][] result = new double[3][];
        for(int i = 0; i < result.Length; i++) {
            result[i] = new double[iData.Count];
        }

        int tick = 0;
        foreach(T[] entry in iData) {
            for(int i = 0; i < entry.Length; i++) {
                result[i][tick] = double.Parse(entry[i].ToString());
            } tick++;
        } return result;
    }
    #pragma warning restore CS8602, CS8604

    /// <summary>
    /// Trim empty integer entries off of a byte array. Generic
    /// </summary>
    /// <param name="array">The array to trim.</param>
    /// <returns>The trimmed array.</returns>
    #pragma warning disable CS8605, CS8600
    public static T[] TrimArray(T[] array) {
        int tick = 0;
        for(int i = array.Length - 1; i > 0; i--) {
            if((byte)(object)array[i] == 0) tick++; else break;
        }
        tick = tick / 4 * 4;
        return (T[])(object)array.Take(array.Length - tick).ToArray();
    }
    #pragma warning restore CS8605, CS8600
}