from django.urls import path
from .views import GapAnalysisView

urlpatterns = [
    path('analyze/', GapAnalysisView.as_view()),
]