library(tidyverse)
#library(kableExtra)
#library(gt)
library(googlesheets4)

cal_sheet <- read_sheet("https://docs.google.com/spreadsheets/d/1Q1JaD24zK_jKIayO_DUMbwfaop_7lmI-TpnRqUvEjjw/edit?usp=sharing",
  sheet = "Weekly Plan"
) # Link to Spring 2025 sheet

cal_cols <- c("session_number", "monday", "session_name", "schedule_notes")
deliverable_cols <- c("date_due", "deliverable_due")

cal_df <-
  cal_sheet |>
  select(all_of(cal_cols)) |>
  mutate(
    session_number = as.character(session_number),
    monday = format(monday, "%b %d"),
    across(c("session_name", "schedule_notes"), ~ replace_na(.x, ""))
  )


del_df <-
  cal_sheet |>
  select(all_of(deliverable_cols)) |>
  filter(!is.na(deliverable_due)) |>
  mutate(date_due = format(date_due, "%b %d"))


# cal_df|>
#    select(week_of, week, lecture_topic, assignment_drop, schedule_notes) |>
#    mutate(week_of = format(week_of, "%b %d")) |>
#    kbl(escape = F,
# col.names = c("Week beginning Monday", "Session", "Topics", "Assignment Posted", "Schedule Notes"))
