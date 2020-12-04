# Need to pip install macrobond-api-constants

import win32com.client
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
import pywintypes

c = win32com.client.Dispatch("Macrobond.Connection")
d = c.Database
s = d.FetchOneSeries("usgdp") # Fetch a Macrobond series

# Define a function that converts a series to pandas dataframe
def toPandasSeries(series):
    pdates = pd.to_datetime([d.strftime('%Y-%m-%d') for d in series.DatesAtStartOfPeriod])
    return pd.Series(series.values, index=pdates)
    
# Define a function that fetches a series and returns it as pandas
def getSeries(db, names):
    series = db.FetchSeries(names)
    return [toPandasSeries(s) for s in series]
    
data1 = toPandasSeries(s)
data1.plot()

# Get a list of all Metadata available for the series
s.Metadata.ListNames()

# Display one specific meta data value
s.Metadata.GetFirstValue("FirstRevisionTimeStamp")

# Fetching several series
data2 = getSeries(d,["spx", "obx","omxsgi"])
indices = pd.DataFrame(data2).T
indices.plot()

indices.columns = ["S&P 500", "OBX", "OMX SGI"] #Naming the columns

indices.plot() #Plotting with columns

# Preformance analysis
rebase = (indices/indices.loc["2018-01-08"])*100-100
rebase1 = rebase.loc["2018-01-08":]
rebase1.plot()

# Get several series from Macrobond as a pandas data frame with a common calendar
def getDataframe(db, unifiedSeriesRequest):
    series = db.FetchSeries(unifiedSeriesRequest)
    return pd.DataFrame({s.Name: toPandasSeries(s) for s in series})
    
from macrobond_api_constants import SeriesFrequency as f
from macrobond_api_constants import SeriesToHigherFrequencyMethod as h
from macrobond_api_constants import SeriesToLowerFrequencyMethod as l
from macrobond_api_constants import SeriesPartialPeriodsMethod as pp

# Fetching two series in different frequency into a monthly frequency with linear interpolation as
# frequency conversion method
r = d.CreateUnifiedSeriesRequest()
r.AddSeries('usgdp').ToHigherFrequencyMethod = h.LINEAR_INTERPOLATION
r.AddSeries('uscpi')
r.Frequency=f.MONTHLY
frames = getDataframe(d, r)
frames

r = d.CreateUnifiedSeriesRequest()
r.AddSeries('usgdp')
a=r.AddSeries('uscpi')
a.ToLowerFrequencyMethod = l.AVERAGE
a.PartialPeriodsMethod=pp.REPEAT_LAST
r.Frequency=f.QUARTERLY
frames = getDataframe(d, r)
frames
