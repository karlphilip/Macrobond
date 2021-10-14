import numpy as np
import pandas as pd

# Creating random monthly series called 'temp','depth','acceleration'
np.random.seed(2019)
N = 24
rng = pd.date_range('2019-01-01', freq='MS', periods=N)
df = pd.DataFrame(np.random.rand(N, 1), columns=['series'], index=rng)

df

# pip install macrobond-api-constants # If you haven't installed it yet
from macrobond_api_constants import SeriesFrequency as f
from macrobond_api_constants import SeriesWeekdays as sw

#Constructing the metadata for upload
names=df.columns[0] # Note that the names need to be lower cases or numbers
description="Series"
region="us" # Find country codes here: https://techinfo.macrobond.com/regions-list/
category="Upload from Python"
frequency = f.MONTHLY
startdate=min(rng)

import win32com.client
import datetime

c = win32com.client.Dispatch("Macrobond.Connection")
d = c.Database

# Depending on which account you want to
com="ih:mb:com:" # For uploading to Company Account
dept="ih:mb:dept:" # For uploading to Department Account
priv="ih:mb:priv:"# For uploading to Personal Account
lib="ih:mb:lib:" # For uploading to Library account

from datetime import date

today = date.today()
todaylong=today.strftime("%Y-%m-%d")
todayshort=today.strftime("%d%m%y")

m = d.CreateEmptyMetadata()

s = d.CreateSeriesObject(priv+names+todayshort, # Name, combining the account you want to upload the data to with the series name
                         description+" "+todaylong, # Description (visable in Macrobond)
                         region, # Region
                         category, # Category
                         frequency, # Frequency
                         sw.FULLWEEK,
                         startdate.to_pydatetime(), # Start date
                         df.values.tolist(), 
                         m)
d.UploadOneOrMoreSeries(s)
print(description+" uploaded")
