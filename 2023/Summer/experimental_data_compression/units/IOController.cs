using System.Collections.Concurrent;

/// <summary>
/// A modular mass data transportation structure.
/// </summary>
public class IOController<T> {
    private ConcurrentQueue<T> data;
    private Module<T>? reader;
    private Module<T>? grapher;

    /// <param name="filename">File to read from. Optional</param>
    public IOController(Module<T>? reader = default, Module<T>? grapher = default) {
        this.reader = reader;
        this.grapher = grapher;
        data = new ConcurrentQueue<T>();
    }

    public IOController() {
        data = new ConcurrentQueue<T>();
    }

    /// <summary>
    /// Adds a single object to the end of the stored data.
    /// </summary>
    /// <param name="value">The value to add.</param>
    public void PushSingle(T value) {
        data.Enqueue(value);
    }

    /// <summary>
    /// Adds a set of data to the end of the stored data.
    /// </summary>
    /// <param name="iData">The data to add.</param>
    public void PushBulk(T[] iData) {
        if(data.IsEmpty) {
            data = new ConcurrentQueue<T>(iData);
        } else {
            foreach(T value in iData) {
                data.Enqueue(value);
            }
        }
    }

    /// <summary>
    /// Removes a single value from the stored data.
    /// </summary>
    /// <returns>The removed value.</returns>
    public T? PullSingle() {
        data.TryDequeue(out T? result);
        return result;
    }

    /// <summary>
    /// Removes a chunk of data from the stored data
    /// </summary>
    /// <param name="n">How much data to remove. -1 is all.</param>
    /// <param name="i">Index to start removing at.</param>
    /// <returns>The removed data.</returns>
    public IEnumerable<T> PullBulk(int n = -1, int i = 0) {
        if(n == -1 || n > data.Count) n = data.Count;
        IEnumerable<T> result = data.Skip(i).AsQueryable().Take(n);
        return result;
    }

    /// <summary>
    /// Clears the stored data.
    /// </summary>
    public void Wipe() {
        data.Clear();
    }

    /// <summary>
    /// Reads the stored file and stores its data.
    /// </summary>
    public void ReadFile() {
        Wipe();
        reader?.GetData(data);
    }

    /// <summary>
    /// Reads an array and stores its data.
    /// </summary>
    /// <param name="iData">The array to read from</param>
    #pragma warning disable CS8604
    public void ReadArray(object? iData) {
        data = new ConcurrentQueue<T>((T[]?)iData);
    }
    #pragma warning restore CS8604

    public int Count() {
        return data.Count;
    }

    public T[] ToArray() {
        return data.ToArray();
    }

    public ConcurrentQueue<T> ViewData() {
        return data;
    }
}