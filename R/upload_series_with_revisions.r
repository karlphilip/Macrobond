# Upload one series and store the uploaded series as a unique series in order to store the historical changes

library(MacrobondAPI)
library(tidyverse)

# Obtaining the values and start date from the data set
ts<-ts (1:50, frequency = 12, start = 2010) # Creating a time series with 50 observations and start date 2010
xts<-as.xts(ts) # Converting the time series to XTS

vector<-as.vector(xts[,1]) # Creating a vector of the data

startdate<-as.Date(index(xts)[1]) # Getting the startdate from the XTS object

# Getting the date of today
today<-as.Date(Sys.time())

# Metadata for upload
# Name (Series identifier)
account<-"ih:mb:priv:" # use "ih:mb:priv:" for personal account, "ih:mb:dept:" for department account, "ih:mb:com:" for company account
name<-"random" # the series identifier, only lowercases and numbers (must start with a letter)
fullnamewithdate<-paste(account, name, today, sep="") # Combining the full name with the date
fullnamewithdate<-str_replace_all(fullnamewithdate, "-", "") # Replacing the "-", since we can't use symbols

# Series description (Display name in the application)
description<-"My random series" # The series name
decriptionwithdate<-paste(description, today) # Combining the description with date today (which is the date of upload) 

# Region
region<-"us" # Specifying the region name, see the list of regions here: https://techinfo.macrobond.com/regions-list/

category<-"Random" # Specifying the category of the series

frequency<-"Monthly" # Specifying the series frequency

seriesNew = CreateTimeSeriesObject(fullnamewithdate, decriptionwithdate, region, category, frequency, startdate, values)
UploadOneOrMoreTimeSeries(seriesNew)
