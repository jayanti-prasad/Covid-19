from datetime import timedelta, date
import datetime as dt

def get_country_data (df, country):
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






 
