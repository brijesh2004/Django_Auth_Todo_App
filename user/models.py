from django.db import models
# Create your models here.

class TodoModel(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User' , on_delete=models.CASCADE , related_name='todos')


    def __str__(self):
        return f"{self.title} (User: {self.user.username})"

