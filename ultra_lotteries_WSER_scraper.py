# This script collects data on lottery participants for WSER

# Importing required modules

import pandas as pd
import urllib
from bs4 import BeautifulSoup as bs

# Defining username + filepath for saving output :: update accordingly!

username = ''
direc = 'C:/Users/' + username + '/Documents/Data/ultra_lotteries/'

# Getting the data

year = []
last = []
first = []
gender = []
age = []
state = []
count = []

start = [11,12,13,14,14,14,14,15,0,15,16]
end = [-2,-2,-2,-1,-1,-1,-1,-1,0,-1,-1]

lid = [0,0,0,1,1,1,1,1,0,1,1]
fid = [1,1,1,2,2,2,2,2,0,2,2]
gid = [2,2,2,3,3,3,3,3,0,3,3]
aid = [3,3,3,4,4,4,4,4,0,0,0]
sid = [4,4,4,5,5,5,5,5,0,4,4]
cid = [5,5,6,7,7,7,7,7,0,6,6]

for y in range(2013,2024):
    
    try:
        
        url = 'https://www.wser.org/lottery' + str(y) + '.html' # Define url
        page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'}) # Request page
        response = urllib.request.urlopen(page) # Open page
        soup = bs(response, 'html.parser') # Get data from the page
        data = soup.find_all('tr') # Get all appropriate data type
        data = data[start[y-2013]:end[y-2013]] # Drop non-relevant data
        
        # Extraction loop
        
        for dat in data:
            
            d = dat.find_all('td')
            year.append(y)
            last.append(d[lid[y-2013]])
            first.append(d[fid[y-2013]])
            gender.append(d[gid[y-2013]])
            state.append(d[sid[y-2013]])
            count.append(d[cid[y-2013]])
            
            if y < 2021:
                
                age.append(d[aid[y-2013]])
                
            else:
                
                age.append(None)
                
    except:
        
        continue

# Clean text / remove tags

last = [str(l)[4:-5] if l != None else None for l in last]
first = [str(f)[4:-5] if f != None else None for f in first]
gender = [str(g)[4:-5] if g != None else None for g in gender]
age = [str(a)[4:-5] if a != None else None for a in age]
state = [str(s)[4:-5] if s != None else None for s in state]
count = [str(c)[4:-5] if c != None else None for c in count]

# Make data into a dataframe

year = pd.Series(year, name = 'Year')
last = pd.Series(last, name = 'Last Name')
first = pd.Series(first, name = 'First Name')
gender = pd.Series(gender, name = 'Gender')
age = pd.Series(age, name = 'Age')
state = pd.Series(state, name = 'State')
count = pd.Series(count, name = 'Tickets')

df = pd.concat([year,last,first,gender,age,state,count], axis = 1)

# Saving WSER lottery data to file

df.to_csv(direc + 'data/WSER.csv', index = False)

