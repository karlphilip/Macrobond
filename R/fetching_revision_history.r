library(MacrobondAPI)
library(xts)

# Fetch a series with revision history
seriesGdp <- FetchOneTimeSeriesWithRevisions("usgdp")

# Get every datapoints' N-th release
initial_release <- getNthRelease(seriesGdp, 0)
first_revision <- getNthRelease(seriesGdp, 1)

# Convert the data to XTS
series.xts <- MakeXtsFromUnifiedResponse(c(firstRelease, secondRelease))
plot(series.xts)

# Compare the difference between the initial release and first revision
revision_difference <- series.xts[,1]-series.xts[,2]
plot(revision_difference)

# Load the series revisions and get the vintage series, that shows what it looked like at a speficic date
s2017 <- getVintage(seriesGdp, as.Date("2017-01-01"))
s2018 <- getVintage(seriesGdp, as.Date("2018-01-01"))
s2019 <- getVintage(seriesGdp, as.Date("2019-01-01"))
s2020 <- getVintage(seriesGdp, as.Date("2020-01-01"))
x <- MakeXtsFromUnifiedResponse(c(s2017, s2018, s2019, s2020))

plot(x)

# Get full history of revisions
ch <- getCompleteHistory(seriesGdp)

values <- cbind(sapply(ch, function(s) getValues(s$series)))

rev.valuesFrame <- xts(values, order.by=getDatesAtStartOfPeriod(ch[[1]]$series))
rev.timestamps <-  cbind(sapply(ch, function(s) s$timestamp))

# Set headings to text of timestamps for convenience
colnames(rev.valuesFrame) <- sapply(rev.timestamps, function(x) { if (is.null(x)) return("start") else return(strftime(x,"%Y-%m-%d %H:%M:%S")) })

View(rev.valuesFrame)
