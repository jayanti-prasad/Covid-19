import argparse 
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib 
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

def dtobject  (date_str):
   parts = date_str.split('-')
   parts = [int(x) for x in parts]
 
   return datetime(parts[2], parts[0], parts[1], 0, 0, 0)

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input file')
   parser.add_argument('-c','--country-name',help='Country name')

   args = parser.parse_args()
   
   df = pd.read_csv(args.input_file)
 
   df = df[df['country'] == args.country_name]

   dates = [ dtobject(x) for x in df['date'].to_list()]

   df.index = dates 
   df['date'] = dates 
   df = df.sort_values(by=['date'])

   fig, ax = plt.subplots(3, 1, sharex=True)
   fig.set_figheight(18)
   fig.set_figwidth(18)
   plt.subplots_adjust(hspace=.0)

   plt.setp(ax[2].get_xticklabels(), rotation=45, horizontalalignment='right')

   ax[2].plot(df['confirmed'],label='Confirmed')
   ax[2].plot(df['confirmed'],'.')
   ax[1].plot(df['recovered'],label='Recovered')
   ax[1].plot(df['recovered'],'.')
   ax[0].plot(df['deaths'],label='Deaths')
   ax[0].plot(df['deaths'],'.')

   date_form = DateFormatter("%m-%d")

   ax[2].xaxis.set_major_formatter(date_form)

   # Ensure a major tick for each week using (interval=1) 
   ax[2].xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

   ax[0].grid()
   ax[1].grid()
   ax[2].grid()

   ax[0].legend()
   ax[1].legend()
   ax[2].legend()

   plt.suptitle(args.country_name)

   plt.show()
   


