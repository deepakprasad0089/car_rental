from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Location)
admin.site.register(CarAgency)
admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(Booking)