import logging
import requests

from django.conf import settings
from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import openai

from .models import QueryResponse
from .serializers import QueryResponseSerializer

logging.basicConfig(filename='query_responses.log', level=logging.INFO,)


def query_openai(prompt):
    openai.api_key = settings.OPENAI_API_KEY 

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]  


def query_llama(prompt):
    return f"LLaMA Model Response: {prompt}"


API_URL = "https://api-inference.huggingface.co/models/gpt2"  
HEADERS = {f"Authorization": "Bearer {settings.HUGGINGFACE_API_KEY}"}  

def query_huggingface(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    return response.json()





class QueryAPIView(APIView):
    def post(self, request):
        try:
            model = request.data.get("model", "openai")  
            query = request.data.get("query")
            if not query:
                return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)
            if model == "openai":
                response = query_openai(query)
            elif model == "llama":
                response = query_llama(query)
            elif model == "huggingface":
                response = query_huggingface(query)
            else:
                return Response({"error": "Invalid model selection."}, status=status.HTTP_400_BAD_REQUEST)
            query_response = QueryResponse.objects.create(query=query, response=response, model_used=model)
            return Response({"model": model, "response": response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QueryHistoryAPIView(APIView):
    def get(self, request):
        responses = QueryResponse.objects.all()
        serializer = QueryResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
