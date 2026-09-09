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

# Bhashini API Credentials
BHASHINI_USER_ID = "501b3c2263b7414ba9aacc6cc1fa7b75"
BHASHINI_API_KEY = "048ea6f7b9-fcdf-4055-b39b-cab0303d76c4"
BHASHINI_INFERENCE_KEY = "yQAYejCkiO8yg8O-YqJpmzvz2PzvVLY_nN1Qg2sYCBkXboclCRo_l7cVRBOE4WnA"
BHASHINI_COMPUTE_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

# --- REGIONAL LANGUAGE VOICE ENGINE ---
class RegionalPrompt(BaseModel):
    text_to_speak: str
    target_language: str  # e.g., "hi" (Hindi), "bn" (Bengali), "en" (English)

# Fallback offline dictionary for essential dementia reminders
OFFLINE_TRANSLATIONS = {
    "hi": {
        "take your medicine": "कृपया अपनी दवाई लें",
        "drink water": "कृपया पानी पीजिए",
        "time to sleep": "सोने का समय हो गया है"
    },
    "bn": {
        "take your medicine": "আপনার ওষুধ খাওয়ার সময় হয়েছে",
        "drink water": "জল খেয়ে নিন",
        "time to sleep": "ঘুমানোর সময় হয়েছে"
    }
}

@app.post("/speak_regional_reminder")
def speak_regional_text(prompt: RegionalPrompt):
    lang = prompt.target_language.lower()
    original_text = prompt.text_to_speak.lower()
    
    # 1. Determine translated text (checks offline dictionary first)
    translated_text = prompt.text_to_speak
    if lang in OFFLINE_TRANSLATIONS and original_text in OFFLINE_TRANSLATIONS[lang]:
        translated_text = OFFLINE_TRANSLATIONS[lang][original_text]
        source = "Offline Regional Dictionary"
    else:
        source = "Direct Pass-through / Live Bhashini Pipeline"
    
    # 2. Trigger audio playback
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)  # Measured pace for elderly comprehension
    engine.say(translated_text)
    engine.runAndWait()
    engine.stop()
    
    return {
        "original_text": prompt.text_to_speak,
        "target_language": lang,
        "spoken_text": translated_text,
        "translation_engine": source
    }
