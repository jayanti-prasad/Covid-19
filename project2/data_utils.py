from datetime import timedelta, date
import datetime as dt
import pandas as pd
import arrow
import re
from cov_utils import  country_normalize
from date_utils import  date_normalize

def get_fitting_data (dF, country,epd_model,num_min_infect):
   df  = get_country_data (dF, country)
   df.index = df['date'].to_list()

   df['removed'] = df['recovered'] +  df['deaths']
   df['infected'] = df['confirmed'] - df['removed']

   df = df [df['infected']  >  num_min_infect]

   if epd_model == 'SIR':
      data = df[['infected','removed']].copy()
      Y0 = data.iloc[0]
      init_val = [Y0['infected'], Y0['removed']]

   if epd_model == 'SIRD':
      data = df[['infected','recovered','deaths']].copy()
      Y0 = data.iloc[0]
      init_val = [Y0['infected'], Y0['recovered'], Y0['deaths']]


   return df, data, init_val


def get_country_data (df, country):
   
   df = country_normalize(df) 

   df = df.fillna(0)
   df = df[df['country'] == country]
   df = date_normalize (df)
   df = df.sort_values(by='date')
   df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
   df = df.loc[:, ~df.columns.str.contains('country')]
   df.index = df['date'].to_list()

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
 
