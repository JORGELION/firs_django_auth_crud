from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    titel = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.titel + " - por " + self.user.username
