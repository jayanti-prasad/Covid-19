import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from common_utils import date_normalize, get_country_data

from datetime import date


def get_top_testing (args, df):

    dates  = list(set(df['date'].to_list()))
    df = df[df['date'] == dates[-1]]

    df = df.fillna(0)
    df["tests_per_mn"] = df["tests_per_mn"].str.replace(",","").astype(float)
    df = df.fillna(0)

    df = df.sort_values(by=['tests_per_mn'],ascending=False)[:50]

    fig = plt.figure (figsize=(18,18))
    ax = fig.add_subplot(111)

    df.plot(x="country", y="tests_per_mn", kind="bar", ax=ax, color="C1")
    plt.setp(ax.get_xticklabels(), rotation=35, horizontalalignment='right',fontsize=10)

    ax.set_title("Covid-19 [tests per million, source: worldometer] :" + str(date.today()))
    plt.setp(ax.get_xticklabels(), rotation=35, horizontalalignment='right',fontsize=10)

    fig.text(0.65, 0.25, 'By Jayanti Prasad',fontsize=50, color='gray',\
         ha='right', va='bottom', alpha=0.5)



def get_top_countries (args, df):
    df = df.replace({'United Kingdom': 'UK'}, regex=True)
    df1 = df.copy()
    df1 = date_normalize (df1)
    df1 = df1.sort_values(by='date')
    last_date = df1.tail(1)['date'].values[0]
    df_last = df1[df1['date'] == last_date]
    #df_last = df_last.sort_values(by=['confirmed'],ascending=False)[:50]
    df_last = df_last.sort_values(by=['deaths'],ascending=False)[:50]

    df_last.to_csv(args.output_dir + "top_countries.csv",columns=['country','confirmed','deaths','recovered'],index=False)

    fig = plt.figure (figsize=(36,24))
    ax = fig.add_subplot(111)

    df_last.plot(x="country", y="confirmed", kind="bar", ax=ax, color="C1")
    df_last.plot(x="country", y="recovered", kind="bar", ax=ax, color="C2")
    df_last.plot(x="country", y="deaths", kind="bar", ax=ax, color="C3")
    ax.set_yscale('log')
    ax.set_ylabel('log')
    ax.set_title("Covid-19:" + str(date.today()))
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right',fontsize=10)
    ax.grid()

    fig.text(0.65, 0.25, 'By Jayanti Prasad',fontsize=50, color='gray',\
         ha='right', va='bottom', alpha=0.5)


    plt.savefig(args.output_dir + os.sep+ "top_countries0.pdf")
    plt.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file',\
      default='data/covid-19-global.csv')
    parser.add_argument('-o','--output-dir',help='Output dir',default='current/')

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.input_file)
    get_top_countries (args, df)
    
