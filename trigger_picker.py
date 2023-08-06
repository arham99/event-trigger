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
Input = Path(r"E:\SEML\DATA RAW MEQ\2022 11\raw315")
FileOutput = input('Insert your desired file name for the trigger output list (press ENTER for default): ')
if len(FileOutput) < 1:
    FileOutput='event_trigger'
###################################################### 
    
    
EventCounter=0
with open (FileOutput + '.dat', 'w') as file:
    for (EntryPath, DirChild, FileName) in os.walk(Input):
        if Path(EntryPath).stem in HourPath:
            WorkDir=PurePath(EntryPath)
            FilesName=glob.glob(os.path.join(WorkDir, '*BHZ.mseed'))
            st=Stream()
            for i in FilesName:
                st += read(i)
            #st.filter('bandpass', freqmin=10, freqmax=20)  # optional prefiltering ## for prefiltering 
            st2=st.copy()
            trig=trigger('recstalta',3, 1, st2, 4, sta=0.5, lta=15 ) ## be coutious of these parameters
            try:
                for i in trig:
                    time=UTCDateTime(i['time'])
                    sta=i['stations']
                    if len(sta) > 3:
                        EventCounter+=1
                        file.write("Event # {}| TIME : {} | STA : {} \n".format(EventCounter, time, sta))
                        print("Event # {}| TIME : {} | STA : {} \n".format(EventCounter, time, sta))
            except Exception:
                pass
