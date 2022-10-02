from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}({self.user})'

    class Meta:
        ordering = ('-date_created',)
