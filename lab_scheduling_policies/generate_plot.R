# library
library(timelineS) 

# Loads the input file.
raw_data <- read.table("timeline-output.ffd", header = T, sep = " ")

timelineG(df = raw_data, names = "process", phase = "service", start = "start_t", end = "end_t")


