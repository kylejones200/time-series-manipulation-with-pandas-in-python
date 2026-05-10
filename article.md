# Time Series manipulation with Pandas in Python

Pandas has built in tools we can use to analyze time series data such as shifting, windowing, resampling, and imputing missing values. This...

### Time Series manipulation with Pandas in Python
**Pandas** has built in tools we can use to analyze time series data such as shifting, windowing, resampling, and imputing missing values. This data engineering work not the fun part of time series analysis, but it is important.


<figcaption>Photo by <a class="markup--anchor markup--figure-anchor" rel="photo-creator noopener" target="_blank">Bianca Ackermann</a> on <a class="markup--anchor markup--figure-anchor"


### Shifting Data
Shifting involves moving data forward or backward in time, commonly used to create **lagged features** or compare values across time.

#### Creating Lagged Features
Lagged features are crucial for capturing the temporal dependencies in time series data. This is just sample data.


You can use this to compare the value today against the value yesterday. It is also useful for creating lagged variables for machine learning models.

#### Windowing (Rolling Statistics)
Windowing calculates statistics over a rolling window, such as moving averages or standard deviations. It smooths data and highlights trends.

The rolling mean is the most common. But you can do a rolling window with lots of different kinds of aggregation.


Like calculating the rolling Standard Deviation which can be helpful when looking at volatility.


#### Resampling
Resampling changes the frequency of time series data, either by **aggregating** data (downsampling) or by **interpolating** data (upsampling). We can aggregate hourly data into daily, weekly, or monthly statistics. Or interpolate data between observations by using upsampling.


#### Imputing Missing Values
ML models hate missing values. Pandas offers several strategies for imputing missing values. For some sensor data, we may only get new values, so we need to fill in the time when the reading was the same.

#### Forward Fill (or Back Fill)


Mean Imputation is useful when you have a gap in observations.


### Combining Techniques
In real like, TS analytics usually needs a combination of shifting, windowing, resampling, and imputing.


### Takeaway
Most TS libraries have features for shifting, windowing, resampling and imputing. The useful thing to know is that Pandas has these built in too. So if you are already using a pandas dataframe, you can create these features without needing a specialized library.
