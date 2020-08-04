#!/usr/bin/env python3
"""
The purpose of viz.py is to quickly create static data visualizations.

:: Functions ::
    kde(data=[])
        - data: The two pandas dataframe columns you want to visualizations
    #Example: kde([econ['fall_count'], sub['fall_count']])

    line(data=None,x=None,y=None,hue=None)
        - data: The pandas dataframe
        - x: The pandas column you want on the x axis
        - y: The pandas column you want on the y axis
        - hue: The pandas column if you want different variables to have different hues in the visualization
    #Example: line(data,'year','fall_count','major')

    bar(data=None,x=None,y=None,hue=None,ci=None)
        - data: The pandas dataframe
        - x: The pandas column you want on the x axis
        - y: The pandas column you want on the y axis
        - hue: The pandas column if you want different variables to have different hues in the visualization
        - ci: Removes confidence intervals in the bar chart
    #Example: bar(sub,'major','fall_count','year')

    
Author(s): Dan Blevins
"""

import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.set_context("talk")
sns.set_style("dark")
sns.despine()

data = pd.read_pickle('../data/fall_grad_headcount.pkl')
econ = data[data['major'] == 'Econ']
sub = data[data['year'] >= 2010]

def kde(data=[]):
    plt.clf()
    plt.close()
    for i in data:
        sns.kdeplot(data=i, shade=True)
    plt.show()

kde([econ['fall_count'], sub['fall_count']])

def line(data=None,x=None,y=None,hue=None):
    plt.clf()
    plt.close()
    unique_vals = data[hue].nunique()
    sns.color_palette("muted", unique_vals)
    plot = sns.lineplot(x=x, y=y, hue=hue, data=data)
    plt.ylim(0, max(data[y]+10))
    plt.xlim(min(data[x]), max(data[x])+1)
    plt.xticks(np.arange(min(data[x]), max(data[x])+1, 2.0))
    plt.ylabel("Count")
    plt.legend(frameon=False)
    plt.show()

line(data,'year','fall_count','major')
    
def bar(data=None,x=None,y=None,hue=None,ci=None):
    plt.clf()
    plt.close()
    unique_vals = data[hue].nunique()
    sns.color_palette("muted")
    plot = sns.barplot(x=x, y=y, hue=hue, data=data)
    plt.ylim(0, max(data[y]+10))
    plt.ylabel("Count")
    plt.legend(frameon=False)
    plt.show()

bar(sub,'major','fall_count','year')