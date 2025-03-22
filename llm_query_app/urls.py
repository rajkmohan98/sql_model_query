from django.urls import path
from .views import QueryAPIView, QueryHistoryAPIView

urlpatterns = [
    path("llm_query/", QueryAPIView.as_view()),
    path("llm_data_history/", QueryHistoryAPIView.as_view()),
]
