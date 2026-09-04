import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# 1. Load the simulated patient data we generated earlier
patient_data = pd.read_csv("mock_gameplay_logs.csv")

# 2. Define the "Teacher" rules 
# The AI needs examples of what a good decision looks like so it can learn.
def teach_ai_difficulty_rules(patient_session):
    reaction_time = patient_session['reaction_time_sec']
    mistakes = patient_session['mistakes_made']
    current_level = patient_session['difficulty_level']
    
    if reaction_time < 3.5 and mistakes == 0:
        return min(5, current_level + 1) # Too easy -> Increase difficulty
    elif reaction_time > 5.5 or mistakes >= 2:
        return max(1, current_level - 1) # Too hard -> Decrease difficulty
    else:
        return current_level             # Perfect -> Keep it the same

# Apply the teacher rules to create the "correct answers" for the AI to study
patient_data['correct_next_level'] = patient_data.apply(teach_ai_difficulty_rules, axis=1)

# 3. Separate what the AI studies (Inputs) from what it must guess (Outputs)
learning_inputs = patient_data[['difficulty_level', 'reaction_time_sec', 'mistakes_made']]
correct_answers = patient_data['correct_next_level']

# 4. Create and train the Machine Learning "Brain"
print("Starting AI training...")
ai_brain = DecisionTreeClassifier()
ai_brain.fit(learning_inputs, correct_answers) # This is where it actually learns!

# 5. Save the trained Brain to a file so our API server can use it later
with open('ai_model.pkl', 'wb') as file:
    pickle.dump(ai_brain, file)

print("Success! The trained AI brain has been saved as 'ai_model.pkl'")