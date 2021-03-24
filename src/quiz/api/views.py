from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from quiz.api.serializers import TestSerializer, UserSerializer
from quiz.models import Test



class TestListCreateView(generics.ListCreateAPIView):
    # authentication_classes = []
    # permission_classes = []
    queryset = Test.objects.all()
    serializer_class = TestSerializer


# class TestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
# class TestUpdateDeleteView(generics.RetrieveUpdateAPIView):
class TestUpdateDeleteView(generics.RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class UserListView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
