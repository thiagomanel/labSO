library("ggplot2")

args = commandArgs(trailingOnly=TRUE)
data = read.csv(args[1], header = TRUE)

summary(data)

#tlbhits,nrefs,tlbsize,alg
p <- ggplot(data, aes(x=tlbsize, y=tlbhits/nrefs, color=alg))
p <- p + geom_line()
ggsave(p, file=paste(args[1], "png", sep="."))
