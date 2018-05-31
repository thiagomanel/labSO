# library
library(timelineS) 

# Loads the input file.
raw_data <- read.table("timeline-output.ffd", header = T, sep = " ")

png(filename = "timeline_plot.png", width = 1000, height = 600, units = "px",res = 120)
timelineG(df = raw_data, names = "process", phase = "service", start = "start_t", end = "end_t")
dev.off()