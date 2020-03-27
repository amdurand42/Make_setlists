import pandas as pd
import numpy as np

'''
FUNCTION: get_min
Converts seconds variable to minutes and rounds up
'''
def get_max_min(total_seconds):
    
    #A clever way to get the ceiling of total seconds divided by 60
    minutes = str((total_seconds + 59)//60)
    #seconds = str(total_seconds%60)
    
    return minutes


'''
FUNCTION: get_sec
Converts 'Length (~)' column to seconds (from minutes:seconds)
1) Go through each timestamp in the length column and convert it to seconds
2) Save the database this way
'''
def get_sec(time_str):
    minutes, sec = time_str.split(':')
    return int(minutes) * 60 + int(sec)

'''
FUNCTION: check_vamp
Checks if a song is a vamp, returns True if it is, False if it isn't
'''
def check_vamp(song):
    if song['Vamp'].str.contains('y').any():
        return True
    else:
        return False
    
'''
FUNCTION: check_tempochange
Checks if a song has a tempo change and if it follows another 
song with a tempo change, returns True if it does, False if it doesn't
'''    
def check_tempochange(prev_song, song):
    if (prev_song['Tempo 2'].isnull().values.any()) | (song['Tempo 2'].isnull().values.any()):
        return False
    else:
        return True
    
'''
FUNCTION: check_genre
Checks if there are not more than two songs with the same genre back-to-back
'''
#def check_genre(2ndprev_song, prev_song, song):
    
    
'''
FUNCTION: Setlist_55min
Makes a setlist that is ~55 minutes long
'''
def Setlist_55min(dfcopy, set_num):

    total_time = 0 #initialize the total time of the set list to 0
    set_time_min = 2880
    set_time_max = 3360
    first_song = True
    
    #Make an empty SetList with the column names of the original song list
    SetList = pd.DataFrame(columns=dfcopy.columns)

    while True:
        
        #Randomly select a song
        song = dfcopy.sample()         
        
        #Ensures that the first song is a vamp
        if first_song:
            num_iter = 0
            while (check_vamp(song) is False):
                if num_iter > 100:
                    print("No more vamp songs left, proceeding with a non-vamp song (first song)")
                    break
                song = dfcopy.sample() 
                num_iter += 1                      
        
        if first_song is False:
            #identifies the previous song
            prev_song = SetList.iloc[[-1]]
            #Checks that no two songs with tempo changes are together
            while (check_tempochange(prev_song, song) is True):
                song = dfcopy.sample() 
            #Note that this fails when it's trying to pick a final song that also vamps for the setlist
            
        first_song = False #only needed to know this to check vamp
        
        #Add the song length to total_time
        total_time += int(song['Length (~)'])

        # If it is less than 3060, append the song name to a new database (SetList). Remove that song from the parent database. Go back to step 1 and repeat
        if total_time < set_time_min:
            SetList = SetList.append(song)
            dfcopy = dfcopy.drop(song.index) 
            if dfcopy.empty:
                break
            continue
    
        #If it is more than 3540, don't add it to the SetList. Go back to step 1 and repeat
        elif total_time > set_time_max:
            #dfcopy = dfcopy.drop(song.index)
            
            if set_num == 3:
                SetList = SetList.append(song)
                break
            
            total_time -= int(song['Length (~)'])
            continue
 
    #If it is more than 3060 and less than 3540, then append the song. Break the loop.
        else:           
            #ensures that the last song is a vamp
            num_iter = 0
            while (check_vamp(song) is False):
                if num_iter > 100:
                    print("No more vamp songs left, proceeding with a non-vamp song (last song)")
                    break
                song = dfcopy.sample() 
                num_iter += 1    
                       
            SetList = SetList.append(song)
            dfcopy = dfcopy.drop(song.index)
            break
    #End of while loop
    
    time_str = get_max_min(total_time)
            
    
    return(SetList, dfcopy, time_str)
        
