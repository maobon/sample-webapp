from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Topic(models.Model):
    # link the user ...
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Entry(models.Model):
    # link the topic ... content text
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}"
