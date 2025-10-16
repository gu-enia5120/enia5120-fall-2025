# -------------------------------------------------------------
# Script Name: sample_usa.R
# Description: Sampling distributions from US population data
# Author: Abhijit Dasgupta
# Last Updated: 2025-10-14 19:40
# -------------------------------------------------------------

# setup ----

set.seed(1000)
base::load('slides/data/pop_samples.rda')
library(usdata)
library(tidyverse)
library(tidymodels)
library(ggExtra)
theme_set(theme_minimal())

D <- tibble(
  age = mean(pop_age$age, na.rm = TRUE),
  race = mean(pop_race$race == "White", na.rm = TRUE)
)

sim_samples <- function(n, reps) {
  d1 <- rep_slice_sample(pop_age, n = n, reps = reps) |>
    group_by(replicate) |>
    summarise(age = mean(age, na.rm = TRUE)) |>
    ungroup()
  d2 <- rep_slice_sample(pop_race, n = n, reps = reps) |>
    group_by(replicate) |>
    summarise(race = mean(race == "White", na.rm = TRUE)) |>
    ungroup()
  d <- d1 |> inner_join(d2, by = "replicate")
  return(d)
}

# Visualization -------------------------------------------------------------

set.seed(1000)
p <- sim_samples(n = 1000, reps = 10) |>
  ggplot(aes(x = age, y = race)) +
  geom_point(alpha = 0.1, color = 'white') +
  stat_density_2d(
    aes(fill = after_stat(level)),
    geom = "polygon",
    color = "black",
    alpha = 0.5,
    show.legend = F
  ) +
  geom_point(data = D, color = 'red', size = 3) +
  geom_vline(
    data = D,
    aes(xintercept = age),
    color = 'red',
    linetype = "dashed"
  ) +
  geom_hline(
    data = D,
    aes(yintercept = race),
    color = 'red',
    linetype = "dashed"
  ) +
  scale_x_continuous('Age', limits = c(30, 45)) +
  scale_y_continuous(
    'Percent White',
    limits = c(0.6, 0.9),
    labels = scales::percent_format(accuracy = 1)
  )
ggMarginal(p, type = "histogram", fill = "lightblue", color = "black")


dc_pop <- usdata::pop_age_2019 |>
  filter(state == 'DC') |>
  uncount(population) |>
  mutate(age = as.numeric(age)) |>
  drop_na(age) |>
  select(state, age)
saveRDS(dc_pop, here::here('slides/data/dc_pop.rds'))
