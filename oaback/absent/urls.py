from django.urls import path
from .views import AbsentTypeView, ResponderView, AbsentView, AbsentDetailView

urlpatterns = [
    path('type', AbsentTypeView.as_view()),
    path('responder', ResponderView.as_view()),
    path('absent', AbsentView.as_view()),
    path('absent/<int:absent_id>', AbsentDetailView.as_view()),
]
