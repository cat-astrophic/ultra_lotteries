# This script matches runners in WSER lottery to ultradata set

# Importing required modules

import pandas as pd
import datetime
import addfips
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Defining username + filepath for saving output :: update accordingly!

username = ''
direc = 'C:/Users/' + username + '/Documents/Data/ultra_lotteries/'

# Read in the data

wser = pd.read_csv(direc + 'data/WSER.csv')
ultra = pd.read_csv(direc + 'data/raw_results_data.csv')
alt_data = pd.read_csv(direc + 'data/altitude_data.csv')
coords = pd.read_csv(direc + 'data/latlong.csv')
inc_data = pd.read_csv(direc + 'data/Income.csv')
edu_data = pd.read_csv(direc + 'data/Education.csv')
emp_data = pd.read_csv(direc + 'data/Unemployment.csv')
pop_data = pd.read_csv(direc + 'data/PopulationEstimates.csv')

# Matching naming conventions across data sets

names = [wser['First Name'][x] + ' ' + wser['Last Name'][x] for x in range(len(wser))]
wser = pd.concat([wser, pd.Series(names, name = 'Name')], axis = 1)

# Race gender count variables

ms = []
fs = []

race_years = [ultra.RACE_Name[i] + ultra.RACE_Distance[i] + str(ultra.RACE_Year[i]) for i in range(len(ultra))]

ultra = pd.concat([ultra, pd.Series(race_years, name = 'RY')], axis = 1)

for i in range(len(ultra)):
    
    tmp = ultra[ultra.RY == ultra.RY[i]]
    tmpf = tmp[tmp.Gender == 'F']
    tmpm = tmp[tmp.Gender == 'M']
    fs.append(len(tmpf))    
    ms.append(len(tmpm))

ultra = pd.concat([ultra, pd.Series(fs, name = 'F_Count'), pd.Series(ms, name = 'M_Count')], axis = 1)

# Matching runners

runner_ids = []

for i in range(len(wser)):
    
    tmp = ultra[ultra.Name == wser.Name[i]] # Subset for runner name
    tmp = tmp[tmp.State == wser.State[i]].reset_index(drop = True) # Subset for runner state
    tmp = tmp[abs(tmp.Age - wser.Age[i]) < 3].reset_index(drop = True) # Subset for runner age
    
    if len(list(set(list(tmp.Runner_ID)))) == 1: # Check for # of Runner_IDs
        
        runner_ids.append(tmp.Runner_ID[0])
        
    else:
        
        runner_ids.append(None)

# Determining who ran WSER that year

competed = []

for i in range(len(wser)):
    
    try:
        
        tmp = ultra[ultra.Runner_ID == runner_ids[i]]
        tmp = tmp[tmp.RACE_Year == wser.Year[i]]
        
        if 'Western States' in list(tmp.RACE_Name):
            
            competed.append(1)
            
        else:
            
            competed.append(0)
            
    except:
        
        competed.append(None)

noncompete = [abs(1-c) if c != None else None for c in competed]

# Defining the outcomes

# Which rows in ultra to keep

keeps = []

for i in range(len(ultra)):
    
    if ultra.Runner_ID[i] in runner_ids:
        
        keeps.append(1)
        
    else:
        
        keeps.append(0)

# Subsetting ultra to save space

keep_ids = [i for i in range(len(keeps)) if keeps[i] == 1]

ultra = ultra[ultra.index.isin(keep_ids)].reset_index(drop = True)

# Creating a columns for race date

def month(s):
    
    l = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    m = l.index(s) + 1
    
    return m

rdate = [datetime.date(ultra.RACE_Year[i], month(ultra.RACE_Month[i]), ultra.RACE_Date[i]) for i in range(len(ultra))]
ultra = pd.concat([ultra, pd.Series(rdate, name = 'Date')], axis = 1)

# Creating lists of unique runners and races

runners = list(ultra.Runner_ID.unique())
races = list(ultra.RACE_Name.unique())

# Getting runner counties and fips and race counties

af = addfips.AddFIPS()
geolocator = Nominatim(user_agent = 'geoapiExercises')

runner_counties = []
runner_fips = []
race_counties = []

def county_finder(loc):
    
    locs = loc.split(', ')
    xxx = ['County' in l for l in locs]
    yyy = [i for i in range(len(xxx)) if xxx[i] == True]
    c = locs[min(yyy)]
    
    return c

for runner in runners:
    
    tmp = ultra[ultra.Runner_ID == runner].reset_index(drop = True)
    
    try:
        
        loc = geolocator.geocode(tmp.City[0] + ', ' + tmp.State[0])
        runner_counties.append(county_finder(loc[0]))
        runner_fips.append(af.get_county_fips(county_finder(loc[0]), tmp.State[0]))
        
    except:
        
        runner_counties.append(None)
        runner_fips.append(None)

for race in races:
    
    tmp = ultra[ultra.RACE_Name == race].reset_index(drop = True)
    
    try:
        loc = geolocator.geocode(tmp.RACE_City[0] + ', ' + tmp.RACE_State[0])
        race_counties.append(county_finder(loc[0]))
        
    except:
        
        race_counties.append(None)

ultra_rnr_counties = [runner_counties[runners.index(ultra.Runner_ID[i])] for i in range(len(ultra))]
ultra_rnr_fips = [runner_fips[runners.index(ultra.Runner_ID[i])] for i in range(len(ultra))]
ultra_race_counties = [race_counties[races.index(ultra.RACE_Name[i])] for i in range(len(ultra))]

ultra_rnr_counties = pd.Series(ultra_rnr_counties, name = 'County')
ultra_rnr_fips = pd.Series(ultra_rnr_fips, name = 'FIPS')
ultra_race_counties = pd.Series(ultra_race_counties, name = 'RACE_County')

ultra = pd.concat([ultra, ultra_rnr_counties, ultra_rnr_fips, ultra_race_counties], axis = 1)

# Gender place percentage

def gpp_fx(row):
    
    if row.Gender == 'F':
        
        p = row.Gender_Place / row.F_Count
        
    elif row.Gender == 'M':
        
        p = row.Gender_Place / row.M_Count
        
    else:
        
        p = None
        
    if p > 1:
        
        p = None
    
    return p

gpp = [gpp_fx(ultra.iloc[i]) for i in range(len(ultra))]
ultra = pd.concat([ultra, pd.Series(gpp, name = 'GPP')], axis = 1)

# Dates

lottery_dates = [datetime.date(2013,12,5), datetime.date(2014,12,4), datetime.date(2015,12,2),
                 datetime.date(2016,12,2), datetime.date(2017,12,1)]

race_dates = [datetime.date(2014,6,28), datetime.date(2015,6,27), datetime.date(2016,6,25),
              datetime.date(2017,6,24), datetime.date(2018,6,23)]

# Adding USGS altitude data to ultra

rnr_alts = []
race_alts = []

for i in range(len(ultra)):
    
    print(i)
    
    try:
        
        runner_c = ultra.County[i].replace(' County', '')
        runner_s = ultra.State[i]
        
    except:
        
        runner_c = None
        runner_s = None
    
    try:
        
        race_c = ultra.RACE_County[i].replace(' County', '')
        race_s = ultra.RACE_State[i]
        
    except:
        
        race_c = None
        race_s = None
    
    try:
        
        alt_tmp = alt_data[alt_data.County == runner_c]
        alt_tmp = alt_tmp[alt_tmp.State == runner_s].reset_index(drop = True)
        rnr_alts.append(alt_tmp.ALtitude[0])
        
    except:
        
        rnr_alts.append(None)
        
    try:
        
        alt_tmp = alt_data[alt_data.County == race_c]
        alt_tmp = alt_tmp[alt_tmp.State == race_s].reset_index(drop = True)
        race_alts.append(alt_tmp.ALtitude[0])
        
    except:
        
        race_alts.append(None)

ultra = pd.concat([ultra, pd.Series(rnr_alts, name = 'Runner_Altitude'), pd.Series(race_alts, name = 'RACE_Altitude')], axis = 1)

# Adding travel distance to ultra

# Creating a matching location key to get county coordinate data

def key_fx(row):
    
    state_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
                   'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
                   'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
                   'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    
    state_names = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
                    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
                    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 
                    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
                    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
                    'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                    'West Virginia', 'Wisconsin', 'Wyoming']
    
    try:
        
        rnr_key = row.County.replace(' County', '') + ', ' + state_names[state_codes.index(row.State)] + ', US'
        
    except:
        
        rnr_key = None
        
    try:
        
        race_key = row.RACE_County.replace(' County', '') + ', ' + state_names[state_codes.index(row.RACE_State)] + ', US'
        
    except:
        
        race_key = None
    
    return rnr_key, race_key

rnr_keys = [key_fx(ultra.iloc[i])[0] for i in range(len(ultra))]
race_keys = [key_fx(ultra.iloc[i])[1] for i in range(len(ultra))]

ultra = pd.concat([ultra, pd.Series(rnr_keys, name = 'Key'), pd.Series(race_keys, name = 'RACE_Key')], axis = 1)

# Getting runner and race coordinates

rnr_lats = []
rnr_lons = []
race_lats = []
race_lons = []

for i in range(len(ultra)):
    
    try:
        
        tmp = coords[coords.Combined_Key == ultra.Key[i]].reset_index(drop = True)
        
        rnr_lats.append(tmp.Lat[0])
        rnr_lons.append(tmp.Long_[0])
        
    except:
        
        rnr_lats.append(None)
        rnr_lons.append(None)
        
    try:
        
        tmp = coords[coords.Combined_Key == ultra.RACE_Key[i]].reset_index(drop = True)
        
        race_lats.append(tmp.Lat[0])
        race_lons.append(tmp.Long_[0])
        
    except:
        
        race_lats.append(None)
        race_lons.append(None)

rnr_lats = pd.Series(rnr_lats, name = 'Lat')
rnr_lons = pd.Series(rnr_lons, name = 'Lon')
race_lats = pd.Series(race_lats, name = 'RACE_Lat')
race_lons = pd.Series(race_lons, name = 'RACE_Lon')

ultra = pd.concat([ultra, rnr_lats, rnr_lons, race_lats, race_lons], axis = 1)

# Calculating the travel distances using geodesic and lats and lons

travel_dists = []

for i in range(len(ultra)):
    
    try:
        
        dist = geodesic((ultra.Lat[i],ultra.Lon[i]),(ultra.RACE_Lat[i],ultra.RACE_Lon[i])).miles
        
    except:
        
        dist = None
    
    travel_dists.append(dist)

ultra = pd.concat([ultra, pd.Series(travel_dists, name = 'Travel_Distance')], axis = 1)

# Adding socioeconomic controls data to ultra

ifips = [str(f) if f > 9999 else '0' + str(f) for f in inc_data.countyid]
inc_data = pd.concat([inc_data, pd.Series(ifips, name = 'FIPS')], axis = 1)

pfips = [str(f) if f > 9999 else '0' + str(f) for f in pop_data.FIPStxt]
pop_data = pd.concat([pop_data, pd.Series(pfips, name = 'FIPS')], axis = 1)

efips = [str(f) if f > 9999 else '0' + str(f) for f in edu_data.fips]
edu_data = pd.concat([edu_data, pd.Series(efips, name = 'FIPS')], axis = 1)

ufips = [str(f) if f > 9999 else '0' + str(f) for f in emp_data.fips]
emp_data = pd.concat([emp_data, pd.Series(ufips, name = 'FIPS')], axis = 1)

edu_hs = [] # percenthsgrad_YYYY -- relative to no HS (2 categories)
edu_sc = [] # percentsomecollege_YYYY -- relative to no HS (2 categories)
edu_ass = [] # percentassociates_YYYY -- relative to no HS (2 categories)
edu_bs = [] # percentbachelors_YYYY -- relative to no HS (2 categories)
edu_grad = [] # percentgrad_degree_YYYY -- relative to no HS (2 categories)
pop = []
inc = []
unemp = []

for i in range(len(ultra)):
    
    try:
        
        itmp = inc_data[inc_data.FIPS == ultra.FIPS[i]]
        itmp = itmp[itmp.year == ultra.RACE_Year[i]].reset_index(drop = True)
        inc.append(itmp.medianhouseholdincome[0])
        
    except:
        
        inc.append(None)
        
    try:
        
        utmp = emp_data[emp_data.FIPS == ultra.FIPS[i]]
        utmp = utmp[utmp.year == ultra.RACE_Year[i]].reset_index(drop = True)
        unemp.append(float(utmp.unemploymentrate[0]))
        
    except:
        
        unemp.append(None)
        
    try:
        
        cname = 'POP_ESTIMATE_' + str(ultra.RACE_Year[i])
        ptmp = pop_data[pop_data.FIPS == ultra.FIPS[i]].reset_index(drop = True)
        pop.append(int(ptmp[cname][0].replace(',','')))
        
    except:
        
        pop.append(None)
        
    try:
        
        c1 = 'percenthsgrad_' + str(ultra.RACE_Year[i])
        c2 = 'percentsomecollege_' + str(ultra.RACE_Year[i])
        c3 = 'percentassociates_' + str(ultra.RACE_Year[i])
        c4 = 'percentbachelors_' + str(ultra.RACE_Year[i])
        c5 = 'percentgrad_degree_' + str(ultra.RACE_Year[i])
        etmp = edu_data[edu_data.FIPS == ultra.FIPS[i]].reset_index(drop = True)
        edu_hs.append(etmp[c1][0])
        edu_sc.append(etmp[c2][0])
        edu_ass.append(etmp[c3][0])
        edu_bs.append(etmp[c4][0])
        edu_grad.append(etmp[c5][0])
        
    except:
        
        edu_hs.append(None)
        edu_sc.append(None)
        edu_ass.append(None)
        edu_bs.append(None)
        edu_grad.append(None)

edu_hs = pd.Series(edu_hs, name = 'Edu_High_School')
edu_sc = pd.Series(edu_sc, name = 'Edu_Some_College')
edu_ass = pd.Series(edu_ass, name = 'Edu_Associate')
edu_bs = pd.Series(edu_bs, name = 'Edu_Bachelor')
edu_grad = pd.Series(edu_grad, name = 'Edu_Grad_Degree')
pop = pd.Series(pop, name = 'Population')
inc = pd.Series(inc, name = 'Median_Household_Income')
unemp = pd.Series(unemp, name = 'Unemployment_Rate')

ultra = pd.concat([ultra, edu_hs, edu_sc, edu_ass, edu_bs, edu_grad, pop, inc, unemp], axis = 1)

# Creating the output data set

# Initializing data storage

years = []
covid = []
rnr_ids = []
rnr_names = []
rnr_cities = []
rnr_counties = []
rnr_states = []
rnr_nats = []
rnr_genders = []
rnr_ages = [] # event year (lottery or WSER)
rnr_fips = []
treated = []
treatment_type = [] # lottery or WSER
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
race_count_pre = []
race_count_post = []
mean_place_pre = []
mean_place_post = []
wins_pre = []
wins_post = []
win_pct_pre = []
win_pct_post = []
mean_pct_f_pre = []
mean_pct_f_post = []
mean_race_size_pre = []
mean_race_size_post = []
mean_race_alt_pre = []
mean_race_alt_post = []
mean_travel_dist_pre = []
mean_travel_dist_post = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []

# Helper functions

def t_type(idx):
    
    if idx == 0:
        
        tt = 'Lottery'
        
    else:
        
        tt = 'Race'
    
    return tt

def ticket_counter(n,y):
    
    fn = n.split(' ')[0]
    ln = n.split(' ')[1]
    wser_tmp = wser[wser.Year == y]
    wser_tmp = wser_tmp[wser['Last Name'] == ln]
    wser_tmp = wser_tmp[wser['First Name'] == fn].reset_index(drop = True)
    tc = wser_tmp.Tickets[0]
    
    return tc

def f_pct_fx(row):
    
    p = row.F_Count / row.RACE_Finisher_Count
    
    if p > 1:
        
        p = None
    
    return p

# Main loop

end_years = [2021, 2020, 2019, 2018, 2017]

for window in range(1,5): # For each window length (1-4 years)
    
    dates = [lottery_dates[window-1], race_dates[window-1]]
    
    for yr in range(2014,end_years[window]): # For each lottery/WSER instance
        
        for d in dates: # For each type (lottery/WSER)
            
            for runner in runners: # For each runner
                
                print('Window ' + str(window) + ' of 4 :: Year ' + str(yr) + ' :: Type ' + str(dates.index(d)+1) + ' :: Runner ' + str(runners.index(runner)+1) + ' of ' + str(len(runners)))
                
                check = wser[wser.Year == yr]
                rname = ultra[ultra.Runner_ID == runner].reset_index(drop = True)['Name'][0]
                
                if rname in list(check.Name):
                    
                    years.append(yr)
                    covid.append(int((d + datetime.timedelta(365*window)) > datetime.date(2020,3,1)))
                    rnr_ids.append(runner)
                    
                    tmp = ultra[ultra.Runner_ID == runner] # subset for runner
                    tmp = tmp[tmp.Date < (d + datetime.timedelta(365*window))] # remove races after window
                    tmp = tmp[tmp.Date > (d - datetime.timedelta(365*window))].reset_index(drop = True) # remove races before window
                    
                    try:
                        
                        rnr_names.append(tmp.Name[0])
                        
                    except:
                        
                        rnr_names.append(None)
                        
                    try:
                        
                        rnr_cities.append(tmp.City[0])
                        
                    except:
                        
                        rnr_cities.append(None)
                        
                    try:
                        
                        rnr_counties.append(tmp.County[0])
                        
                    except:
                        
                        rnr_counties.append(None)
                        
                    try:
                        
                        rnr_states.append(tmp.State[0])
                        
                    except:
                        
                        rnr_states.append(None)
                        
                    try:
                        
                        rnr_nats.append(tmp.Country[0])
                        
                    except:
                        
                        rnr_nats.append(None)
                        
                    try:
                        
                        rnr_genders.append(tmp.Gender[0])
                        
                    except:
                        
                        rnr_genders.append(None)
                        
                    try:
                        
                        rnr_ages.append(tmp.Age[0] + d.year - tmp.RACE_Year[0])
                        
                    except:
                        
                        rnr_ages.append(None)
                        
                    try:
                        
                        rnr_fips.append(tmp.FIPS[0])
                        
                    except:
                        
                        rnr_fips.append(None)
                        
                    tmpx = ultra[ultra.Runner_ID == runner]
                    tmpx = tmpx[tmpx.RACE_Year == yr].reset_index(drop = True)
                    
                    try:
                        
                        treated.append(int('Western States' in list(tmpx.RACE_Name)))
                        
                    except:
                        
                        treated.append(None)
                        
                    try:
                        
                        treatment_type.append(t_type(dates.index(d)))
                        
                    except:
                        
                        treatment_type.append(None)
                        
                    try:
                        
                        tickets.append(ticket_counter(tmp.Name[0],yr))
                        
                    except:
                        
                        tickets.append(None)
                        
                    try:
                        
                        window_len.append(window)
                        
                    except:
                        
                        window_len.append(None)
                        
                    pre = tmp[tmp.Date < d].reset_index(drop = True)
                    post = tmp[tmp.Date >= d].reset_index(drop = True)
                    
                    try:
                        
                        wser_pre.append(int('Western States' in list(pre.RACE_Name)))
                        
                    except:
                        
                        wser_pre.append(None)
                        
                    tmp2 = ultra[ultra.Runner_ID == runner]
                    tmp2 = tmp2[tmp2.Date < (d - datetime.timedelta(365*window))]
                    
                    try:
                        
                        rnr_races_before_pre.append(len(tmp2))
                        
                    except:
                        
                        rnr_races_before_pre.append(None)
                        
                    try:
                        
                        race_count_pre.append(len(pre))
                        
                    except:
                        
                        race_count_pre.append(None)
                        
                    try:
                        
                        race_count_post.append(len(post))
                        
                    except:
                        
                        race_count_post.append(None)
                        
                    try:
                        
                        mean_place_pre.append(pre.GPP.mean())
                        
                    except:
                        
                        mean_place_pre.append(None)
                        
                    try:
                        
                        mean_place_post.append(post.GPP.mean())
                        
                    except:
                        
                        mean_place_post.append(None)
                        
                    wpre = pre[pre.Gender_Place == 1]
                    wpost = post[post.Gender_Place == 1]
                    
                    try:
                        
                        wins_pre.append(len(wpre))
                        
                    except:
                        
                        wins_pre.append(None)
                        
                    try:
                        
                        wins_post.append(len(wpost))
                        
                    except:
                        
                        wins_post.append(None)
                        
                    try:
                        
                        win_pct_pre.append(len(wpre) / len(pre))
                        
                    except:
                        
                        win_pct_pre.append(None)
                        
                    try:
                        
                        win_pct_post.append(len(wpost) / len(post))
                        
                    except:
                        
                        win_pct_post.append(None)
                        
                    try:
                        
                        pre_f_list = [f_pct_fx(pre.iloc[i]) for i in range(len(pre))]
                        xpre_f_list = [x for x in pre_f_list if x != None]
                        mean_pct_f_pre.append(sum(xpre_f_list) / len(xpre_f_list))
                        
                    except:
                        
                        mean_pct_f_pre.append(None)
                        
                    try:
                        
                        post_f_list = [f_pct_fx(post.iloc[i]) for i in range(len(post))]
                        xpost_f_list = [x for x in post_f_list if x != None]
                        mean_pct_f_post.append(sum(xpost_f_list) / len(xpost_f_list))
                        
                    except:
                        
                        mean_pct_f_post.append(None)
                        
                    try:
                        
                        mean_race_size_pre.append(pre.RACE_Finisher_Count.mean())
                        
                    except:
                        
                        mean_race_size_pre.append(None)
                        
                    try:
                        
                        mean_race_size_post.append(post.RACE_Finisher_Count.mean())
                        
                    except:
                        
                        mean_race_size_post.append(None)
                        
                    try:
                        
                        mean_race_alt_pre.append(pre.RACE_Altitude.mean())
                        
                    except:
                        
                        mean_race_alt_pre.append(None)
                        
                    try:
                        
                        mean_race_alt_post.append(post.RACE_Altitude.mean())
                        
                    except:
                        
                        mean_race_alt_post.append(None)
                        
                    try:
                        
                        mean_travel_dist_pre.append(pre.Travel_Distance.mean())
                        
                    except:
                        
                        mean_travel_dist_pre.append(None)
                        
                    try:
                        
                        mean_travel_dist_post.append(post.Travel_Distance.mean())
                        
                    except:
                        
                        mean_travel_dist_post.append(None)
                        
                    try:
                        
                        con_hs.append(tmpx.Edu_High_School[0])
                        
                    except:
                        
                        con_hs.append(None)
                        
                    try:
                        
                        con_sc.append(tmpx.Edu_Some_College[0])
                        
                    except:
                        
                        con_sc.append(None)
                        
                    try:
                        
                        con_ass.append(tmpx.Edu_Associate[0])
                        
                    except:
                        
                        con_ass.append(None)
                        
                    try:
                        
                        con_bs.append(tmpx.Edu_Bachelor[0])
                        
                    except:
                        
                        con_bs.append(None)
                        
                    try:
                        
                        con_grad.append(tmpx.Edu_Grad_Degree[0])
                        
                    except:
                        
                        con_grad.append(None)
                        
                    try:
                        
                        con_pop.append(tmpx.Population[0])
                        
                    except:
                        
                        con_pop.append(None)
                        
                    try:
                        
                        con_inc.append(tmpx.Median_Household_Income[0])
                        
                    except:
                        
                        con_inc.append(None)
                        
                    try:
                        
                        con_unemp.append(tmpx.Unemployment_Rate[0])
                        
                    except:
                        
                        con_unemp.append(None)

years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_names = pd.Series(rnr_names, name = 'Name')
rnr_cities = pd.Series(rnr_cities, name = 'City')
rnr_counties = pd.Series(rnr_counties, name = 'County')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_nats = pd.Series(rnr_nats, name = 'Country')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
race_count_pre = pd.Series(race_count_pre, name = 'Races_Pre')
race_count_post = pd.Series(race_count_post, name = 'Races_Post')
mean_place_pre = pd.Series(mean_place_pre, name = 'Mean_Place_Pre')
mean_place_post = pd.Series(mean_place_post, name = 'Mean_Place_Post')
wins_pre = pd.Series(wins_pre, name = 'Wins_Pre')
wins_post = pd.Series(wins_post, name = 'Wins_Post')
win_pct_pre = pd.Series(win_pct_pre, name = 'Win_Pct_Pre')
win_pct_post = pd.Series(win_pct_post, name = 'Win_Pct_Post')
mean_pct_f_pre = pd.Series(mean_pct_f_pre, name = 'Percent_Female_Pre')
mean_pct_f_post = pd.Series(mean_pct_f_post, name = 'Percent_Female_Post')
mean_race_size_pre = pd.Series(mean_race_size_pre, name = 'Mean_Race_Size_Pre')
mean_race_size_post = pd.Series(mean_race_size_post, name = 'Mean_Race_Size_Post')
mean_race_alt_pre = pd.Series(mean_race_alt_pre, name = 'Mean_Race_Altitude_Pre')
mean_race_alt_post = pd.Series(mean_race_alt_post, name = 'Mean_Race_Altitude_Post')
mean_travel_dist_pre = pd.Series(mean_travel_dist_pre, name = 'Mean_Travel_Distance_Pre')
mean_travel_dist_post = pd.Series(mean_travel_dist_post, name = 'Mean_Travel_Distance_Post')
con_hs = pd.Series(con_hs, name = 'Edu_High_School')
con_sc = pd.Series(con_sc, name = 'Edu_Some_College')
con_ass = pd.Series(con_ass, name = 'Edu_Associate')
con_bs = pd.Series(con_bs, name = 'Edu_Bachelor')
con_grad = pd.Series(con_grad, name = 'Edu_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Median_Household_Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')

df = pd.concat([years, covid, rnr_ids, rnr_names, rnr_cities, rnr_counties, rnr_states,
                rnr_nats, rnr_genders, rnr_ages, rnr_fips, treated, treatment_type, tickets,
                window_len, wser_pre, rnr_races_before_pre, race_count_pre, race_count_post,
                mean_place_pre, mean_place_post, wins_pre, wins_post, win_pct_pre, win_pct_post,
                mean_pct_f_pre, mean_pct_f_post, mean_race_size_pre, mean_race_size_post,
                mean_race_alt_pre, mean_race_alt_post, mean_travel_dist_pre, mean_travel_dist_post,
                con_hs, con_sc, con_ass, con_bs, con_grad, con_pop, con_inc, con_unemp], axis = 1)

baddies = [i for i in range(len(df)) if df.Name[i] != None]
df = df[df.index.isin(baddies)].reset_index(drop = True)

# Add runner altitude as an additional control

def add_alt(r):
    
    tmp = ultra[ultra.Runner_ID == r]
    a = max(tmp.Runner_Altitude)
    
    if a > 0:
        
        pass
        
    else:
        
        a = None
        
    return a

runner_fips_alt = [add_alt(df.Runner_ID[i]) for i in range(len(df))]
runner_fips_alt = pd.Series(runner_fips_alt, name = 'Runner_Altitude')
df = pd.concat([df, runner_fips_alt], axis = 1)

# Write df to file

df.to_csv(direc + 'data/output.csv', index = False)

# For consistency with how this actually happened

df = pd.read_csv(direc + 'data/output.csv')

# Create regression specific dataframes with pre/post indicator

# Race Counts

period = []
years = []
covid = []
rnr_ids = []
rnr_states = []
rnr_genders = []
rnr_ages = []
rnr_fips = []
treated = []
treatment_type = []
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []
con_alt = []
race_count = []

for i in range(len(df)):
    
    if (df.Races_Pre[i] >= 0) and (df.Races_Post[i] >= 0):
        
        # Pre
        
        period.append('Pre')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        race_count.append(df.Races_Pre[i])
        
        # Post
        
        period.append('Post')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        race_count.append(df.Races_Post[i])
        
    else:
        
        continue

period = pd.Series(period, name = 'Period')
years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
con_hs = pd.Series(con_hs, name = 'EDU_High_School')
con_sc = pd.Series(con_sc, name = 'EDU_Some_College')
con_ass = pd.Series(con_ass, name = 'EDU_Associate')
con_bs = pd.Series(con_bs, name = 'EDU_Bachelor')
con_grad = pd.Series(con_grad, name = 'EDU_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')
con_alt = pd.Series(con_alt, name = 'Home_Altitude')
race_count = pd.Series(race_count, name = 'Races')

df_races = pd.concat([period, years, covid, rnr_ids, rnr_fips, rnr_states, rnr_genders,
                      rnr_ages, treated, treatment_type, tickets, window_len, wser_pre,
                      rnr_races_before_pre, con_hs, con_sc, con_ass, con_bs, con_grad,
                      con_pop, con_inc, con_unemp, con_alt, race_count], axis = 1)

# Mean Place

period = []
years = []
covid = []
rnr_ids = []
rnr_states = []
rnr_genders = []
rnr_ages = []
rnr_fips = []
treated = []
treatment_type = []
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []
con_alt = []
mean_place = []

for i in range(len(df)):
    
    if (df.Mean_Place_Pre[i] >= 0) and (df.Mean_Place_Post[i] >= 0):
        
        # Pre
        
        period.append('Pre')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        mean_place.append(df.Mean_Place_Pre[i])
        
        # Post
        
        period.append('Post')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        mean_place.append(df.Mean_Place_Post[i])
        
    else:
        
        continue

period = pd.Series(period, name = 'Period')
years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
con_hs = pd.Series(con_hs, name = 'EDU_High_School')
con_sc = pd.Series(con_sc, name = 'EDU_Some_College')
con_ass = pd.Series(con_ass, name = 'EDU_Associate')
con_bs = pd.Series(con_bs, name = 'EDU_Bachelor')
con_grad = pd.Series(con_grad, name = 'EDU_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')
con_alt = pd.Series(con_alt, name = 'Home_Altitude')
mean_place = pd.Series(mean_place, name = 'Place')

df_place = pd.concat([period, years, covid, rnr_ids, rnr_fips, rnr_states, rnr_genders,
                      rnr_ages, treated, treatment_type, tickets, window_len, wser_pre,
                      rnr_races_before_pre, con_hs, con_sc, con_ass, con_bs, con_grad,
                      con_pop, con_inc, con_unemp, con_alt, mean_place], axis = 1)

# Wins

period = []
years = []
covid = []
rnr_ids = []
rnr_states = []
rnr_genders = []
rnr_ages = []
rnr_fips = []
treated = []
treatment_type = []
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []
con_alt = []
wins = []

for i in range(len(df)):
    
    if (df.Wins_Pre[i] >= 0) and (df.Wins_Post[i] >= 0):
        
        # Pre
        
        period.append('Pre')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        wins.append(df.Wins_Pre[i])
        
        # Post
        
        period.append('Post')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        wins.append(df.Wins_Post[i])
        
    else:
        
        continue

period = pd.Series(period, name = 'Period')
years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
con_hs = pd.Series(con_hs, name = 'EDU_High_School')
con_sc = pd.Series(con_sc, name = 'EDU_Some_College')
con_ass = pd.Series(con_ass, name = 'EDU_Associate')
con_bs = pd.Series(con_bs, name = 'EDU_Bachelor')
con_grad = pd.Series(con_grad, name = 'EDU_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')
con_alt = pd.Series(con_alt, name = 'Home_Altitude')
wins = pd.Series(wins, name = 'Wins')

df_wins = pd.concat([period, years, covid, rnr_ids, rnr_fips, rnr_states, rnr_genders,
                     rnr_ages, treated, treatment_type, tickets, window_len, wser_pre,
                     rnr_races_before_pre, con_hs, con_sc, con_ass, con_bs, con_grad,
                     con_pop, con_inc, con_unemp, con_alt, wins], axis = 1)

# Win Percent

period = []
years = []
covid = []
rnr_ids = []
rnr_states = []
rnr_genders = []
rnr_ages = []
rnr_fips = []
treated = []
treatment_type = []
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []
con_alt = []
win_pct = []

for i in range(len(df)):
    
    if (df.Win_Pct_Pre[i] >= 0) and (df.Win_Pct_Post[i] >= 0):
        
        # Pre
        
        period.append('Pre')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        win_pct.append(df.Win_Pct_Pre[i])
        
        # Post
        
        period.append('Post')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        win_pct.append(df.Win_Pct_Post[i])
        
    else:
        
        continue

period = pd.Series(period, name = 'Period')
years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
con_hs = pd.Series(con_hs, name = 'EDU_High_School')
con_sc = pd.Series(con_sc, name = 'EDU_Some_College')
con_ass = pd.Series(con_ass, name = 'EDU_Associate')
con_bs = pd.Series(con_bs, name = 'EDU_Bachelor')
con_grad = pd.Series(con_grad, name = 'EDU_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')
con_alt = pd.Series(con_alt, name = 'Home_Altitude')
win_pct = pd.Series(win_pct, name = 'Win_Percentage')

df_win_pct = pd.concat([period, years, covid, rnr_ids, rnr_fips, rnr_states, rnr_genders,
                        rnr_ages, treated, treatment_type, tickets, window_len, wser_pre,
                        rnr_races_before_pre, con_hs, con_sc, con_ass, con_bs, con_grad,
                        con_pop, con_inc, con_unemp, con_alt, win_pct], axis = 1)

# Race Size

period = []
years = []
covid = []
rnr_ids = []
rnr_states = []
rnr_genders = []
rnr_ages = []
rnr_fips = []
treated = []
treatment_type = []
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []
con_alt = []
race_size = []

for i in range(len(df)):
    
    if (df.Mean_Race_Size_Pre[i] >= 0) and (df.Mean_Race_Size_Post[i] >= 0):
        
        # Pre
        
        period.append('Pre')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        race_size.append(df.Mean_Race_Size_Pre[i])
        
        # Post
        
        period.append('Post')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        race_size.append(df.Mean_Race_Size_Post[i])
        
    else:
        
        continue

period = pd.Series(period, name = 'Period')
years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
con_hs = pd.Series(con_hs, name = 'EDU_High_School')
con_sc = pd.Series(con_sc, name = 'EDU_Some_College')
con_ass = pd.Series(con_ass, name = 'EDU_Associate')
con_bs = pd.Series(con_bs, name = 'EDU_Bachelor')
con_grad = pd.Series(con_grad, name = 'EDU_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')
con_alt = pd.Series(con_alt, name = 'Home_Altitude')
race_size = pd.Series(race_size, name = 'Race_Size')

df_size = pd.concat([period, years, covid, rnr_ids, rnr_fips, rnr_states, rnr_genders,
                     rnr_ages, treated, treatment_type, tickets, window_len, wser_pre,
                     rnr_races_before_pre, con_hs, con_sc, con_ass, con_bs, con_grad,
                     con_pop, con_inc, con_unemp, con_alt, race_size], axis = 1)

# Race Altitude

period = []
years = []
covid = []
rnr_ids = []
rnr_states = []
rnr_genders = []
rnr_ages = []
rnr_fips = []
treated = []
treatment_type = []
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []
con_alt = []
race_alt = []

for i in range(len(df)):
    
    if (df.Mean_Race_Altitude_Pre[i] >= 0) and (df.Mean_Race_Altitude_Post[i] >= 0):
        
        # Pre
        
        period.append('Pre')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        race_alt.append(df.Mean_Race_Altitude_Pre[i])
        
        # Post
        
        period.append('Post')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        race_alt.append(df.Mean_Race_Altitude_Post[i])
        
    else:
        
        continue

period = pd.Series(period, name = 'Period')
years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
con_hs = pd.Series(con_hs, name = 'EDU_High_School')
con_sc = pd.Series(con_sc, name = 'EDU_Some_College')
con_ass = pd.Series(con_ass, name = 'EDU_Associate')
con_bs = pd.Series(con_bs, name = 'EDU_Bachelor')
con_grad = pd.Series(con_grad, name = 'EDU_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')
con_alt = pd.Series(con_alt, name = 'Home_Altitude')
race_alt = pd.Series(race_alt, name = 'Race_Altitude')

df_race_alt = pd.concat([period, years, covid, rnr_ids, rnr_fips, rnr_states, rnr_genders,
                         rnr_ages, treated, treatment_type, tickets, window_len, wser_pre,
                         rnr_races_before_pre, con_hs, con_sc, con_ass, con_bs, con_grad,
                         con_pop, con_inc, con_unemp, con_alt, race_alt], axis = 1)

# Mean Travel Distance

period = []
years = []
covid = []
rnr_ids = []
rnr_states = []
rnr_genders = []
rnr_ages = []
rnr_fips = []
treated = []
treatment_type = []
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []
con_alt = []
travel = []

for i in range(len(df)):
    
    if (df.Mean_Travel_Distance_Pre[i] >= 0) and (df.Mean_Travel_Distance_Post[i] >= 0):
        
        # Pre
        
        period.append('Pre')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        travel.append(df.Mean_Travel_Distance_Pre[i])
        
        # Post
        
        period.append('Post')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        travel.append(df.Mean_Travel_Distance_Post[i])
        
    else:
        
        continue

period = pd.Series(period, name = 'Period')
years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
con_hs = pd.Series(con_hs, name = 'EDU_High_School')
con_sc = pd.Series(con_sc, name = 'EDU_Some_College')
con_ass = pd.Series(con_ass, name = 'EDU_Associate')
con_bs = pd.Series(con_bs, name = 'EDU_Bachelor')
con_grad = pd.Series(con_grad, name = 'EDU_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')
con_alt = pd.Series(con_alt, name = 'Home_Altitude')
travel = pd.Series(travel, name = 'Travel_Distance')

df_travel = pd.concat([period, years, covid, rnr_ids, rnr_fips, rnr_states, rnr_genders,
                       rnr_ages, treated, treatment_type, tickets, window_len, wser_pre,
                       rnr_races_before_pre, con_hs, con_sc, con_ass, con_bs, con_grad,
                       con_pop, con_inc, con_unemp, con_alt, travel], axis = 1)

# Proportion of Women

period = []
years = []
covid = []
rnr_ids = []
rnr_states = []
rnr_genders = []
rnr_ages = []
rnr_fips = []
treated = []
treatment_type = []
tickets = []
window_len = []
wser_pre = []
rnr_races_before_pre = []
con_hs = []
con_sc = []
con_ass = []
con_bs = []
con_grad = []
con_pop = []
con_inc = []
con_unemp = []
con_alt = []
pct_f = []

for i in range(len(df)):
    
    if (df.Percent_Female_Pre[i] >= 0) and (df.Percent_Female_Post[i] >= 0):
        
        # Pre
        
        period.append('Pre')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        pct_f.append(df.Percent_Female_Pre[i])
        
        # Post
        
        period.append('Post')
        treated.append(df.Treated[i])
        treatment_type.append(df.Treatment_Type[i])
        years.append(df.Year[i])
        covid.append(df.COVID[i])
        rnr_ids.append(df.Runner_ID[i])
        rnr_fips.append(df.FIPS[i])
        rnr_states.append(df.State[i])
        rnr_genders.append(df.Gender[i])
        rnr_ages.append(df.Age[i])
        tickets.append(df.Tickets[i])
        window_len.append(df.Window[i])
        wser_pre.append(df.WSER_Pre[i])
        rnr_races_before_pre.append(df.Prior_Race_Experience[i])
        con_hs.append(df.Edu_High_School[i])
        con_sc.append(df.Edu_Some_College[i])
        con_ass.append(df.Edu_Associate[i])
        con_bs.append(df.Edu_Bachelor[i])
        con_grad.append(df.Edu_Graduate[i])
        con_pop.append(df.Population[i])
        con_inc.append(df.Median_Household_Income[i])
        con_unemp.append(df.Unemployment_Rate[i])
        con_alt.append(df.Runner_Altitude[i])
        pct_f.append(df.Percent_Female_Post[i])
        
    else:
        
        continue

period = pd.Series(period, name = 'Period')
years = pd.Series(years, name = 'Year')
covid = pd.Series(covid, name = 'COVID')
rnr_ids = pd.Series(rnr_ids, name = 'Runner_ID')
rnr_states = pd.Series(rnr_states, name = 'State')
rnr_genders = pd.Series(rnr_genders, name = 'Gender')
rnr_ages = pd.Series(rnr_ages, name = 'Age')
rnr_fips = pd.Series(rnr_fips, name = 'FIPS')
treated = pd.Series(treated, name = 'Treated')
treatment_type = pd.Series(treatment_type, name = 'Treatment_Type')
tickets = pd.Series(tickets, name = 'Tickets')
window_len = pd.Series(window_len, name = 'Window')
wser_pre = pd.Series(wser_pre, name = 'WSER_Pre')
rnr_races_before_pre = pd.Series(rnr_races_before_pre, name = 'Prior_Race_Experience')
con_hs = pd.Series(con_hs, name = 'EDU_High_School')
con_sc = pd.Series(con_sc, name = 'EDU_Some_College')
con_ass = pd.Series(con_ass, name = 'EDU_Associate')
con_bs = pd.Series(con_bs, name = 'EDU_Bachelor')
con_grad = pd.Series(con_grad, name = 'EDU_Graduate')
con_pop = pd.Series(con_pop, name = 'Population')
con_inc = pd.Series(con_inc, name = 'Income')
con_unemp = pd.Series(con_unemp, name = 'Unemployment_Rate')
con_alt = pd.Series(con_alt, name = 'Home_Altitude')
pct_f = pd.Series(pct_f, name = 'Percent_Female')

df_f = pd.concat([period, years, covid, rnr_ids, rnr_fips, rnr_states, rnr_genders,
                  rnr_ages, treated, treatment_type, tickets, window_len, wser_pre,
                  rnr_races_before_pre, con_hs, con_sc, con_ass, con_bs, con_grad,
                  con_pop, con_inc, con_unemp, con_alt, pct_f], axis = 1)

# Write these dfs to file

df_races.to_csv(direc + 'data/data_race_count.csv', index = False)
df_place.to_csv(direc + 'data/data_mean_place.csv', index = False)
df_wins.to_csv(direc + 'data/data_wins.csv', index = False)
df_win_pct.to_csv(direc + 'data/data_win_percentage.csv', index = False)
df_size.to_csv(direc + 'data/data_mean_race_size.csv', index = False)
df_race_alt.to_csv(direc + 'data/data_mean_race_altitude.csv', index = False)
df_travel.to_csv(direc + 'data/data_mean_travel_distance.csv', index = False)
df_f.to_csv(direc + 'data/data_mean_percent_female.csv', index = False)

