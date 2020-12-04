library(MacrobondAPI)

# Fetch one series
series<-FetchOneTimeSeries("usgdp")
series

plot(series)

# Convert the series to XTS
series.xts<-as.xts(series)

# Get Metadata of series
getMetadata(series)

# Fetch several series
data<-FetchTimeSeries(c("usgdp", "spx", "uscpi"))

plot(data$usgdp)

# Fetch several series in the same frequency (Monthly)
seriesRequest <- CreateUnifiedTimeSeriesRequest()
setFrequency(seriesRequest, TimeSeriesFrequency[["Monthly"]]) # Specifying the frequency to monthly
addSeries(seriesRequest, "usgdp") # Adding usgdp
seriesExpressionCpi <- addSeries(seriesRequest, "uscpi") # Adding uscpi
twoSeries <- FetchTimeSeries(seriesRequest)

series.xts <- MakeXtsFromUnifiedResponse(twoSeries)# Convert to XTS

# Fetch several series in the same frequency (Monthly) with Frequency conversion methods
seriesRequest <- CreateUnifiedTimeSeriesRequest()
setFrequency(seriesRequest, "Monthly")
addSeries(seriesRequest, "usgdp")
seriesExpressionCpi <- addSeries(seriesRequest, "uscpi")
setToHigherFrequencyMethod(seriesExpressionCpi, "LinearInterpolation") # ToHigherFrequencyMethod set to LinearInterpolation
twoSeries <- FetchTimeSeries(seriesRequest)

series.xts <- MakeXtsFromUnifiedResponse(twoSeries)

# Fetch several series in the same frequency (Quarterly) with Frequency conversion methods
seriesRequest <- CreateUnifiedTimeSeriesRequest()
setFrequency(seriesRequest, "Quarterly")
addSeries(seriesRequest, "usgdp")
seriesExpressionCpi <- addSeries(seriesRequest, "uscpi")
setToLowerFrequencyMethod(seriesExpressionCpi, "Average") # ToLowerFrequencyMethod set to Average
setPartialPeriodsMethod(seriesExpressionCpi, "RepeatLastValue") # PartialPeriodsMethod set to Repeat
twoSeries <- FetchTimeSeries(seriesRequest)

series.xts <- MakeXtsFromUnifiedResponse(twoSeries)
