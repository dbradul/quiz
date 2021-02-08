from django.urls import path

from quiz.views import TestDetailView, TestListView

app_name = 'tests'

urlpatterns = [
    path('', TestListView.as_view(), name='list'),
    path('<uuid:uuid>/', TestDetailView.as_view(), name='details'),
]
