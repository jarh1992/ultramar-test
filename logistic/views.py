from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, ListView
from .multiForm import MultiFormsView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import (BookingCreationForm,
	BookingChangeForm,
	VehicleCreationForm,
	VehicleChangeForm,)
from .models import Booking, Vehicle
from datetime import datetime
import json


class PanelView(LoginRequiredMixin, MultiFormsView):
    """
    Vista que carga el panel principal
    """
    login_url = '/login/'
    form_classes = {'create_booking_form': BookingCreationForm,
                    'modify_booking_form': BookingChangeForm,
                    'create_vehicle_form': VehicleCreationForm,
                    'modify_vehicle_form': VehicleChangeForm,
                    }
    success_url = reverse_lazy('panel')
    template_name = "pages/panel/panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("type"):
            my_type = self.request.GET.get("type")
            my_data = json.loads(self.request.GET.get("data"))
            if my_type == 'B':
                for i in my_data:
                    Booking.objects.get(id=int(i)).delete()
            elif my_type == 'V':
                for i in my_data:
                    Comments.objects.get(id=int(i)).delete()
        context['bookings'] = Booking.objects.all()
        context['vehicles'] = Comments.objects.all()
        return context

    def create_booking_form_form_valid(self, form):
        form.save(self.request)
        return redirect('panel')

    def create_comment_form_form_valid(self, form):
        comment = form.save(commit=False)
        comment.id_user = CustomUser.objects.get(id=self.request.user.id)
        comment.save()
        return redirect('panel')

    def modify_booking_form_form_valid(self, form):
        booking_num = int(self.request.POST.get('m-id_prev'))
        book = Book.objects.get(booking_num=booking_num)
        book.booking_num = self.request.POST.get("m-booking_num")
        book.loading_port = self.request.POST.get("m-loading_port")
		book.discharge_port = self.request.POST.get("m-discharge_port")
		sad = self.request.POST.get("m-ship_arr_date")
		sdd = self.request.POST.get("m-ship_dep_date")
        book.ship_arr_date = datetime.strptime(sad, '%m/%d/%Y').strftime('%Y-%m-%d')
        book.ship_dep_date = datetime.strptime(sdd, '%m/%d/%Y').strftime('%Y-%m-%d')
        book.save()
        return redirect('panel')

    def modify_comment_form_form_valid(self, form):
        id_user = int(self.request.POST.get('m-id_user'))
        user = CustomUser.objects.get(id=id_user)
        user.username = self.request.POST.get('m-username')
        user.first_name = self.request.POST.get('m-first_name')
        user.last_name = self.request.POST.get('m-last_name')
        user.email = self.request.POST.get('m-email')
        user.save()
        return redirect('panel')
from django.shortcuts import render

# Create your views here.
