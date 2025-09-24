airports <- read.csv("data/airport-locations.tsv", sep = "\t", stringsAsFactors = FALSE)
source("latlong2state.R")
airports$state <- latlong2state(airports[, c("longitude", "latitude")])
airports_contig <- na.omit(airports)
# Projection
library(mapproj)
airports_projected <- mapproject(airports_contig$longitude, airports_contig$latitude, "albers", param = c(39, 45))
par(mar = c(0, 0, 0, 0))
plot(airports_projected, asp = 1, type = "n", bty = "n", xlab = "", ylab = "", axes = FALSE)
points(airports_projected, pch = 20, cex = 0.1, col = "red")

library(deldir)
par(mar = c(0, 0, 0, 0))
plot(airports_projected, asp = 1, type = "n", bty = "n", xlab = "", ylab = "", axes = FALSE)
points(airports_projected, pch = 20, cex = 0.1, col = "red")
vtess <- deldir(airports_projected$x, airports_projected$y)
plot(vtess, wlines = "tess", wpoints = "none", number = FALSE, add = TRUE, lty = 1)

library(tidyverse)
diamonds <- diamonds %>%
    mutate(across(c(cut, color, clarity), ~ factor(., ordered = F)))
model <- lm(log(price) ~ log(carat) + cut + color + clarity + depth,
    data = diamonds
)
library(gtsummary)
theme_gtsummary_compact()
gtsummary::tbl_regression(model) %>% as_gt()

mod_tidy <- broom::tidy(model)
mod_aug <- broom::augment(model)

library(extrafont)
theme_set(theme_classic() +
    theme(
        axis.title = element_text(size = 18, family = "Avenir"),
        axis.text = element_text(size = 16, family = "Avenir"),
        title = element_text(size = 24, family = "Avenir"),
        plot.margin = unit(c(0.05, 0.05, 0.05, 0.05), "npc")
    ))

library(coefplot)
coefplot::coefplot.lm(model) +
    labs(x = "Coefficient", y = "Predictor")


set.seed(2405)
diamonds2 <- slice_sample(diamonds, prop = 0.01) #<<
model2 <- lm(log(price) ~ log(carat) + cut + color + clarity + depth,
    data = diamonds2
)
model2_tidy <- broom::tidy(model2)
ggplot(
    model2_tidy %>% filter(term != "(Intercept)"),
    aes(
        x = term, y = estimate,
        ymin = estimate - 2 * std.error,
        ymax = estimate + 2 * std.error
    )
) +
    geom_pointrange(color = "blue") +
    labs(
        x = "Predictor", y = "Coefficient",
        title = "Coefficient Plot"
    ) +
    geom_hline(yintercept = 0, linetype = 2) +
    coord_flip()

ggplot(mod_aug, aes(x = seq_along(.cooksd), .cooksd)) +
    geom_col(fill = "red") +
    labs(x = "Obs number", y = "Cook's distance")
