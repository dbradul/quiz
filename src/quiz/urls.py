from django.urls import path

from quiz.views import TestDetailView, TestListView, TestResultQuestionView, TestResultCreateView, \
    TestResultDetailsView, TestResultUpdateView

app_name = 'tests'

urlpatterns = [
    path('', TestListView.as_view(), name='list'),


    path('<uuid:uuid>/', TestDetailView.as_view(), name='details'),
    path('<uuid:uuid>/results/create', TestResultCreateView.as_view(), name='result_create'),
    path('<uuid:uuid>/results/<uuid:result_uuid>/details', TestResultDetailsView.as_view(), name='result_details'),
    path('<uuid:uuid>/results/<uuid:result_uuid>/update', TestResultUpdateView.as_view(), name='result_update'),
    path('<uuid:uuid>/results/<uuid:result_uuid>/questions/next', TestResultQuestionView.as_view(), name='question'),
]
