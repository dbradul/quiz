from django.urls import path

from quiz.api.views import TestListCreateView, TestUpdateDeleteView, UserListView

app_name = 'api'

urlpatterns = [
    path('tests/', TestListCreateView.as_view(), name='test-list'),
    path('tests/<int:pk>', TestUpdateDeleteView.as_view(), name='test-detail'),
    path('users/', UserListView.as_view()),
]
