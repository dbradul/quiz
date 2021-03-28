from django.urls import path

from quiz.api.views import (
    TestListView,
    TestDetailView,
    UserListView,
    ResultUpdateDeleteView,
    ResultListCreateView,
    QuestionListView,
    ChoiceRetrieveView,
    QuestionDetailView
)

app_name = 'api'

urlpatterns = [
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<int:pk>/', TestDetailView.as_view(), name='test-details'),
    path('tests/<int:pk>/results/', ResultListCreateView.as_view(), name='test-result-list'),
    # path('tests/<int:pk>/results/<int:id>/', ResultUpdateDeleteView.as_view(), name='test-result-detail'),
    path('results/<int:pk>/', ResultUpdateDeleteView.as_view(), name='test-result-details'),
    path('choices/<int:pk>/', ChoiceRetrieveView.as_view(), name='question-choice-details'),
    path('tests/<int:pk>/questions/', QuestionListView.as_view(), name='test-question-list'),
    # path('tests/<int:pk>/questions/<int:id>/', QuestionDetailView.as_view(), name='test-question-choice-list'),
    path('tests/<int:pk>/questions/<int:order_number>/', QuestionDetailView.as_view(), name='test-question-details'),
    # path('tests/<int:pk>/questions/<int:id>/choices/', ChoiceListView.as_view(), name='test-question-choice-list'),

    path('users/', UserListView.as_view()),
]
