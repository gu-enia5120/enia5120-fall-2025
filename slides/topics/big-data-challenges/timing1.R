library(tibble)
library(readr)
library(ggplot2)
times <- rep(0, 8)
set.seed(9320)
for (i in 1:8) {
  n <- 10^i
  x <- rnorm(n)
  y <- 3 + 2 * x - 5 * (x^2)
  d <- tibble(x, y)
  start <- Sys.time()
  print(ggplot(d, aes(x, y)) +
    geom_point())
  times[i] <- Sys.time() - start
}

out <- tibble(n = 10^(1:8), times = times)
write_csv(out, file = 'timing1.csv')
