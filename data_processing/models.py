from django.db import models


class DataFile(models.Model):
    user = models.ForeignKey('core.User', blank=False, null=False, on_delete=models.CASCADE)
    csv = models.FileField()
    result = models.TextField(blank=True, null=True)
