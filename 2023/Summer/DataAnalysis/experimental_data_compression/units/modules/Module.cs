using System.Collections.Concurrent;

/// <summary>
/// Base module used in the program for bounding IO
/// </summary>
public abstract class Module<T> {
    public Module() {}

    /// <summary>
    /// Reads and stores data.
    /// </summary>
    public abstract void GetData(ConcurrentQueue<T> data);
}