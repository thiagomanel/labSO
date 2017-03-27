library("ggplot2")

args = commandArgs(trailingOnly=TRUE)
data = read.csv(args[1], header = TRUE)

summary(data)

p <- ggplot(data, aes(x=nframes, y=nfaults, color=alg))
p <- p + geom_line()
ggsave(p, file=paste(args[1], "png", sep="."))
