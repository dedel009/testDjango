from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:qid>/', views.detail, name='detail'),
    path('answer/create/<int:qid>/', views.answer_create, name='answer_create'),
    path('answer/modify/<int:aid>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:aid>/', views.answer_delete, name='answer_delete'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:qid>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:qid>/', views.question_delete, name="question_delete"),
]
