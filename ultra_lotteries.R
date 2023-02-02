# This script runs the econometrics for the ultra_lotteries project

# Loading libraries

library(stargazer)
library(sandwich)
library(ggplot2)
library(lmtest)
library(dplyr)

# Directory info

username <- ''
direc <- paste('C:/Users/', username, '/Documents/Data/ultra_lotteries/', sep = '')

# Reading in the data

races <- read.csv(paste(direc, 'Data/data_race_count.csv', sep = ''))
place <- read.csv(paste(direc, 'Data/data_mean_place.csv', sep = ''))
wins <- read.csv(paste(direc, 'Data/data_wins.csv', sep = ''))
winpct <- read.csv(paste(direc, 'Data/data_win_percentage.csv', sep = ''))
size <- read.csv(paste(direc, 'Data/data_mean_race_size.csv', sep = ''))
alt <- read.csv(paste(direc, 'Data/data_mean_race_altitude.csv', sep = ''))
travel <- read.csv(paste(direc, 'Data/data_mean_travel_distance.csv', sep = ''))
f <- read.csv(paste(direc, 'Data/data_mean_percent_female.csv', sep = ''))

# Adding a POST variable for to make lm && stargazer happy

races$Post <- as.numeric(races$Period == 'Post')
place$Post <- as.numeric(place$Period == 'Post')
wins$Post <- as.numeric(wins$Period == 'Post')
winpct$Post <- as.numeric(winpct$Period == 'Post')
size$Post <- as.numeric(size$Period == 'Post')
alt$Post <- as.numeric(alt$Period == 'Post')
travel$Post <- as.numeric(travel$Period == 'Post')
f$Post <- as.numeric(f$Period == 'Post')

# Subsetting for individual regressions

races.l <- races[which(races$Treatment_Type == 'Lottery'),]
races.l <- races.l[order(nrow(races.l):1),]
row.names(races.l) <- c(1:dim(races.l)[1])
races.l1 <- races.l[which(races.l$Window == 1),]
races.l2 <- races.l[which(races.l$Window == 2),]
races.l3 <- races.l[which(races.l$Window == 3),]
races.l4 <- races.l[which(races.l$Window == 4),]

races.r <- races[which(races$Treatment_Type == 'Race'),]
races.r<- races.r[order(nrow(races.r):1),]
row.names(races.r) <- c(1:dim(races.r)[1])
races.r1 <- races.r[which(races.r$Window == 1),]
races.r2 <- races.r[which(races.r$Window == 2),]
races.r3 <- races.r[which(races.r$Window == 3),]
races.r4 <- races.r[which(races.r$Window == 4),]

place.l <- place[which(place$Treatment_Type == 'Lottery'),]
place.l <- place.l[order(nrow(place.l):1),]
row.names(place.l) <- c(1:dim(place.l)[1])
place.l1 <- place.l[which(place.l$Window == 1),]
place.l2 <- place.l[which(place.l$Window == 2),]
place.l3 <- place.l[which(place.l$Window == 3),]
place.l4 <- place.l[which(place.l$Window == 4),]

place.r <- place[which(place$Treatment_Type == 'Race'),]
place.r<- place.r[order(nrow(place.r):1),]
row.names(place.r) <- c(1:dim(place.r)[1])
place.r1 <- place.r[which(place.r$Window == 1),]
place.r2 <- place.r[which(place.r$Window == 2),]
place.r3 <- place.r[which(place.r$Window == 3),]
place.r4 <- place.r[which(place.r$Window == 4),]

wins.l <- wins[which(wins$Treatment_Type == 'Lottery'),]
wins.l <- wins.l[order(nrow(wins.l):1),]
row.names(wins.l) <- c(1:dim(wins.l)[1])
wins.l1 <- wins.l[which(wins.l$Window == 1),]
wins.l2 <- wins.l[which(wins.l$Window == 2),]
wins.l3 <- wins.l[which(wins.l$Window == 3),]
wins.l4 <- wins.l[which(wins.l$Window == 4),]

wins.r <- wins[which(wins$Treatment_Type == 'Race'),]
wins.r<- wins.r[order(nrow(wins.r):1),]
row.names(wins.r) <- c(1:dim(wins.r)[1])
wins.r1 <- wins.r[which(wins.r$Window == 1),]
wins.r2 <- wins.r[which(wins.r$Window == 2),]
wins.r3 <- wins.r[which(wins.r$Window == 3),]
wins.r4 <- wins.r[which(wins.r$Window == 4),]

winpct.l <- winpct[which(winpct$Treatment_Type == 'Lottery'),]
winpct.l <- winpct.l[order(nrow(winpct.l):1),]
row.names(winpct.l) <- c(1:dim(winpct.l)[1])
winpct.l1 <- winpct.l[which(winpct.l$Window == 1),]
winpct.l2 <- winpct.l[which(winpct.l$Window == 2),]
winpct.l3 <- winpct.l[which(winpct.l$Window == 3),]
winpct.l4 <- winpct.l[which(winpct.l$Window == 4),]

winpct.r <- winpct[which(winpct$Treatment_Type == 'Race'),]
winpct.r<- winpct.r[order(nrow(winpct.r):1),]
row.names(winpct.r) <- c(1:dim(winpct.r)[1])
winpct.r1 <- winpct.r[which(winpct.r$Window == 1),]
winpct.r2 <- winpct.r[which(winpct.r$Window == 2),]
winpct.r3 <- winpct.r[which(winpct.r$Window == 3),]
winpct.r4 <- winpct.r[which(winpct.r$Window == 4),]

size.l <- size[which(size$Treatment_Type == 'Lottery'),]
size.l <- size.l[order(nrow(size.l):1),]
row.names(size.l) <- c(1:dim(size.l)[1])
size.l1 <- size.l[which(size.l$Window == 1),]
size.l2 <- size.l[which(size.l$Window == 2),]
size.l3 <- size.l[which(size.l$Window == 3),]
size.l4 <- size.l[which(size.l$Window == 4),]

size.r <- size[which(size$Treatment_Type == 'Race'),]
size.r<- size.r[order(nrow(size.r):1),]
row.names(size.r) <- c(1:dim(size.r)[1])
size.r1 <- size.r[which(size.r$Window == 1),]
size.r2 <- size.r[which(size.r$Window == 2),]
size.r3 <- size.r[which(size.r$Window == 3),]
size.r4 <- size.r[which(size.r$Window == 4),]

alt.l <- alt[which(alt$Treatment_Type == 'Lottery'),]
alt.l <- alt.l[order(nrow(alt.l):1),]
row.names(alt.l) <- c(1:dim(alt.l)[1])
alt.l1 <- alt.l[which(alt.l$Window == 1),]
alt.l2 <- alt.l[which(alt.l$Window == 2),]
alt.l3 <- alt.l[which(alt.l$Window == 3),]
alt.l4 <- alt.l[which(alt.l$Window == 4),]

alt.r <- alt[which(alt$Treatment_Type == 'Race'),]
alt.r<- alt.r[order(nrow(alt.r):1),]
row.names(alt.r) <- c(1:dim(alt.r)[1])
alt.r1 <- alt.r[which(alt.r$Window == 1),]
alt.r2 <- alt.r[which(alt.r$Window == 2),]
alt.r3 <- alt.r[which(alt.r$Window == 3),]
alt.r4 <- alt.r[which(alt.r$Window == 4),]

travel.l <- travel[which(travel$Treatment_Type == 'Lottery'),]
travel.l <- travel.l[order(nrow(travel.l):1),]
row.names(travel.l) <- c(1:dim(travel.l)[1])
travel.l1 <- travel.l[which(travel.l$Window == 1),]
travel.l2 <- travel.l[which(travel.l$Window == 2),]
travel.l3 <- travel.l[which(travel.l$Window == 3),]
travel.l4 <- travel.l[which(travel.l$Window == 4),]

travel.r <- travel[which(travel$Treatment_Type == 'Race'),]
travel.r<- travel.r[order(nrow(travel.r):1),]
row.names(travel.r) <- c(1:dim(travel.r)[1])
travel.r1 <- travel.r[which(travel.r$Window == 1),]
travel.r2 <- travel.r[which(travel.r$Window == 2),]
travel.r3 <- travel.r[which(travel.r$Window == 3),]
travel.r4 <- travel.r[which(travel.r$Window == 4),]

f.l <- f[which(f$Treatment_Type == 'Lottery'),]
f.l <- f.l[order(nrow(f.l):1),]
row.names(f.l) <- c(1:dim(f.l)[1])
f.l1 <- f.l[which(f.l$Window == 1),]
f.l2 <- f.l[which(f.l$Window == 2),]
f.l3 <- f.l[which(f.l$Window == 3),]
f.l4 <- f.l[which(f.l$Window == 4),]

f.r <- f[which(f$Treatment_Type == 'Race'),]
f.r<- f.r[order(nrow(f.r):1),]
row.names(f.r) <- c(1:dim(f.r)[1])
f.r1 <- f.r[which(f.r$Window == 1),]
f.r2 <- f.r[which(f.r$Window == 2),]
f.r3 <- f.r[which(f.r$Window == 3),]
f.r4 <- f.r[which(f.r$Window == 4),]

ff.l1 <- f.l1[which(f.l1$Gender == 'F'),]
ff.l2 <- f.l2[which(f.l2$Gender == 'F'),]
ff.l3 <- f.l3[which(f.l3$Gender == 'F'),]
ff.l4 <- f.l4[which(f.l4$Gender == 'F'),]

ff.r1 <- f.r1[which(f.r1$Gender == 'F'),]
ff.r2 <- f.r2[which(f.r2$Gender == 'F'),]
ff.r3 <- f.r3[which(f.r3$Gender == 'F'),]
ff.r4 <- f.r4[which(f.r4$Gender == 'F'),]

# Running regressions

mod.races.l1 <- lm(Races ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = races.l1)

mod.races.l2 <- lm(Races ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = races.l2)

mod.races.l3 <- lm(Races ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = races.l3)

mod.races.l4 <- lm(Races ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = races.l4)

mod.races.r1 <- lm(Races ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = races.r1)

mod.races.r2 <- lm(Races ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = races.r2)

mod.races.r3 <- lm(Races ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = races.r3)

mod.races.r4 <- lm(Races ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = races.r4)

mod.place.l1 <- lm(Place ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = place.l1)

mod.place.l2 <- lm(Place ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = place.l2)

mod.place.l3 <- lm(Place ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = place.l3)

mod.place.l4 <- lm(Place ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = place.l4)

mod.place.r1 <- lm(Place ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = place.r1)

mod.place.r2 <- lm(Place ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = place.r2)

mod.place.r3 <- lm(Place ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = place.r3)

mod.place.r4 <- lm(Place ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                   + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                   + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = place.r4)

mod.wins.l1 <- lm(Wins ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = wins.l1)

mod.wins.l2 <- lm(Wins ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = wins.l2)

mod.wins.l3 <- lm(Wins ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = wins.l3)

mod.wins.l4 <- lm(Wins ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = wins.l4)

mod.wins.r1 <- lm(Wins ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = wins.r1)

mod.wins.r2 <- lm(Wins ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = wins.r2)

mod.wins.r3 <- lm(Wins ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = wins.r3)

mod.wins.r4 <- lm(Wins ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = wins.r4)

mod.winpct.l1 <- lm(Win_Percentage ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = winpct.l1)

mod.winpct.l2 <- lm(Win_Percentage ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = winpct.l2)

mod.winpct.l3 <- lm(Win_Percentage ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = winpct.l3)

mod.winpct.l4 <- lm(Win_Percentage ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = winpct.l4)

mod.winpct.r1 <- lm(Win_Percentage ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = winpct.r1)

mod.winpct.r2 <- lm(Win_Percentage ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = winpct.r2)

mod.winpct.r3 <- lm(Win_Percentage ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = winpct.r3)

mod.winpct.r4 <- lm(Win_Percentage ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = winpct.r4)

mod.size.l1 <- lm(Race_Size ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = size.l1)

mod.size.l2 <- lm(Race_Size ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = size.l2)

mod.size.l3 <- lm(Race_Size ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = size.l3)

mod.size.l4 <- lm(Race_Size ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = size.l4)

mod.size.r1 <- lm(Race_Size ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = size.r1)

mod.size.r2 <- lm(Race_Size ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = size.r2)

mod.size.r3 <- lm(Race_Size ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = size.r3)

mod.size.r4 <- lm(Race_Size ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                  + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                  + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = size.r4)

mod.alt.l1 <- lm(Race_Altitude ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                 + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                 + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = alt.l1)

mod.alt.l2 <- lm(Race_Altitude ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                 + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                 + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = alt.l2)

mod.alt.l3 <- lm(Race_Altitude ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                 + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                 + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = alt.l3)

mod.alt.l4 <- lm(Race_Altitude ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                 + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                 + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = alt.l4)

mod.alt.r1 <- lm(Race_Altitude ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                 + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                 + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = alt.r1)

mod.alt.r2 <- lm(Race_Altitude ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                 + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                 + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = alt.r2)

mod.alt.r3 <- lm(Race_Altitude ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                 + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                 + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = alt.r3)

mod.alt.r4 <- lm(Race_Altitude ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                 + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                 + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = alt.r4)

mod.travel.l1 <- lm(Travel_Distance ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = travel.l1)

mod.travel.l2 <- lm(Travel_Distance ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = travel.l2)

mod.travel.l3 <- lm(Travel_Distance ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = travel.l3)

mod.travel.l4 <- lm(Travel_Distance ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = travel.l4)

mod.travel.r1 <- lm(Travel_Distance ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = travel.r1)

mod.travel.r2 <- lm(Travel_Distance ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = travel.r2)

mod.travel.r3 <- lm(Travel_Distance ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = travel.r3)

mod.travel.r4 <- lm(Travel_Distance ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                    + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                    + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = travel.r4)

mod.f.l1 <- lm(Percent_Female ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
               + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
               + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = f.l1)

mod.f.l2 <- lm(Percent_Female ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
               + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
               + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = f.l2)

mod.f.l3 <- lm(Percent_Female ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
               + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
               + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = f.l3)

mod.f.l4 <- lm(Percent_Female ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
               + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
               + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = f.l4)

mod.f.r1 <- lm(Percent_Female ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
               + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
               + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = f.r1)

mod.f.r2 <- lm(Percent_Female ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
               + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
               + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = f.r2)

mod.f.r3 <- lm(Percent_Female ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
               + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
               + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = f.r3)

mod.f.r4 <- lm(Percent_Female ~ Treated*Post + factor(Gender) + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
               + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
               + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = f.r4)

mod.ff.l1 <- lm(Percent_Female ~ Treated*Post + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = ff.l1)

mod.ff.l2 <- lm(Percent_Female ~ Treated*Post + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = ff.l2)

mod.ff.l3 <- lm(Percent_Female ~ Treated*Post + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = ff.l3)

mod.ff.l4 <- lm(Percent_Female ~ Treated*Post + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = ff.l4)

mod.ff.r1 <- lm(Percent_Female ~ Treated*Post + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = ff.r1)

mod.ff.r2 <- lm(Percent_Female ~ Treated*Post + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = ff.r2)

mod.ff.r3 <- lm(Percent_Female ~ Treated*Post + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = ff.r3)

mod.ff.r4 <- lm(Percent_Female ~ Treated*Post + Age + I(Age*Age) + Tickets + WSER_Pre + Prior_Race_Experience
                + Home_Altitude + Population + Income + Unemployment_Rate + EDU_High_School + EDU_Some_College + EDU_Associate
                + EDU_Bachelor + EDU_Graduate + factor(Runner_ID) + factor(Year), data = ff.r4)

# Robust standard errors

se.races.l1 <- coeftest(mod.races.l1, vcov. = vcovCL, cluster = ~FIPS)
se.races.l2 <- coeftest(mod.races.l2, vcov. = vcovCL, cluster = ~FIPS)
se.races.l3 <- coeftest(mod.races.l3, vcov. = vcovCL, cluster = ~FIPS)
se.races.l4 <- coeftest(mod.races.l4, vcov. = vcovCL, cluster = ~FIPS)

se.races.r1 <- coeftest(mod.races.r1, vcov. = vcovCL, cluster = ~FIPS)
se.races.r2 <- coeftest(mod.races.r2, vcov. = vcovCL, cluster = ~FIPS)
se.races.r3 <- coeftest(mod.races.r3, vcov. = vcovCL, cluster = ~FIPS)
se.races.r4 <- coeftest(mod.races.r4, vcov. = vcovCL, cluster = ~FIPS)

se.place.l1 <- coeftest(mod.place.l1, vcov. = vcovCL, cluster = ~FIPS)
se.place.l2 <- coeftest(mod.place.l2, vcov. = vcovCL, cluster = ~FIPS)
se.place.l3 <- coeftest(mod.place.l3, vcov. = vcovCL, cluster = ~FIPS)
se.place.l4 <- coeftest(mod.place.l4, vcov. = vcovCL, cluster = ~FIPS)

se.place.r1 <- coeftest(mod.place.r1, vcov. = vcovCL, cluster = ~FIPS)
se.place.r2 <- coeftest(mod.place.r2, vcov. = vcovCL, cluster = ~FIPS)
se.place.r3 <- coeftest(mod.place.r3, vcov. = vcovCL, cluster = ~FIPS)
se.place.r4 <- coeftest(mod.place.r4, vcov. = vcovCL, cluster = ~FIPS)

se.wins.l1 <- coeftest(mod.wins.l1, vcov. = vcovCL, cluster = ~FIPS)
se.wins.l2 <- coeftest(mod.wins.l2, vcov. = vcovCL, cluster = ~FIPS)
se.wins.l3 <- coeftest(mod.wins.l3, vcov. = vcovCL, cluster = ~FIPS)
se.wins.l4 <- coeftest(mod.wins.l4, vcov. = vcovCL, cluster = ~FIPS)

se.wins.r1 <- coeftest(mod.wins.r1, vcov. = vcovCL, cluster = ~FIPS)
se.wins.r2 <- coeftest(mod.wins.r2, vcov. = vcovCL, cluster = ~FIPS)
se.wins.r3 <- coeftest(mod.wins.r3, vcov. = vcovCL, cluster = ~FIPS)
se.wins.r4 <- coeftest(mod.wins.r4, vcov. = vcovCL, cluster = ~FIPS)

se.winpct.l1 <- coeftest(mod.winpct.l1, vcov. = vcovCL, cluster = ~FIPS)
se.winpct.l2 <- coeftest(mod.winpct.l2, vcov. = vcovCL, cluster = ~FIPS)
se.winpct.l3 <- coeftest(mod.winpct.l3, vcov. = vcovCL, cluster = ~FIPS)
se.winpct.l4 <- coeftest(mod.winpct.l4, vcov. = vcovCL, cluster = ~FIPS)

se.winpct.r1 <- coeftest(mod.winpct.r1, vcov. = vcovCL, cluster = ~FIPS)
se.winpct.r2 <- coeftest(mod.winpct.r2, vcov. = vcovCL, cluster = ~FIPS)
se.winpct.r3 <- coeftest(mod.winpct.r3, vcov. = vcovCL, cluster = ~FIPS)
se.winpct.r4 <- coeftest(mod.winpct.r4, vcov. = vcovCL, cluster = ~FIPS)

se.size.l1 <- coeftest(mod.size.l1, vcov. = vcovCL, cluster = ~FIPS)
se.size.l2 <- coeftest(mod.size.l2, vcov. = vcovCL, cluster = ~FIPS)
se.size.l3 <- coeftest(mod.size.l3, vcov. = vcovCL, cluster = ~FIPS)
se.size.l4 <- coeftest(mod.size.l4, vcov. = vcovCL, cluster = ~FIPS)

se.size.r1 <- coeftest(mod.size.r1, vcov. = vcovCL, cluster = ~FIPS)
se.size.r2 <- coeftest(mod.size.r2, vcov. = vcovCL, cluster = ~FIPS)
se.size.r3 <- coeftest(mod.size.r3, vcov. = vcovCL, cluster = ~FIPS)
se.size.r4 <- coeftest(mod.size.r4, vcov. = vcovCL, cluster = ~FIPS)

se.alt.l1 <- coeftest(mod.alt.l1, vcov. = vcovCL, cluster = ~FIPS)
se.alt.l2 <- coeftest(mod.alt.l2, vcov. = vcovCL, cluster = ~FIPS)
se.alt.l3 <- coeftest(mod.alt.l3, vcov. = vcovCL, cluster = ~FIPS)
se.alt.l4 <- coeftest(mod.alt.l4, vcov. = vcovCL, cluster = ~FIPS)

se.alt.r1 <- coeftest(mod.alt.r1, vcov. = vcovCL, cluster = ~FIPS)
se.alt.r2 <- coeftest(mod.alt.r2, vcov. = vcovCL, cluster = ~FIPS)
se.alt.r3 <- coeftest(mod.alt.r3, vcov. = vcovCL, cluster = ~FIPS)
se.alt.r4 <- coeftest(mod.alt.r4, vcov. = vcovCL, cluster = ~FIPS)

se.travel.l1 <- coeftest(mod.travel.l1, vcov. = vcovCL, cluster = ~FIPS)
se.travel.l2 <- coeftest(mod.travel.l2, vcov. = vcovCL, cluster = ~FIPS)
se.travel.l3 <- coeftest(mod.travel.l3, vcov. = vcovCL, cluster = ~FIPS)
se.travel.l4 <- coeftest(mod.travel.l4, vcov. = vcovCL, cluster = ~FIPS)

se.travel.r1 <- coeftest(mod.travel.r1, vcov. = vcovCL, cluster = ~FIPS)
se.travel.r2 <- coeftest(mod.travel.r2, vcov. = vcovCL, cluster = ~FIPS)
se.travel.r3 <- coeftest(mod.travel.r3, vcov. = vcovCL, cluster = ~FIPS)
se.travel.r4 <- coeftest(mod.travel.r4, vcov. = vcovCL, cluster = ~FIPS)

se.f.l1 <- coeftest(mod.f.l1, vcov. = vcovCL, cluster = ~FIPS)
se.f.l2 <- coeftest(mod.f.l2, vcov. = vcovCL, cluster = ~FIPS)
se.f.l3 <- coeftest(mod.f.l3, vcov. = vcovCL, cluster = ~FIPS)
se.f.l4 <- coeftest(mod.f.l4, vcov. = vcovCL, cluster = ~FIPS)

se.f.r1 <- coeftest(mod.f.r1, vcov. = vcovCL, cluster = ~FIPS)
se.f.r2 <- coeftest(mod.f.r2, vcov. = vcovCL, cluster = ~FIPS)
se.f.r3 <- coeftest(mod.f.r3, vcov. = vcovCL, cluster = ~FIPS)
se.f.r4 <- coeftest(mod.f.r4, vcov. = vcovCL, cluster = ~FIPS)

se.ff.l1 <- coeftest(mod.ff.l1, vcov. = vcovCL, cluster = ~FIPS)
se.ff.l2 <- coeftest(mod.ff.l2, vcov. = vcovCL, cluster = ~FIPS)
se.ff.l3 <- coeftest(mod.ff.l3, vcov. = vcovCL, cluster = ~FIPS)
se.ff.l4 <- coeftest(mod.ff.l4, vcov. = vcovCL, cluster = ~FIPS)

se.ff.r1 <- coeftest(mod.ff.r1, vcov. = vcovCL, cluster = ~FIPS)
se.ff.r2 <- coeftest(mod.ff.r2, vcov. = vcovCL, cluster = ~FIPS)
se.ff.r3 <- coeftest(mod.ff.r3, vcov. = vcovCL, cluster = ~FIPS)
se.ff.r4 <- coeftest(mod.ff.r4, vcov. = vcovCL, cluster = ~FIPS)

# Viewing the results

stargazer(se.races.l1, se.races.l2, se.races.l3, se.races.l4, se.races.r1, se.races.r2, se.races.r3, se.races.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))
stargazer(se.place.l1, se.place.l2, se.place.l3, se.place.l4, se.place.r1, se.place.r2, se.place.r3, se.place.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))
stargazer(se.wins.l1, se.wins.l2, se.wins.l3, se.wins.l4, se.wins.r1, se.wins.r2, se.wins.r3, se.wins.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))
stargazer(se.winpct.l1, se.winpct.l2, se.winpct.l3, se.winpct.l4, se.winpct.r1, se.winpct.r2, se.winpct.r3, se.winpct.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))
stargazer(se.size.l1, se.size.l2, se.size.l3, se.size.l4, se.size.r1, se.size.r2, se.size.r3, se.size.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))
stargazer(se.alt.l1, se.alt.l2, se.alt.l3, se.alt.l4, se.alt.r1, se.alt.r2, se.alt.r3, se.alt.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))
stargazer(se.travel.l1, se.travel.l2, se.travel.l3, se.travel.l4, se.travel.r1, se.travel.r2, se.travel.r3, se.travel.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))
stargazer(se.f.l1, se.f.l2, se.f.l3, se.f.l4, se.f.r1, se.f.r2, se.f.r3, se.f.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))
stargazer(se.ff.l1, se.ff.l2, se.ff.l3, se.ff.l4, se.ff.r1, se.ff.r2, se.ff.r3, se.ff.r4, type = 'text', omit.stat = c('f', 'ser'), omit = c('Runner_ID', 'Year'))

# Saving results

write.csv(stargazer(se.races.l1, se.races.l2, se.races.l3, se.races.l4, se.races.r1, se.races.r2, se.races.r3, se.races.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/race_count.txt', sep = ''))
write.csv(stargazer(se.place.l1, se.place.l2, se.place.l3, se.place.l4, se.place.r1, se.place.r2, se.place.r3, se.place.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/mean_place.txt', sep = ''))
write.csv(stargazer(se.wins.l1, se.wins.l2, se.wins.l3, se.wins.l4, se.wins.r1, se.wins.r2, se.wins.r3, se.wins.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/wins.txt', sep = ''))
write.csv(stargazer(se.winpct.l1, se.winpct.l2, se.winpct.l3, se.winpct.l4, se.winpct.r1, se.winpct.r2, se.winpct.r3, se.winpct.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/win_percentage.txt', sep = ''))
write.csv(stargazer(se.size.l1, se.size.l2, se.size.l3, se.size.l4, se.size.r1, se.size.r2, se.size.r3, se.size.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/mean_race_size.txt', sep = ''))
write.csv(stargazer(se.alt.l1, se.alt.l2, se.alt.l3, se.alt.l4, se.alt.r1, se.alt.r2, se.alt.r3, se.alt.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/mean_race_altitude.txt', sep = ''))
write.csv(stargazer(se.travel.l1, se.travel.l2, se.travel.l3, se.travel.l4, se.travel.r1, se.travel.r2, se.travel.r3, se.travel.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/mean_travel_distance.txt', sep = ''))
write.csv(stargazer(se.f.l1, se.f.l2, se.f.l3, se.f.l4, se.f.r1, se.f.r2, se.f.r3, se.f.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/percent_female_all.txt', sep = ''))
write.csv(stargazer(se.ff.l1, se.ff.l2, se.ff.l3, se.ff.l4, se.ff.r1, se.ff.r2, se.ff.r3, se.ff.r4, omit = c('Runner_ID', 'Year')), paste(direc, 'Results/percent_female_female_only.txt', sep = ''))

