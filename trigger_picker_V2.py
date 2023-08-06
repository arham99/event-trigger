#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 12:10:30 2022

@author: arhamze
"""
from pathlib import PurePath, Path
from obspy import read, Trace, Stream, UTCDateTime
from obspy.signal.trigger import coincidence_trigger as trigger
import os, glob
from pprint import pprint

HourPath=["00","01","02","03","04","05","06","07","08","09","10","11","12"
           ,"13","14","15","16","17","18","19","20","21","22","23"]

########################################################
#Input and output path 
Input = Path(r"E:\SEML\DATA RAW MEQ\RAW DATA 2023\2023 06\raw181")
FileOutput = input('Insert your desired file name for the trigger output list (press ENTER for default): ')
FileOutput2=FileOutput
if len(FileOutput) < 1:
    FileOutput='event_trigger'
###################################################### 
EventCounter=0
with open (FileOutput + '.dat', 'w') as file1, open (FileOutput2 + '_trigger.pick', 'w') as file2:
    for (EntryPath, DirChild, FileName) in os.walk(Input):
        if Path(EntryPath).stem in HourPath:
            WorkDir=PurePath(EntryPath)
            FilesName=glob.glob(os.path.join(WorkDir, '*BHZ.mseed'))
            st=Stream()
            for i in FilesName:
                st += read(i)
            #st.filter('bandpass', freqmin=10, freqmax=20)  # optional prefiltering ## for prefiltering 
            st2=st.copy()
            trig=trigger('recstalta',2.5, 1.5, st2, 4, sta=0.4, lta=7 ) ## be coutious of these parameters
            try:
                for i in trig:
                    time=UTCDateTime(i['time'])
                    date=str(time.date)
                    date_split=date.split('-')
                    date2=''.join(date_split)
                    HH=f"{time.hour:02d}";MM=f"{time.minute:02d}";SS=f"{time.second:02d}";MSS=time.microsecond
                    HHMM=str(HH)+str(MM)
                    second_fix=SS+'.'+str(MSS)
                    sta=i['stations']
                    sta.sort()
                    if len(sta) >=4 :
                        EventCounter+=1
                        file1.write("Event # {}| TIME : {} | STA : {} \n".format(EventCounter, time, sta))
                        print("Event # {}| TIME : {} | STA : {} \n".format(EventCounter, time, sta))
                        try:
                            for x in sta:
                                file2.write("%s %s %s %s %s %s %8i %4s %11.8f %s %3.8f %3.1f %.5f %3.1f\n" % (x,'?','BHZ','i',
                                'P','c',int(date2),HHMM,float(second_fix),'GAU',0.0, 0.0 , 0.0, 
                                0.0 )) # writing file according to the format
                        except Exception:
                            pass
                    file2.write('\n')
            except Exception:
                pass
