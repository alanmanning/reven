import numpy as np
import pylab as plt
import datetime as DT
import pandas as pd
import holidays
from IPython.core.debugger import Tracer; debug_here = Tracer()

plt.close('all')


def get_holidays(hh_params,all_data):
    bc_holidays = holidays.CA(prov='BC')
    all_data['holiday'] = all_data.index.isin(bc_holidays)
    return all_data
    
def get_workdays(hh_params,all_data):
    #Figure out when the workdays are
    #TODO: Make the following work
    if False:
        workday_inds = np.logical_and(all_data.index.weekday >=0, np.logical_and(all_data.index.weekday <5,all_data['holiday']))
        all_data['workday'] = workday_inds
    else:
        all_data['workday'] = np.ones(all_data.shape[0],dtype=bool)

    return all_data


all_data = pd.read_pickle('data/all_data.pickle')


#TODO: write functions to infer the following values.
#-Workday/nonWorkday bedtime/waketime
#-Empty home detection (ie, extended vacations)
#   -Easy if heat isn't left on during winter
#-Throw out outliers




#household parameters
#'wd' = 'workday'
#'nwd' = 'nonworkday'
#NOTE: using hours only for the time. Later, will have to round up or down depending
#   on given times. Remember that power and weather are given in hourly increments.
hh_params = {
        'reg-schedule': False,
        'work-on-holidays': True,
        'wd-waketime':   DT.time(6,0),
        'wd-leavetime':  DT.time(8,0),
        'wd-returntime': DT.time(17,0),
        'wd-bedtime':    DT.time(22,0)
        }

all_data = get_workdays(hh_params,all_data)
all_data = get_holidays(hh_params,all_data)

#Figure out when sleeping,morning,working,evening,etc.
all_data['sleeping'] = np.logical_or(all_data.index.time >= hh_params['wd-bedtime'],
        all_data.index.time < hh_params['wd-waketime'])
all_data['awake'] = np.logical_not(all_data['sleeping'])

print('Average power while sleeping = %g ' % (all_data['kwh'][all_data['sleeping']]).mean())
print('Average power while awake = %g ' % (all_data['kwh'][all_data['awake']]).mean())

##### PARX Analysis
#Don't know if I can use this analysis because it requires a lot of data! Need to calculate the 10th
#and 90th percentiles for a home at a given temperature and hour...
#-Here's what I'll do. Fit a line to the three regions (heating, normal, cooling) and calculate
# the 90th/10th percential of deviations from that line. Use that as the occupancy variables.

temp_region = (5,16,20)

assert len(temp_region) == 3, 'Need 3 temp regions to copy the Arkadian analysis'
#inds = (all_data.index.time == DT.time(1,0))

################################################################
#### FIGURE OUT TEMPERATURE VARIABLES
################################################################
temp_inds = []
for i in range(len(temp_region)+1):
    if i==0:
        val = all_data['temp'] < temp_region[i]
    elif i==len(temp_region):
        val = all_data['temp'] >= temp_region[-1]
    else:
        val = (all_data['temp'] < temp_region[i]) & (all_data['temp'] >= temp_region[i-1])
    temp_inds.append(val)
    
all_data['xt1'] = np.zeros(all_data.shape[0])
all_data['xt2'] = np.zeros(all_data.shape[0])
all_data['xt3'] = np.zeros(all_data.shape[0])

all_data.loc[temp_inds[3],'xt1'] = all_data.loc[temp_inds[3],'temp'] - 20
#all_data.loc[temp_inds[2],'xt1.5'] = #nothing
all_data.loc[temp_inds[1],'xt2'] = 16 - all_data.loc[temp_inds[1],'temp']
all_data.loc[temp_inds[0],'xt3'] = 5 - all_data.loc[temp_inds[0],'temp']

###Confirm graphically
#plt.plot(all_data['temp'],all_data['xt1'],'.g')
#plt.plot(all_data['temp'],all_data['xt2'],'.m')
#plt.plot(all_data['temp'],all_data['xt3'],'.r')
#plt.show()

################################################################
#### FIGURE OUT OCCUPANCY VARIABLES
################################################################

#TODO: Make this more efficient
#-No need to make large xo arrays since they are just summed together at the end
#-But I know it works this way

#Make arrays for occupancy variables
#xo1 = pd.DataFrame(np.zeros((all_data.shape[0],24)))
#xo1.index = all_data.index
#xo2 = xo1.copy()
xo1 = pd.DataFrame(np.zeros(all_data.shape[0]))
xo1.index = all_data.index
xo2 = xo1.copy()



for hour in np.sort(np.array(all_data.index.hour.unique())):
    hour_inds = (all_data.index.hour == hour)

    for i in range(len(temp_inds)):
        j = (hour_inds & temp_inds[i])

        if len(np.where(j)[0])>1:
            p1 = np.polyfit(all_data.loc[j,'temp'], all_data.loc[j,'kwh'], 1)
            line = p1[1]+p1[0]*all_data.loc[j,'temp'] 

#            #Confirm graphically
            plt.plot(all_data.loc[j,'temp'],all_data.loc[j,'kwh']+30*hour,'.b')
            plt.plot(all_data.loc[j,'temp'],line+30*hour,'-g')

            #Figure out the occupancy variables (xo1/xo2 keeps track of outliers--
            #where consumption is abnormally high or low and likely indicates
            #more or less people in the house than normal).
            resid = all_data.loc[j,'kwh'] - line
            qi = resid.quantile(0.9)
            inds = resid >= qi
            if inds.any():
                ilocs = [all_data.index.get_loc(ii) for ii in inds[inds].index]
                xo1.iloc[ilocs]+=np.ones((len(ilocs),1))
                plt.plot(all_data.loc[inds[inds].index,'temp'],all_data.loc[inds[inds].index,'kwh']+30*hour,'.r')
            qi = resid.quantile(0.1)
            inds = resid <= qi
            if inds.any():
                ilocs = [all_data.index.get_loc(ii) for ii in inds[inds].index]
                xo2.iloc[ilocs]+=np.ones((len(ilocs),1))
                plt.plot(all_data.loc[inds[inds].index,'temp'],all_data.loc[inds[inds].index,'kwh']+30*hour,'.c')

#plt.show()
#xo1.columns = ['xo1-'+str(x) for x in list(range(24))]
#xo2.columns = ['xo2-'+str(x) for x in list(range(24))]
#xo1.to_pickle('data/xo1.pickle')
#xo2.to_pickle('data/xo2.pickle')

if (xo1>1.1).any()[0] or (xo2>1.1).any()[0]:
    print('ERROR: occupancy variables have been double-set. This should not happen. Have fun tracking down the bug!')

all_data['xo1'] = xo1
all_data['xo2'] = xo2

all_data.to_pickle('data/all_data.pickle')

################################################################
#### FIGURE OUT TEMPERATURE VARIABLES
################################################################




#
#
#f = plt.figure()
#ax = f.add_subplot(111)
#ax.plot(power['kwh'],weather['temp'],'.')
#ax.set_xlabel('Power Consumption (kWh)')
#ax.set_ylabel('Temperature (deg C)')
#ax.set_title('Temperature vs. Consumption')
#
#f = plt.figure()
#ax = f.add_subplot(111)
#ax.plot(power['kwh'],weather['wspeed'],'.')
#ax.set_xlabel('Power Consumption (kWh)')
#ax.set_ylabel('Windspeed')
#ax.set_title('Temperature vs. Windspeed')
#
#kwh_msk    = np.ma.masked_array(power.kwh,np.isnan(power.kwh))
#temp_msk   = np.ma.masked_array(weather.temp,np.isnan(weather.temp))
#wspeed_msk = np.ma.masked_array(weather.wspeed,np.isnan(weather.wspeed))
#wdir_msk   = np.ma.masked_array(weather.wdir,np.isnan(weather.wdir))
#
#
#sleep_hour = 0
#wake_hour = 6
#tco = [10,15] #cutoff temps. Below tco[0] the heat will probably come on, above tco[1] the AC may come on
#
#night_inds = np.logical_and(power.index.hour > sleep_hour, power.index.hour <= wake_hour)
#day_inds = ~night_inds
#
#avg_night_kwh  = np.ma.average(kwh_msk[night_inds].reshape((-1,wake_hour-sleep_hour)),axis=1)
#avg_night_temp = np.ma.average(temp_msk[night_inds].reshape((-1,wake_hour-sleep_hour)),axis=1)
#avg_night_date = power.index[(np.roll(np.diff(night_inds*1),shift=1)==1)].date
#
#avg_day_kwh  = np.ma.average(kwh_msk[day_inds].reshape((-1,24-(wake_hour-sleep_hour))),axis=1)
#avg_day_temp = np.ma.average(temp_msk[day_inds].reshape((-1,24-(wake_hour-sleep_hour))),axis=1)
#avg_day_date = power.index[(np.roll(np.diff(day_inds*1),shift=1)==1)].date
#
#
#
#
###Confirm that the averaging is done properly
##for i in range(len(avg_night_date)):
##    ax.plot([avg_night_date[i],avg_night_date[i]],[0,20],':r')
##ax.plot(weather.index[night_inds],temp_msk[night_inds],'xb')
##ax.plot(power.index[night_inds],kwh_msk[night_inds],'xc')
#
#
#f = plt.figure()
#ax=f.add_subplot(111)
#ax.plot(avg_night_date, avg_night_temp,'ob')
#ax.plot(avg_day_date, avg_day_temp,'dk')
#ax=ax.twinx()
#ax.plot(avg_night_date, avg_night_kwh, 'oc')
#ax.plot(avg_day_date, avg_day_kwh,'dm')
#ax = plt.figure().add_subplot(111)
#ax.plot(avg_night_temp,avg_night_kwh,'.')
#plt.show()
#
#inds = (avg_night_temp <= tco[0]).filled(False)
#print('Average consumption during cold nights: ',np.ma.average(avg_night_kwh[inds]))
#inds = np.logical_and( (avg_night_temp > tco[0]).filled(False), (avg_night_temp <= tco[1]).filled(False) )
#print('Average consumption during warm nights: ',np.ma.average(avg_night_kwh[inds]))
#inds = (avg_night_temp > tco[1]).filled(False)
#print('Average consumption during hot nights: ', np.ma.average(avg_night_kwh[inds]))
#
#inds = (avg_day_temp <= tco[0]).filled(False)
#print('Average consumption during cold days: ',np.ma.average(avg_day_kwh[inds]))
#inds = np.logical_and( (avg_day_temp > tco[0]).filled(False), (avg_day_temp <= tco[1]).filled(False) )
#print('Average consumption during warm days: ',np.ma.average(avg_day_kwh[inds]))
#inds = (avg_day_temp > tco[1]).filled(False)
#print('Average consumption during hot days: ', np.ma.average(avg_day_kwh[inds]))
#
#
#
#
#
##TODO:
#
#
#
#
##f=plt.figure()
##ax = f.add_subplot(111)
##ax.plot(avg_night_date,avg_night_kwh,'-r')
##ax = ax.twinx()
##ax.plot(avg_night_date,avg_night_temp,'g')
##plt.show()
#
#
##Define night time consumption as between 12 and 6
#
#
##TODO: remove this next line. Have to fix the daily average... the values don't seem right.
#
#x = np.ma.average(kwh_msk.reshape((24,-1)),axis=0)[:,np.newaxis] #calculate the average consumption for each day
#daily_mean = (x*np.ones((x.shape[0],24))).flatten() #put the daily mean into an array of the same shape as kwh
#
#
#
#
#f=plt.figure()
#ax=f.add_subplot(211)
#ax.plot(power.index,kwh_msk,'-b',linewidth=0.5,alpha=0.5)
#ax.plot(power.index,daily_mean,'-r')
#ax=f.add_subplot(212)
#ax.plot(power.index,kwh_msk-daily_mean,'.')
#
#plt.show(block=False)
#
##f = plt.figure()
##ax = f.add_subplot(111)
##ax.plot(power['kwh'],weather['wdir'],'.')
##ax.set_xlabel('Power Consumption (kWh)')
##ax.set_ylabel('Wind Dir')
##ax.set_title('Temperature vs. Windspeed')
#
#'''
