# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:03:52 2021

@author: -
"""

def remove_dodgy_data(all_data): 
    
    #identify all the rows in dataframe where there are nan (infinite values)
    rows = all_data.index[np.isnan(all_data.drop('Month', axis=1)).any(1)]     

    #create an empty list to store dodgy rows which are either 1 second before or after a period when the hydrophone stopped (missing data)
    dodge_rows = []

    #loop through the rows where there are missing data and find times when hydrophone stopped/started recording 
    for i in range (0, len(rows)-1): 
        #print(rows[i])

        #point where the hydrophone stopped  recording 
        if (rows[i+1]-rows[i] != 1): 
            if (rows[i]+2) not in dodge_rows: 
                dodge_rows.append(rows[i]+2)
            if (rows[i]+1) not in dodge_rows:  
                dodge_rows.append(rows[i]+1)

        #point where hydrophone restarted recording 
        if (rows[i]-rows[i-1]) != 1:
            if (rows[i]-2) not in dodge_rows: 
                dodge_rows.append(rows[i]-2)
            if (rows[i]-1) not in dodge_rows: 
                dodge_rows.append(rows[i]-1)

    #include the dodgy values 1 second after the last period of missing data, not included in above range
    dodge_rows.append(rows[len(rows)-1]+1)
    dodge_rows.append(rows[len(rows)-1]+2)

    #new dataframe does not include data points before or after a period of missing hydrophone data or any missing data (nan) values
    clean_data = all_data 
    for i in range(0, len(dodge_rows)): 
        clean_data = clean_data.drop(dodge_rows[i])

    #remove nan values 
    clean_data.dropna(inplace=True)
    return clean_data