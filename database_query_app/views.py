from django.shortcuts import render
import logging
import json
import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SQLQueryResponse
from .serializers import SQLQueryResponseSerializer
from .database import get_db_connection

logging.basicConfig(filename="query_responses.log", level=logging.INFO)

class SQLQueryAPIView(APIView):
    def post(self, request):
        try:
            query = request.data.get("query")
            database = request.data.get("database", "postgres")  

            if not query:
                return Response({"error": "SQL query is required."}, status=status.HTTP_400_BAD_REQUEST)

            conn = get_db_connection(database)
            if conn is None:
                return Response({"error": "Failed to connect to the database."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    columns = [col[0] for col in cursor.description]  # Get column names
                    response_data = cursor.fetchall()  # Fetch data once

                    # Convert to Pandas DataFrame
                    df = pd.DataFrame(response_data, columns=columns)
                    result_dict = df.to_dict(orient="records")  

            except Exception as e:
                return Response({"error": f"Database query failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            finally:
                conn.close()  

            # Save query response to DB
            query_response = SQLQueryResponse.objects.create(
                sql_query=query,
                sql_response=json.dumps(result_dict),  # Save formatted response
                database_used=database
            )

            logging.info(f"DB: {database}, Query: {query}, Response: {result_dict}")

            return Response({
                "database": database,
                "query": query,
                "response": result_dict
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QueryHistoryAPIView(APIView):
    def get(self, request):
        responses = SQLQueryResponse.objects.all()
        serializer = SQLQueryResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)