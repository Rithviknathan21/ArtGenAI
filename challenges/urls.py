from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProblemViewSet, SubmissionViewSet
from .views import home
router = DefaultRouter()
router.register(r'problems', ProblemViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', home, name='home'),  # Home page URL

]
