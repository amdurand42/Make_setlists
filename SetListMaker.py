import pandas as pd
import numpy as np

import SetListMaker_functions as sf

#Uncomment this next line if want every column to show when print the setlists
pd.set_option('display.expand_frame_repr', False)

#Loading in the csv file. Has already been massaged
df_orig = pd.read_csv('SongListData.csv')

#Stripping the left and right whitespace from all csv entries
df_orig.columns = df_orig.columns.str.strip()
df_orig = df_orig.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

#Testing a sort by length of song - it works!
df_orig = df_orig.sort_values('Length (~)')

#Convert timestamps to seconds    
df_orig['Length (~)'] = df_orig['Length (~)'].apply(sf.get_sec)

print(sf.get_max_min(sum(df_orig['Length (~)'])))

#Make a copy of the original setlist to grab individual songs from
dfcopy = df_orig.copy()

#Checking the database
#print(df_orig.head())

SetList1, df_songsleft, total_time1 = sf.Setlist_55min(dfcopy, 1)
SetList2, df_songsleft, total_time2 = sf.Setlist_55min(df_songsleft, 2)
SetList3, df_finalsongsleft, total_time3 = sf.Setlist_55min(df_songsleft, 3)

print(SetList1)
print(total_time1)

print(SetList2)
print(total_time2)

print(SetList3)
print(total_time3)

