import datetime
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from accounts.models import User
from quiz.forms import ChoiceFormSet
from quiz.models import Test, Result, Question
from quiz.tasks import mine_bitcoin, normalize_phones


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'tests/list.html'
    context_object_name = 'tests'


class TestDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = Test
    template_name = 'tests/details.html'
    context_object_name = 'test'
    pk_url_kwarg = 'uuid'
    paginate_by = 3

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        return self.model.objects.get(uuid=uuid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=self.get_queryset(), **kwargs)
        # context['result_list'] = self.get_queryset()
        return context

    def get_queryset(self):
        return Result.objects.filter(
            test=self.get_object(),
            user=self.request.user
        ).order_by('state')


class TestResultDetailsView(LoginRequiredMixin, DetailView):
    model = Result
    template_name = 'results/details.html'
    context_object_name = 'result'
    pk_url_kwarg = 'uuid'


    def get_object(self):
        uuid = self.kwargs.get('result_uuid')
        return self.get_queryset().get(uuid=uuid)


class TestResultCreateView(LoginRequiredMixin, CreateView):

    def post(self, request, uuid):
        result = Result.objects.create(
            test=Test.objects.get(uuid=uuid),
            user=request.user,
            state=Result.STATE.NEW,
            current_order_number=0
        )
        result.save()

        return HttpResponseRedirect(reverse(
            'tests:question',
            kwargs={
                'uuid': uuid,
                'result_uuid': result.uuid,
                # 'order_number': 1
            }
        ))

class TestResultQuestionView(LoginRequiredMixin, UpdateView):

    def get(self, request, uuid, result_uuid):

        order_number = Result.objects.get(uuid=result_uuid).current_order_number+1

        question = Question.objects.get(
            test__uuid=uuid,
            order_number=order_number
        )

        choices = ChoiceFormSet(queryset=question.choices.all())

        return render(
            request=request,
            template_name='tests/question.html',
            context = {
                'question': question,
                'choices': choices
            }
        )

    def post(self, request, uuid, result_uuid):

        order_number = Result.objects.get(uuid=result_uuid).current_order_number+1

        question = Question.objects.get(
            test__uuid=uuid,
            order_number=order_number
        )

        choices = ChoiceFormSet(data=request.POST)
        selected_choices = [
            'is_selected' in form.changed_data
            for form in choices.forms
        ]

        result = Result.objects.get(
            uuid=result_uuid
        )
        result.update_result(order_number, question, selected_choices)

        if result.state == Result.STATE.FINISHED:
            return HttpResponseRedirect(reverse(
                'tests:result_details',
                kwargs={
                    'uuid': uuid,
                    'result_uuid': result.uuid,
                }
            ))
        else:
            return HttpResponseRedirect(reverse(
                'tests:question',
                kwargs={
                    'uuid': uuid,
                    'result_uuid': result.uuid,
                    # 'order_number': order_number+1
                }
            ))

class TestResultUpdateView(LoginRequiredMixin, UpdateView):

    def get(self, request, uuid, result_uuid):
        result = Result.objects.get(uuid=result_uuid)

        return HttpResponseRedirect(reverse(
            'tests:question',
            kwargs={
                'uuid': uuid,
                'result_uuid': result_uuid,
                # 'order_number': result.current_order_number+1
            }
        ))




def bitcoin(request):
    mine_bitcoin.delay(10)
    mine_bitcoin.apply_async(args=(10,), eta=datetime.datetime.now() + datetime.timedelta(hours=24))
    return HttpResponse('DONE!')



def normalize(request):
    # qs = User.objects.filter(email__endswith='.com')
    normalize_phones.delay(filter=dict(email__endswith='.com'))
    return HttpResponse('DONE!')