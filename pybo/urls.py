from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:qid>/', views.detail, name='detail'),
    path('answer/create/<int:qid>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create')
]
