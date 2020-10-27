import argparse
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from predict_share_price import format_data, plot_data 

def AR(p,df):
    df_temp = df

    #Generating the lagged p terms
    for i in range(1,p+1):
       df_temp['Shifted_values_%d' % i ] = df_temp['Value'].shift(i)

    print("df:",df_temp.shape)

    train_size = (int)(0.8 * df_temp.shape[0])

    #Breaking data set into test and training
    df_train = pd.DataFrame(df_temp[0:train_size])
    df_test = pd.DataFrame(df_temp[train_size:df.shape[0]])
    print("df_train:",df_train.shape)
    print("df_test:",df_test.shape)

    df_train_2 = df_train.dropna()
    print("df_train:",df_train_2.shape)

    #X contains the lagged values ,hence we skip the first column
    X_train = df_train_2.iloc[:,1:].values.reshape(-1,p)
    #Y contains the value,it is the first column
    y_train = df_train_2.iloc[:,0].values.reshape(-1,1)

    print(X_train.shape, y_train.shape)


    #Running linear regression to generate the coefficents of lagged terms
    lr = LinearRegression()

    lr.fit(X_train,y_train)

    theta  = lr.coef_.T
    intercept = lr.intercept_
    df_train_2['Predicted_Values'] = X_train.dot(lr.coef_.T) + lr.intercept_
    # df_train_2[['Value','Predicted_Values']].plot()

    X_test = df_test.iloc[:,1:].values.reshape(-1,p)
    df_test['Predicted_Values'] = X_test.dot(lr.coef_.T) + lr.intercept_
    # df_test[['Value','Predicted_Values']].plot()

    RMSE = np.sqrt(mean_squared_error(df_test['Value'], df_test['Predicted_Values']))

    print("The RMSE is :", RMSE,", Value of p : ",p)

    return [df_train_2,df_test,theta,intercept,RMSE]



if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input File')
   window = 24

   args = parser.parse_args()

   df = pd.read_csv(args.input_file)

   print(df.shape, df.columns)

   df['Date'] = [format_data(d) for d in df['Date'].to_list()]
   df.index =   df['Date'].to_list()
   df = df.sort_values(by='Date')

   df['Value'] = df['Open Price']

   X = df['Open Price']
   
   #plot_data(X)

   [df_train_2,df_test,theta,intercept,RMSE] = AR(4, df)

   print(intercept,RMSE) 



