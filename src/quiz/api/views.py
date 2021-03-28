from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from quiz.api.serializers import TestSerializer, UserSerializer, ResultSerializer, QuestionSerializer, ChoiceSerializer
from quiz.models import Test, Result, Question, Choice


class TestListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Test.objects.all()
    serializer_class = TestSerializer


# class TestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
# class TestUpdateDeleteView(generics.RetrieveUpdateAPIView):
class TestDetailView(generics.RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class ResultListCreateView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def perform_create(self, serializer):
        test_id = self.kwargs['pk']
        serializer.save(
            test=Test.objects.get(id = test_id),
            user_id=1, #self.request.user,
            state=Result.STATE.NEW,
            current_order_number=1
        )


class QuestionListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        test_id = self.kwargs['pk']
        qs = Question.objects.filter(test__id = test_id).all()
        return qs


class ChoiceListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        question_id = self.kwargs['id']
        qs = Choice.objects.filter(question__id = question_id).all()
        return qs


class ChoiceRetrieveView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class QuestionDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_object(self):
        print('get_queryset')
        pk = self.kwargs['pk']
        order_number = self.kwargs['order_number']
        object = Question.objects.get(test__id=pk, order_number=order_number)
        return object


class ResultUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    # lookup_url_kwarg = 'id'

    # def get_object(self):
    #     # test_id = self.kwargs['pk']
    #     # test_result_id = self.kwargs['id']
    #     # return Result.objects.get(test__id=test_id, id=test_result_id)
    #     return Result.objects.get(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        super().perform_update(serializer)
        if 'choice_id' in serializer.initial_data:
            serializer.instance.update_result(
                order_number=int(serializer.initial_data.get('current_order_number')),
                selected_choices=[int(serializer.initial_data.get('choice_id'))]
            )


class UserListView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
