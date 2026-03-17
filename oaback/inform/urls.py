from django.urls import path
from .views import InformView, InformDetailView, InformReadView, ImageUploadView, FileUploadView

urlpatterns = [
    path('inform', InformView.as_view()),
    path('inform/read', InformReadView.as_view()),
    path('inform/<int:pk>', InformDetailView.as_view()),
    path('image/upload', ImageUploadView.as_view()),
    path('file/upload', FileUploadView.as_view()),
]
