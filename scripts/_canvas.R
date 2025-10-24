library(vvcanvas)

api_key = grep('GU_CANVAS', readLines('~/.creds'), value = T) |>
  str_extract("(?<=\").*?(?=\")")
base_url <- "https://georgetown.instructure.com"
canvas <- canvas_authenticate(api_key, base_url)
enia5120 <- get_courses(canvas) |> filter(str_detect(course_code, "ENIA"))
course_id <- enia5120$id
