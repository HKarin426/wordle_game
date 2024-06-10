from django.urls import path
from .views import index, reset_game

urlpatterns = [
    path('', index, name='index'),
    path('reset/', reset_game, name='reset'),  # 리셋 기능을 위한 URL
]
