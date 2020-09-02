import os
import pandas as pd
import argparse 
from common_utils import get_country_data
from plutils import plot_data 

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file',\
      default='data/covid-19-global.csv')
    parser.add_argument('-c','--country',help='Country name',default='India')
    parser.add_argument('-o','--output-dir',help='Output dir',default='current')

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    dF = pd.read_csv(args.input_file)
    df = get_country_data (dF, args.country)



    df.index = df['date'].to_list() 
    df.to_csv(args.output_dir + os.sep + args.country+".csv")

    plot_data (df,['deaths','recovered','confirmed'],0,args.country,6,args.output_dir)
    #plot_data (df,['deaths','recovered','confirmed'],1,args.country,3,args.output_dir)


