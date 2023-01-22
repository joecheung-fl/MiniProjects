"""
This program using Pandas instead of itertools implementing the code example in RealPython
with much more compact and easy to understand code
https://realpython.com/python-itertools/#building-relay-teams-from-swimmer-data
"""
import pandas as pd
import tabulate as tb
import statistics


df = pd.read_csv("https://raw.githubusercontent.com/realpython/materials/master/itertools-in-python3/swimmers.csv",
                 parse_dates=["Time1", "Time2", "Time3"])
df["Time"] = df[["Time1", "Time2", "Time3"]].apply(statistics.median, axis=1)

grouped = df.groupby(['Stroke', 'Name']).agg({'Time': min})  # Only min time for each swimmer in each stroke
grouped = grouped.sort_values(['Stroke', 'Time'], ascending=True).groupby('Stroke')
grouped = grouped.head(8)  # The Team A & B are the first 8 swimmers in each stroke
grouped = grouped.reset_index()
grouped.drop('Time', axis=1, inplace=True)  # Time is not needed anymore
for n, team_name in enumerate(("Team A", "Team B")):
    # 1. Group by Stroke
    # 2. When n=0, only get first 4 rows in each group (i.e. Team A); When n=1, last 4 rows (i.e. Team B)
    # 3. After .nth() method, df returned. So, do group by Stroke again and reduce all rows with swimmers to 1 row
    group = grouped.groupby("Stroke").nth(tuple(range(n * 4, n * 4 + 4))).groupby("Stroke").agg({"Name": lambda x: " ".join(x)})
    print(team_name, tb.tabulate(group, headers="keys", tablefmt="psql"), sep="\n")

