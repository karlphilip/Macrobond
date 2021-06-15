library(MacrobondAPI) #This sample requires Macrobond API 1.2-4 or later

library(ggplot2)

library(tidyverse)

library(rnaturalearth)

library(rnaturalearthdata)

library(plotly)

GetRegion <- function(entity) getFirstMetadataValue(getMetadata(entity), "Region")

GetRegionNames <- function(entities) sapply(entities, GetRegion)

GetLastValueFromMetadata <- function(entity) getFirstMetadataValue(getMetadata(entity), "LastValue")

GetRegionsIso2 <- function(regionEntities) sapply(regionEntities, function(entity) getFirstMetadataValue(getMetadata(entity), "IsoCountryCode2"))

FetchOneTimeSeries()

‍

# Searching for a concept in Macrobond and accessing the available data globally

query <- CreateSearchQuery()

setEntityTypeFilter(query, "TimeSeries")

addAttributeValueFilter(query, "RegionKey" , "owdc0008")

searchResult <- SearchEntities(query)

entities <- getEntities(searchResult)

regionNames <- GetRegionNames(entities) #Getting the Region names from the search result

regionEntities <- FetchEntities(regionNames)#Getting the Region Entities from Region in order to translate it to ISO2

regionIso <- GetRegionsIso2(regionEntities) #Getting the ISO 2

entitiesAndRegions <- mapply(function (entity, iso) c(entity = entity, iso = iso), entities, regionIso) #Converting the ISO

‍

# Inserting the country list for the map from rnaturalearth

mapdata <- ne_countries(scale = "medium", returnclass = "sf")

‍

# Remove entries for which we do not have matching iso codes

entitiesAndRegions <- entitiesAndRegions[unlist(sapply(entitiesAndRegions, function(x) !is.null(x$iso) && x$iso %in% mapdata$iso_a2))]

lastValues <- sapply(entitiesAndRegions, function(x) GetLastValueFromMetadata(x$entity))#Getting the last value from the meta data

isoCodes <- sapply(entitiesAndRegions, function(x) x$iso) #Getting the ISO2 codes

‍

# Creating a dataframe with region and last value

insert_data <- data.frame(iso_a2 = isoCodes, value = lastValues)

‍

# Joining the values with the map dataset

mapdata <- left_join(mapdata, insert_data, by="iso_a2")

mapdata <- subset(mapdata, select = c(name, value, geometry, iso_a2))

library(viridis)

‍

# Creating the map

map <- ggplot(data = mapdata, aes(text = paste(name, "<br>", "Fully vaccinated:", value,"%"))) +

geom_sf(aes(fill = value))+

ggtitle(GetConceptDescription(getConcepts(entities[[1]])))+

labs(title = GetConceptDescription(getConcepts(entities[[1]])), x = "Source: Macrobond")+

scale_fill_viridis_c(name = "%", option = "viridis", trans= "reverse")+

theme(axis.text.x = element_blank(),

axis.text.y = element_blank(),

axis.ticks = element_blank(),

axis.title.y=element_blank(),

rect = element_blank())

map

‍

# Creating a widget

fig <- ggplotly(map, tooltip = c("text"))

fig
