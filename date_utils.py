from datetime import timedelta, date
import datetime as dt
import re

def get_date_diff(date1,date2):
   a = arrow.get(date1)
   b = arrow.get(date2)
   delta = (b-a) 
   return delta.days


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
 
