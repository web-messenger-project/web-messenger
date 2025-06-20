from django.db import models

class userDB(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=75)

    login = models.CharField(max_length=50)
    email = models.CharField(max_length=125)
    password = models.CharField(max_length=100)

    creation_date = models.DateField(auto_now_add=True)

    included_in_these_chats = models.JSONField(default=list)

class chatDB(models.Model):
    name = models.CharField(max_length=50)
    members = models.JSONField(default=list)

    messages = models.JSONField(default=list)