import pandas as pd

# 1. Load the mock data we just created
df = pd.read_csv("mock_gameplay_logs.csv")

# 2. Pick a specific patient (Player 1)
player_id = 1
player_data = df[df['player_id'] == player_id]

# 3. Get their most recent game session
last_game = player_data.iloc[-1]
current_level = last_game['difficulty_level']
reaction_time = last_game['reaction_time_sec']
mistakes = last_game['mistakes_made']

print(f"--- PATIENT {player_id} PERFORMANCE ---")
print(f"Current Level: {current_level}")
print(f"Reaction Time: {reaction_time} seconds")
print(f"Mistakes Made: {mistakes}")
print("-" * 30)

# 4. The DDA Logic (Dynamic Difficulty Adjustment)
if reaction_time < 3.5 and mistakes == 0:
    next_level = min(5, current_level + 1)
    print("AI DECISION: Game was too easy. Increasing difficulty to stimulate brain.")
elif reaction_time > 5.5 or mistakes >= 2:
    next_level = max(1, current_level - 1)
    print("AI DECISION: Game was too hard. Decreasing difficulty to avoid frustration.")
else:
    next_level = current_level
    print("AI DECISION: Perfect balance. Keeping difficulty the same.")

print(f"Next Level Assigned: {next_level}")