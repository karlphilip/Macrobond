# Upload several series into Macrobond with the same frequency

library(MacrobondAPI)
library(astsa) #Package for the different timeseries

# Getting the data
s1<-as.xts(birth)
s2<-as.xts(UnempRate)
s3<-as.xts(unemp)
s4<-as.xts(salmon)

data.xts<-merge.xts(s1, s2, s3, s4)

# Creating a table with metadata
series<-c("birth", "UnempRate", "unemp", "salmon")
description<-c("U.S. Monthly Live Births" ,"U.S. Unemployment Rate", "U.S. Unemployment", "Farm Bred Norwegian Salmon, export price, US Dollars per Kilogram")
region<-c("us","us","us", "no") # Find country codes here: https://techinfo.macrobond.com/regions-list/
category<-c("Demography", "Labor market", "Labor market", "Commodities & Energy")
frequency<-"Monthly"
start.date<-as.Date(index(data.xts[1]))

metadata<-data.frame(series, description, region, category, start.date)

com<-"ih:mb:com:" # For uploading to Company Account
dept<-"ih:mb:dept:" # For uploading to Department Account
priv<-"ih:mb:priv:"# For uploading to Personal Account
lib<-"ih:mb:lib" # For uploading to Library account

# Looping to upload several series

for(i in 1:nrow(metadata)){
  values<-as.vector(data.xts[,i]) #Getting the values into a vector
  
  #Creating the time series object
  series<-CreateTimeSeriesObject(paste(priv, tolower(metadata[i,1]), sep=""), # Series name
                                 paste(metadata[i,2], sep=""),  # Description (visable in Macrobond)
                                 paste(metadata[i,3]), # Region
                                 paste(metadata[i,4]), # Category
                                 paste(frequency), # Frequency
                                 start.date, # Start date
                                 values)
  
  # Uploading the time series
  UploadOneOrMoreTimeSeries(series)
  
  print(paste(metadata[i,2], "has been uploaded"))
}
