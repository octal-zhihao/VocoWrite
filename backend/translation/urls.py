from django.urls import path
from .views import TranslationView

urlpatterns = [
    path('api/', TranslationView.as_view(), name='translate')
]
