import numpy as np
import os
import matplotlib.pyplot as plt 


def plot_frame(df, country, output_dir):

    dates = df.index 

    fig = plt.figure(figsize=(18,18))
    ax = [fig.add_subplot(311)]
    ax.append(fig.add_subplot(312))
    ax.append(fig.add_subplot(313))


    cases = df.columns[1:]
    colors = ['blue','green','red','black']

    for i in range (0, len(cases)):
        Y = df[cases[i]]

        labels = [dates[i] for i in range(0, len(dates))  if i% 3 == 0]
        plt.xticks(np.arange(0,len(dates),3), labels)

        plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')

        ax[i].plot(dates, Y,c=colors[i])
        ax[i].scatter(dates, Y,c=colors[i])

        ax[i].set_ylabel(cases[i])
        ax[i].grid()

        if i == 0:
            ax[i].set_title(country)
        if i < 2 :
            ax[i].set_xticklabels([])

    #plt.show()
    plt.savefig(output_dir  + os.sep + country+ ".pdf")


