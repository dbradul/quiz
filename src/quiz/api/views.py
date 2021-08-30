import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from quiz.api.serializers import (
    TestSerializer,
    UserSerializer,
    ResultSerializer,
    QuestionSerializer,
    ChoiceSerializer,
    TestDetailSerializer,
    QuestionDetailSerializer,
)
from quiz.models import Test, Result, Question, Choice


class TestListView(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # authentication_classes = []
    # permission_classes = []
    queryset = Test.objects.all()
    serializer_class = TestSerializer


# class TestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
# class TestUpdateDeleteView(generics.RetrieveUpdateAPIView):
class TestDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Test.objects.all()
    serializer_class = TestDetailSerializer


class ResultListCreateView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        test_id = self.kwargs['pk']
        serializer.save(
            test=Test.objects.get(id=test_id),
            user=self.request.user,
        )


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        test_id = self.kwargs['pk']
        qs = Question.objects.filter(test__id = test_id).all()
        return qs


class ChoiceListView(generics.ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        question_id = self.kwargs['id']
        qs = Choice.objects.filter(question__id = question_id).all()
        return qs


class ChoiceRetrieveView(generics.RetrieveAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer

    def get_object(self):
        print('get_queryset')
        pk = self.kwargs['pk']
        order_number = self.kwargs['order_number']
        object = Question.objects.get(test__id=pk, order_number=order_number)
        return object


class QuestionDetailViewNaive(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer


class ResultUpdateDeleteView(generics.RetrieveUpdateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def tg_auth(request, auth_token):
    user = User.objects.filter(tg_auth_token=auth_token).first()
    if user:
        jwt_token = str((AccessToken.for_user(user)))
        response, status = json.dumps({'jwt_token': jwt_token, 'username': user.username}), 200
    else:
        response, status = json.dumps({'error': 'No information available for the given token'}), 404
    return HttpResponse(content=response, status=status)


@permission_classes([IsAuthenticated])
@login_required(login_url=reverse_lazy('accounts:login'))
def tg_introduce(request):
    return HttpResponseRedirect(f"https://t.me/hillel_quiz_bot?start={request.user.tg_auth_token}")
