from django.urls import path
from .views import InformView, InformDetailView, InformReadView

urlpatterns = [
    path('inform', InformView.as_view()),
    path('inform/read', InformReadView.as_view()),
    path('inform/<int:pk>', InformDetailView.as_view()),
]
