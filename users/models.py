from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

class User(models.Model):
    name = models.CharField("Name", max_length=40, unique=True)
    secret = models.CharField("Secret", max_length=20)
    registrationDate = models.DateField("Registration Date", auto_now_add=True)

    def __str__(self):
        return self.name

class UserAPIKey(AbstractAPIKey):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_key",
    )
