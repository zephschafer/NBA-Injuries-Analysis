# -*- coding: utf-8 -*-
"""
This script creates a stacked bar chart of missed games due to injury. Each 
bar represents a year, each stack with in the corrresponds to an injury "category"
or "keyword".

Required inputs:
    -mg_il_ps_merged_df.p
    
Outputs:
    -stacked bar chart
    
@author: evanl
"""

import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import numpy.random as nr

pd.set_option('display.expand_frame_repr', False)

#--------------------------User Inputs---------- ----------------------
#file path for pickle of concatenated/merged mg,il, player stats dataframes
injury_df_filepath =  '../../data/03_processed/mg_il_ps_merged_df.p'

#save path for plot
plot_savepath =  '../../results/01_plots/bar_missed_games_all_durations.png'

#-------------------------Load Files------------------------------------------
#load player injury event dataframe
injury_df = pickle.load(open(injury_df_filepath, "rb" ) )

#-------------------------Process Dataframe----------------------------------

#Add a column for total (regular + post season) games missed
injury_df['Tot_games_missed'] = injury_df['Reg_games_missed'] + injury_df['Post_games_missed']

"""Slice data set"""

#Only look at players that averaged more than 10 minutes per game ('MPPG' > 10)
injury_df = injury_df[injury_df['MPPG'] > 10.0]

#Exclude those 'injuries' which are not relevant (healthy scratches, rest, sick, n/a, other)
injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]


#------------------------Make plots-------------------------------------------

#group by year, category, and sum total missed games. Unstack to plot
data = injury_df.groupby(['Year'])['Tot_games_missed'].sum()

#create plot
ax = data.plot(kind='bar', stacked=True, figsize=(15, 10))

# Set the x-axis label
ax.set_xlabel("Year", fontsize = 16, weight='bold')

# Set the y-axis label
ax.set_ylabel("Games Missed Due to Injury", fontsize =16,weight='bold')

# Set the x-axis tick labels
ax.set_xticklabels(data.index,rotation = 0, fontsize = 16)

# Set the y-axis tick labels
y_tick_labels = []
for tick in ax.get_yticks():
    y_tick_labels.append(int(tick))
    
ax.set_yticklabels(y_tick_labels, fontsize = 16)

# Set legend properties
ax.legend(list(data.columns), fontsize = 16)
ax.legend(loc='best')

#----------------------Save plot---------------------------------------------
fig = ax.get_figure()
fig.savefig(plot_savepath, dpi = 300)