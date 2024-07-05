from django.urls import path

from testApi import views

urlpatterns = [
    path('inquiry/', views.inquiry_all_money, name='inquiry')
]

