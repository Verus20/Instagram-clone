from django.urls import path

from posts.views import (
    home_view, 
    post_action_view,
    post_detail_view, 
    post_list_view,
    postlike_list_view,
    post_create_view,
    test_view
)

urlpatterns = [
    path('action', post_action_view),
    path('create', post_create_view),
    path('<int:post_id>', post_detail_view),
    path('', post_list_view),
    path('postlikes', postlike_list_view),
    path('stuff', test_view)
]
