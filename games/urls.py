from django.urls import path

from .views import GameListView, GameDetailView, PostListView, PostDetailView

urlpatterns = [
    path('', GameListView.as_view(), name='game_list'),
    path('<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
