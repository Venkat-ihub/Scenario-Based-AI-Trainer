import streamlit as st
import google.generativeai as genai
import json
import os

# Configure the generative AI API
my_api_key_gemini = ""
genai.configure(api_key=my_api_key_gemini)

# Detailed scenario prompts
scenarios = {
    "Doctor": {
        "Role": "You are an empathetic and knowledgeable doctor specializing in general medicine. Your goal is to assist the user, who is playing the role of a patient, by understanding their symptoms, providing advice, suggesting possible causes, and recommending appropriate next steps. Always maintain a professional, compassionate tone.",
        "Guidelines": """
            Initial Interaction:
            Greet the patient warmly.
            
            Symptom Exploration:
            Use open-ended questions to gather detailed information about their symptoms, such as:
                When did the symptoms start?
                How severe are they on a scale of 1 to 10?
                Are there any associated symptoms (e.g., fever, fatigue, etc.)?
                Have they taken any medication or sought treatment so far?
            Diagnosis & Advice:
            Based on the information provided, suggest potential causes for their symptoms, clearly stating that this is not a definitive diagnosis.
            Provide practical advice for symptom management (e.g., rest, hydration, over-the-counter medications) where applicable.
            Mention any red flags that warrant immediate medical attention and recommend consulting a healthcare provider if necessary.
            Tone and Language:
            Be empathetic and avoid using overly technical language unless necessary, always explaining terms in simple words.
            Reassure the patient when needed, showing understanding of their concerns.
            End of Conversation:
            Summarize key points of the discussion.
            Offer to answer any further questions.
            Wish them a quick recovery or good health.
        """
    },
    "Car Dealer": "You are a knowledgeable car dealer. Actively discuss the user's car preferences, budget, and usage, offering personalized suggestions for suitable cars.",
    "Furniture Showroom": "You are a sales representative in a furniture showroom. Actively listen to the user's furniture needs, ask about their style preferences and room dimensions, and suggest options that fit their budget and taste.",
    "Real Estate Agent": "You are an experienced real estate agent. Have a detailed conversation about the user's preferences, such as location, price range, and property type, and suggest properties that meet their criteria.",
    "Teacher": "You are an experienced teacher. Engage the user with personalized educational advice, asking about their goals and suggesting actionable steps for improvement in their chosen subject area.",
}

# Example function to select and use the appropriate role:

def initiate_conversation(role):
    if role in scenarios:
        print(f"Starting conversation as a {role}:")
        print(scenarios[role]['Role'] if isinstance(scenarios[role], dict) else scenarios[role])
    else:
        print("Sorry, I don't recognize that role.")

# Example usage:
role = input("Enter the role for the chatbot (Doctor, Car Dealer, etc.): ")
initiate_conversation(role)

# File for conversation history
HISTORY_FILE = "conversation_history.json"

# Function to send a query to the AI model
def ask_gemini(question, context):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"{context} {question}")

        if response.text:
            return response.text
        else:
            return "Sorry, I couldn't generate a response to that!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Load saved conversation history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return {}

# Save conversation history
def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Streamlit app setup
st.title("Interactive AI Chat with Scenario-Based Conversations")

# Load history
history = load_history()

# Select a scenario
selected_scenario = st.selectbox("Choose a scenario:", list(scenarios.keys()))
context = scenarios[selected_scenario]

# Option to review past conversations
review_mode = st.checkbox("Review Past Conversations")

# Review mode functionality
if review_mode:
    past_conversations = list(history.keys())
    if past_conversations:
        selected_past_conversation = st.selectbox("Select a conversation to review:", past_conversations)
        if selected_past_conversation:
            st.write(f"**Reviewing conversation: {selected_past_conversation}**")
            for message in history[selected_past_conversation]:
                if message["role"] == "user":
                    st.write(f"**You:** {message['content']}")
                else:
                    st.write(f"**AI ({selected_scenario}):** {message['content']}")
    else:
        st.write("No past conversations to review.")
else:
    st.write(f"**You are now in the '{selected_scenario}' scenario.**")

    # Initialize session state for conversation
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Input form for user messages
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:")
        submit = st.form_submit_button("Send")

    # Handle user input and AI response
    if submit and user_input:
        # Add user's input to the conversation
        st.session_state.conversation.append({"role": "user", "content": user_input})

        # Get AI response
        ai_response = ask_gemini(user_input, context)
        st.session_state.conversation.append({"role": "ai", "content": ai_response})

        # Save conversation in history
        conversation_name = f"{selected_scenario}_{len(history) + 1}"
        history[conversation_name] = st.session_state.conversation
        save_history(history)

    # Display ongoing conversation
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**AI ({selected_scenario}):** {message['content']}")
