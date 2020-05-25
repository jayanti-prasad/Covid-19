import pandas as pd
import argparse 
import matplotlib.pyplot as plt 

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file', default=\
      '/Users/jayanti/Data/COVID-19/India/csv/district_wise.csv')

    args = parser.parse_args()

    dF = pd.read_csv(args.input_file)

    df = dF[['District','Confirmed','Recovered','Deceased']].copy()

    print(df.shape, df.columns)

    df.loc[df.shape[0]+1] = ['Delhi',12910,6267,231]
    df = df.sort_values(by='Confirmed',ascending=False)
   
    df = df [ df['Confirmed'] > 0]
    df = df[df ['District'] !='Unknown']
    df = df[df ['District'] !='Unassigned']


    df.index = df['District'].to_list()

 
    df = df.iloc[:30]
  
    count = 1 
    for index, row in df.iterrows():
       print(count, row['District'],row['Confirmed'],row['Recovered'],row['Deceased'])
       count +=1


    fig = plt.figure (figsize=(18,12))
    ax = fig.add_subplot(311)
    bx = fig.add_subplot(312)
    cx = fig.add_subplot(313)

    ax.bar(df['District'].to_list(), df['Deceased'].to_list(),color='red')
    bx.bar(df['District'].to_list(), df['Recovered'].to_list(),color='green')
    cx.bar(df['District'].to_list(), df['Confirmed'].to_list(),color='blue')

    plt.setp(cx.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.set_xticklabels([])
    bx.set_xticklabels([])
    #ax.set_yscale('log')
    ax.grid()
    bx.grid()
    cx.grid()
    ax.set_title("India - Covid-19 : 30 most affected districts [by Jayanti Prasad, source:covid19india.org]")
    cx.set_ylabel("Confirmed")
    bx.set_ylabel("Recovered")
    ax.set_ylabel("Deceased")

    plt.show()

