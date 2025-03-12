from django.db import models

# models.py
from django.contrib.auth.models import AbstractUser

#task 1. Modle
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=True)
    is_judge = models.BooleanField(default=False)

#task 2. Modle
# models.py
class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    test_cases = models.JSONField()  # Store input-output pairs

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    result = models.CharField(max_length=255)
