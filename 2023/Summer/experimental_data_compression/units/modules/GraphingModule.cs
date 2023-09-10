using System.Collections.Concurrent;
using ScottPlot;

/// <summary>
/// A basic grapher.
/// </summary>
public class GraphingController {
    private string plotfile;

    public GraphingController(string plotfile) {
        this.plotfile = plotfile;
    }

    /// <summary>
    /// Graphs the given data.
    /// </summary>
    public void Graph(ConcurrentQueue<long[]> data) {
        double[][] iData0 = Utils<long>.SwapAxes(data);
        Dictionary<long, LinkedList<double>[]> iData = Utils.SortData(iData0[0], iData0[2], iData0[1], 1);

        Plot plot = new(400, 400);
        foreach(long key in iData.Keys) {
            plot.AddScatterPoints(iData[key][0].ToArray(), iData[key][1].ToArray(), markerSize:3, label:key.ToString());
        }
        plot.SaveFig(plotfile);
    }
}
