# PredictWind Bermuda Race Wind Data Analysis and Best Sailing Path using Dijkstra's Algorithm and Other Techniques

During the summer, I had a great opportunity to stay with a Ukrainian family in Philadelphia who happened to know Mr. Askold Sandursky. He was looking for weather data assistant for a yacht sailing competition to Bermuda and invited me to help with some data analysis for a future route. He taught me a lot about different models and how he used them before for the competition. His analysis were impressive, but too general, and I saw that the primary challenge was dealing with the immense volume of weather data from various models (PWS, ECMWF, GFS, SPIRE, and UKMO), which made manual analysis impractical. To tackle this issue, I developed a Python program that automated the analysis of 20 weather data gathering stations along our route, identifying deviations between predictions and actual data on prediction day. Collecting data every 3 hours daily throughout the month aimed to unveil patterns and determine the best models for wind speed, gusts, directions, and temperature; then, explain why they emerged within a small research of each model.

The most significant challenge was integrating the most reliable weather forecasting models for specific wind characteristics to find the shortest competition route. I was delighted to apply knowledge from my CPSC 223 & 365 classes at Yale, Dijkstra's Algorithm. However, ensuring a continuous path, independent of weather grid points, presented additional hurdles in computation (for further discussion).

Despite these challenges, our yacht secured an impressive third place out of five boats in the competition. This project (published on GitHub) underscored the significance of data analysis and algorithmic solutions in optimizing even yacht racing routes, demonstrating their potential in the field. You can find more details about their performance [here](https://yachtscoring.com/event_results_cumulative.cfm?eID=14646) and Cape Gazzete [Article](https://www.capegazette.com/article/new-jersey-crew-crosses-bay-win-lewes-cup/261257).
<br><br>

![Data Provider, Application Photo, Predict Wind](DataSource.png)
