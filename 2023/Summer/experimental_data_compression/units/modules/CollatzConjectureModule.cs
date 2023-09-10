using System.Collections.Concurrent;

/// <summary>
/// A read module that provides the start, pipeline and cycle numbers following the rules of the Collatz Conjecture.
/// </summary>
public class CollatzConjectureModule<T> : Module<T> {
    private readonly HashSet<long> pipeline;
    private readonly long limit;

    /// <param name="limit">How many entries to generate.</param>
    public CollatzConjectureModule(long limit) {
        pipeline = new HashSet<long>();
        this.limit = limit;
        SetPipeline();
    }

    /// <summary>
    /// Reads in the pipeline file.
    /// </summary>
    private void SetPipeline() {
        string[] data = File.ReadAllText("resources/pipeline.csv").Split("\n");

        for(int i = 1; i < data.Length; i++) {
            pipeline.Add(long.Parse(data[i]));
        }
    }

    /// <summary>
    /// Does a single cycle on a number.
    /// </summary>
    /// <param name="x">The number.</param>
    /// <returns>The result.</returns>
    private long CycleNum(long x) {
        float even = (float)x / 2;
        return (even == (int)(x / 2)) ? (long)even : (x * 3 + 1);
    }

    /// <summary>
    /// Cycle shell function. Cycles a number until it hits the pipeline.
    /// </summary>
    /// <param name="x"></param>
    /// <returns></returns>
    private long[] CycleShell(long x) {
        long value = x;
        long cycles = 0;

        while(!pipeline.Contains(value)) {
            value = CycleNum(value);
            cycles++;
        }

        return new long[]{x, value, cycles};
    }

    /// <summary>
    /// The main read function.
    /// </summary>
    /// <param name="data">The data to write to.</param>
    public override void GetData(ConcurrentQueue<T>? data = null) {
        if(data != null) {
            LoadingBar bar = new(limit);
            bar.Bar();
            for(int i = 1; i <= limit; i++) {
                data.Enqueue((T)(object)CycleShell(i));
                bar.Increment();
            }
            Thread.Sleep(LoadingBar.consoleAccessMs);
            Console.WriteLine("\n");
        } else {
            for(int i = 1; i <= limit; i++) {
                Utils<long>.PrintArray(CycleShell(i));
            }
        }
    }
}