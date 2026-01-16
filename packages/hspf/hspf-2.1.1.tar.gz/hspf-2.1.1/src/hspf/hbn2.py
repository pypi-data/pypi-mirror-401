# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:33:52 2022
Utility functions for accessing data from the hbn files as they relate to the
nutrients relevant for our current calibration methods. (See calibration_helpers.py)

@author: mfratki

MODIFIED TO USE CYTHON FOR SPEED
"""
from . import helpers
import pandas as pd
import math
from struct import unpack
from pandas import DataFrame
from datetime import datetime, timedelta
from collections import defaultdict

# Attempt to import the compiled Cython module
try:
    from hspf import hbn_cy
except ImportError:
    print("="*80)
    print("WARNING: Could not import compiled 'hbn_cy' module.")
    print("Falling back to slow, pure-Python implementation.")
    print("To fix this, compile the Cython extension by running:")
    print("python setup.py build_ext --inplace --compiler=mingw32")
    print("="*80)
    hbn_cy = None

# ... (The rest of your helper functions like get_simulated_flow, etc. remain here) ...
CF2CFS = {'hourly':3600,
          'daily':86400,
          'monthly':2592000,
          'yearly':31536000,
          'h':3600,
          'D':86400,
          'ME':2592000,
          'Y':31536000,
          'YE':31536000,
          2:3600,
          3:86400,
          4:2592000,
          5:31536000}

AGG_DEFAULTS = {'cfs':'mean',
                'mg/l':'mean',
                'degF': 'mean',
                'lb':'sum'}

UNIT_DEFAULTS = {'Q': 'cfs',
                 'TSS': 'mg/l',
                 'TP' : 'mg/l',
                 'OP' : 'mg/l',
                 'TKN': 'mg/l',
                 'N'  : 'mg/l',
                 'WT' : 'degF',
                 'WL' : 'ft'}

def get_simulated_implnd_constituent(hbn,constituent,time_step):
    t_cons = helpers.get_tcons(constituent,'IMPLND')
    df = sum([hbn.get_multiple_timeseries(t_opn='IMPLND', 
                                       t_con= t_con, 
                                       t_code = time_step) for t_con in t_cons])
    if constituent == 'TSS':
        df = df*2000
    return df


def get_simulated_perlnd_constituent(hbn,constituent,time_step):
    t_cons = helpers.get_tcons(constituent,'PERLND')
    df = sum([hbn.get_multiple_timeseries(t_opn='PERLND', 
                                       t_con= t_con, 
                                       t_code = time_step) for t_con in t_cons])
    if constituent == 'TSS':
        df = df*2000
    return df

def get_simulated_catchment_constituent(hbn,constituent,time_step):
    return pd.concat([get_simulated_perlnd_constituent(hbn,constituent,time_step),
                      get_simulated_implnd_constituent(hbn,constituent,time_step)])
        
def get_simulated_flow(hbn,time_step,reach_ids,unit = None):
    if unit is None:
        unit = 'cfs'
    assert unit in ['cfs','acrft']
    sign = [math.copysign(1,reach_id) for reach_id in reach_ids]
    reach_ids = [abs(reach_id) for reach_id in reach_ids]
    flows = hbn.get_multiple_timeseries('RCHRES',time_step,'ROVOL',reach_ids)
    flows = (flows*sign).sum(axis=1)
    if unit == 'cfs':
        flows = flows/CF2CFS[time_step]*43560
    flows.attrs['unit'] = unit
    return flows

def get_simulated_temperature(hbn,units,time_step,reach_ids):
    raise NotImplementedError()
    
def get_simulated_reach_constituent(hbn,constituent,time_step,reach_ids,unit = None):
    sign = [math.copysign(1,reach_id) for reach_id in reach_ids]
    if unit is None:
        unit = UNIT_DEFAULTS[constituent]
    else:
        assert(unit in ['mg/l','lb','cfs','degF'])
    t_cons = helpers.get_tcons(constituent,'RCHRES','lb')
    df = pd.concat([hbn.get_multiple_timeseries('RCHRES',time_step,t_con,[abs(reach_id) for reach_id in reach_ids])*sign for t_con in t_cons],axis=1).sum(axis=1)
    if constituent == 'TSS':
        df = df*2000
    if unit == 'mg/l':
        flow = get_simulated_flow(hbn,time_step,reach_ids,'acrft')*1233481.8375475
        df = df*453592.37 / flow
    df.attrs['unit'] = unit
    df.attrs['constituent'] = constituent
    df.attrs['reach_ids'] = reach_ids
    return df

class hbnInterface:
    def __init__(self,file_paths,Map = True):
        self.names = [file_path for file_path in file_paths]
        self.hbns = [hbnClass(file_path,Map) for file_path in file_paths]
    # ... (rest of hbnInterface is unchanged) ...
    def _clear_cache(self):
        [hbn._clear_cache() for hbn in self.hbns]
        
    def get_time_series(self, t_opn, t_cons, t_code, opnid, activity = None):
        return pd.concat([hbn.get_time_series(t_opn, t_cons, t_code, opnid, activity) for hbn in self.hbns],axis = 1)
        
    def get_multiple_timeseries(self,t_opn,t_code,t_con,opnids = None,activity = None,axis = 1):
        return pd.concat([hbn.get_multiple_timeseries(t_opn,t_code,t_con,opnids,activity) for hbn in self.hbns],axis = 1)

    def get_reach_constituent(self,constituent,reach_ids,time_step,unit = None):
        if constituent == 'Q':
            df = get_simulated_flow(self,time_step,reach_ids,unit = unit)
        elif constituent == 'WT':
            df = get_simulated_temperature(self,time_step,reach_ids)
        else:     
            df = get_simulated_reach_constituent(self,constituent,time_step,reach_ids,unit)
        return df.to_frame()
    
    def output_names(self):
        dd = defaultdict(set)    
        dics =  [hbn.output_names() for hbn in self.hbns]
        for dic in dics:
            for key, vals in dic.items():
                [dd[key].add(val) for val in vals]
        return dd

class hbnClass:
    def __init__(self,file_name,Map = True):
        self.file_name = file_name
        self.tcodes = {'minutely':1,'hourly':2,'daily':3,'monthly':4,'yearly':5, 
                       1:'minutely',2:'hourly',3:'daily',4:'monthly',5:'yearly',
                       'min':1,'h':2,'D':3,'M':4,'Y':5,'H':2,'ME':4,'YE':5}
        self.pandas_tcodes = {1:'min',2:'h',3:'D',4:'ME',5:'YE'}
        self._clear_cache()
        if Map:
            self.map_hbn()

    def map_hbn(self):
        """
        Maps the HBN file contents using the fast Cython implementation if available,
        otherwise falls back to the pure Python implementation.
        """
        self._clear_cache()
        if hbn_cy:
            # Use the fast Cython implementation
            self.mapn, self.mapd, self.data = hbn_cy.map_hbn_file(self.file_name)
        else:
            # Fallback to slow Python implementation (from your original file)
            with open(self.file_name, 'rb') as f:
                self.data = f.read()

            if not self.data or self.data[0] != 0xFD:
                print('BAD HBN FILE - must start with magic number 0xFD')
                return
            
            data_view = memoryview(self.data)
            mapn = defaultdict(list)
            mapd = defaultdict(list)
            index = 1
            while index < len(data_view):
                if index + 28 > len(data_view): break
                rc1, rc2, rc3, rc, rectype, operation_bytes, id, activity_bytes = unpack('4BI8sI8s', data_view[index:index + 28])
                reclen = (rc * 4194304) + (rc3 * 16384) + (rc2 * 64) + (rc1 >> 2) - 24
                operation = operation_bytes.decode('ascii', 'ignore').strip()
                activity = activity_bytes.decode('ascii', 'ignore').strip()

                if rectype == 1:
                    if index + 36 > len(data_view): break
                    tcode = unpack('I', data_view[index + 32: index + 36])[0]
                    mapd[operation, id, activity, tcode].append((index, reclen))
                elif rectype == 0:
                    i = index + 28
                    slen = 0
                    while slen < reclen:
                        if i + slen + 4 > len(data_view): break
                        ln = unpack('I', data_view[i + slen: i + slen + 4])[0]
                        if i + slen + 4 + ln > len(data_view): break
                        n = unpack(f'{ln}s', data_view[i + slen + 4: i + slen + 4 + ln])[0].decode('ascii', 'ignore').strip()
                        mapn[operation, id, activity].append(n.replace('-', ''))
                        slen += 4 + ln
                
                if reclen < 36: index += reclen + 29
                else: index += reclen + 30
            
            self.mapn = dict(mapn)
            self.mapd = dict(mapd)

    def read_data(self,operation,id,activity,tcode):
        dfname = f'{operation}_{activity}_{id:03d}_{tcode}'
        if dfname in self.data_frames:
            return self.data_frames[dfname]

        names = self.mapn.get((operation, id, activity))
        entries = self.mapd.get((operation, id, activity, tcode))
        if not names or not entries:
            return None
        nvals = len(names)

        if hbn_cy:
            # Use the fast Cython implementation
            times, rows = hbn_cy.read_data_entries(self.data, entries, nvals)
        else:
            # Fallback to slow Python implementation
            rows_list, times_list = [], []
            data_view = memoryview(self.data)
            for (index, reclen) in entries:
                if index + 56 + (4 * nvals) > len(data_view): continue
                yr, mo, dy, hr, mn = unpack('5I', data_view[index + 36: index + 56])
                try:
                    dt = datetime(yr, mo, dy, 0, mn) + timedelta(hours=hr-1)
                except ValueError:
                    continue # Skip bad date entries
                times_list.append(dt)
                row = unpack(f'{nvals}f', data_view[index + 56: index + 56 + (4 * nvals)])
                rows_list.append(row)
            times, rows = times_list, rows_list
        
        if not times: return None
        df = DataFrame(rows, index=times, columns=names).sort_index()

        if not df.empty:
            self.summaryindx.append(dfname)
            self.summary.append((operation, activity, str(id), self.tcodes[tcode], str(df.shape), df.index[0], df.index[-1]))
            self.output_dictionary[dfname] = names
            resampled_df = df.resample(self.pandas_tcodes[tcode]).mean()
            self.data_frames[dfname] = resampled_df
            return resampled_df
        else:
            return None
    
    def _clear_cache(self):
        self.data_frames = {}
        self.summary = []
        self.summarycols = ['Operation', 'Activity', 'segment', 'Frequency', 'Shape', 'Start', 'Stop']
        self.summaryindx = []
        self.output_dictionary = {}
    
    # ... (rest of your hbnClass methods like infer_opnids, get_time_series, etc. are unchanged) ...
    def infer_opnids(self,t_opn, t_cons,activity):
        result = [k[-2] for k,v in self.mapn.items() if (t_cons in v) & (k[0] == t_opn) & (k[-1] == activity)]
        if len(result) == 0:
            print('No Constituent-OPNID relationship found')
            return None
        return result
    
    def infer_activity(self,t_opn, t_cons):  
        result = [k[-1] for k,v in self.mapn.items() if (t_cons in v) & (k[0] == t_opn)]
        if len(result) == 0:
            print('No Constituent-Activity relationship found')
            return None
        assert(len(set(result)) == 1)
        return result[0]
    
    def get_time_series(self, t_opn, t_cons, t_code, opnid, activity = None):
        if isinstance(t_code,str):
            t_code = self.tcodes[t_code]
        if activity is None:
            activity = self.infer_activity(t_opn,t_cons)        
            if activity is None:
                return None
        df = self.read_data(t_opn,opnid,activity,t_code)
        if df is not None and t_cons in df.columns:
            series = df[t_cons].copy()
            series = series[series.index >= '1996-01-01']
            return series
        else:
            return None

    def get_multiple_timeseries(self,t_opn,t_code,t_con,opnids = None,activity = None):
        if isinstance(t_code,str):
            t_code = self.tcodes[t_code]
        if activity is None:
            activity = self.infer_activity(t_opn,t_con)
            if activity is None:
                return None
        if opnids is None:
            opnids = self.infer_opnids(t_opn,t_con,activity)
            if opnids is None:
                return None
        frames = []
        for opnid in opnids:
            series = self.get_time_series(t_opn,t_con,t_code,opnid,activity)
            if series is not None:
                frames.append(series.rename(opnid))
        if len(frames) > 0:
            return pd.concat(frames,axis=1)
        return None
    
    def output_names(self):
        activities = set([k[-1] for k,v in self.mapn.items()])
        dic = {}
        for activity in activities:
            t_cons = [v for k,v in self.mapn.items() if k[-1] == activity]   
            dic[activity] = set([item for sublist in t_cons for item in sublist])
        return dic