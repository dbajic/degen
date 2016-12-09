#lo sum exp function

#rm(list=ls())

library(akima)
library('ggplot2')
library(matrixStats)

log.sum.exp<- function(x) {
  return(logSumExp(x))
}

plotConvexHull=function(samples,t.obs){
  plot(samples,xlab = "edges",ylab = "triangles")
  hpts <- chull(samples)
  hpts <- c(hpts, hpts[1])
  lines(samples[hpts, ],col="blue")
  points(t.obs[1],t.obs[2],cex=1,col="red")  
}


innerProd = function(theta,t){
  sum(t*theta)
}

l.hat = function(theta,t.obs){
  #innerProdThetaSamples = apply(X=samples,1,FUN=innerProd,theta=theta)
  #likelihood = innerProd(theta,t.obs) - log.sum.exp(innerProdThetaSamples)
  
  offSamples = sweep(samples,2,t.obs)
  theta.offSamples = apply(X=offSamples,1,FUN=innerProd,theta=theta)
  likelihood = -logSumExp(theta.offSamples)
  return(-likelihood)
}

l.hat2 = function(theta,t.obs){
  Delta = samples - t.obs;
  innerProdThetaSamples = apply(X=Delta,1,FUN=innerProd,theta=theta)
  likelihood = - log.sum.exp(innerProdThetaSamples)
  return(-likelihood)
}

gr = function(theta,t.obs){
  
  nstats = length(theta);
  grad = rep(0,nstats);
  
  innerSamples = apply(X=samples,1,FUN=innerProd,theta=theta) 
  log.c.theta = log.sum.exp(innerSamples)
  
  for(j in 1:nstats){ 
    nonZero = which(samples[,j]!=0)
    log.mu.ti.theta = log.sum.exp(innerSamples[nonZero]+log(samples[nonZero,j]))
    grad[j] = t.obs[j] - exp(log.mu.ti.theta - log.c.theta)  
  }
  
  #take minus sign since we need the gradient for the negative log likelihood.
  grad = -grad
  
  return(grad)
}

gr2 = function(theta,t.obs){

  Delta = sweep(samples,2,t.obs)#samples - t.obs;
  
  innerSamplesDelta = apply(X=Delta,1,FUN=innerProd,theta=theta) 
  logWts = innerSamplesDelta - log.sum.exp(innerSamplesDelta);
  
  gradSamples  = exp(logWts)*Delta
  grad = apply(gradSamples,2,sum)
  # Take minus sign since we need the gradient for the negative log likelihood
  grad = -grad
  
  return(grad)
}

hessian = function(theta,t.obs){
  nstats = length(theta)
  hessian = matrix(0,nstats,nstats)
  
  innerSamples = apply(X=samples,1,FUN=innerProd,theta=theta) 
  log.c.theta = log.sum.exp(innerSamples)
  
  # Compute the diagonal elements
  
  for(j in 1:nstats){ 
    nonZero = which(samples[,j]!=0)
    log.mu.ti.theta = log.sum.exp(innerSamples[nonZero]+log(samples[nonZero,j]))
    log.mu.tisq.theta = log.sum.exp(innerSamples[nonZero]+2*log(samples[nonZero,j]))
    
    hessian[j,j] = -exp(log.mu.tisq.theta - log.c.theta)+
      exp(2*(log.mu.ti.theta - log.c.theta))  
  }
  
  # Compute the off diagonal elements:
  for(j in 1:nstats){
    for(k in 1:j){
      if(j != k){
        nonZerok = which(samples[,k]!=0)
        nonZeroj = which(samples[,j]!=0)
        
        
        log.mu.tj.theta = log.sum.exp(innerSamples[nonZero]+log(samples[nonZero,j]))
        log.mu.tk.theta = log.sum.exp(innerSamples[nonZero]+log(samples[nonZero,k]))
        log.mu.tjtk.theta = log.sum.exp(innerSamples[nonZero]+log(samples[nonZero,j]) + log(samples[nonZero,k]))
        
        hessian[j,k] = -exp(log.mu.tjtk.theta - log.c.theta)+
          exp(log.mu.tj.theta + log.mu.tk.theta - 2*log.c.theta);
        hessian[k,j] = hessian[j,k];
      }
    }
  }
  hessian = -hessian;
  return(hessian)
  
}

 estimateMCMLE=function(samples,t.obs,theta0){
   B = nrow(samples);
   result = optim(runif(2,-2,2),l.hat,gr = gr,t.obs=t.obs,method="BFGS",hessian=TRUE);
   theta.MCMLE = result$par;
   
   # Computing the std errors and confidence intervals
   
   # We are minimizing the negatyive log likelihood, 
   # So the hessian of the negative log likelihood is the Fisher Info
   
   obsFisherInfo<-result$hessian
   varCovar = solve(obsFisherInfo)
   estSigma<-sqrt(diag(varCovar))
   upper<-result$par+1.96*estSigma
   lower<-result$par-1.96*estSigma
   interval<-data.frame(value=result$par, upper=upper, lower=lower)
   
   innerProdTheta = apply(X=samples,1,FUN=innerProd,theta=theta.MCMLE)
   logWts = innerProdTheta - log.sum.exp(innerProdTheta)
   gradSamples1 =  samples*exp(logWts)
   t.obs - apply(gradSamples1,2,sum)
   gradSamples = sweep(gradSamples1,2,t.obs/B) #t.obs/B - gradSamples1
   apply(gradSamples,2,sum)
   mcmcstdErr = sqrt(diag(solve(obsFisherInfo)%*%var(gradSamples)%*%solve(obsFisherInfo))/B)
   
   
   cbind(MCMLE=theta.MCMLE,stddev = estSigma,MCError = mcmcstdErr)
 }

t.obs = c(41,18)
samples = read.csv("n18k3samples.csv", header=FALSE)

B = nrow(samples)
mle = estimateMCMLE(samples,t.obs,runif(2,-2,2))


# Some degeneracy plots

 estLogc.theta = function(theta,samples){
   innerProdThetaSamples = apply(X=samples,1,FUN=innerProd,theta=theta)
   log.sum.exp(innerProdThetaSamples)
 }
 
 
 estlogProb = function(theta,stats,logc.theta){
   if(is.na(logc.theta)){logc.theta = estLogc.theta(theta,samples)}
   sum(theta*stats) - logc.theta
 }

# Weight given by MLE to points
theta.mle = mle[,1]
logc.theta = estLogc.theta(theta.mle,samples);
wtSamples = apply(samples,1,FUN = estlogProb,theta = theta.mle,logc.theta=logc.theta)

contour(interp(samples[,1], samples[,2], wtSamples,duplicate = "mean"))
image(interp(samples[,1], samples[,2], wtSamples,duplicate = "mean"))

# Plot the prob for empty graph
logProbs = apply(thetaData,1,estProb,stats=c(0,0))


# Entropy plots
# Compute the counting measure

counts = table(samples)
xx = as.data.frame(ftable(counts,row.vars = 1:2))
statsList = cbind(as.numeric(levels(xx[,1]))[xx[,1]], as.numeric(levels(xx[,2]))[xx[,2]])
freq = xx[,3]

estEntropy = function(thetaval,statsList1=statsList,freq1 = freq,samples1=samples){
  inner.theta.t = apply(statsList1,1,function(x){sum(x*thetaval)})
  logc.theta = estLogc.theta(thetaval,samples1);
  ans = logc.theta - (sum(exp(inner.theta.t)*inner.theta.t*freq1)/exp(logc.theta))
  c.theta = sum(exp(inner.theta.t)*freq1)
  ans = log(c.theta) - (sum(exp(inner.theta.t)*inner.theta.t*freq1)/c.theta)  
 if(is.nan(c.theta) || is.nan(ans)){
    logc.theta = estLogc.theta(thetaval,samples1);
    ans = logc.theta - sum(freq1*inner.theta.t*exp(inner.theta.t - logc.theta))
  }
  return(ans)
}


 theta1 = seq(-10,25,0.5) #edgeparam
 theta2 = seq(-25,10,0.5) #triangle
 
 thetaData = as.matrix(expand.grid(theta1,theta2))
 entropyGrid = rep(0,nrow(thetaData))
 for(i in 1:nrow(thetaData)){
   entropyGrid[i] = estEntropy(thetaData[i,])
   print(i)
 }
 
 entropyGrid = apply(thetaData,1,estEntropy)
 thetaData[which(is.na(entropyGrid)),]
 
 contour(interp(thetaData[,1], thetaData[,2], entropyGrid,duplicate = "mean"))
 image(interp(thetaData[,1], thetaData[,2], entropyGrid,duplicate = "mean"))
 
 condata = as.data.frame(cbind(thetaData,entropyGrid))
 colnames(condata) = c("Edge", "Triangle", "Entropy")
 
 
 v <- ggplot(condata, aes(x=Edge,y=Triangle,z=Entropy))
 v + geom_contour()
 v + geom_contour(aes(color = ..level..))+scale_fill_gradient(low="blue",high="red") 
 v + geom_tile(aes(fill=Entropy))  + scale_fill_gradient(low="blue", high="red")+theme_bw()
 
 pdf("entropyPlotK=3.pdf")
 p = v + geom_tile(aes(fill=Entropy))+
   scale_fill_gradientn(colours = rainbow(3)[c(3,2,1)])+theme_bw()
   scale_fill_gradientn(colours = c("blue","yellow","red"))+
   theme_bw(base_size = 20)+theme(aspect.ratio=1)+
   xlab("Edge Parameter") +
   ylab("Triangle Parameter")
 plot(p)
 dev.off()

