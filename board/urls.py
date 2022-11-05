from django.urls import path
from .views import PostsList, PostCreateView, PostDetail, make_response, personal_posts_view, personal_responses_view, delete_post, PostUpdateView, delete_response, accept_response

urlpatterns = [
    path('', PostsList.as_view()),
    path('add_post', PostCreateView.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('make_response/<int:post_pk>', make_response, name='make_response'),
    path('<str:username>/posts', personal_posts_view, name='personal_posts'),
    path('<str:username>/responses', personal_responses_view, name='personal_responses'),
    path('<int:pk>/delete', delete_post, name='delete_post'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete_response', delete_response, name='delete_response'),
    path('<int:pk>/accept_response', accept_response, name='edit_response'),

]
