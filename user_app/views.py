from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import *
from django.shortcuts import redirect
from .models import CustomUser


class UserView(LoginRequiredMixin, FormView):
    """
    Vista para cargar la pagina de gestion de usuario
    """

    login_url = '/login/'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('user')
    template_name = "pages/user_man/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = self.form_class(initial={
            'username': self.request.user.username,
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
        })
        return context

    def form_valid(self, form):
        user = CustomUser.objects.get(id=self.request.user.id)
        user.id_user = int(self.request.POST.get('m-id_user'))
        user.username = self.request.POST.get('m-username')
        user.first_name = self.request.POST.get('m-first_name')
        user.last_name = self.request.POST.get('m-last_name')
        user.email = self.request.POST.get('m-email')
        user.save()
        return redirect('user')

    def dispatch(self, request, *args, **kwargs):
        if self.request.POST.get('del') == 'true':
            user = CustomUser.objects.get(id=self.request.user.id)
            user.delete()
            return redirect('login')

        return super(UserView, self).dispatch(request, *args, **kwargs)


class CustomUserCreationView(FormView):
    """
    Vista para cargar la pagina de signup
    """

    model = CustomUser
    login_url = '/login/'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/sign_up.html"

    def form_valid(self, form):
        form.save(self.request)
        return redirect('user')
