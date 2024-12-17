from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', views.homepage, name='homepage'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add_questions/', views.add_questions, name='add_questions'),
    path('history/', views.history, name='history'),
    path('history/<int:history_id>/', views.quiz_history_detail, name='quiz_history_detail'),
]
