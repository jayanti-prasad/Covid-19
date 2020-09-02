from datetime import timedelta, date
import datetime as dt
import pandas as pd
import arrow
import re

from datetime import datetime

def get_dtobject  (date_str):
   parts = date_str.split('-')
   parts = [int(x) for x in parts]
   print("parts",parts)
   return datetime(parts[0], parts[1], parts[2], 0, 0, 0)


def get_date_diff(date1,date2):
   a = arrow.get(date1)
   b = arrow.get(date2)
   delta = (b-a) 
   return delta.days


def lockdown_info(lockdown_file,  country):
   df = pd.read_csv(lockdown_file)
   P = df['population']
   L = df['lockdown']
   T = df['num_testing']

   P.index = df['country'].to_list()
   L.index = df['country'].to_list()
   T.index = df['country'].to_list()

   return P[country], L[country], T[country]
 

def get_population(pop_file, country):
   df_p = pd.read_csv(pop_file)
   P = df_p['pop_2020'].str.replace(",","").astype(int)
   P.index = df_p['country'].to_list()
   return  P[country]


def get_top_countries(df, count):
    df = country_normalize(df)
    df1 = df.copy()
    df1 = date_normalize (df1)
    df1 = df1.sort_values(by='date')
    last_date = df1.tail(1)['date'].values[0]
    df_top = df1[df1['date'] == last_date]
    df_top = df_top.sort_values(by=['confirmed'],ascending=False)[:count]
    return df_top['country'].to_list()


def country_normalize(df):
   df = df.replace({'United States': 'US'}, regex=True)
   df = df.replace({'United Kingdom': 'UK'}, regex=True)
   df = df.replace({'Korea, South': 'SK'}, regex=True)
   df = df.replace({'Saudi Arabia': 'SaudiArabia'}, regex=True)
   df = df.replace({'United Arab Emirates': 'UAE'}, regex=True)
   df = df.replace({'Dominican Republic': 'DR'}, regex=True)
   df = df.replace({'South Africa': 'SA'}, regex=True)
   df = df.replace({'Czechia': 'Czech'}, regex=True)
   df = df.replace({'Bosnia and Herzegovina': 'BH'}, regex=True)
   df = df.replace({'New Zealand': 'NZ'}, regex=True)
   df = df.replace({'Cote d\'Ivoire': 'CDI'}, regex=True)

   return df 


def get_country_data (df, country):
   
   df = country_normalize(df) 

   df = df.fillna(0)
   df = df[df['country'] == country]
   df = date_normalize (df)
   df = df.sort_values(by='date')
   df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
   df = df.loc[:, ~df.columns.str.contains('country')]

   dates = df['date'].to_list()
   dates = [get_dtobject(x) for x in dates]

   df.index = dates
   df['date'] = dates 

   return df 


def get_country_data_owid (df, country):
   df = country_normalize(df)
   df = df.fillna(0)

   df = df [df['location'] == country]
   df = df[['date','total_cases','total_deaths']].copy()
   df.rename(columns = {'date':'date', 'total_cases':'confirmed','total_deaths':'deaths'}, inplace = True)

   df = df.sort_values(by='date')
   df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
   df = df.loc[:, ~df.columns.str.contains('country')]
   df.index = df['date'].to_list()

   return df


def get_country_data_kaggle (df, country):

    df = df[['Country/Region','ObservationDate','Confirmed','Recovered','Deaths']].copy() 
    df = country_normalize(df)
    df = df.fillna(0)
    df = df [df['Country/Region'] == country]

    df.rename(columns = {'ObservationDate':'date', 'Confirmed':'confirmed',\
      'Recovered':'recovered','Deaths':'deaths'}, inplace = True)

    df = df.sort_values(by='date')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('Country/Region')]

    dates = df['date'].to_list()
    new_dates = []
    for d in dates:
       parts = d.split('/') 
       dd = parts[2]+"-"+parts[0]+"-"+parts[1]
       new_dates.append(dd)  

    df['date'] = new_dates 

    df.index = new_dates 

    return df


def date_normalize (df):
    dates = df['date'].to_list()
    dates1 = []
    for d in dates:
      dd = d.split('-')
      dates1.append(dd[2]+"-"+dd[0]+"-"+dd[1])
    df['date'] = dates1
    return df

def get_dates (start_date, num_days):

   date_time_str = start_date + " 12:00:00"
   tmp_date = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
   dates = []
   for i in range(0, num_days):
      tmp_date  = tmp_date + timedelta(days=1)
      dates.append(str(tmp_date).split(" ")[0])
   return dates

def strip_year (dates):
   dates = [re.sub(r'[1-3][0-9]{3}-','',d)  for d in dates]
   return dates 
 
