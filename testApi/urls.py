from django.urls import path

from testApi import views

urlpatterns = [
    path('workout-plan-management-list/', views)
]