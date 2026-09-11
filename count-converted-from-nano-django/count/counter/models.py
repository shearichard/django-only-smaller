from django.db import models


class CountLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
