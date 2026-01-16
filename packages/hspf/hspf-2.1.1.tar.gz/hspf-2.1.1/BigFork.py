# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:08:26 2024

@author: mfratki
"""

from hspf.hspfModel import hspfModel
import duckdb
from hspf import warehouse


model_name = 'BigFork'
db_path = 'C:/Users/mfratki/Documents/Calibrations/BigFork/model/HSPF_models.duckdb'

warehouse.init_hspf_db(db_path, reset = True)
with warehouse.connect(db_path) as con:
    warehouse.create_



model = hspfModel('C:/Users/mfratki/Documents/Calibrations/BigFork/model/BigFork_0.uci')



from pyhcal.calibrators import calibrator

cal = calibrator('C:\\Users\\mfratki\\Documents\\Calibrations\\Nemadji')
cal = calibrator('C:/Users/mfratki/Documents/Calibrations/BigFork')
cal = calibrator('C:/Users/mfratki/Documents/Calibrations/BigFork/past')
cal.load_model('BigFork_WQ')

#%%
df = equis.download(['S007-352'])
df = equis.replace_nondetects(df)
df = equis.normalize_timezone(df)
df = equis.convert_units(df)
df = equis.map_constituents(df)
df = equis.normalize_columns(df)

[modl_db.get_outlets_by_reach(reach_id,'BigFork')['reach_id'].to_list() for reach_id in cal.uci.network._upstream(70)]


# lbs/acr/yr TP from each landcover
reach_ids = cal.uci.network._upstream(70) + cal.uci.network._upstream(132)
reach_names = cal.uci.table('RCHRES','GEN-INFO')['RCHID'].loc[reach_ids].reset_index()
df = reports.subwatershed_total_phosphorous_loading(cal.uci,cal.model.hbns,as_load=False,group_landcover = False).mean(axis=0).reset_index()
df = df.loc[df['reach_id'].isin(reach_ids)]
df.columns = ['perlnd_id','hspf_landcover','acres','reach_id','TP (lb/acr/yr)']
#df_q = cal.model.reports.ann_avg_subwatershed_loading('Q').reset_index()
#df_q = df_q.loc[df_q['TVOLNO'].isin(reach_ids)][['TVOLNO','weighted_mean_Q']]
df_q = cal.model.hbns.get_multiple_timeseries('PERLND',5,'PERO').mean().reset_index()
df_q.columns = ['perlnd_id','Q (in/acr/yr)']
df = pd.merge(df, df_q, right_on = 'perlnd_id', left_on='perlnd_id', how='left')
df = pd.merge(df, reach_names, right_on = 'OPNID', left_on='reach_id', how='left')
df.drop(columns = 'OPNID',inplace=True)
df.rename(columns = {'RCHID':'Reach Name'},inplace=True)
df.to_csv(cal.output_path.joinpath('Landscape_Loading.csv'),index=False)

# lbs/yr outflow of each reach
drainage_areas = [cal.uci.network.drainage_area([reach_id]) for reach_id in reach_ids]
df = cal.model.hbns.get_rchres_data('TP',reach_ids,'lb','yearly').mean()
df2 = cal.model.hbns.get_multiple_timeseries('RCHRES',5,'PTOTIN',reach_ids).mean()
df_q = cal.model.hbns.get_rchres_data('Q',reach_ids,'acrft','yearly').mean()
df_q2 = cal.model.hbns.get_multiple_timeseries('RCHRES',5,'IVOL',reach_ids).mean()
df = pd.concat([df,df2,df_q,df_q2],axis=1).reset_index()
df.columns = ['reach_id','TP Outflow (lb/yr)','TP Inflow (lb/yr)','Q Outflow (acrft/yr)','Q Inflow (acrft/yr)']
df = pd.merge(df, reach_names, right_on = 'OPNID', left_on='reach_id', how='left')
df.drop(columns = 'OPNID',inplace=True)
df.rename(columns = {'RCHID':'Reach Name'},inplace=True)
df['Drainage Area (acres)'] = drainage_areas
df.to_csv(cal.output_path.joinpath('Channel_Loads.csv'),index=False)

reach_ids = cal.uci.network._upstream(70) + cal.uci.network._upstream(132)
df = reports.subwatershed_total_phosphorous_loading(cal.uci,cal.model.hbns,as_load=False,group_landcover = False).mean(axis=0).reset_index()
df = df.loc[df['reach_id'].isin(reach_ids)]
df.columns = ['perlnd_id','hspf_landcover','acres','reach_id','TP (lb/acr/yr)']





dfs = [] 
for reach_id in cal.uci.network._upstream(70):
    outlet = modl_db.get_outlets_by_reach(reach_id,'BigFork')
    outlet = outlet.loc[outlet['station_origin']=='equis']
    if not outlet.empty:
        reach_ids = [int(num) for num in set(outlet['reach_id'].to_list())]
        station_ids = outlet['station_id'].to_list()

        df= cal.compare_simulated_observed(station_ids,reach_ids,'TP','YE')
        df['outlet_id'] = outlet['outlet_id'].values[0]
        dfs.append(df)

{'H57008001':{'station_name': 'Whisky Creek',
              'opnids': [203,205,207]}}

#%% Reach 470
'''
- Model only
avg_ann_outflow()
avg_monthly_outflow()
avg_ann_watershed_loading()
avg_ann_subwatershed_loading()
avg_monthly_watershed_loading()
avg_monthly_subwatershed_loading()


avg_ann_stats()
avg_monthly_stts()


'''

constituent = 'TP'
units = 'mg/l'
sample_flag = True


station_ids = ['S001-235','S005-115']
flow_station_ids = ['E05011002']
reach_ids = [103]


#station_ids = ['S004-000']
station_ids = ['S005-369']
#station_ids = ['E77069001']
flow_station_ids = ['E77069001']
reach_ids = [470]

station_ids = ['H77031001']
flow_station_id = ['H77031001']
reach_ids = [210]

station_ids = ['H77107001']
flow_station_id = ['H77107001']
reach_ids = [350]


drng_area = cal.uci.network.drainage_area(reach_ids) #923540.16
df = cal.compare_simulated_observed(station_ids,reach_ids,constituent,'D')

df = cal.compare_wplmn(station_ids,reach_ids,constituent,units)
metrics.hydro_stats(df.dropna(),drng_area)
metrics.stats(df.dropna(),units)
metrics.aggregate(df.dropna(),units)

ff.contTimeseries(df,station_ids,constituent,units)
ff.timeseries(df,station_ids,constituent,units)

ff.FDCexceed(df.dropna(),station_ids,constituent,units)
df_exceed = ff._exceedence(df.dropna())
for month in df.index.month.unique():
    dfsub = df.loc[df.index.month == month]
    ff._FDCexceed(dfsub.dropna(),station_ids,constituent,units)
    plt.title(month)

    
    
    ff.FDCexceed(dfsub.dropna(),station_ids,constituent,units)
    plt.title(month)

def replace_table(uci1,uci2,operation,table_name,table_id):
    table = uci2.table(operation,table_name,table_id,False)
    uci1.replace_table(table,operation,table_name,table_id)

for table in ['PWAT-PARM1','PWAT-PARM2','PWAT-PARM3','PWAT-PARM4','MON-UZSN','MON-LZETPARM']:
    replace_table(cal2.uci,cal.uci,'PERLND',table,0)



#%%


# cal.update_table(.03, 'PERLND','PWAT-PARM3',0,columns = 'BASETP',operator = 'set')
# cal.update_table(.2, 'PERLND','PWAT-PARM3',0,columns = 'BASETP',opnids = wetland_perlnds,operator = 'set')
# cal.update_table(.2, 'PERLND','PWAT-PARM3',0,columns = 'BASETP',opnids = forest_perlnds,operator = 'set')
# cal.update_table(.15, 'PERLND','PWAT-PARM3',0,columns = 'BASETP',opnids = ag_perlnds,operator = 'set')

cal.update_table(.8,'PERLND','MON-LZETPARM',0,operator = 'set')
cal.update_table(.1,'PERLND','MON-LZETPARM',0,columns = ['LZEMAR','LZEJAN','LZEFEB','LZEAPR','LZEMAY','LZEOCT','LZENOV'],operator = 'set')

cal.update_table(.1,'PERLND','MON-LZETPARM',0,wetland_perlnds,operator = 'set')
cal.update_table(.4,'PERLND','MON-LZETPARM',0,wetland_perlnds,operator = 'set',columns = ['LZEMAR','LZEAPR','LZEMAY'])
cal.update_table(.9,'PERLND','MON-LZETPARM',0,wetland_perlnds,operator = 'set',columns = ['LZEJUN','LZEJUL','LZEAUG'])
cal.update_table(.4,'PERLND','MON-LZETPARM',0,wetland_perlnds,operator = 'set',columns = ['LZESEP','LZEOCT','LZEDEC'])


cal.update_table(.1,'PERLND','MON-LZETPARM',0,forest_perlnds,operator = 'set')
cal.update_table(.6,'PERLND','MON-LZETPARM',0,forest_perlnds,operator = 'set',columns = ['LZEMAR','LZEAPR','LZEMAY'])
cal.update_table(.9,'PERLND','MON-LZETPARM',0,forest_perlnds,operator = 'set',columns = ['LZEJUN','LZEJUL','LZEAUG'])
cal.update_table(.6,'PERLND','MON-LZETPARM',0,forest_perlnds,operator = 'set',columns = ['LZESEP','LZEOCT','LZEDEC'])


cal.update_table(.1,'PERLND','MON-LZETPARM',0,ag_perlnds,operator = 'set')
cal.update_table(.4,'PERLND','MON-LZETPARM',0,ag_perlnds,operator = 'set',columns = ['LZEMAR','LZEAPR','LZEMAY'])
cal.update_table(.9,'PERLND','MON-LZETPARM',0,ag_perlnds,operator = 'set',columns = ['LZEJUN','LZEJUL','LZEAUG'])
cal.update_table(.4,'PERLND','MON-LZETPARM',0,ag_perlnds,operator = 'set',columns = ['LZESEP','LZEOCT','LZEDEC'])



cal.update_table(.5,'PERLND','MON-UZSN',0,operator = 'set')

cal.update_table(2,'PERLND','MON-UZSN',0,wetland_perlnds,operator = 'set')
cal.update_table(1,'PERLND','MON-UZSN',0,wetland_perlnds,operator = 'set',columns = ['UZSMAR','UZSAPR','UZSMAY'])
cal.update_table(1.5,'PERLND','MON-UZSN',0,wetland_perlnds,operator = 'set',columns = ['UZSJUN','UZSJUL','UZSAUG'])
cal.update_table(1,'PERLND','MON-UZSN',0,wetland_perlnds,operator = 'set',columns = ['UZSSEP','UZSOCT','UZSDEC'])


# cal.update_table(1,'PERLND','MON-UZSN',0,forest_perlnds,operator = 'set')
# cal.update_table(2,'PERLND','MON-UZSN',0,forest_perlnds,operator = 'set',columns = ['UZSMAR','UZSAPR','UZSMAY'])
# cal.update_table(4,'PERLND','MON-UZSN',0,forest_perlnds,operator = 'set',columns = ['UZSJUN','UZSJUL','UZSAUG'])
# cal.update_table(2,'PERLND','MON-UZSN',0,forest_perlnds,operator = 'set',columns = ['UZSSEP','UZSOCT','UZSNOV'])


# cal.update_table(1,'PERLND','MON-UZSN',0,ag_perlnds,operator = 'set')
# cal.update_table(2,'PERLND','MON-UZSN',0,ag_perlnds,operator = 'set',columns = ['UZSMAR','UZSAPR','UZSMAY'])
# cal.update_table(4,'PERLND','MON-UZSN',0,ag_perlnds,operator = 'set',columns = ['UZSJUN','UZSJUL','UZSAUG'])
# cal.update_table(2,'PERLND','MON-UZSN',0,ag_perlnds,operator = 'set',columns = ['UZSSEP','UZSOCT','UZSNOV'])

# cal.update_table(1,'PERLND','MON-COVER',0,operator = 'set')

# cal.update_table(2,'PERLND','MON-COVER',0,wetland_perlnds,operator = 'set')
# cal.update_table(.6,'PERLND','MON-COVER',0,wetland_perlnds,operator = 'set',columns = ['COVMAR','COVAPR','COVMAY'])
# cal.update_table(.9,'PERLND','MON-COVER',0,wetland_perlnds,operator = 'set',columns = ['COVJUN','COVJUL','COVAUG'])
# cal.update_table(.9,'PERLND','MON-COVER',0,wetland_perlnds,operator = 'set',columns = ['COVSEP','COVOCT','COVDEC'])


# cal.update_table(1,'PERLND','MON-COVER',0,forest_perlnds,operator = 'set')
# cal.update_table(1,'PERLND','MON-COVER',0,forest_perlnds,operator = 'set',columns = ['COVMAR','COVAPR','COVMAY'])
# cal.update_table(.9,'PERLND','MON-COVER',0,forest_perlnds,operator = 'set',columns = ['COVJUN','COVJUL','COVAUG'])
# cal.update_table(2,'PERLND','MON-COVER',0,forest_perlnds,operator = 'set',columns = ['COVSEP','COVOCT','COVEROV'])


# cal.update_table(1,'PERLND','MON-COVER',0,ag_perlnds,operator = 'set')
# cal.update_table(1,'PERLND','MON-COVER',0,ag_perlnds,operator = 'set',columns = ['COVMAR','COVAPR','COVMAY'])
# cal.update_table(.9,'PERLND','MON-COVER',0,ag_perlnds,operator = 'set',columns = ['COVJUN','COVJUL','COVAUG'])
# cal.update_table(.75,'PERLND','MON-COVER',0,ag_perlnds,operator = 'set',columns = ['COVJUN'])








# cal.update_table(.2,'PERLND','MON-INTERCEP',0,operator = 'set')


cal.update_table(.03,'PERLND','MON-INTERCEP',0,wetland_perlnds,operator = 'set')
cal.update_table(.1,'PERLND','MON-INTERCEP',0,wetland_perlnds,operator = 'set',columns = ['INTMAR','INTAPR','INTMAY'])
cal.update_table(.3,'PERLND','MON-INTERCEP',0,wetland_perlnds,operator = 'set',columns = ['INTJUN','INTJUL','INTAUG'])
cal.update_table(.1,'PERLND','MON-INTERCEP',0,wetland_perlnds,operator = 'set',columns = ['INTSEP','INTOCT','INTDEC'])

cal.update_table(2,'PERLND','MON-INTERCEP',0,perlnds,operator = '*',columns = ['INTJUL','INTAUG','INTMAY'])


# cal.update_table(.03,'PERLND','MON-INTERCEP',0,wetland_perlnds,operator = 'set')
# cal.update_table(.04,'PERLND','MON-INTERCEP',0,wetland_perlnds,operator = 'set',columns = ['INTMAR','INTAPR','INTMAY'])
# cal.update_table(.4,'PERLND','MON-INTERCEP',0,wetland_perlnds,operator = 'set',columns = ['INTJUN','INTJUL','INTAUG'])
# cal.update_table(.04,'PERLND','MON-INTERCEP',0,wetland_perlnds,operator = 'set',columns = ['INTSEP','INTOCT','INTDEC'])



# cal.update_table(.03,'PERLND','MON-INTERCEP',0,ag_perlnds,operator = 'set')
# cal.update_table(.1,'PERLND','MON-INTERCEP',0,ag_perlnds,operator = 'set',columns = ['INTMAR','INTAPR','INTMAY'])
# cal.update_table(.3,'PERLND','MON-INTERCEP',0,ag_perlnds,operator = 'set',columns = ['INTJUN','INTJUL','INTAUG'])
# cal.update_table(.1,'PERLND','MON-INTERCEP',0,ag_perlnds,operator = 'set',columns = ['INTSEP','INTOCT','INTDEC'])

#%%
# 

# df = cal.get_observed_data(station_ids,'Q','cfs','D',sample_flag=False).to_frame()
# df_sta = pd.DataFrame(data=[[-93.8071635476731, 48.1966267253807, area]],
#                       index=df.columns, columns=['lon', 'lat', 'area'])
# dfs, df_kge = baseflow.separation(df, df_sta, return_kge=True)
# test = {k:df.resample('D').mean() for k,df in dfs.items()}
# df = df.resample('D').mean()
# def plot_baseflow(method): 
#     fig,ax = plt.subplots()
#     df.plot(ax = ax)
#     test[method].plot(ax = ax)
#     ax.legend(['Observed Flow','Baseflow Filter'])
#     plt.title(method)

#%%

station_ids = ['E77069001']
flow_station_id = ['E77069001']
reach_ids = [470]
drng_area = cal.uci.network.drainage_area(470) #923540.16
perlnds = cal.uci.network.get_opnids('PERLND',550,[210])
reaches = cal.uci.network.get_opnids('RCHRES',550,[210])
reaches = cal.uci.network.get_opnids('RCHRES',550)

wetland_perlnds = list(cal.uci.opnid_dict['PERLND'].index[cal.uci.opnid_dict['PERLND']['landcover'].isin([0])])
forest_perlnds = list(cal.uci.opnid_dict['PERLND'].index[cal.uci.opnid_dict['PERLND']['landcover'].isin([2,3,4,5,6,7])])
ag_perlnds = list(cal.uci.opnid_dict['PERLND'].index[cal.uci.opnid_dict['PERLND']['landcover'].isin([8,10])])
urban_perlnds = list(cal.uci.opnid_dict['PERLND'].index[cal.uci.opnid_dict['PERLND']['landcover'].isin([1])])


df = cal.compare_simulated_observed(station_ids,reach_ids,constituent,'D',unit = units,wplmn = False)

df = cal.compare_simulated_observed(station_ids,reach_ids,constituent,units,
                                    time_step = 'D', agg_period = 'D',
                                    flow_station_ids = flow_station_id, sample_flag = sample_flag,
                                    dropna = False)



metrics.stats(df.dropna(),units)

metrics.hydro_stats(df.dropna(),drng_area)
cal.model.reports.avg_ann_outflow()
cal.model.reports.avg_monthly_outflow()

cal.save_output(constituent,station_ids,reach_ids,flow_station_id,drng_area)


ff.contTimeseries(df,station_ids,constituent,units)

ff.FDCexceed(df.dropna(),station_ids,constituent,units)
ff.LDC(df.dropna(),station_ids,constituent,units,time_step = 'D')
ff.timeseries(df,station_ids,constituent,units)
ff.rating(df.dropna(),station_ids,constituent,units)
ff.scatter(df.dropna(),station_ids,constituent,units)


#%% Calibratoin Log
#Run1
cal.load_model(1)

forest_perlnds = list(cal.uci.opnid_dict['PERLND'].index[cal.uci.opnid_dict['PERLND']['landcover'].isin([2,3,4,5,6,7])])
wetland_perlnds = list(cal.uci.opnid_dict['PERLND'].index[cal.uci.opnid_dict['PERLND']['landcover'].isin([0])])

cal.update_table(.5,'PERLND','PWAT-PARM2',0,forest_perlnds,'LZSN',operator = '*')


cal.update_table(.5,'PERLND','PWAT-PARM3',0,forest_perlnds,'BASETP',operator = '*')
cal.update_table(2,'PERLND','PWAT-PARM3',0,
                     opnids = wetland_perlnds,
                     columns = 'BASETP',
                     operator = '*')


#Run 2
cal.load_model(2)


#%% Reach 210
station_ids = ['H77031001']
flow_station_id = ['H77031001']
reach_ids = [210]

perlnds = list(cal.uci.network.get_opnids('PERLND',210))
forest_perlnds = cal.uci.opnid_dict['PERLND'].loc[perlnds]
forest_perlnds = list(forest_perlnds.index[forest_perlnds['landcover'].isin([2,3,4,5,6,7])])
wetland_perlnds = list(cal.uci.opnid_dict['PERLND'].index[cal.uci.opnid_dict['PERLND']['landcover'].isin([0])])

drng_area = cal.uci.network.drainage_area(210)
df = cal.compare_simulated_observed(station_ids,reach_ids,constituent,units,
                                    time_step = 'D', agg_period = 'D',
                                    flow_station_ids = flow_station_id, sample_flag = sample_flag,
                                    dropna = False)
metrics.stats(df.dropna(),units)
#df = df.loc[df.index.year >= 2017]
metrics.hydro_stats(df.dropna(),drng_area)
ff.contTimeseries(df,station_ids,constituent,units)
ff.FDCexceed(df.dropna(),station_ids,constituent,units)
ff.scatter(df.dropna(),station_ids,constituent,units)

ff.timeseries(df,station_ids,constituent,units)
ff.rating(df.dropna(),station_ids,constituent,units)


cal.save_output(constituent,station_ids,reach_ids,flow_station_id,drng_area)

# Calibration

perlnds = list(cal.uci.network.get_opnids('PERLND',210))
#Run1
cal.update_table(2,'PERLND','MON-UZSN',0,
                     opnids = perlnds,
                     columns = ['UZSJUL','UZSAUG','UZSSEP'],
                     operator = '*')
cal.update_table(2,'PERLND','MON-UZSN',0,
                     opnids = perlnds,
                     columns = ['UZSJUL','UZSAUG','UZSSEP'],
                     operator = '*')
#Run2
cal.update_table(.4,'PERLND','MON-INTERCEP',0,
                 columns = ['INTJUL','INTAUG'],
                 opnids = forest_perlnds,
                 operator = 'set')

cal.update_table(.9,'PERLND','MON-LZETPARM',0,
                 columns = ['LZEAUG','LZESEP'],
                 opnids = forest_perlnds,
                 operator = 'set')

#Run3
cal.update_table(.75,'PERLND','PWAT-PARM2',0,
                     opnids = perlnds,
                     columns = 'LZSN',
                    operator = '*')
#Run4
cal.update_table(.8,'PERLND','PWAT-PARM4',0,columns = 'LZETP',operator = 'set')
#run 5
cal.update_table(.3,'PERLND','MON-INTERCEP',0,columns = ['INTJUL','INTAUG'],opnids = forest_perlnds,operator = 'set')
cal.update_table(.25,'PERLND','MON-INTERCEP',0,columns = ['INTJUL'],opnids = forest_perlnds,operator = 'set')
cal.update_table(.15,'PERLND','MON-INTERCEP',0,columns = ['INTMAY','INTSEP'],opnids = forest_perlnds,operator = 'set')

#run 6
cal.update_table(.99,'PERLND','PWAT-PARM4',0,
                     opnids = perlnds,
                     columns = 'AGWRC',
                    operator = 'set')

#%% Reach 350
station_ids = ['H77107001']
flow_station_id = ['H77107001']
reach_ids = [350]
drng_area = cal.uci.network.drainage_area(350)
perlnds = list(cal.uci.network.get_opnids('PERLND',350,[210]))
forest_perlnds = cal.uci.opnid_dict['PERLND'].loc[perlnds]
forest_perlnds = list(forest_perlnds.index[forest_perlnds['landcover'].isin([2,3,4,5,6,7])])
wetland_perlnds = list(cal.uci.opnid_dict['PERLND'].index[cal.uci.opnid_dict['PERLND']['landcover'].isin([0])])



df = cal.compare_simulated_observed(station_ids,reach_ids,constituent,units,
                                    time_step = 'D', agg_period = 'D',
                                    flow_station_ids = flow_station_id, sample_flag = sample_flag,
                                    dropna = False)
metrics.stats(df.dropna(),units)

#df = df.loc[df.index.year < 2015]
metrics.hydro_stats(df.dropna(),drng_area)
ff.contTimeseries(df,station_ids,constituent,units)
ff.FDCexceed(df.dropna(),station_ids,constituent,units)
ff.timeseries(df,station_ids,constituent,units)
cal.save_output(constituent,station_ids,reach_ids,flow_station_id,drng_area)
#%%
# Goal: Reduce total annual sediment for reaches downstream of 210
perlnds = cal.uci.network.get_opnids('PERLND',550,[210])
cal.update_table(.5,'PERLND','SED-PARM3',0,columns = 'KSER',opnids = perlnds)




order = cal.uci.network.calibration_order(550)
reach_ids = order[2]

for reach_ids in order[18:]:
    df = cal.model.reports.scour()
    df = df.loc[df['LKFG'] == 0]
    positives = df.loc[(df.index.isin(reach_ids)) & (df['depscour'] > 0)].index
    if len(positives)>0:
        print(positives)
        break
    
cal.update_table(1.3,'RCHRES','SILT-CLAY-PM',0,columns = 'M', opnids = positives)
cal.update_table(1.3,'RCHRES','SILT-CLAY-PM',1,columns = 'M', opnids = positives)


# Negative scours
df_scour = cal.model.reports.scour()
negatives = df_scour.loc[df_scour['depscour'] < -700].index

cal.update_table(.25,'RCHRES','SILT-CLAY-PM',0,columns = 'M', opnids = negatives)
cal.update_table(.25,'RCHRES','SILT-CLAY-PM',1,columns = 'M', opnids = negatives)

cal.update_table(.25,'RCHRES','SILT-CLAY-PM',0,columns = 'M', opnids = negatives)
cal.update_table(.25,'RCHRES','SILT-CLAY-PM',1,columns = 'M', opnids = negatives)



import matplotlib.pyplot as plt
import numpy as np

df = cal.model.reports.runoff().groupby(cal.model.reports.runoff().index.year).sum().mean(axis=0)
x = df.index.levels[0]
y1 = df[:,'agwo']
y2 = df[:,'ifwo']
y3 = df[:,'suro']
# plot bars in stack manner
plt.bar(x, y1, color='g')
plt.bar(x,y2, bottom=y1, color='y')
plt.bar(x,y3, bottom=y1+y2, color='b')


df = cal.model.reports.runoff()
n_years = df.index.year.max()-df.index.year.min()
df = df.groupby(cal.model.reports.runoff().index.month).sum()/n_years
df.columns = df.columns.swaplevel(0,1)
x = df.index
y1 = df['agwo'].mean(axis=1)
y2 = df['ifwo'].mean(axis=1)
y3 = df['suro'].mean(axis=1)
# plot bars in stack manner
plt.bar(x, y1, color='g')
plt.bar(x,y2, bottom=y1, color='y')
plt.bar(x,y3, bottom=y1+y2, color='b')

land_cover = 'Old Decid Forest AB'
df = cal.model.reports.runoff()
n_years = df.index.year.max()-df.index.year.min()
df = df.groupby(cal.model.reports.runoff().index.month).sum()/n_years
dfsub = df[land_cover]
x = dfsub.index
y1 = dfsub.loc[:,'agwo']
y2 = dfsub.loc[:,'ifwo']
y3 = dfsub.loc[:,'suro']
# plot bars in stack manner
plt.bar(x, y1, color='g')
plt.bar(x,y2, bottom=y1, color='y')
plt.bar(x,y3, bottom=y1+y2, color='b')



station_ids = ['H76033001']
reach_ids = [290]
drng_area = cal.uci.network.drainage_area(290)


flow_station_id = None
constituent = 'Q'
units = 'cfs'
df = cal.compare_simulated_observed(station_ids,reach_ids,constituent,units,'D',flow_station_ids = flow_station_id)



df

metrics.monthly()

metrics.hydro_stats(df,drng_area)
metrics.NSE(df)

cal.load_model(64)

#cal.dm.download_station_data()
# Set relevant reaches to hourly timeseries.
cal.initialize([202,213,203,154,117,205,207,158])

station_ids = ['H57037001']
reach_ids = [154]
drng_area = cal.uci.network.drainage_area(154)

station_ids = ['E57028001']
reach_ids = [117]
drng_area = 4352000

station_ids = ['S007-461']
reach_ids = [213]

station_ids = ['S002-097']
flow_station_ids = ['E57028001']
reach_ids = [117]
constituent = 'N'
units = 'mg/l'
filepath = cal.output_path.joinpath(f'{constituent}_{reach_ids[0]}')


df = cal.compare_simulated_observed(station_ids,reach_ids,constituent,units,'D',flow_station_ids = flow_station_id)

df['observed_flow'].plot()
df['simulated_flow'].plot()
df['simulated'].plot()
df['observed.plot()']

ff.contTimeseries(df,[constituent],units,filepath)
ff.timeseries(df,station_ids,constituent,units,filepath = cal.output_path.joinpath('test'))


drng_area = cal.uci.network.drainage_area(154)
df = cal.compare_simulated_observed(['E57028001'],[117],'Q','cfs','D')*60*60*24/43560/drng_area*12
metrics.hydro_stats(df,drng_area)

station_ids = ['S010-822','S004-880','S003-271','S002-103']
reach_ids = [158]
len(cal.compare_simulated_observed(station_ids,reach_ids,'TP','mg/l','D')) # 19
len(cal.compare_simulated_observed(station_ids,reach_ids,'N','mg/l','D'))  # 19


station_ids = ['S001-060','S004-881','S001-032']
reach_ids = [202]
len(cal.compare_simulated_observed(station_ids,reach_ids,'TP','mg/l','D')) # 105
len(cal.compare_simulated_observed(station_ids,reach_ids,'N','mg/l','D'))  # 88

tation_ids = ['S007-461']
reach_ids = [213]
df = cal.compare_simulated_observed(station_ids,reach_ids,'TP','mg/l','D') # 106
ff.scatter(df,station_ids,'TP','mg/l')
ff.timeseries(df,station_ids,'TP','mg/l')
len(cal.compare_simulated_observed(station_ids,reach_ids,'N','mg/l','h'))  # 89


station_ids = ['S005-322']
reach_ids = [154]

tation_ids = ['S007-461']
reach_ids = [213]


constituent = 'TP'
units = 'mg/l'
df = cal.compare_simulated_observed(station_ids,reach_ids,constituent,units,'D')
ff.scatter(df,station_ids,constituent,units)
ff.timeseries(df,station_ids,constituent,units)


len(cal.compare_simulated_observed(station_ids,reach_ids,'N','mg/l','h'))  # 57
len(cal.compare_simulated_observed(station_ids,reach_ids,'TP','mg/l','h')) # 74

cal.get_observed_data(station_ids,'N','mg/l','h')

df = cal.compare_simulated_observed(station_ids,reach_ids,'TP','mg/l','h')
#df = cal.compare_simulated_observed(station_ids,reach_ids,'Q','cfs','D')
df[df<0] = 0 
df.plot()
cal.aggregate(station_ids,reach_ids,'TSS','mg/l','D').plot()



cal.dm.download_station_data('E57028001','wiski')

station_ids [ 'H76108002','']
station_ids = ['H49009001']
station_ids = ['S006-770']


station_id = 'S006-770'
station_id = 'H49009001'
cal.dm.get_data(station_id = station_id,constituent = 'WT',unit = 'deg c')

cal.save_outputs(station_ids)


# Hydrology
cal.metrics.hydrology.stats(station_ids)
cal.metrics.hydrology.nse(station_ids)
cal.model.reports.runoff()
# Figures
cal.figures.hydrology.timeseries(station_ids)
cal.figures.hydrology.exceedence(station_ids)




# Sediment
cal.metrics.sediment.stats(station_ids,units='mg/l')
cal.model.reports.scour()
# Figures
cal.figures.sediment.timeseries(station_ids,units= 'mg/l')
cal.figures.sediment.exceedence(station_ids)





cal.MODL_DB[['station_id','true_opnid','name']]



model = hspfModel(cal.model_path.joinpath('HawkYellowMedicine_0.uci'))



cal.load_model(0)
cal.set_dates(start_date = '2013-01-01',
              end_date = '2024-12-31')





precip = cal.model.wdms.series('UpperRed_Met_2022.wdm',111)
pevt =  cal.model.wdms.series('UpperRed_Met_2022.wdm',121)*.6
df = precip - pevt
df.resample('Y').plot()

plt.plot(precip-pevt)

df = cal.model.hbns.get_multiple_timeseries('PERLND','yearly','PERO',activity ='PWATER')

df = cal.model.hbns.get_multiple_timeseries('PERLND','yearly','SURO',activity ='PWATER')
df.sum()/27



df.groupby('sender').message
   .resample('D').count()
   .unstack('sender')
   .plot()
)



precip = cal.model.wdms.series('UpperRed_Met_2022.wdm',101)
precip = precip.loc[precip.index >= '1996-01-01']
precip_monthly = precip.resample('MS').sum()
supy = cal.model.hbns.get_multiple_timeseries('PERLND','monthly','SUPY',activity = 'PWATER')
prain = cal.model.hbns.get_multiple_timeseries('PERLND','yearly','PRAIN',activity = 'SNOW')
wyield = cal.model.hbns.get_multiple_timeseries('PERLND','yearly','WYIELD',activity = 'SNOW')






