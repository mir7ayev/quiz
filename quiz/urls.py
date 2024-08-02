from django.urls import path
from .views import QuizViewSet

urlpatterns = [
    path('subjects/', QuizViewSet.as_view({'get': 'subjects'})),
    path('questions/', QuizViewSet.as_view({'post': 'questions'})),
    path('answers/', QuizViewSet.as_view({'post': 'answers'})),
]
