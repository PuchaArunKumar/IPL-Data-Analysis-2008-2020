import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt
import seaborn as sns
df1 = pd.read_csv("IPL Matches 2008-2020.csv")
df2 = pd.read_csv("IPL Ball-by-Ball 2008-2020.csv")
df1["Year"] = pd.to_datetime(df1["date"]).dt.year

# Count of matches played in each season 
matches_per_season = df1.groupby('Year').size()
plt.figure(figsize=(10, 6))
sns.barplot(x=matches_per_season.index, y=matches_per_season.values, palette="viridis")
plt.title('Matches Played per Season')
plt.xlabel('Season')
plt.ylabel('Matches Played')
plt.xticks(rotation=45)
plt.show()

# Total runs scored in each season
df = df1.merge(df2, on="id", how="inner") 
season_totals = df.groupby("Year")["total_runs"].sum()
plt.figure(figsize=(10, 6))
sns.barplot(x=season_totals.index, y=season_totals.values, palette="magma")
plt.title('Total Runs Scored per Season')
plt.xlabel('Season')
plt.ylabel('Total Runs')
plt.xticks(rotation=45)
plt.show()

# Average runs scored per match in each season
season_averages = df.groupby(["Year", "id"])["total_runs"].sum().groupby("Year").mean()
plt.figure(figsize=(10, 6))
sns.barplot(x=season_averages.index, y=season_averages.values, palette="rocket")
plt.title('Average Runs Scored per Match in each Season')
plt.xlabel('Season')
plt.ylabel('Average Runs per Match')
plt.xticks(rotation=45)
plt.show()

# Umpire who umpired the most
most_frequent_umpire = df.groupby("umpire1")["umpire2"].size().idxmax()
print("The umpire who umpired the most is:", most_frequent_umpire)

# Team that has won the most toss
most_toss_wins = df['toss_winner'].value_counts().idxmax()
print("The team that has won the most tosses is:", most_toss_wins)

# Decision taken by the teams after winning the toss
toss_decisions = df.groupby("id").agg({'toss_winner': 'first', 'toss_decision': 'first'}).reset_index()
toss_decisions = toss_decisions.groupby("toss_winner")["toss_decision"].value_counts().unstack(fill_value=0)
plt.figure(figsize=(10, 6))
toss_decisions.plot(kind='bar', stacked=True, colormap='coolwarm')
plt.title('Decision after Winning the Toss')
plt.xlabel('Toss Winner')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Toss Decision')
plt.show()

# Toss decision variation across seasons
toss_decision_season = df.groupby(["Year", "id"])["toss_decision"].first().unstack(fill_value='').apply(pd.Series.value_counts, axis=1).fillna(0)
plt.figure(figsize=(10, 6))
toss_decision_season.plot(kind='bar', stacked=True, colormap='summer')
plt.title('Toss Decision Variation Across Seasons')
plt.xlabel('Season')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Toss Decision')
plt.show()

# Percentage of matches won by the team winning the toss
total_matches = df.shape[0]
toss_win_match_win = df[df['toss_winner'] == df['winner']].shape[0]
percentage = (toss_win_match_win / total_matches) * 100
plt.figure(figsize=(6, 6))
plt.pie([toss_win_match_win, total_matches - toss_win_match_win], labels=['Toss Winner Match Win', 'Toss Winner Match Loss'], autopct='%1.1f%%', startangle=140, colors=['green', 'red'])
plt.title('Percentage of Matches Won by Toss Winner')
plt.show()

# Number of times the chasing team has won the match
chasing_wins = df[df['toss_winner'] != df['winner']]['id'].nunique()
print(" Number of times the chasing team has won the match:", chasing_wins)

# Count the number of matches played by each team
matches_played = df['team1'].value_counts() + df['team2'].value_counts()
most_matches_played = matches_played.idxmax()
print("Teams that have played the most number of matches:", most_matches_played)

# Team that has won the most number of times
most_wins = df['winner'].value_counts().idxmax()
print(" The team that has won the most number of times is:", most_wins)

# Calculate winning percentage of a Team with the highest winning percentage
total_matches = df['team1'].value_counts() + df['team2'].value_counts()
total_wins = df['winner'].value_counts()
winning_percentage = (total_wins / total_matches) * 100
highest_winning_percentage_team = winning_percentage.idxmax()
print("The team with the highest winning percentage is:", highest_winning_percentage_team)

# Venue where the team that has won the most matches has won the most matches
team_name = df['winner'].value_counts().idxmax()
team_wins_at_venue = df[df['winner'] == team_name]['venue'].value_counts()
lucky_venue = team_wins_at_venue.idxmax()
print("The lucky venue for", team_name, "is:", lucky_venue)

# Inning-wise comparison between teams
inning_wise_comparison = df.groupby(['team1', 'team2', 'winner'])['id'].count().unstack(fill_value=0)
print(" Inning-wise comparison between teams:",inning_wise_comparison)

# Team that has scored the most number of 200+ scores
high_scores = df.groupby(['id', 'inning', 'batting_team'])['total_runs'].sum().reset_index()
high_scores_200 = high_scores[high_scores['total_runs'] >= 200]
teams_with_200_scores = high_scores_200['batting_team'].value_counts()
team_with_most_200_scores = teams_with_200_scores.idxmax()
print(" The team that has scored the most number of 200+ scores is:", team_with_most_200_scores)

# Highest run scored by a team in a single match
highest_runs_by_team = df.groupby(['id', 'batting_team'])['total_runs'].sum().reset_index()
max_runs_by_team = highest_runs_by_team.groupby('batting_team')['total_runs'].max()
max_runs_team = max_runs_by_team.idxmax()
max_runs = max_runs_by_team.max()
print("The highest run scored by a team in a single match is:", max_runs, "by", max_runs_team)


# Batsmen who have faced the most number of balls
most_balls_faced = df.groupby('batsman')['ball'].count().sort_values(ascending=False)
top_batsmen = most_balls_faced.head(5)
print("Batsmen who have faced the most number of balls:",)
print(top_batsmen)

# Leading run-scorers of all time
leading_run_scorers = df.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 8))
leading_run_scorers.plot(kind='bar', color='green')
plt.title('Leading Run-Scorers of all Time')
plt.xlabel('Batsman')
plt.ylabel('Runs')
plt.xticks(rotation=45)
plt.show()

# Batsman who has hit the most number of 4's
most_fours = df[df['batsman_runs'] == 4].groupby('batsman')['batsman_runs'].count().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 8))
most_fours.plot(kind='bar', color='purple')
plt.title('Batsman with Most Number of 4s')
plt.xlabel('Batsman')
plt.ylabel('4s')
plt.xticks(rotation=45)
plt.show()

# Batsman who has hit the most number of 6's
most_sixes = df[df['batsman_runs'] == 6].groupby('batsman')['batsman_runs'].count().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 8))
most_sixes.plot(kind='bar', color='brown')
plt.title('Batsman with Most Number of 6s')
plt.xlabel('Batsman')
plt.ylabel('6s')
plt.xticks(rotation=45)
plt.show()

# Calculate strike rate for each batsman
balls_faced = df.groupby('batsman')['ball'].count()
runs_scored = df.groupby('batsman')['batsman_runs'].sum()
strike_rate = (runs_scored / balls_faced) * 100
highest_strike_rate_batsman = strike_rate.idxmax()
highest_strike_rate = strike_rate.max()
print(" Batsman with the highest strike rate:", highest_strike_rate_batsman," with strike rate:", highest_strike_rate)

# Leading wicket-taker
leading_wicket_taker = df2['bowler'].value_counts().idxmax()
wickets_taken = df2['bowler'].value_counts().max()
print(" Leading wicket-taker is", leading_wicket_taker," with the number of wickets taken:", wickets_taken)

# Stadium that has hosted the most number of matches
most_matches_hosted = df['venue'].value_counts().idxmax()
matches_hosted = df['venue'].value_counts().max()
print(" Stadium that has hosted the most number of matches were", most_matches_hosted,"in which the number of matches hosted:", matches_hosted)

