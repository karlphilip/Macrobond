import pandas as pd
import matplotlib.pyplot as plt
import win32com.client
import numpy as np
import datetime
c = win32com.client.Dispatch("Macrobond.Connection")
d = c.Database

# Fetch the timeseries with revision
s = d.FetchOneSeriesWithRevisions("usgdp")

# Defining a function which returns the initial release of each observation and the timestamp when the value was released
def InitialReleasetoTimestampSeries(series):
    firstReleaseSeries = s.GetNthRelease(0)
    firstReleaseDates = [vm.GetFirstValue("RevisionTimestamp").strftime("%Y-%m-%d %H:%M:%S") for vm in firstReleaseSeries.ValuesMetadata]

    dataframe = pd.DataFrame(firstReleaseSeries.Values, firstReleaseDates)
    dataframe.columns =[firstReleaseSeries.Name]
    return(dataframe)
  
# Fetching the series above with the InitialReleasetoTimestampSeries function
InitialReleasetoTimestampSeries(s)

# Defining a function which returns the timestamps of each release and the latest value available in each of the releases
def toTimestampSeries(series):
    h = series.GetCompleteHistory()
    value=[h[i].Metadata.GetFirstValue("LastValue") for i in range(1, len(h))]
    timestamp=[h[i].Metadata.GetFirstValue("RevisionTimestamp").strftime("%Y-%m-%d %H:%M:%S") for i in range(1, len(h))]
    
    dataframe = pd.DataFrame(value, timestamp)
    dataframe.columns =[h[1].Name]
    return(dataframe)
  
# Fetching the series above with the toTimestampSeries function
toTimestampSeries(s)

# Defining a function which returns the timestamps of each release and the latest value available in each of the releases together with the observation the value is refering to
def toTimestampSeriesWithObservation(series):
    h = series.GetCompleteHistory()
    value=[h[i].Metadata.GetFirstValue("LastValue") for i in range(1, len(h))]
    timestamp=[h[i].Metadata.GetFirstValue("RevisionTimestamp").strftime("%Y-%m-%d %H:%M:%S") for i in range(1, len(h))]
    obs=[h[i].Metadata.GetFirstValue("EndDate").strftime("%Y-%m-%d") for i in range(1, len(h))]
    
    dataframe = pd.DataFrame()
    dataframe['Timestamp'] = timestamp
    dataframe['Observation date'] = obs
    dataframe['Value'] = value
    return(dataframe)

# Fetching the series above with the toTimestampSeriesWithObservation function
toTimestampSeriesWithObservation(s)
