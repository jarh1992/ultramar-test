from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .multiForm import MultiFormsView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import (BookingCreationForm,
                    BookingChangeForm,
                    VehicleCreationForm,
                    VehicleChangeForm)
from .models import Booking, Vehicle, Transport
from datetime import datetime
import json
import pandas as pd
from django.forms.models import model_to_dict
import mimetypes
from main.settings import APPS_DIR


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
        context['transports'] = Transport.objects.all()
        return context

    def create_booking_form_form_valid(self, form):
        form.save(self.request)
        return redirect('panel')

    def create_vehicle_form_form_valid(self, form):
        form.save(self.request)
        if self.request.POST.get('booking') != '---':
            booking_num = int(self.request.POST.get('booking'))
            booking = Booking.objects.get(id=booking_num)
            vin = int(self.request.POST.get('vin'))
            transport = Transport(
                booking=booking,
                vehicle=Vehicle.objects.get(vin=vin)
            )
            transport.save()
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
        booking_num = int(self.request.POST.get('booking'))
        booking = Booking.objects.get(id=booking_num)
        vehicle.save()
        return redirect('panel')

    def dispatch(self, request, *args, **kwargs):
        if self.request.POST.get('actn_button') == 'Export Excel':
            transports = Transport.objects.all()
            rows = []
            for t in transports:
                booking = model_to_dict(t.booking)
                del booking['id']
                vehicle = model_to_dict(t.vehicle)
                del vehicle['id']
                rows.append({**booking, **vehicle})
            df = pd.DataFrame(rows)
            media_path = APPS_DIR+"/media/"
            filename = 'transports.xlsx'
            df.to_excel(media_path + filename, engine='xlsxwriter', encoding="UTF-8")
            with open(media_path + filename, 'rb') as file:
                mime_type, _ = mimetypes.guess_type(media_path + filename)
                response = HttpResponse(file, content_type=mime_type)
                response['Content-Disposition'] = f"attachment; filename={filename}"
                return response
        return super(PanelView, self).dispatch(request, *args, **kwargs)
