import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the results from the CSV file
file_path = '/mnt/data/combat_simulation_results.csv'
df = pd.read_csv(file_path)

# Display the first few rows to understand the data structure
print("First few rows of the data:")
print(df.head())

# Calculate the number of wins for each class
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Class', 'Wins']

# Calculate the total number of battles each class participated in
class_counts = df['Player1_Class'].value_counts() + df['Player2_Class'].value_counts()
class_counts = class_counts.reset_index()
class_counts.columns = ['Class', 'Total_Battles']

# Merge win counts and class counts
stats = pd.merge(win_counts, class_counts, on='Class')

# Calculate win rate
stats['Win_Rate'] = stats['Wins'] / stats['Total_Battles']

# Display the statistics
print("Win rate statistics:")
print(stats)

# Bar plot of win rates
plt.figure(figsize=(10, 6))
plt.bar(stats['Class'], stats['Win_Rate'], color='skyblue')
plt.xlabel('Class')
plt.ylabel('Win Rate')
plt.title('Win Rate by Class')
plt.xticks(rotation=45)
plt.show()

# Save the plot as an image file
plt.savefig("win_rate_by_class.png")

# Calculate the number of battles and wins for each pair of classes
pair_results = df.groupby(['Player1_Class', 'Player2_Class', 'Winner']).size().unstack(fill_value=0)
pair_results.columns = [f'Wins_as_{col}' for col in pair_results.columns]
pair_results = pair_results.reset_index()

# Display pair results for debugging
print("Pair results:")
print(pair_results)

# Pivot table for heatmap
pivot_table = df.pivot_table(index='Player1_Class', columns='Player2_Class', values='Winner', aggfunc=lambda x: (x == x.name).sum(), fill_value=0)

# Display pivot table for debugging
print("Pivot table:")
print(pivot_table)

# Heatmap of class-vs-class win counts
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, annot=True, fmt='d', cmap='Blues')
plt.title('Class vs Class Win Counts')
plt.xlabel('Player 2 Class')
plt.ylabel('Player 1 Class')
plt.show()

# Save the heatmap as an image file
plt.savefig("class_vs_class_heatmap.png")

# Generate detailed bar plots for each class
for player_class in pivot_table.index:
    plt.figure(figsize=(10, 6))
    sns.barplot(x=pivot_table.columns, y=pivot_table.loc[player_class])
    plt.title(f'Performance of {player_class} Against Other Classes')
    plt.xlabel('Opponent Class')
    plt.ylabel('Win Count')
    plt.xticks(rotation=45)
    plt.show()
    plt.savefig(f"{player_class}_vs_classes.png")