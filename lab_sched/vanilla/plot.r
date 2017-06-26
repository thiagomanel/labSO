library(ggplot2)
args = commandArgs(trailingOnly=TRUE)

data_path = args[1]

#mode,pid,sample,start,end
data = read.table(sep = " ", data_path, header = T)
summary(data)

data$elapsed = data$end - data$start
p = ggplot(data=data, aes(x=factor(mode), y=elapsed, color=factor(mode), group=factor(mode))) + geom_boxplot()
ggsave("elapsed.png", p)
