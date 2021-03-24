from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, FormView
from django.views.generic.list import ListView

from accounts.forms import AccountCreateForm, AccountUpdateForm, ContactUs
from accounts.models import User


class AccountCreateView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = AccountCreateForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.info(self.request, "New user has just been created!")
        return result


class AccountLoginView(LoginView):
    template_name = 'login.html'

    def get_redirect_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.info(self.request, f'User {self.request.user} has been successfully logged in!')
        return result


class AccountLogoutView(LogoutView):
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        messages.info(self.request, f'User {self.request.user} has been logged out!')
        return result


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile.html'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('index')
    paginate_by = 5

    def get_object(self, queryset=None):
        return self.request.user


class AccountPasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    model = User
    template_name = 'password.html'
    success_url = reverse_lazy('accounts:login')


class LeaderboardView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'leaderboard.html'
    context_object_name = 'users'


class LeaderboardStatsView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = ['accounts.view_stats']
    model = User

    def get(self, request):
        return HttpResponse('EXTENDED STATS')


class ContactUsView(LoginRequiredMixin, FormView):
    template_name = 'contact_us.html'
    success_url = reverse_lazy('index')
    form_class = ContactUs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                from_email=request.user.email,
                recipient_list=settings.EMAIL_HOST_RECIPIENT.split(':'),
                fail_silently=False,
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

