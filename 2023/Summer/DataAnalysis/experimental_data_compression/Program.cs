string path = "2023/Summer/DataAnalysis/experimental_data_compression/resources/";

int[] dataDistribution = new int[]{3, 3, 2};
Module<long[]> readerModule = new CollatzConjectureModule<long[]>(1000000);
GraphingController graphingModule = new GraphingController(path + "plot.png");

EncoderController controller = new(dataDistribution, path + "output.png", readerModule, graphingModule);
controller.ReadData();
controller.EncodeData();
controller.DecodeData();
controller.GraphData();
controller.PrintInfo();