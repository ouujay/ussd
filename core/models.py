from django.db import models

class Session(models.Model):
    session_id = models.CharField(max_length=120, unique=True)
    phone_number = models.CharField(max_length=20)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
