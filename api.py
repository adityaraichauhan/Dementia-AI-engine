from fastapi import FastAPI
from pydantic import BaseModel
import pyttsx3
import pickle

# 1. WAKE UP THE AI: Load the trained Brain when the server starts
with open('ai_model.pkl', 'rb') as file:
    ai_brain = pickle.load(file)

app = FastAPI(title="Dementia App AI Engine")

# --- SMART GAME DIFFICULTY LOGIC (NOW USING ML) ---
class GameSession(BaseModel):
    reaction_time: float
    mistakes: int
    current_level: int

@app.post("/get_next_difficulty")
def calculate_difficulty(data: GameSession):
    # Package the patient's stats in the exact order the AI studied them:
    # [current_level, reaction_time, mistakes]
    patient_stats = [[data.current_level, data.reaction_time, data.mistakes]]
    
    # Ask the AI Brain to predict the best next level based on its training
    predicted_level_array = ai_brain.predict(patient_stats)
    next_level = int(predicted_level_array[0]) # Extract the number from the AI's answer
    
    # Generate a simple reason for the dashboard
    if next_level > data.current_level:
        reason = "AI recognized an 'easy' pattern. Increasing level."
    elif next_level < data.current_level:
        reason = "AI recognized a 'struggle' pattern. Decreasing level."
    else:
        reason = "AI recognized a 'perfect' pattern. Keeping level."
        
    return {"new_difficulty_level": next_level, "ai_reasoning": reason}

# --- OFFLINE VOICE LOGIC (UNCHANGED) ---
class VoicePrompt(BaseModel):
    text_to_speak: str

@app.post("/speak_reminder")
def speak_text(prompt: VoicePrompt):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140) 
    engine.say(prompt.text_to_speak)
    engine.runAndWait()
    engine.stop() 
    
    return {"status": "Success", "message": f"Spoke: {prompt.text_to_speak}"}

# --- COGNITIVE HEALTH SCORING ---
class PatientHistory(BaseModel):
    patient_id: int
    games_played_this_week: int
    average_reaction_time: float
    total_mistakes_this_week: int

@app.post("/calculate_health_score")
def get_cognitive_score(history: PatientHistory):
    # A simple baseline scoring algorithm (100 is perfect health)
    base_score = 100
    
    # Deduct points for slow average reaction times and frequent mistakes
    time_penalty = max(0, (history.average_reaction_time - 3.5) * 5)
    mistake_penalty = history.total_mistakes_this_week * 2
    
    final_score = max(0, base_score - time_penalty - mistake_penalty)
    
    # Determine the clinical alert level
    if final_score >= 85:
        status = "Stable"
    elif final_score >= 60:
        status = "Mild Decline - Monitor"
    else:
        status = "Significant Decline - Alert Doctor"
        
    return {
        "cognitive_health_score": round(final_score, 1),
        "clinical_status": status
    }