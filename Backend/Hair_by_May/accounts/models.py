from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    # more fields will be added here as needed

    def __str__(self):
        return self.username