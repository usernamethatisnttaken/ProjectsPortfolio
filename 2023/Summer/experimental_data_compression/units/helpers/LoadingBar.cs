/// <summary>
/// Provides a few loading bars to play around with.
/// </summary>
public class LoadingBar {
    public const int consoleAccessMs = 125;

    private long tick;
    private long max;

    public LoadingBar(long max) {
        tick = 0;
        this.max = max;
    }

    /// <summary>
    /// Simple loading bar.
    /// </summary>
    public void Bar() {
        int length = 50;
        Console.Write("_");
        void Bar() {
            while(true) {
                float percent = tick * 100 / max;
                string result = "";
                for(int j = 0; j < length; j++) {
                    result += j * 100 / length < percent ? "█" : "_";
                }
                Console.Write("\r{0} " + tick + "/" + max + " datapoints", result);
                if(tick == max) break;
                Thread.Sleep(consoleAccessMs);
            }
        }
        Thread thread = new(Bar);
        thread.Start();
    }

    /// <summary>
    /// Increment the progress made by one.
    /// </summary>
    public void Increment() {
        tick += tick < max ? 1 : 0;
    }
}