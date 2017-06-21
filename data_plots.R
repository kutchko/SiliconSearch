rm(list=ls())

library(tidyverse)

setwd('~/insight/tech_cities/')

metro.data <- read_csv('metro_summary_data.csv')
str(metro.data)

high.tech <- metro.data %>%
    filter(PercentTech > 3)
LA <- metro.data %>%
    filter(grepl('Los Angeles', CBSA))

ggplot(metro.data, aes(x=PercentTech)) +
    geom_histogram() +
    geom_vline(xintercept=3, linetype='dotted') +
    labs(x='Percent of jobs in tech industry',
         y='Count',
         title='Distribution of tech industry sizes by metro area') +
    theme_bw()


ggplot(metro.data, aes(x=TotalPeople, y=TotalTech)) +
    geom_point() +
    scale_x_log10() +
    scale_y_log10() +
    theme_bw()
metro.data %>%
    filter(TotalPeople > 10000000)
metro.data %>%
    ggplot(aes(x=MedianAge)) +
    geom_histogram() +
    geom_vline(data = high.tech, aes(xintercept = MedianAge), linetype='dotted')
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
    ggplot(aes(x=PercentCollege)) +
    geom_histogram() +
    geom_vline(data = high.tech, aes(xintercept = PercentCollege), linetype='dotted') +
    geom_vline(data = LA, aes(xintercept = PercentCollege),
               linetype='dotted', colour='red')

ggplot(metro.data, aes(x=MedianIncome)) +
    geom_histogram(binwidth = 1000) +
    geom_vline(data = high.tech, aes(xintercept = MedianIncome), linetype='dotted')
ggplot(metro.data, aes(x=PercentFemale)) +
    geom_histogram() +
    geom_vline(data = high.tech, aes(xintercept = PercentFemale), linetype='dotted')
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

metro.data %>%
    ggplot(aes(x=Percent18to35)) +
    geom_histogram() +
    geom_vline(data = high.tech, aes(xintercept = Percent18to35), linetype='dotted') +
    geom_vline(data = LA, aes(xintercept = Percent18to35),
               linetype='dotted', colour='red')


