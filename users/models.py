from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Hồ sơ của {self.user.username}"

    def __str__(self):
        return self.user.username
    
    
