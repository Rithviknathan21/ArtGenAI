from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework import serializers, viewsets
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import docker
import os

# 1. Custom User Model with Roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('participant', 'Participant'),
        ('judge', 'Judge'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')

# 2. Problem Model
class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    constraints = models.TextField()
    test_cases = models.JSONField()

# 3. Submission Model
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=[('python', 'Python'), ('cpp', 'C++')])
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

# 4. Real-Time Leaderboard
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

# 5. Code Execution using Docker
class CodeExecutor:
    @staticmethod
    def run_code(code, language):
        client = docker.from_env()
        container = client.containers.run(
            "python:3.8" if language == "python" else "gcc:latest",
            command=f'python -c "{code}"' if language == "python" else f'gcc -o main main.cpp && ./main',
            remove=True,
            stdout=True,
            stderr=True,
        )
        return container

# 6. Contest Model
class Contest(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    problems = models.ManyToManyField(Problem)

# 7. Rating System (Elo-based)
def update_rating(winner, loser):
    k = 32
    expected_win = 1 / (1 + 10 ** ((loser.score - winner.score) / 400))
    winner.score += int(k * (1 - expected_win))
    loser.score -= int(k * expected_win)
    winner.save()
    loser.save()

# 8. Multi-Language Support
SUPPORTED_LANGUAGES = ['python', 'cpp']

def is_language_supported(language):
    return language in SUPPORTED_LANGUAGES

# 9. API for External Code Evaluation
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def evaluate_code(request):
    code = request.data.get("code")
    language = request.data.get("language")
    if not is_language_supported(language):
        return Response({"error": "Unsupported language"}, status=400)
    result = CodeExecutor.run_code(code, language)
    return Response({"output": result})

# 10. Admin Panel for Contests
class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time')
admin.site.register(Contest, ContestAdmin)

# 11. Achievements System
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_earned = models.DateTimeField(default=timezone.now)

# 12. Discussion Forum
class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

# 13. Problem Difficulty Rating
class ProblemRating(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)  # Scale 1-5

# 14. Secure Backup and Recovery (Dummy Command)
def backup_database():
    os.system("pg_dump cp_platform > backup.sql")

# 15. Analytics Dashboard (Dummy Data)
def get_contest_insights():
    return {
        "total_users": User.objects.count(),
        "total_submissions": Submission.objects.count(),
        "active_contests": Contest.objects.filter(start_time__lte=timezone.now(), end_time__gte=timezone.now()).count()
    }

# 16. Django REST Framework Serializers
class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

# 17. Viewsets for API
class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

# 18. Django URL Routing
router = DefaultRouter()
router.register(r'problems', ProblemViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/evaluate/', evaluate_code),
]

# 19. Setup Django Channels for Real-Time Updates (Leaderboard)
ASGI_APPLICATION = "cp_platform.routing.application"

# 20. Running Django Server
if __name__ == "__main__":
    os.system("python manage.py runserver")
