import pandas as pd
import matplotlib.pyplot as plt
import win32com.client
import numpy as np
import time
import datetime
import pywintypes
from macrobond_api_constants import SeriesFrequency as f

c = win32com.client.Dispatch("Macrobond.Connection")
d = c.Database


def toPandasSeries(series):
    pdates = pd.to_datetime([d.strftime('%Y-%m-%d') for d in series.DatesAtStartOfPeriod])
    return pd.Series(series.values, index=pdates)

# Fetch a series with revisions
s = d.FetchOneSeriesWithRevisions("usgdp")


#Get every datapoints' N-th release
x = toPandasSeries(s.GetNthRelease(0))
y = toPandasSeries(s.GetNthRelease(1))
z = toPandasSeries(s.GetNthRelease(2))

#Remove NaN
x = x[np.logical_not(np.isnan(x))]
y = y[np.logical_not(np.isnan(y))]
z = z[np.logical_not(np.isnan(z))]

df = pd.DataFrame([x,y,z])
data = df
data

#Get full timeseries for a specific release update (or version)
def toPandasSeries(series):
    pdates = pd.to_datetime([d.strftime('%Y-%m-%d') for d in series.DatesAtStartOfPeriod])
    return pd.Series(series.values, index=pdates)

#Get every revisions that has been made for series' specific datapoint (take notice of series' frequency here)
pl = toPandasSeries(s.GetObservationHistory(datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc)))
pl

# Fetch a specific revision based on the release date
v = toPandasSeries(s.GetVintage(datetime.datetime(2019, 1, 1, 12, 31, tzinfo=datetime.timezone.utc)))
v

#Get the complete revision history from one series
history = s.GetCompleteHistory()

#Last value for a series based on release timestamp
tables = pd.DataFrame(columns=['Timestamp', 'Observation date', 'Value'])

for i in range(1, len(history)):
    try:
        x = str(history[i].Metadata.GetFirstValue("RevisionTimestamp"))
        d=toPandasSeries(history[i])
        dna=d.dropna()
        z=dna[-1]
        y=dna.index[-1]
    except:
        pass
    tables = tables.append({'Timestamp': x, 'Observation date': y, 'Value': z}, ignore_index=True)
tables

for i in range(1, len(history)):
    try:
        x = str(history[i].Metadata.GetFirstValue("RevisionTimestamp"))
        d=toPandasSeries(history[i])
    except:
        pass
    tables = tables.append({'Timestamp': x, 'Observation date': y, 'Value': z}, ignore_index=True)
tables

# Get full revision history into one dataframe

full_history=pd.DataFrame()
for x in range(13, len(history)):
    full_history[str(history[x].Metadata.GetFirstValue("RevisionTimestamp"))]=toPandasSeries(history[x])
full_history
