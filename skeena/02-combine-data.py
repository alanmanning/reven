import numpy as np
import pylab as plt
import datetime as DT
import holidays
import pandas as pd
import scipy.signal as scisig
from IPython.core.debugger import Tracer; debug_here = Tracer()

plt.close('all')

"""
weather station location: http://tools.pacificclimate.org/dataportal/pcds/map/
-Can get station ID from here. Each station has a "climate ID"..

Guernsey: 48° 24' 48.3012", -123° 19' 30.8994"

-Don't forget about daylight savings time

-ToDo: figure out how to combine the consumption and weather data in one data set,
where missing values are import as N/A's
"""


#TODO: -verify these times
#-correct the weather and add or subtract appropriate hours
#-BC Hydro data already has daylight times added or subtracted (they do this at 3 AM)


ds_times = [
        [pd.Timestamp('2010-03-14 02:00:00'),pd.Timestamp('2010-11-07 02:00:00')],
        [pd.Timestamp('2011-03-13 02:00:00'),pd.Timestamp('2011-11-06 02:00:00')],
        [pd.Timestamp('2012-03-11 02:00:00'),pd.Timestamp('2012-11-04 02:00:00')],
        [pd.Timestamp('2013-03-10 02:00:00'),pd.Timestamp('2013-11-03 02:00:00')],
        [pd.Timestamp('2014-03-09 02:00:00'),pd.Timestamp('2014-11-02 02:00:00')],
        [pd.Timestamp('2015-03-08 02:00:00'),pd.Timestamp('2015-11-01 02:00:00')],
        [pd.Timestamp('2016-03-13 02:00:00'),pd.Timestamp('2016-11-06 02:00:00')],
        [pd.Timestamp('2017-03-12 02:00:00'),pd.Timestamp('2017-11-05 02:00:00')],
        [pd.Timestamp('2018-03-11 02:00:00'),pd.Timestamp('2018-11-04 02:00:00')],
        [pd.Timestamp('2019-03-10 02:00:00'),pd.Timestamp('2019-11-03 02:00:00')]]

def bch_get_kwh(s):
    s = s.replace('"','')
    if s == 'N/A':
        return np.nan
    else:
        try:
            r = float(s)
        except:
            r = np.nan
        return r

def bch_get_date(s):
    s = s.replace('"','')
    return DT.datetime.strptime(s,'%Y-%m-%d %H:%M')

def ec_get_date(s):
    s = s.replace('"','')
    return DT.datetime.strptime(s,'%Y-%m-%d %H:%M')

def ec_get_vals(s):
    s = s.replace('"','')
    try:
        r = float(s)
    except:
        r = np.nan
    return r

print('Starting script')

fname = 'consumption-data/since-2014-05.csv'
power = pd.read_csv(fname,usecols=(2,3),converters = {2:bch_get_date,3:bch_get_kwh})
print('Loaded power data')
power.columns = ['date','kwh']
power = power.set_index('date')

weather = pd.read_csv('historical-weather-data/114-2014-to-2017-combined.csv',skiprows=16,usecols=(0,6,12,14),
        converters = {0:ec_get_date,6:ec_get_vals,12:ec_get_vals,14:ec_get_vals})
weather.columns=['date','temp','wspeed','wdir']

#Adjust weather dates for daylight savings
mindate = np.min(weather.date)
for i in range(len(ds_times)):
    if mindate.year <= ds_times[i][0].year:
        inds = (weather.date >= ds_times[i][0]) & (weather.date <= (ds_times[i][1]-pd.Timedelta(2,unit='h')))
        inds = np.where(inds)[0] #necessary b/c of pandas?
        if len(inds)>0:
            weather.iloc[inds,0]+=pd.Timedelta(1,unit='h')
        if mindate.year == 2015:
            debug_here()
weather = weather.set_index('date')

#make sure starting dates are the same
stime1 = power.index[0]
stime2 = weather.index[0]
if stime1 > stime2:
    ind = np.nonzero(weather.index == stime1)[0]
    if len(ind) == 1:
        ind = ind[0]
    else:
        print('ERROR: overlapping dates')
        debug_here()
    weather = weather.iloc[ind:]
if stime1 < stime2:
    ind = np.nonzero(power.index == stime1)[0]
    if len(ind) == 1:
        ind = ind[0]
    else:
        print('ERROR: overlapping dates')
        debug_here()
    power = power.iloc[ind:]

#make sure ending dates are the same
stime1 = power.index[-1]
stime2 = weather.index[-1]
if stime1 < stime2:
    ind = np.nonzero(weather.index == stime1)[0]
    if len(ind) == 1:
        ind = ind[0]
    else:
        print('ERROR: overlapping dates')
        debug_here()
    weather = weather.iloc[0:ind+1]
if stime1 > stime2:
    ind = np.nonzero(power.index == stime1)[0]
    if len(ind) == 1:
        ind = ind[0]
    else:
        print('ERROR: overlapping dates')
        debug_here()
    power = power.iloc[0:ind+1]
    #cut from power

#Confirm that the power and weather dates are now the same.
a = np.abs(np.sum(np.array((power.index-weather.index).total_seconds())))
assert a<1e-8, 'ERROR: Power and weather dates do not match'

#combine weather and power into same dataframe
#add a column saying whether it was a workday or not
all_data = pd.concat([power,weather],axis=1) 

#Confirm they are the same
ok = True
ok1 = (all_data['kwh'][all_data['kwh'].notnull()] == power['kwh'][power['kwh'].notnull()]).all()
ok2 = (all_data['temp'][all_data['temp'].notnull()] == weather['temp'][weather['temp'].notnull()]).all()
assert ok1 and ok2, 'Array not concatenated properly'

#Remove duplicate dates from DST. This is far easier than dealing with them in an odd way (like converting to 1/2 interval?
all_data = all_data[~all_data.index.duplicated()]

#Remove the rows with any NaN values
all_data = all_data.dropna(axis=0,how='any')

all_data.to_pickle('data/all_data.pickle')


