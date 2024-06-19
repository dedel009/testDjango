from django.urls import path

from .views import base_views, question_views, answer_views

app_name = 'pybo'

urlpatterns = [
    path('', base_views.main, name='main'),
    path('<int:qid>/', base_views.detail, name='detail'),
    path('answer/create/<int:qid>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:aid>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:aid>/', answer_views.answer_delete, name='answer_delete'),
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:qid>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:qid>/', question_views.question_delete, name="question_delete"),
]
