from django.db import models

class QueryResponse(models.Model):
    query = models.TextField()
    response = models.TextField()
    model_used = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query}... -> {self.model_used}"


