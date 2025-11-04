# -------------------------------------------------------------
# Script Name: coin-tossing.R
# Description: Coin tossing simulations for inference
# Author: Abhijit Dasgupta
# Last Updated: 2025-10-14 19:44
# -------------------------------------------------------------

library(tidyverse)
library(tidymodels)
theme_set(theme_minimal())
load('slides/data/binomial_params.rda')

set.seed(1000)
n_tosses <- 10
tosses <- sample(
  c('H', 'T'),
  size = n_tosses,
  replace = TRUE,
  prob = c(p2, 1 - p2)
)
mean(tosses == "H")

many_tosses <- replicate(
  1000,
  sample(c('H', 'T'), size = n_tosses, replace = TRUE, prob = c(p2, 1 - p2))
)
tibble(heads = apply(many_tosses, 2, function(x) mean(x == "H"))) |>
  ggplot(aes(heads)) +
  geom_histogram(color = 'black', fill = 'lightblue') +
  scale_x_continuous(
    "Percent heads",
    limits = c(0, 1),
    labels = scales::label_percent()
  )
