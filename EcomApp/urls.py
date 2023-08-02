from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('/quiz', Quiz.as_view(), name='quiz'),
    path('r/<str:topic>/', RandomQuesions.as_view(), name='random'),
    path('q/<str:topic>/', QuizQuesions.as_view(), name='questions'),
]