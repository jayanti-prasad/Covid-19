import numpy as np
import os
import matplotlib.pyplot as plt 


def plot_country(df, country, flag):

    dates = df['date'].to_list()
    days =  [int(i) for i in range (0, df.shape[0])]

    fig = plt.figure(figsize=(18,18))
    ax = [fig.add_subplot(311)]
    ax.append(fig.add_subplot(312))
    ax.append(fig.add_subplot(313))

    cases = ['confirmed','recovered','deaths']
    colors = ['blue','green','red']

    for i in range (0, len(cases)):
        Y = df[cases[i]]
        Y.index = dates

        labels = [dates[i] for i in range(0, len(days))  if i% 3 == 0]
        plt.xticks(np.arange(0,len(days),3), labels)

        plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')

        if flag > 0:
            dY = Y.diff(periods=1).iloc[1:]
            ax[i].plot(dates[1:], dY,c=colors[i])
            ax[i].scatter(dates[1:], dY,c=colors[i])
        else :
            ax[i].plot(dates, Y,c=colors[i])
            ax[i].scatter(dates, Y,c=colors[i])

        ax[i].set_ylabel(cases[i])
        ax[i].grid()

        if i == 0:
            ax[i].set_title(country)
        if i < 2 :
            ax[i].set_xticklabels([])

    #plt.show()
    plt.savefig("tmp" + os.sep + country+ ".pdf")

