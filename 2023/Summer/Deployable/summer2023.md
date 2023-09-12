---
permalink: /2023/summer/
---
## Data Analysis
### Experimental Data Compression:
A data transformer I made as an experiment that takes a large amount of input data and encodes/decodes it into/from a PNG file  
Status: One single bug (*ahem* feature): Image size hardcapping seems to be broken, so it is softcapped by processing time instead. Please do not try to do 1E7+ entries, as that image's size is >10MB, and I don't want your computer to hate you
<details>
    <summary>Controls</summary>
    <p>
    &emsp;To Run: dotnet run --project ./2023/Summer/DataAnalysis/experimental_data_compression/experimental_data_compression.csproj
    </p>
<details>
![](dataCompression.gif)

<h2></h2>