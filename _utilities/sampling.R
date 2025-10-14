library(usdata)
library(tidyverse)
library(rsample)

pop_age <- pop_age_2019 |> mutate(population_down = round(population/1000)) |> 
  uncount(population_down) |> 
  select(state, age) |> 
  group_by(state) |> 
  mutate(id = row_number(),
age = as.numeric(age)) |> 
  ungroup()

pop_race <- pop_race_2019 |> mutate(population_down = round(population/1000)) |> 
  uncount(population_down) |> 
  select(state, race, hispanic) |> 
  group_by(state) |> 
  mutate(id = row_number()) |> 
  ungroup()

save(pop_age, pop_race, file = here::here('slides','data','pop_samples.rda'))
