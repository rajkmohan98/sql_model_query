from django.db import models



class SQLQueryResponse(models.Model):
    sql_query = models.TextField()
    sql_response = models.TextField()
    database_used = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.database_used} --> {self.sql_query}"
    