#' Name Unnamed R Code Chunks in Quarto Documents
#'
#' This function automatically adds labels to unnamed R code chunks in a Quarto
#' (.qmd) file. It identifies chunks that lack a `#| label:` directive and assigns
#' sequential labels based on the file's base name. The function also checks for
#' and reports any duplicate labels that remain after processing.
#'
#' @param f Character string. The file path to a .qmd (Quarto markdown) file.
#'   The file must exist and have a .qmd extension.
#'
#' @return Invisibly returns `NULL`. The function modifies the input file in place
#'   by writing the updated content back to the original file.
#'
#' @details
#' The function performs the following steps:
#' \enumerate{
#'   \item Validates that the file exists and has a .qmd extension
#'   \item Reads the entire file into memory
#'   \item Identifies all R code chunks marked with \code{```\{r\}}
#'   \item For each chunk without a \code{#| label:} directive, adds a label
#'         in the format \code{filename-NN} where NN is a zero-padded counter
#'   \item Renumbers all labels with the file slug to ensure sequential ordering
#'   \item Checks for duplicate labels and throws an error if any are found
#'   \item Writes the modified content back to the file
#' }
#'
#' The function requires the \code{stringr} and \code{glue} packages to be installed.
#'
#' @import stringr
#' @export
#'
#' @examples
#' \dontrun{
#' # Add labels to unnamed chunks in a slide deck
#' name_chunks("slides/week-06.qmd")
#'
#' # Process multiple files
#' qmd_files <- list.files("slides", pattern = "\\.qmd$", full.names = TRUE)
#' lapply(qmd_files, name_chunks)
#' }
name_chunks <- function(f) {
  require(stringr)
  if (!file.exists(f)) {
    stop("File does not exist")
  }
  if (!str_detect(f, "\\.qmd$")) {
    stop("File is not a .qmd file")
  }

  x <- readLines(f)
  slug <- tools::file_path_sans_ext(
    basename(f)
  )
  nchunks <- sum(str_detect(x, "\\`\\`\\`\\{r\\}"))
  ctr <- 0
  start <- 1
  # for (ii in 1:nchunks) {
  while (start < length(x)) {
    ind <- min(grep("\\`\\`\\`\\{r\\}", x[start:length(x)])) + start - 1
    if (is.infinite(ind) | ind >= length(x)) {
      break
    }
    meta <- character()
    for (i in (ind + 1):length(x)) {
      if (!str_detect(x[i], "^\\#\\|")) {
        break
      }
      meta <- c(meta, x[i])
    }
    if (!any(str_detect(meta, "label"))) {
      ctr <- ctr + 1
      labelstr <- as.character(glue::glue(
        "#| label: {slug}-{str_pad(ctr, 2, side = 'left', pad='0')}"
      ))
      x <- append(x, labelstr, after = ind)
    }
    start <- ind + 1
  }
  # Fix duplicate label issue
  inds <- grep(paste0('label: ', slug), x)
  n <- length(inds)
  labs = as.character(glue::glue(
    '#| label: {slug}-{str_pad(1:n, 2, side = "left", pad="0")}'
  ))
  x[inds] <- labs

  # Check for further duplicate label
  labs <- grep('\\#\\| label:', x, value = TRUE)
  if (any(duplicated(labs))) {
    warning('There are still duplicate labels in the file after processing.')
    print(glue::glue(
      'Duplicated labels: {paste(unique(str_remove(labs[duplicated(labs)], "#\\\\| label: ")), collapse = ", ")}'
    ))
    stop('Please check the file and fix the labels manually.')
  }
  writeLines(x, f)
}
