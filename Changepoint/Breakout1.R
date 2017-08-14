library(BreakoutDetection)

ffile <- read.csv("for_exp.csv",stringsAsFactors = FALSE)
jobs <- unique(ffile$JOB_NAME)
r <- ffile[ffile$JOB_NAME==jobs[44],]
plot(as.ts(r$Scaled))
res = breakout(r$Scaled,method='multi', beta=.00018, degree=1, plot=TRUE)
res$plot
print(res$plot)


#library(ecp)
#library(Rcpp)
#ediv = e.divisive(as.matrix(r$MSU_CPU), min.size=64, R=199, alpha=1)
#plot(as.ts(r$MSU_CPU))
#abline(v=ediv$estimates,col="red")