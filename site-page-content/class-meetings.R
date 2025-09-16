library(tidyverse)
#library(kableExtra)
#library(gt)
library(googlesheets4)
cal_sheet <- read_sheet(
  "https://docs.google.com/spreadsheets/d/1lB7i-PtFJXRGZyiPryy-DAUB7kKPi7RuUZNeP-8x4YY/edit?usp=sharing",
  sheet = "Calendar"
)

cal_cols <- c(
  "Week",
  "Date",
  "Learning topic",
  "Computational/Data topic",
  "Assignment provided",
  "Assignment due",
  "Project",
  "Project due dates"
)
# deliverable_cols <- c("date_due", "deliverable_due")

cal_df <-
  cal_sheet |>
  select(all_of(cal_cols)) |>
  janitor::clean_names() |>
  mutate(across(where(is.POSIXct), \(x) format(x, "%b %d"))) |>
  mutate(across(where(is.character), \(x) replace_na(x, "")))

#del_df <-
#  cal_sheet |>
#  select(all_of(deliverable_cols)) |>
#  filter(!is.na(deliverable_due)) |>
#  mutate(date_due = format(date_due, "%b %d"))

# cal_df|>
#    select(week_of, week, lecture_topic, assignment_drop, schedule_notes) |>
#    mutate(week_of = format(week_of, "%b %d")) |>
#    kbl(escape = F,
# col.names = c("Week beginning Monday", "Session", "Topics", "Assignment Posted", "Schedule Notes"))
