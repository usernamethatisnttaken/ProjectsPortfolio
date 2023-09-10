/// <summary>
/// Encodes an entry into what will be a set of pixels' RGBA channels.
/// </summary>
public class PixelbitEncoder {
    private IOController<long[]> decodeData;
    private IOController<byte> encodeData;
    private int[] subentryBytes;
    private int bytesPerEntry;

    /// <param name="dataDistribution">The amount of channels that should be used for each piece of information in the entry.</param>
    /// <param name="decodeData">The data structure that represents either incoming data for encoding or outgoing data for decoding.</param>
    /// <param name="encodeData">The data structure that represents either incoming data for decoding or outgoing data for encoding.</param>
    public PixelbitEncoder(int[] dataDistribution, IOController<long[]> decodeData, IOController<byte> encodeData) {
        this.decodeData = decodeData;
        this.encodeData = encodeData;
        subentryBytes = dataDistribution;
        bytesPerEntry = ByteRequirement();
    }

    /// <summary>
    /// Calculates how many bytes are required to store one entry.
    /// </summary>
    /// <returns>The entry's byte count.</returns>
    private int ByteRequirement() {
        int result = 0;
        foreach(int count in subentryBytes) {
            result += count;
        } return (int)Math.Ceiling((double)(result / ImageController.CHANNELS)) * ImageController.CHANNELS;
    }

    /// <summary>
    /// Stores the metadata/decoding information in the data (2 pixels worth).
    /// </summary>
    private void LogMetadata() {
        encodeData.PushSingle((byte)bytesPerEntry);
        for(int i = 0; i < subentryBytes.Length; i++) {
            if(i <= ImageController.CHANNELS * 2 - 1) {
                encodeData.PushSingle((byte)subentryBytes[i]);
            } else Console.WriteLine("WARNING: You are entering data with too many pieces, some/all of your data will not be read properly.");
        }
        for(int i = 0; i < ImageController.CHANNELS * 2 - 1 - subentryBytes.Length; i++) {
            encodeData.PushSingle(byte.MinValue);
        }
    }

    /// <summary>
    /// Encodes all stored entries and the metadata into pixelbits.
    /// </summary>
    public void EncodeAllChannels() {
        LoadingBar bar = new(decodeData.Count());
        bar.Bar();

        LogMetadata();
        long[][] data = decodeData.ToArray();
        for(int i = 0; i < data.Length; i++) {
            EncodeSingle(data[i]);
            bar.Increment();
        }
        decodeData.Wipe();

        Thread.Sleep(LoadingBar.consoleAccessMs);
        Console.WriteLine("\n");
    }

    /// <summary>
    /// Encodes a single entry worth of data into pixelbits.
    /// </summary>
    /// <param name="entry">The entry to encode.</param>
    private void EncodeSingle(long[] entry) {
        byte[] result = new byte[bytesPerEntry];
        for(int i = 0; i < entry.Length; i++) {
            byte[] bytes = BitConverter.GetBytes(entry[i]);
            for(int j = subentryBytes[i] - 1; j >= 0; j--) {
                encodeData.PushSingle(bytes[j]);
            }
        } 
    }

    /// <summary>
    /// Decodes a byte array into their corresponding CSV entries.
    /// </summary>
    public void DecodeAllChannels() {
        byte[] pixels = Utils<byte>.TrimArray(encodeData.ToArray());
        bytesPerEntry = pixels[0];

        LoadingBar bar = new(pixels.Length / bytesPerEntry - 1);
        bar.Bar();

        int subentries = 0;
        for(int i = 1; i < ImageController.CHANNELS * 2; i++) {
            if(pixels[i] == 0) break;
            subentries++;
        }
        subentryBytes = new int[subentries];
        for(int i = 1; i < ImageController.CHANNELS * 2; i++) {
            if(pixels[i] == 0) break;
            subentryBytes[i - 1] = pixels[i];
        }

        for(int i = 1; i < pixels.Length / bytesPerEntry; i++) {
            int tick = 0;
            long[] entry = new long[subentryBytes.Length];
            for(int j = 0; j < entry.Length; j++) {
                byte[] subentry = new byte[4];
                for(int k = subentryBytes[j] - 1; k >= 0; k--) {
                    subentry[k] = pixels[tick++ + bytesPerEntry * i];
                }
                entry[j] = BitConverter.ToInt32(subentry);
            }
            decodeData.PushSingle(entry);
            bar.Increment();
        }

        Thread.Sleep(LoadingBar.consoleAccessMs);
        Console.WriteLine("\n");
    }

    /// <summary>
    /// Calculates how many bytes are required to store an entry. Rounds up to the nearest integer/pixel/four-byte.
    /// </summary>
    /// <returns>The amount of bytes an entry takes to encode.</returns>
    public int BytesPerEntry() {
        return bytesPerEntry;
    }
}