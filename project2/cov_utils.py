from datetime import timedelta, date
import datetime as dt
import pandas as pd
import arrow
import re
from date_utils import  date_normalize, get_date_diff


def get_lockdown_day(first_date, df_l, country):

   info = df_l[df_l['country']==country]
   lockdown_date = info['lockdown'].iloc[0]
   lday = get_date_diff (first_date, lockdown_date)
   return lday


def lockdown_info(lockdown_file,  country):
   df = pd.read_csv(lockdown_file)
   P = df['population']
   L = df['lockdown']
   T = df['num_testing']

   P.index = df['country'].to_list()
   L.index = df['country'].to_list()
   T.index = df['country'].to_list()

   return P[country], L[country], T[country]
 

def get_population(country, df_p):
   #df_p = pd.read_csv(pop_file)
   df_p = country_normalize (df_p)

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

