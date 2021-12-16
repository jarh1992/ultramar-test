from django.db import models


class Booking(models.Model):
    booking_num = models.IntegerField('Booking Number', null=False, blank=False, unique=True)
    loading_port = models.CharField('Loading port', null=False, blank=False, max_length=50)
    discharge_port = models.CharField('Discharge port', null=False, blank=False, max_length=50)
    ship_arr_date = models.DateField('Ship arrival date', blank=False, null=False)
    ship_dep_date = models.DateField('Ship departure date', blank=False, null=False)

    def __str__(self):
        return str(self.booking_num)


class Vehicle(models.Model):
    vin = models.IntegerField('Vehicle Identification Number', null=False, blank=False, unique=True)
    make = models.CharField('Make', null=False, blank=False, max_length=50)
    model = models.IntegerField('Model', null=False, blank=False)
    weight = models.IntegerField('Weight', null=False, blank=False)

    def __str__(self):
        return str(self.vin)


class Transport(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.id)