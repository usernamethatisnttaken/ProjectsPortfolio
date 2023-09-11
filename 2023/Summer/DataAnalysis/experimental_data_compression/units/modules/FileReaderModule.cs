using System.Collections.Concurrent;

/// <summary>
/// IO module used for reading from a single CSV file.
/// </summary>
public class FileReaderModule<T> : Module<T> {
    private string filename;
    private long fileInd;

    public FileReaderModule(string filename) {
        this.filename = filename;
        fileInd = 1;
    }

    /// <summary>
    /// Retrieves the data from the file.
    /// </summary>
    /// <param name="data">The structure to enter the data to.</param>
    public override void GetData(ConcurrentQueue<T> data) {
        string[] lines = File.ReadAllLines(filename);
        for(; fileInd < lines.LongLength; fileInd++) {
            string[] tokens = lines[(int)fileInd].Trim().Split(",");
            long[] entry = new long[tokens.Length];
            for(int i = 0; i < tokens.Length; i++) {
                entry[i] = long.Parse(tokens[i]);
            }
            data.Enqueue((T)(object)entry);
        }
    }
}