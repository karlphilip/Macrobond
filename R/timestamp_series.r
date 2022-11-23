library(MacrobondAPI)

# Fetching a time series with the revisions
seriesGdp <- FetchOneTimeSeriesWithRevisions("usgdp")

# Function to build a timeseries of initial release with the timestamp of the release and the value
initial.timestamp<-function(series) {
  firstRelease <- getNthRelease(seriesGdp, 0)
  timestamp<-data.frame(getTimesFromHistoricalSeries(firstRelease))
  data<-data.frame(t(timestamp), getValues(firstRelease))
  rownames(data) <- 1:nrow(data)
  colnames(data) <- c("Timestamp", "Value")
  return(data)
}

initial.timestamp(seriesGdp)

# Function to build a timeseries with the timestamp of the release and the value
timestamp.series<-function(series) {
  full<-getCompleteHistory(series)
  
  value<-c()
  timestamp<-as.Date(NA)

    for(i in 1:length(full)){
    z<-getValues(full[[i]]$series)
    y<-na.omit(z)
    value[i]<-y[length(y)]
  
    timestamp[i]<-getFirstMetadataValue(getMetadata(full[[i]]$series), "RevisionTimestamp")
    }
  df<-data.frame(timestamp, value)[-1,]
  return(df)
}

timestamp.ser<-timestamp.series(seriesGdp)
init.timestamp.ser<-initial.timestamp(seriesGdp)
