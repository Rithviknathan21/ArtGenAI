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

class Contest(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='scheduled')

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1200)

class Submission(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
    ]
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)

class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)

