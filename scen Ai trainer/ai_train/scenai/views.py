from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Conversation, Message
import google.generativeai as genai

# Configure the generative AI API
genai.configure(api_key="AIzaSyB5YNppBGZgDl6pIxCRdfq5HOJ-Pfnvdjw")

# Define scenarios
SCENARIOS = {
    "Doctor": "You are a professional and empathetic doctor. Respond to the user as a doctor would, providing clear and helpful medical advice.",
    "Car Dealer": "You are a knowledgeable car dealer. Help the user choose the right car by explaining features, pricing, and financing options.",
    "Furniture Showroom": "You are a sales representative in a furniture showroom. Guide the user in selecting furniture based on their preferences and budget.",
    "Real Estate Agent": "You are an experienced real estate agent. Help the user find a home by discussing locations, pricing, and property features.",
    "Teacher": "You are an experienced teacher. Respond to the user with educational advice, lesson planning suggestions, or subject-specific guidance.",
}

# Function to interact with Gemini API
def ask_gemini(question, context):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"{context} {question}")
        return response.text if response.text else "Sorry, I couldn't generate a response to that!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Conversation view (chat and review mode)
def conversation_view(request):
    if request.method == "POST":
        scenario = request.POST.get("scenario")
        user_message = request.POST.get("message")
        context = SCENARIOS.get(scenario)

        # Fetch or create conversation
        conversation, created = Conversation.objects.get_or_create(scenario=scenario)

        # Save user message
        Message.objects.create(conversation=conversation, role="user", content=user_message)

        # Generate AI response
        ai_response = ask_gemini(user_message, context)
        Message.objects.create(conversation=conversation, role="ai", content=ai_response)

        return JsonResponse({"user_message": user_message, "ai_response": ai_response})

    # Load conversations for review
    conversations = Conversation.objects.all().order_by("-timestamp")
    return render(request, "conversation.html", {"scenarios": SCENARIOS, "conversations": conversations})

# Review conversation view
def review_conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()
    return render(request, "review_conversation.html", {"conversation": conversation, "messages": messages})
