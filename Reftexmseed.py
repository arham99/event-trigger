 # -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 08:34:41 2020

@author: Rendy Delliansyah  ST., MT.
"""

from pathlib import Path,WindowsPath,PurePath
from obspy import read,UTCDateTime
import os,glob
from multiprocessing import Process, Pool
from obspy.core import Stream, read

def trace(st,Input,dirr,Station):
    for tr in st:
        chan = tr.stats.channel[-1]
        chan_map = {
            "Z": "BHZ",
            "N": "BHN",
            "E": "BHE"}
        tr.stats.channel = chan_map[chan]
        tr.stats.station = Station[dirr.parts[len(dirr.parts)-2]]
    return st
            
def write(save,st2,dirr):
    for component in ["Z", "N", "E"]:
        this_st = st2.select(component=component)
        s=this_st[0].stats
        filename = (f"{s.station}_({dirr.parts[len(dirr.parts)-2]})_{s.network}_{s.starttime.year}"
                    f"{s.starttime.month:>02}{s.starttime.day:>02}"
                    f"_{s.starttime.hour:>02}{s.starttime.minute:>02}"
                    f"{s.starttime.second:>02}_{s.channel}.mseed")
        
        Year=(f'{s.starttime.year}')
        fol=(f"{s.starttime.year}{s.starttime.month:>02}{s.starttime.day:>02}"
              f"_{s.starttime.julday:>03}/{s.starttime.hour:>02}")
    
        foldername=os.path.join(save,Year,fol)
        if not os.path.exists(foldername):
            os.makedirs(os.path.join(foldername))   
        
        this_st.write(os.path.join(foldername,filename), format="mseed")
    return s
    

# Input=Path(r"D:\PYTHON
Input=Path(r"E:\SEML\DATA RAW MEQ\RAW DATA 2023\2023 06\raw181\001_Raw")

# save=Path(r"D:\PYTHON")
save=Path(r"E:\SEML\DATA RAW MEQ\RAW DATA 2023\2023 06\raw181\002_Convert")

listOfFile=sorted([((aa.split(".")[0]),aa) for aa in os.listdir(Input)])

Station=dict(
        AD13 = 'ML01' ,
        B211 = 'ML02' , ### ganti kode sensor sebelumnya A022
        B4AC = 'ML03' ,  
        AD26 = 'ML04' ,   
        AD1A = 'ML05' ,      
        B4BC = 'ML06' ,
        B48F = 'ML07' ,  
        AD16 = 'ML08' ,  
        AD14 = 'ML09' ,  
        B207 = 'ML10' ,   
        B4A5 = 'ML11' ,  
        B262 = 'ML12' ,   
        B492 = 'ML13' ,   
        AD17 = 'ML14' ,
        B48E = 'ML15'
        )

# ab=dict(M10b  = '33. MEQ_17-12 Des 2013' , M15b  = '31. MEQ_21-15 Nov 2013' ,
#        M16b1  = '8. MEQ_03-28 Des 2012'  , M16c  = '33. MEQ_17-12 Des 2013' ,
#        )

# for ix in ab:
   # globals()[ix]=[ii for ii, tupl in enumerate(listOfFile) if tupl[1] ==ab[ix]]
# lstdir=[]    
i=0
for entry in range(len(listOfFile)):
    fullPath = Path.joinpath(Input,listOfFile[entry][1])  
    for (dirpath, dirnames, filenames) in os.walk(fullPath):
        if Path(dirpath).stem=='1' and len(Path(dirpath).parts)>len(fullPath.parts):
            dirr=PurePath(dirpath)
            # lstdir.append(dirr)           
            # if dirr.parts[len(dirr.parts)-2]=='B14E':# or dirr.parts[len(dirr.parts)-2]=='B4BD' or \
                # dirr.parts[len(dirr.parts)-2]=='AD16' or dirr.parts[len(dirr.parts)-2]=='B13C' :
                        
            # if entry>= list(M10b)[0]:
            #     Station['AD16']='M10b' 
            
            # if entry>= list(M15b)[0]:
            #     Station['B4BD'] ='M15b' 
                
            # # if entry>= list(M16b1)[0]:
            # #     Station['B13C'] ='M16b' 
                
   
            # if entry>= list(M16c)[0]:
            #     Station['B48E'] ='M16c'
                
            # for dire in range(0,1):#lstdir:   
            stt =Stream()   
            for file in range(0,len(filenames)):# filenames:
                if '0036EE80' in filenames[file]:
                    if  any('0000000' in s for s in filenames)==False : 
                        try:
                            stt +=read(os.path.join(dirr,filenames[file]),network="ML", location="",
                                      component_codes="ZNE")                             
                            stt.sort(['starttime'])    
                            # stt.merge(method=1, fill_value=0)
                            stt=trace(stt,Input,dirr,Station)
                   
                                                        
                            min_date = min(tr.stats.starttime for tr in stt)
                            max_date = max(tr.stats.endtime for tr in stt)
                            min_date = UTCDateTime(min_date.year, min_date.month, min_date.day,min_date.hour)
                            max_date = UTCDateTime(max_date.year, max_date.month, max_date.day,max_date.hour)
        
                            while min_date <= max_date:
                                stt1 = stt.slice(min_date, min_date + 3600)
                                if not len(stt1):
                                    continue
                                min_date += 3600
                                
                                s=write(save,stt1,dirr)
                                                   
                            print(f"{i} | {dirr.parts[len(dirr.parts)-3]}|{dirr.parts[len(dirr.parts)-4]}|{dirr.parts[len(dirr.parts)-2]}| {filenames[file]} "
                                      f"Tahun: {s.starttime.year} Bulan: {s.starttime.month:>02} Tanggal: {s.starttime.day:>02} "
                                  f"Jam: {(s.starttime.hour):>02}") 
                        except:
                            continue     

                    else:
                        try:
                            st =read(os.path.join(dirr,filenames[file]),network="ML", location="",
                                      component_codes="ZNE") 

                            st2=trace(st,Input,dirr,Station)
                            s=write(save,st2,dirr)
                            print(f"{i} | {dirr.parts[len(dirr.parts)-3]}|{dirr.parts[len(dirr.parts)-4]}|{dirr.parts[len(dirr.parts)-2]}| {filenames[file]} "
                                      f"Tahun: {s.starttime.year} Bulan: {s.starttime.month:>02} Tanggal: {s.starttime.day:>02} "
                                      f"Jam: {s.starttime.hour:>02}")  
                        except:
                            continue
                elif '0036EE80' not in filenames[file]:
                    if  any('0000000' in s for s in filenames)==True :
                        try:
                            stt +=read(os.path.join(dirr,filenames[file]),network="ML", location="",
                                      component_codes="ZNE")                             
                            stt.sort(['starttime'])    
                            # stt.merge(method=1, fill_value=0)
                            stt=trace(stt,Input,dirr,Station)
                            min_date = min(tr.stats.starttime for tr in stt)
                            max_date = max(tr.stats.endtime for tr in stt)
                            min_date = UTCDateTime(min_date.year, min_date.month, min_date.day,min_date.hour)
                            max_date = UTCDateTime(max_date.year, max_date.month, max_date.day,max_date.hour)
        
                            while min_date <= max_date:
                                stt1 = stt.slice(min_date, min_date + 3600)
                                if not len(stt1):
                                    continue
                                min_date += 3600
                                
                                s=write(save,stt1,dirr)
                                                   
                            print(f"{i} | {dirr.parts[len(dirr.parts)-3]}|{dirr.parts[len(dirr.parts)-4]}|{dirr.parts[len(dirr.parts)-2]}| {filenames[file]} "
                                      f"Tahun: {s.starttime.year} Bulan: {s.starttime.month:>02} Tanggal: {s.starttime.day:>02} "
                                  f"Jam: {(s.starttime.hour):>02}") 
                        except:
                            continue     
                    


                i =i+1
