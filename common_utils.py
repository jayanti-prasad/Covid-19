from datetime import timedelta, date
import datetime as dt
import pandas as pd

def get_population(country):
   df_p = pd.read_csv("../data/world_population.csv")
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
   dates = [d.replace('2020-','') for d in dates]
   return dates 
 
