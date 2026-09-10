# Smriti 🌸 - Dementia AI Engine

Dementia isolates patients and overwhelms caregivers. **Smriti** is a culturally localized, AI-powered cognitive care platform designed to bridge this gap through adaptive therapy, real-time monitoring, and extreme accessibility. Initially tailored for the elderly population in Northeast India, Smriti breaks both language and technology barriers.

## 🚀 Key Features

### 1. Patient Portal (Accessible & Localized)
* **High-Contrast UI:** Designed specifically for seniors with a large-button PIN pad.
* **Culturally Rooted Cognitive Games:** Replaces generic puzzles with familiar cultural contexts (e.g., *Market Day Basket*, *Bihu Sound & Rhythm Match*).
* **Multilingual Native Voice:** Fully integrated with the **Bhashini API** for real-time text translation and voice synthesis (TTS) in regional languages (e.g., Assamese).
* **Smriti AI Assistant:** Powered by Gemini AI, allowing patients to ask questions and receive spoken, localized responses.

### 2. Clinical Caregiver Dashboard
* **Patient Roster & Alerts:** Centralized command center showing active alerts for missed routines (medication, hydration).
* **ML Analytics (85% Rule):** The engine dynamically adjusts game difficulty based on real-time accuracy and reaction time, enforcing the proven "85% rule for optimal learning" to prevent cognitive frustration.
* **Secure Onboarding:** 1-Touch Fingerprint/Face ID authentication for clinicians.

### 3. Extreme Accessibility & Offline Mode
* **WhatsApp Companion Bot:** Patients can receive reminders and one-click game links directly on WhatsApp, eliminating the need to learn a new interface.
* **Offline PWA Support:** Patients can play games in zero-connectivity areas. Data caches locally and automatically syncs to the cloud once network access is restored.

## 🛠️ Tech Stack
* **Backend:** FastAPI (Python), Hosted on Render
* **Frontend:** React / Next.js, HTML5 Audio integration for seamless TTS playback
* **AI & Machine Learning:** Custom DDA (Dynamic Difficulty Adjustment) Engine, Google Gemini API
* **Language & Voice Services:** Official Government of India Bhashini API (Translation & Chained TTS Pipeline)
* **Database & Security:** MongoDB, fully compliant with the **DPDP Act 2023**

## 📡 Core API Endpoints
The backend powers complex, chained AI tasks in a single request:
* `POST /speak_regional_reminder`: Translates cognitive therapy prompts into native languages.
* `POST /synthesize_speech`: A chained Bhashini pipeline that instantly translates text and returns a raw Base64 audio string for frontend rendering.

## 🔮 Future Scope
* Implementation of SMS and IVR calling for patients in extreme low-connectivity areas without smartphone access.
* Expansion of the Brain Games library to include diverse cultural contexts across other Indian states.
