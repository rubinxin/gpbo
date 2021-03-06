#!/usr/bin/env python2
#encoding: UTF-8

# Comparing var fid PES to fixed PES and EI on branin for various fixed step sizes. cost/noise fixed at (1e-6)/s)**0.2


import scipy as sp
from matplotlib import pyplot as plt
import gpbo.core.GPdc
import gpbo.core.OPTutils
import gpbo.core.search
import os
import pickle


d=2
lb = sp.array([[-1.]*d])
ub = sp.array([[1.]*d])
pwr = 0.2
cfn = lambda s:((1e-6)/s)**pwr
ojf = gpbo.core.OPTutils.gencamel(cfn=cfn)
camelmin = -1.031628453489877
kindex = gpbo.core.GPdc.MAT52
prior = sp.array([0.]+[-1.]*d)
sprior = sp.array([1.]*(d+1))
kernel = [kindex,prior,sprior]
nreps = 8
bd = 15
slist = [1e-4,1e-6,1e-8]
f,a = plt.subplots(3)

for s in slist:
    
    names = ["../cache/camelnoise/EIMLE_"+str(int(100*sp.log10(s)))+"_"+str(pwr)+"_"+str(i)+".p" for i in xrange(nreps)]
    results = gpbo.core.search.multiMLEFS(ojf, lb, ub, kernel, s, bd, names)
    yr = [r[11].flatten() for r in results]
    C = results[0][5]
    
    names = ["../cache/camelnoise/PESFS_"+str(int(100*sp.log10(s)))+"_"+str(pwr)+"_"+str(i)+".p" for i in xrange(nreps)]
    results = gpbo.core.search.multiPESFS(ojf, lb, ub, kernel, s, bd, names)
    zr = [r[11].flatten() for r in results]
    C = results[0][5]
    
        
    Z = sp.vstack(yr)-camelmin
    m = sp.mean(sp.log10(Z),axis=0)
    v = sp.var(sp.log10(Z),axis=0)
    
    sq = sp.sqrt(v)
    
    a[2].fill_between(sp.array([sum(C[:j]) for j in xrange(len(C))]),(m-sq).flatten(),(m+sq).flatten(),facecolor='lightblue',edgecolor='lightblue',alpha=0.5)
    a[2].plot([sum(C[:j]) for j in xrange(len(C))],m.flatten(),'x-')
    
    
    Z = sp.vstack(zr)-camelmin
    m = sp.mean(sp.log10(Z),axis=0)
    v = sp.var(sp.log10(Z),axis=0)
    sq = sp.sqrt(v)
    a[2].fill_between(sp.array([sum(C[:j]) for j in xrange(len(C))]),(m-sq).flatten(),(m+sq).flatten(),facecolor='lightgreen',edgecolor='lightgreen',alpha=0.5)
    a[2].plot([sum(C[:j]) for j in xrange(len(C))],m.flatten(),'.-')
    
    
    
    
    f.savefig("tmp.png")
    

s=1e-1

#for i in xrange(nreps):
#    fname = "../cache/rosennoise/PESVS_"+str(int(100*sp.log10(s)))+"_"+str(pwr)+"_"+str(i)+".p"
#    [X,Y,S,D,R,C2,T,Tr,Ymin,Xmin,Yreg, Rreg] = search.PESVS(ojf,lb,ub,kernel,s,ba,lambda x,s:cfn(s),-9,-1,fname)
names = ["../cache/braninnoise/PESVS_"+str(int(100*sp.log10(s)))+"_"+str(pwr)+"_"+str(i)+".p" for i in xrange(nreps)]
results = gpbo.core.search.multiPESVS(ojf, lb, ub, kernel, s, bd, lambda x, s:cfn(s), -9, -1, names)
Rz = [sp.log10(sp.array(r[11])-camelmin).flatten() for r in results]
Cz = [[sum(r[5][:j]) for j in xrange(len(r[5]))] for r in results]
#for i in xrange(nreps):
#    a[2].plot(Cz[i],Rz[i].flatten(),'rx-')
[a[1].plot(r[5],'r') for r in results]
    #a[2].plot(sp.array([sum(C2[:j]) for j in xrange(len(C2))]).flatten(),(sp.log(Yreg)).flatten(),'ro-')

for i in xrange(nreps):
    a[2].plot(Cz[i],Rz[i],'r')



sx = sp.logspace(0,-8,100)
cx = map(cfn,sx)
a[0].loglog(sx,cx)
f.savefig("../figs/braninnoise.png")
plt.show()
