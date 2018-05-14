import numpy as np
import pylab as plt
import datetime as DT
import pandas as pd
import holidays
import statsmodels.api as sm
import patsy
from IPython.core.debugger import Tracer; debug_here = Tracer()

plt.close('all')


print('Loading data for ARMA analysis')
all_data = pd.read_pickle('data/all_data.pickle')

#Observations need to be in rows
#Variables need to be in columns
#See: https://groups.google.com/forum/#!topic/pystatsmodels/amZ4oaGVsUk

#TODO: Figure out exogeneous variables. Why are there 4 columns in xt?...
#   Oh! I know why. You have to select the hour by row and column for xt.
#   This is because as its programmed, the percentile outliers have to be calculated
#   separately for each hour. I should just be able to collapse this into one column...

hour = 0

endog = all_data.loc[:,'kwh']
exog =  all_data.loc[:,['xo1','xo2','xt1','xt2','xt3']]


order = list(range(2,7))
bics = []
for i in range(len(order)):
    model = sm.tsa.ARMA(endog=endog, order=(order[i],0), exog=exog, dates=None, freq=None, missing='none')
    results = model.fit()
    bics.append(results.bic)
    print(i,bics[-1])

plt.figure()
plt.plot(order,bics,'o')

plt.figure()
plt.plot(all_data['kwh'],'-b',linewidth=2,alpha=0.5)
plt.plot(results.fittedvalues,'-r')

plt.show()

a=np.sum(all_data['kwh'])
b=np.sum(results.fittedvalues)

#TODO:
#   -Get some metrics to see how well models compares (compare integrals)
#   -Figure out how to choose model order
#   -Put code into modules
#   -Look at some other accounts.. what to do about working vs. retired?

#results = model.fit()
#print(results.summary())
#
#plt.plot(all_data['kwh'],'-b',linewidth=2)
#plt.plot(results.fittedvalues.shift(-1),'-r')
#plt.show()


