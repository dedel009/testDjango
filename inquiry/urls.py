from django.urls import path

from inquiry import views

app_name = 'inquiry'

urlpatterns = [
    path('inquiry/', views.deposit_inquiry_all_money, name='deposit')
]

