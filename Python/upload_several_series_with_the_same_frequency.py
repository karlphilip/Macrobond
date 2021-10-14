import numpy as np
import pandas as pd

# Creating random monthly series called 'temp','depth','acceleration'
np.random.seed(2019)
N = 24
rng = pd.date_range('2019-01-01', freq='MS', periods=N)
df = pd.DataFrame(np.random.rand(N, 3), columns=['temp','depth','acceleration'], index=rng)

df

# If you haven't installed it macrobond-api-constants, run the line below
# pip install macrobond-api-constants
from macrobond_api_constants import SeriesFrequency as f
from macrobond_api_constants import SeriesWeekdays as sw

#Constructing the metadata for upload
names=list(df.columns) # Note that the names need to be lower cases or numbers
description=["Temperature", "Depth", "Acceleration"]
region=["us","us","us"] # Find country codes here: https://techinfo.macrobond.com/regions-list/
category=["Upload from Python","Upload from Python","Upload from Python"]
frequency = f.MONTHLY
startdate=[min(rng), min(rng), min(rng)]

# Depending on which account you want to
com="ih:mb:com:" # For uploading to Company Account
dept="ih:mb:dept:" # For uploading to Department Account
priv="ih:mb:priv:"# For uploading to Personal Account
lib="ih:mb:lib:" # For uploading to Library account

import win32com.client
import datetime

c = win32com.client.Dispatch("Macrobond.Connection")
d = c.Database

m = d.CreateEmptyMetadata()

for i in range(len(names)):
    s = d.CreateSeriesObject(priv+names[i], # Name, combining the account you want to upload the data to with the series name
                         description[i], # Description (visable in Macrobond)
                         region[i], # Region
                         category[i], # Category
                         frequency, # Frequency
                         sw.FULLWEEK,
                         startdate[i].to_pydatetime(), # Start date
                         df.iloc[:,i], 
                         m)
    d.UploadOneOrMoreSeries(s)
    print(description[i]+" uploaded")
