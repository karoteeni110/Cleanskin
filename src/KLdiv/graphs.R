library(ggplot2)


summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE, conf.interval=.95, .drop=TRUE) {
    library(plyr)
    
    # New version of length which can handle NA's: if na.rm==T, don't count them
    length2 <- function (x, na.rm=FALSE) {
        if (na.rm) sum(!is.na(x))
        else       length(x)
    }
    
    # This does the summary. For each group's data frame, return a vector with
    # N, mean, and sd
    datac <- ddply(data, groupvars, .drop=.drop,
                   .fun = function(xx, col) {
                       c(N    = length2(xx[[col]], na.rm=na.rm),
                         mean = mean   (xx[[col]], na.rm=na.rm),
                         sd   = sd     (xx[[col]], na.rm=na.rm)
                       )
                   },
                   measurevar
                )
    
    # Rename the "mean" column    
    datac <- rename(datac, c("mean" = measurevar))
    
    datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean
    
    # Confidence interval multiplier for standard error
    # Calculate t-statistic for confidence interval: 
    # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
    ciMult <- qt(conf.interval/2 + .5, datac$N-1)
    datac$ci <- datac$se * ciMult
    
    return(datac)
}


# figure 1

abstract <- read.csv('../../data/cs_abstract_kld.txt', header=T)
abstract2 <- summarySE(abstract, measurevar = 'kld', groupvars = c('category'))

pdf("../../results/MYfig1.pdf", h=7, w=6)
ggplot(abstract2, aes(x=reorder(category, kld, FUN=mean), y=kld)) + geom_errorbar(aes(ymin=kld-ci, ymax=kld+ci)) + geom_point() + coord_flip() + ylab('KL divergence (bits)') + xlab('') + scale_y_continuous(limits=c(4,6.5)) + theme_bw()# ,breaks=c(2.0,2.2,2.4,2.6,2.8,3.0)) + theme_bw()
dev.off()

# figure 2

mdat <- read.table('RESULTS_MEAN.txt', header=T)

pdf("MYfig2.pdf", h=3.6, w=5)
ggplot(mdat, aes(cat_kld, p100, label=category)) + geom_point(fill='lightgrey', colour='black', shape=21, size=2) + stat_smooth(method='lm', linetype='dashed', fullrange=T, se=FALSE) + scale_y_continuous(breaks=c(0.2,0.3,0.4,0.5,0.6), limits=c(0.2,0.6)) + ylab('Average Precision@100') + xlab('KL divergence (bits)') + theme_bw()
dev.off()

