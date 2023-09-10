int[] dataDistribution = new int[]{3, 3, 2};
Module<long[]> readerModule = new CollatzConjectureModule<long[]>(1000000);
GraphingController graphingModule = new GraphingController("resources/plot.png");

EncoderController controller = new(dataDistribution, "resources/output.png", readerModule, graphingModule);
controller.ReadData();
controller.EncodeData();
controller.DecodeData();
controller.GraphData();
controller.PrintInfo();