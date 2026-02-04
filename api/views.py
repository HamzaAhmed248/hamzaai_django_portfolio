import os
from datetime import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ollama import Client  # Ollama cloud client

from .models import Conversation, KnowledgeBase
from .serializers import ConversationSerializer

# ---------- FRONTEND PAGES ----------
def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# ---------- UTILITY ----------
def get_client_ip(request):
    """Get the real IP address of the user"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


# ---------- CHATBOT ----------
def get_chatbot_response(question):
    """Send question and KnowledgeBase prompt to Ollama cloud model and return the response"""
    
    API_KEY = os.getenv("OLLAMA_API_KEY")  # Load key from .env

    if not API_KEY:
        return "Error: Ollama API key is not configured"

    try:
        client = Client(
            host="https://ollama.com",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )

        # Include KnowledgeBase prompt
        try:
            prompt = KnowledgeBase.get_prompt()
        except Exception:
            prompt = "You are a helpful assistant."

        messages = [
            {"role": "system", 
            "content": prompt},  # Send the KB prompt
            {"role": "user", 
            "content": question}   # Send the user question
        ]
        
        # Stream response from the model
        response_text = ""
        for part in client.chat("gpt-oss:120b", messages=messages, stream=True):
            response_text += part["message"]["content"]

        return response_text

    except Exception as e:
        return f"Error: {str(e)}"


# ---------- CHAT API ----------
@api_view(['POST'])
def chat(request):
    """Receive question, get chatbot response, save conversation, return serialized data"""

    ip_address = get_client_ip(request)
    question = request.data.get("question")

    if not question:
        return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Get answer from Ollama cloud, including the KnowledgeBase prompt
    answer = get_chatbot_response(question)

    # Save conversation by IP
    conversation, _ = Conversation.objects.get_or_create(
        ip_address=ip_address,
        defaults={"conversation_text": ""}
    )

    now = datetime.now()
    conversation.conversation_text += (
        f"Q : {question} ( Time : {now.strftime('%I:%M %p')} | Date : {now.strftime('%d/%m/%Y')} )\n"
        f"Ans : {answer}\n"
    )
    conversation.save()

    return Response(ConversationSerializer(conversation).data)
