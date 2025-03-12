from rest_framework import viewsets
from .models import Problem, Submission
from .serializers import ProblemSerializer, SubmissionSerializer

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

from django.db.models import Sum
from django.shortcuts import render
from .utils import check_plagiarism
from .models import User

def leaderboard(request):
    users = User.objects.annotate(total_score=Sum('submission__score')).order_by('-total_score')
    return render(request, 'leaderboard.html', {'users': users})

def submit_code(request):
    check_plagiarism(request.user, request.POST['code'])
