import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Institute FAQ Assistant",
    page_icon="🎓",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make the chat container look cleaner */
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    
    /* Style the sidebar buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 20px;
        border: 1px solid #4a90e2;
        background-color: transparent;
        color: #4a90e2;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #4a90e2;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Chat Logic ---
def get_response(user_input):
    msg = user_input.lower().strip()
    
    responses = {
        ("hi", "hello", "hey", "namaste"): "Hello! I'm your Institute Assistant. How can I help you today? 👋",
        ("time", "hours", "open", "schedule", "timing"): "🕒 The institute is open **Monday to Friday, 9:00 AM to 5:00 PM**.",
        ("fee", "cost", "price", "tuition", "fees"): "💰 Fees vary by course. Generally, it ranges from **₹50,000 to ₹2,00,000 per semester**.",
        ("contact", "call", "phone", "email", "address", "location"): "📞 Reach us at **0712 619 2403** or visit us at **123 Education Lane, Nagpur**.",
        ("apply", "admission", "join"): "📝 Admissions are open! Apply on our website's **'Admissions'** page.",
        ("course", "major", "study", "program", "offer"): "📚 We offer programs in:\n- Data Science\n- Web Development\n- Digital Marketing\n- AI & Machine Learning",
        ("scholarship", "aid"): "🎖 We offer **merit-based scholarships** up to 50%. Deadline: **March 1st**.",
        ("job", "placement", "career", "internship"): "💼 Our placement cell helps students secure roles with top global companies.",
        ("hostel", "dorm", "housing"): "🏠 On-campus housing is available on a **first-come, first-served** basis.",
    }

    for keywords, response in responses.items():
        if any(word in msg for word in keywords):
            return response
            
    return "I'm sorry, I didn't quite catch that. Could you try asking about timings, fees, courses, or admissions?"

# --- Sidebar: Useful Info & Actions ---
with st.sidebar:
    st.title("🎓 Info Hub")
    st.info("Quickly find answers to common questions or reset your chat below.")
    
    st.markdown("### ⚡ Quick Actions")
    if st.button("Clear Conversation"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]
        st.rerun()

    st.markdown("---")
    st.markdown("**Contact Support**")
    st.markdown("📧 support@institute.com")
    st.markdown("📞 0712 619 2403")

# --- Main UI ---
st.title("Institute FAQ Assistant")
st.caption("🚀 Powered by Streamlit | v2.0")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Institute Assistant. How can I help you with courses, fees, or admissions today?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Suggested Chips (Horizontal Buttons) ---
st.write("Try asking:")
cols = st.columns([1,1,1,1])
suggestions = ["🕒 Timings", "💰 Fees", "📚 Courses", "📝 Admissions"]

for i, suggestion in enumerate(suggestions):
    if cols[i % 4].button(suggestion, key=f"suggest_{i}"):
        # Simulate user input from button
        user_text = suggestion.split(" ")[1] # Get word after emoji
        st.session_state.messages.append({"role": "user", "content": suggestion})
        response = get_response(user_text)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- Chat Input ---
if prompt := st.chat_input("Ask me about the institute..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response with a slight delay for "thinking" feel
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_response(prompt)
        
        # Simple typewriter effect
        typed_response = ""
        for char in full_response:
            typed_response += char
            time.sleep(0.01)
            message_placeholder.markdown(typed_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
