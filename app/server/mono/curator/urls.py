from django.urls import path

from . import views

app_name = 'curator'
urlpatterns = [
    path('exhibition/<int:pk>/', views.exhibition, name='exhibition'),
]