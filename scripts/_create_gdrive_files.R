library(googledrive)
library(tidyverse) |> suppressMessages()
drive_auth(email = "ad1704@georgetown.edu")

for (i in 3:14) {
  drive_create(paste('Week', i), type = 'document', path = "ENIA 5120")
}


notes <- drive_ls("ENIA 5120", type = 'document')
bl = drive_share(notes$id, role = 'writer', type = 'anyone') |>
  mutate(links = drive_link(id))
saveRDS(bl, here::here('_artifacts', 'gdrive_shared_notes.rds'))
