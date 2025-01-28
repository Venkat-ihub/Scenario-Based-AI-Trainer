import google.generativeai as genai
import os

# Set your Gemini API key
my_api_key_gemini = "AIzaSyB5YNppBGZgDl6pIxCRdfq5HOJ-Pfnvdjw"  # Replace with your actual API key

# Configure the generative AI API
genai.configure(api_key=my_api_key_gemini)

# Define scenario contexts
scenarios = {
    "doctor": "You are a professional and empathetic doctor. Respond to the user as a doctor would, providing clear and helpful medical advice.",
    "car_dealer": "You are a knowledgeable car dealer. Help the user choose the right car by explaining features, pricing, and financing options.",
    "furniture_sales": "You are a sales representative in a furniture showroom. Guide the user in selecting furniture based on their preferences and budget.",
    "real_estate_agent": "You are an experienced real estate agent. Help the user find a home by discussing locations, pricing, and property features.",
    "teacher": "You are an experienced teacher. Respond to the user with educational advice, lesson planning suggestions, or subject-specific guidance.",
}

# Function to generate a response from Gemini
def ask_gemini(question, context):
    try:
        # Use the generative model to generate content
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"{context} {question}")

        # Check if there's valid text in the response
        if response.text:
            return response.text
        else:
            return "Sorry, I couldn't generate a response to that!"
    except Exception as e:
        # Handle any exceptions (like invalid API key, network issues, etc.)
        return f"An error occurred: {str(e)}"

# Main scenario-based chatbot
def scenario_based_ai_trainer():
    print("Welcome to the Scenario-Based AI Trainer!")
    print("Available scenarios:")
    for key in scenarios.keys():
        print(f"- {key}")

    # Let the user select a scenario
    selected_scenario = input("\nChoose a scenario: ").strip().lower()
    if selected_scenario not in scenarios:
        print("Invalid scenario selected. Defaulting to 'doctor'.")
        selected_scenario = "doctor"

    context = scenarios[selected_scenario]
    print(f"\nYou are now interacting in the '{selected_scenario}' scenario. Type 'quit' to exit.\n")

    # Start the conversation loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        # Get the response from Gemini
        reply = ask_gemini(user_input, context)
        print(f"AI ({selected_scenario.capitalize()}): {reply}")

# Run the AI Trainer
if __name__ == "__main__":
    scenario_based_ai_trainer()
