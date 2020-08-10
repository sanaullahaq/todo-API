from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)  # it can be left blank
    created = models.DateTimeField(auto_now_add=True)
    # this will automatically add date and time and the user can't edit this

    dateCompleted = models.DateTimeField(null=True, blank=True)
    # this is similar to blank=True but since the date has a format like 'D M Y' that's why we should use null=True
    # and blank=True if we want to left this field blank, more details on django model files documentation

    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
