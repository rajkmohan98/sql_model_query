from django.urls import path
from .views import SQLQueryAPIView, QueryHistoryAPIView

urlpatterns = [
    path("sql_query/", SQLQueryAPIView.as_view(), name="query"),
    path("sql_data_history/", QueryHistoryAPIView.as_view(), name="history"),
]
