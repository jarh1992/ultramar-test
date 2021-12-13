from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, Form
from .models import *


class VehicleCreationForm(ModelForm):
    """
    Formulario para creacion de Vehicles
    """

    class Meta:
        model = Vehicle
        fields = '__all__'

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(Vehicle)s's %(vin)s are not unique.",
            }
        }


class VehicleChangeForm(Form):
    """
    Formulario para modificacion de Vehicles
    """

    prefix = 'm'
    vin = forms.IntegerField(required=True)
    make = forms.CharField(max_length=50, required=True)
    model = forms.IntegerField(required=True)
    weight = forms.IntegerField(required=True)


class BookingCreationForm(ModelForm):
    """
    Formulario para creacion de Booking
    """

    ship_arr_date = forms.DateField(
        required=True,
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-provide': 'datepicker'
            }
        )
    )
    ship_dep_date = forms.DateField(
        required=True,
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-provide': 'datepicker'
            }
        )
    )

    class Meta:
        model = Booking
        fields = '__all__'

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(Booking)s's %(booking_num)s are not unique.",
            }
        }


class BookingChangeForm(Form):
    """
    Formulario para modificacion de Bookings
    """

    prefix = 'm'
    booking_num = forms.IntegerField(required=True)
    loading_port = forms.CharField(max_length=50, required=True)
    discharge_port = forms.CharField(max_length=50, required=True)
    ship_arr_date = forms.DateField(
        required=True,
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-provide': 'datepicker'
            }
        )
    )
    ship_dep_date = forms.DateField(
        required=True,
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-provide': 'datepicker'
            }
        )
    )
