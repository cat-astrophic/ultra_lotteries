# This script creates a stacked bar chart for the paper

# Loading library

library(ggplot2)

# Data prep

year <- c(rep(2011, 9), rep(2012, 9), rep(2013, 9), rep(2014, 9), rep(2015, 9), rep(2016, 9), rep(2017, 9), 
          rep(2018, 9), rep(2019, 9), rep(2020, 9), rep(2021, 9), rep(2022, 9), rep(2023, 9), rep(2024, 9))

tix <- c(1286, 500, 0, 0, 0, 0, 0, 0, 0, 
         1221, 461, 258, 0, 0, 0, 0, 0, 0, 
         1486, 480, 207, 122, 0, 0, 0, 0, 0, 
         1727, 561, 258, 106, 52, 0, 0, 0, 0, 
         1427, 641, 281, 136, 57, 24, 0, 0, 0, 
         2233, 639, 377, 171, 71, 14, 5, 0, 0, 
         2427, 1023, 397, 256, 112, 31, 2, 0, 0, 
         2658, 1060, 668, 283, 161, 71, 8, 0, 0, 
         3113, 1281, 697, 455, 191, 95, 30, 0, 0, 
         3250, 1447, 914, 549, 315, 126, 54, 9, 0, 
         0, 0, 0, 0, 0, 0, 0, 0, 0, 
         3318, 1063, 722, 514, 328, 186, 59, 18, 0, 
         3560, 1578, 731, 525, 374, 232, 127, 37, 5, 
         4434, 2216, 1231, 606, 420, 256, 147, 70, 8)

t <- rep(seq(1, 9, 1), 14)

df <- as.data.frame(cbind(year, tix, t))
colnames(df) <- c('Year', 'Entrants', 'N')
df$t <- factor(df$N, levels = c(9, 8, 7, 6, 5, 4, 3, 2, 1))

# Making the plot

ggplot(df, aes(fill = t, y = Entrants, x = Year)) +
  coord_flip() +
  theme_bw() +
  geom_bar(aes(x = Year, y = Entrants, col = t), position = 'stack', stat = 'identity') +
  scale_x_continuous(breaks = seq(2011, 2024, 1), labels = seq(2011, 2024, 1)) +
  scale_y_continuous(breaks = seq(0, 10000, 1000), labels = seq(0, 10000, 1000)) +
  ggtitle('WSER Lottery Entrants History') +
  theme(plot.title = element_text(hjust = 0.5), legend.title.align = 0.19666) +
  annotate('text', x = 2021, y = 2666, label = 'No lottery because of 2020 race cancellation')

