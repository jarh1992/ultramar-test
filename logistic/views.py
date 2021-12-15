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
                    Booking.objects.get(booking_num=int(i)).delete()
            elif my_type == 'V':
                for i in my_data:
                    Vehicle.objects.get(vin=int(i)).delete()
        context['bookings'] = Booking.objects.all()
        context['vehicles'] = Vehicle.objects.all()
        return context

    def create_booking_form_form_valid(self, form):
        form.save(self.request)
        return redirect('panel')

    def create_vehicle_form_form_valid(self, form):
        form.save(self.request)
        return redirect('panel')

    def modify_booking_form_form_valid(self, form):
        booking_num = int(self.request.POST.get('m-id_prev'))
        booking = Booking.objects.get(booking_num=booking_num)
        booking.booking_num = self.request.POST.get("m-booking_num")
        booking.loading_port = self.request.POST.get("m-loading_port")
        booking.discharge_port = self.request.POST.get("m-discharge_port")
        sad = self.request.POST.get("m-ship_arr_date")
        sdd = self.request.POST.get("m-ship_dep_date")
        booking.ship_arr_date = datetime.strptime(sad, '%m/%d/%Y').strftime('%Y-%m-%d')
        booking.ship_dep_date = datetime.strptime(sdd, '%m/%d/%Y').strftime('%Y-%m-%d')
        booking.save()
        return redirect('panel')

    def modify_vehicle_form_form_valid(self, form):
        vin = int(self.request.POST.get('m-id_prev'))
        vehicle = Vehicle.objects.get(vin=vin)
        vehicle.make = self.request.POST.get("m-make")
        vehicle.model = self.request.POST.get("m-model")
        vehicle.weight = self.request.POST.get("m-weight")
        booking_num = self.request.POST.get("m-booking")
        booking = Booking.objects.get(id=booking_num)
        vehicle.booking = booking
        vehicle.save()
        return redirect('panel')
