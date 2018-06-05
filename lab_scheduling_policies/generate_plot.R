# library
library(timelineS)

# Generate timeline plot.
# This plot shows the progress of each process over the time.
# The history of a process is divided in two moments: expected time and extra time.
# The expected time is the time that the process needs to terminate its job.
# The extra time is the additional time that the processes needed to terminate its job.

raw_data <- read.table("timeline-output.ffd", header = T, sep = " ")

png(filename = "timeline_plot.png", width = 1000, height = 600, units = "px",res = 120)
timelineG(df = raw_data, names = "process", phase = "service", start = "start_t", end = "end_t")
dev.off()

# Generate boxplot.
# BoxPlot about the extra time needed by the processes.

extra_time_data = read.csv("extra-time-output.ffd", header = F)

png(filename = "extra_time_plot.png", width = 600, height = 600, units = "px",res = 120)
boxplot(x = extra_time_data, ylab = "Extra processing time")
dev.off()
