rm(list=ls())

library(tidyverse)

setwd('~/insight/tech_cities/')

metro.data <- read_csv('metro_summary_data.csv')
str(metro.data)

ggplot(metro.data, aes(x=TotalPeople, y=TotalTech)) +
    geom_point() +
    scale_x_log10() +
    scale_y_log10() +
    theme_bw()
metro.data %>%
    filter(TotalPeople > 10000000)
metro.data %>%
    ggplot(aes(x=MedianAge)) +
    geom_histogram()
metro.data %>%
    filter(MedianAge > 50)
metro.data %>%
    filter(MedianAge < 30)
metro.data %>%
    filter(grepl('UT', CBSA))

metro.data %>%
    ggplot(aes(x=PercentHighSchool, y=PercentCollege)) +
    geom_point(aes(colour=PercentPostGrad)) +
    scale_colour_gradient(low='pink', high='darkred') +
    theme_bw()
metro.data %>%
    select(CBSA, PercentHighSchool, PercentCollege, PercentPostGrad) %>%
    gather(Metric, Percent, -CBSA) %>%
    ggplot(aes(x=Percent)) +
    geom_histogram() +
    theme_bw() + 
    facet_grid(~ Metric, scales='free_x')
metro.data %>% filter(PercentHighSchool < .8)

metro.data %>%
    filter(PercentHighSchool > 1)

ggplot(metro.data, aes(x=MedianIncome)) +
    geom_histogram(binwidth = 1000)
ggplot(metro.data, aes(x=PercentFemale)) +
    geom_histogram()
metro.data %>%
    filter(PercentFemale < 0.48)
metro.data %>%
    filter(PercentFemale > 0.525)
metro.data %>%
    ggplot(aes(x=PercentBornOutOfState)) +
    geom_histogram()
metro.data %>%
    ggplot(aes(x=PercentImmigrant)) +
    geom_histogram()

metro.data %>%
    filter(PercentImmigrant > 0.3)
metro.data %>%
    filter(PercentBornOutOfState > 0.7)

metro.data %>%
    ggplot(aes(x=PercentTech)) +
    geom_histogram()

metro.data %>%
    ggplot(aes(x=MedianRent)) +
    geom_histogram() +
    scale_x_log10()
metro.data %>%
    ggplot(aes(x=MedianHouseValue)) +
    geom_histogram() +
    scale_x_log10()

metro.data %>%
    filter(MedianHouseValue > 400000)
metro.data %>%
    filter(MedianRent > 1000)

metro.data %>%
    ggplot(aes(x=DiversityIndex)) +
    geom_histogram()


