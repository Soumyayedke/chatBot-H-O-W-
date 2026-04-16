import streamlit as st
import re
import datetime
import pandas as pd
import os

# ---------------------------
# CONFIG
# ---------------------------
LOG_FILE = "chat_logs.csv"

# ---------------------------
# ENTITY RECOGNITION
# ---------------------------
def extract_entities(text):
    entities = {}

    # Semester (SEM 1, sem 5, etc.)
    sem_match = re.search(r"(sem|semester)\s*(\d+)", text, re.IGNORECASE)
    if sem_match:
        entities["semester"] = int(sem_match.group(2))

    # Course code (CS101, ME202 etc.)
    course_match = re.search(r"\b([A-Z]{2,4}\d{2,4})\b", text)
    if course_match:
        entities["course_code"] = course_match.group(1)

    # Date keywords
    if "today" in text.lower():
        entities["date"] = str(datetime.date.today())
    elif "tomorrow" in text.lower():
        entities["date"] = str(datetime.date.today() + datetime.timedelta(days=1))

    # Year phrases
    if "first year" in text.lower():
        entities["semester"] = 1
    elif "second year" in text.lower():
        entities["semester"] = 3
    elif "third year" in text.lower():
        entities["semester"] = 5
    elif "fourth year" in text.lower():
        entities["semester"] = 7

    return entities


# ---------------------------
# INTENT DETECTION
# ---------------------------
def detect_intent(text):
    text = text.lower()

    if "exam" in text:
        return "exam_query"
    elif "schedule" in text or "timetable" in text:
        return "schedule_query"
    elif "result" in text:
        return "result_query"
    elif "help" in text:
        return "help"
    else:
        return "unknown"


# ---------------------------
# RESPONSE GENERATION
# ---------------------------
def generate_response(user_input, state):
    entities = extract_entities(user_input)
    intent = detect_intent(user_input)

    # Merge with previous state (multi-turn support)
    if "last_entities" in state:
        for key, value in state["last_entities"].items():
            if key not in entities:
                entities[key] = value

    if intent == "unknown":
        intent = state.get("last_intent", "unknown")

    # Save state
    state["last_entities"] = entities
    state["last_intent"] = intent

    # ---------------- RESPONSE LOGIC ----------------
    if intent == "exam_query":
        if "semester" in entities and "course_code" in entities:
            return f"Exam for {entities['course_code']} (SEM {entities['semester']}) is scheduled next week."
        elif "semester" in entities:
            return f"SEM {entities['semester']} exams are expected next month. Please confirm course code."
        else:
            return "Which semester or course are you asking about?"

    elif intent == "schedule_query":
        if "semester" in entities:
            return f"Timetable for SEM {entities['semester']} will be released on the portal soon."
        else:
            return "Please specify semester for timetable."

    elif intent == "result_query":
        return "Results are usually announced 30 days after exams."

    elif intent == "help":
        return "You can ask about exams, schedules, or results. Example: 'When is SEM 5 CS exam?'"

    # ---------------- FALLBACK STRATEGY ----------------
    else:
        return (
            "I'm not sure I understood that.\n\n"
            "👉 Try asking:\n"
            "- 'When is SEM 3 exam?'\n"
            "- 'Timetable for CS101'\n\n"
            "If your query is complex, contact advisor:\n"
            "📧 advisor@college.edu"
        )


# ---------------------------
# LOGGING
# ---------------------------
def log_interaction(user, bot, intent):
    data = {
        "timestamp": datetime.datetime.now(),
        "user_input": user,
        "bot_response": bot,
        "intent": intent
    }

    df = pd.DataFrame([data])

    if os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)


# ---------------------------
# ANALYTICS (SIMPLE)
# ---------------------------
def show_logs():
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        st.subheader("📊 Interaction Logs")
        st.dataframe(df)

        st.subheader("📈 Intent Distribution")
        st.bar_chart(df["intent"].value_counts())
    else:
        st.info("No logs yet.")


# ---------------------------
# SIMULATED MULTI-PLATFORM BEHAVIOR
# ---------------------------
def platform_hint(platform):
    if platform == "Web":
        return "🌐 Web Chat: Full UI enabled"
    elif platform == "Mobile":
        return "📱 Mobile: Short responses preferred"
    elif platform == "WhatsApp":
        return "💬 WhatsApp: Text-only, quick replies"
    return ""


# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="CampusQuery AI", layout="centered")

st.title("🎓 CampusQuery AI")
st.caption("Ask about exams, schedules, and results")

# Platform selector
platform = st.selectbox("Select Platform Simulation", ["Web", "Mobile", "WhatsApp"])
st.info(platform_hint(platform))

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "state" not in st.session_state:
    st.session_state.state = {}

# Input
user_input = st.text_input("Ask your question:")

if st.button("Send") and user_input:
    response = generate_response(user_input, st.session_state.state)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

    log_interaction(user_input, response, st.session_state.state.get("last_intent"))

# Chat display
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")

# Logs
if st.checkbox("Show Logs & Analytics"):
    show_logs()


# ---------------------------
# IMPROVEMENT SUGGESTIONS
# ---------------------------
st.markdown("---")
st.subheader("🔧 Suggested Improvements")

st.markdown("""
- Add NLP model (spaCy / BERT) for better entity extraction  
- Expand intents:
  - fee_query
  - admission_query
  - placement_query  
- Add real database/API for exam schedules  
- Improve WhatsApp UX with buttons (via Twilio API)  
- Auto-learn FAQs from logs  
- Add multilingual support (Hindi, Marathi)
""")
