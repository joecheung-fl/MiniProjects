"""
This program using Pandas instead of itertools implementing the code example in RealPython
with much more compact and easy to understand code
https://realpython.com/python-itertools/#analyzing-the-sp500
"""
import pandas as pd
import tabulate as tb
import numpy as np


df = pd.read_csv("https://raw.githubusercontent.com/realpython/materials/master/itertools-in-python3/SP500.csv")
df['Change'] = df['Adj Close'].pct_change() * 100
df['Sign'] = np.sign(df['Change'])

# Steps to figure out longest consecutive num of days with positive change
# Reference: https://stackoverflow.com/questions/27626542/counting-consecutive-positive-values-in-python-pandas-array
# 1. (df['Sign'] != df['Sign'].shift()).cumsum())
# If sign is the same as previous one, it will be False that is counted as zero and so
# the cumsum number will keep unchanged. The longer the occurrence the continuity is,
# the greater the count of that cumsum is
# 2. (df['Sign'].groupby((df['Sign'] != df['Sign'].shift()).cumsum()).cumcount() + 1)
# It results in the count of cumsum and assign it to each rows of df
# 3. df['Sign'] * (#2)
# The longest continuity may be 'down' day and so must be multiplied by the sign so that
# max() used later will find out the longest continuity of 'up' day
df['ConPositive'] = df['Sign'] * (df['Sign'].groupby((df['Sign'] != df['Sign'].shift()).cumsum()).cumcount() + 1)

index_max = df['Change'].argmax()
index_min = df['Change'].argmin()
index_streak = df['ConPositive'].argmax()
longest_streak = int(df.iloc[index_streak]['ConPositive'])

#print(tb.tabulate(df.head(5), headers="keys", tablefmt="psql"))
print('Max gain: {1:.2f}% on {0}'.format(df.iloc[index_max]['Date'], df.iloc[index_max]['Change']))
print('Max loss: {1:.2f}% on {0}'.format(df.iloc[index_min]['Date'], df.iloc[index_min]['Change']))
print('Longest growth streak: {num_days} days ({first} to {last})'.format(
    num_days=longest_streak,
    first=df.iloc[index_streak - longest_streak + 1]['Date'],
    last=df.iloc[index_streak]['Date']
))