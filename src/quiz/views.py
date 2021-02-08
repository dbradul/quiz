from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from quiz.models import Test


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'tests/list.html'
    context_object_name = 'tests'


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'tests/details.html'
    context_object_name = 'test'
    pk_url_kwarg = 'uuid'

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        return self.get_queryset().get(uuid=uuid)