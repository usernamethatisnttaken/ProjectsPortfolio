using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

/// <summary>
/// A single unit that handles both writing to and reading from a single file.
/// </summary>
public class ImageController {
    public const int CHANNELS = 4;
    private readonly string filename;
    private readonly IOController<byte> decodeData;
    private Vector4<int> imageDimensions;
    private bool hasWritten = false;
    private bool hasRead = false;
    
    /// <param name="filename">The file the controller will take care of.</param>
    /// <param name="decodeData">The data structure that represents either incoming data for encoding or outgoing data for decoding.</param>
    public ImageController(string filename, IOController<byte> decodeData) {
        this.filename = filename;
        this.decodeData = decodeData;
        imageDimensions = new(0, 0);
    }

    /// <summary>
    /// Sets the dimensions of the image.
    /// </summary>
    /// <param name="dims">The dimensions.</param>
    public void SetDimensions(Vector4<int> dims) {
        imageDimensions = dims;
    }

    /// <summary>
    /// Reads the data from the given filename. Will overwrite all currntly stored data.
    /// </summary>
    #pragma warning disable CA1416
    public void Read() {
        using(Bitmap image = new(filename)) {
            imageDimensions = new(image.Width, image.Height);

            BitmapData imageData = image.LockBits(new Rectangle(0, 0, imageDimensions.x, imageDimensions.y), ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
            byte[] data = new byte[Size()];
            Marshal.Copy(imageData.Scan0, data, 0, data.Length);
            decodeData.ReadArray(data);

            image.UnlockBits(imageData);
            hasRead = true;
        }
    }
    #pragma warning restore CA1416

    /// <summary>
    /// Flushes the controller's currently stored data into the given filename. WILL overwrite the file's contents.
    /// </summary>
    #pragma warning disable CA1416
    public void Flush() {
        if(imageDimensions.x != 0) {
            using(Bitmap image = new(imageDimensions.x, imageDimensions.y)) {
                BitmapData imageData = image.LockBits(new Rectangle(0, 0, imageDimensions.x, imageDimensions.y), ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb);
                Marshal.Copy(decodeData.PullBulk().ToArray(), 0, imageData.Scan0, decodeData.Count());

                image.UnlockBits(imageData);
                image.Save(filename, ImageFormat.Png);
                decodeData.Wipe();
                hasWritten = true;
            }
        } else throw new Exception("Image dimensions have not been set");
    }
    #pragma warning restore CA1416

    /// <summary>
    /// Returns the size of the controller's image in bytes.
    /// </summary>
    /// <returns>The size in bytes.</returns>
    public int Size() {
        return imageDimensions.x * imageDimensions.y * CHANNELS;
    }

    public bool HasWritten() {
        return hasWritten;
    }

    public bool HasRead() {
        return hasRead;
    }

    public override string ToString()
    {
        string[] pathSplit = filename.Split("/");
        string name = pathSplit[pathSplit.Length - 1].Split(".")[0];
        return name + " Controller (" + imageDimensions.x + "/" + imageDimensions.y + "px)";
    }
}