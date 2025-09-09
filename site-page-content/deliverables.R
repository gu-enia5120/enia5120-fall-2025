due <- cal_df  |>
  filter(deliverable_due != "")

due_tbl <- due |>
  slice(1:10) |>
  transmute(due = week_of + lubridate::ddays(4), deliverable_due)

## update A3 date (or others)
due_tbl[due_tbl$deliverable_due == "A3 and Dataset(s) proposal for project", "due"] <- as.Date("2024-02-05")

due_tbl |>
  bind_rows(due |> slice(11)  |> transmute(due = week_of, deliverable_due)) |>
  mutate(due = format(due, "%a, %b %d")) |>
  kbl(escape = F, col.names = c("Due Date", "Deliverable"))
