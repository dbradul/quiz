from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from quiz.api.views import (
    TestListView,
    TestDetailView,
    UserListView,
    ResultUpdateDeleteView,
    ResultListCreateView,
    QuestionListView,
    ChoiceRetrieveView,
    QuestionDetailView,
    QuestionDetailViewNaive,
    tg_auth, tg_introduce,
)

app_name = 'api'



urlpatterns = [
    path('tests/', TestListView.as_view(), name='tests-list'),
    path('tests/<int:pk>/', TestDetailView.as_view(), name='test-details'),
    path('tests/<int:pk>/results/', ResultListCreateView.as_view(), name='test-results-list'),
    # path('tests/<int:pk>/results/<int:id>/', ResultUpdateDeleteView.as_view(), name='test-result-detail'),
    path('results/<int:pk>/', ResultUpdateDeleteView.as_view(), name='test-result-details'),
    path('choices/<int:pk>/', ChoiceRetrieveView.as_view(), name='question-choice-details'),
    path('tests/<int:pk>/questions/', QuestionListView.as_view(), name='test-question-list'),
    path('questions/<int:pk>/', QuestionDetailViewNaive.as_view(), name='test-question-detail'),
    # path('tests/<int:pk>/questions/<int:id>/', QuestionDetailView.as_view(), name='test-question-choice-list'),
    path('tests/<int:pk>/questions/<int:order_number>/', QuestionDetailView.as_view(), name='test-question-details'),
    # path('tests/<int:pk>/questions/<int:id>/choices/', ChoiceListView.as_view(), name='test-question-choice-list'),
    path('users/', UserListView.as_view()),

    path('tg_auth/<uuid:auth_token>/', tg_auth, name='tg_auth'),
    path('tg_introduce/', tg_introduce, name='tg_introduce'),
]


schema_view = get_schema_view(
   openapi.Info(
      title="Quiz API",
      default_version='v1',
      description="Quiz RestAPI description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]